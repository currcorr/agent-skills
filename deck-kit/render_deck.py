#!/usr/bin/env python3
"""render_deck.py — render a markdown deck through the layout system.

Usage:
    python3 render_deck.py content/<deck>.md --brand <name> [--pdf]

Reads a per-slide markdown content file, applies a brand token file
(brands/<name>.yaml) to the master layout (layout/), and writes a
self-contained HTML deck to out/. With --pdf, prints it to a one-page-
per-slide PDF via headless Chrome.

All paths resolve relative to this file's directory (the kit root), so the
kit works when run from any location. Content format (see README.md):

    ---
    title: Deck title
    client: Prepared for ...
    date: July 2026
    ---

    ```slide
    archetype: content
    kicker: Section label
    title: Action title stating the takeaway as a sentence
    takeaway: Optional takeaway-bar text
    ---
    - bullet
      - sub-bullet
    ```

Content errors fail loudly with file:line references. Placeholders are never
rendered. Stdlib only — no PyYAML, no pip installs.
"""

import argparse
import base64
import html
import math
import re
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent
LAYOUT_DIR = KIT / "layout"
BRANDS_DIR = KIT / "brands"
OUT_DIR = KIT / "out"

ARCHETYPES = (
    "title", "exec-summary", "agenda", "section-divider", "content",
    "two-col", "data", "kpi", "framework", "quote", "timeline",
    "journey", "workstreams", "comparison", "closing",
)

# keys accepted in a ```slide block header, per archetype
COMMON_KEYS = {"archetype", "kicker", "notes"}
SLIDE_KEYS = {
    "title":           COMMON_KEYS | {"title", "subtitle"},
    "exec-summary":    COMMON_KEYS | {"title", "subtitle", "takeaway", "source"},
    "agenda":          COMMON_KEYS | {"title"},
    "section-divider": COMMON_KEYS | {"title", "subtitle", "label"},
    "content":         COMMON_KEYS | {"title", "subtitle", "takeaway", "source"},
    "two-col":         COMMON_KEYS | {"title", "subtitle", "takeaway", "source",
                                      "split"},
    "data":            COMMON_KEYS | {"title", "subtitle", "takeaway", "source",
                                      "unit", "dense", "label-width"},
    "kpi":             COMMON_KEYS | {"title", "subtitle", "takeaway", "source"},
    "framework":       COMMON_KEYS | {"title", "subtitle", "takeaway", "source",
                                      "x-axis", "y-axis", "plot", "target"},
    "quote":           COMMON_KEYS | {"attribution"},
    "timeline":        COMMON_KEYS | {"title", "subtitle", "takeaway", "source",
                                      "axis", "gate"},
    # journey deliberately takes no 'takeaway' — brackets on the exhibit
    # carry the message (doctrine/journey-spec.md)
    "journey":         COMMON_KEYS | {"title", "subtitle", "source", "highlight"},
    # workstreams deliberately takes no 'takeaway' — the gate annotation on
    # the exhibit carries the message
    "workstreams":     COMMON_KEYS | {"title", "subtitle", "source", "weeks",
                                      "gate", "checkpoint"},
    "comparison":      COMMON_KEYS | {"title", "subtitle", "takeaway", "source",
                                      "highlight-col"},
    "closing":         COMMON_KEYS | {"title", "contact"},
}

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    str(Path.home() / "Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
]


class DeckError(Exception):
    """A content or brand error the user can fix. Always carries file:line."""


def err(path, line, msg):
    raise DeckError(f"{path}:{line}: {msg}")


# --------------------------------------------------------------------------
# Minimal YAML subset parser (brand token files) — nested dicts, scalars,
# '>' folded blocks. Deliberately small; brand files are simple by design.
# --------------------------------------------------------------------------

def parse_brand_yaml(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    root, stack = {}, [(-1, None)]  # (indent, dict) ; None sentinel replaced below
    stack = [(-1, root)]
    i = 0
    while i < len(lines):
        raw = lines[i].rstrip()
        if not raw.strip() or raw.lstrip().startswith("#"):
            i += 1
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if ":" not in line:
            err(path, i + 1, f"expected 'key: value', got {line!r}")
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if len(key) > 1 and key[0] in "\"'" and key[-1] == key[0]:
            key = key[1:-1]  # quoted key, e.g. a font family name
        if value and value[0] in "\"'":
            # quoted value: take up to the closing quote, ignore the rest
            quote = value[0]
            end = value.find(quote, 1)
            if end == -1:
                err(path, i + 1, f"unclosed {quote} quote in value for {key!r}")
            value = quote + value[1:end] + quote
        else:
            # unquoted: strip trailing comment ('# ' — a bare hex like #1A2C44
            # never has a space after the hash)
            value = value.split(" #", 1)[0].strip()
            if value.startswith("# "):
                value = ""
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        if value in (">", ">-"):  # folded multiline
            block, j = [], i + 1
            while j < len(lines) and (not lines[j].strip() or
                                      len(lines[j]) - len(lines[j].lstrip()) > indent):
                if lines[j].strip():
                    block.append(lines[j].strip())
                j += 1
            parent[key] = " ".join(block)
            i = j
            continue
        if value == "":
            child = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            if value and value[0] in "\"'" and value[-1] == value[0] and len(value) > 1:
                value = value[1:-1]
            parent[key] = value
        i += 1
    return root


def _rgb(hexc):
    h = hexc.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def _mix(c1, c2, t):
    """Blend c1 toward c2 by fraction t (0..1). Returns a hex string."""
    a, b = _rgb(c1), _rgb(c2)
    return "#%02X%02X%02X" % tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _is_warm(hexc):
    r, _g, b = _rgb(hexc)
    return r >= b


HEX_RE = r"#[0-9a-fA-F]{6}"

# Optional palette keys (all fall back — old brand files keep working):
#   chart:      nested map 1..4 of series colors; fallback = accent + muted
#               derivatives (muted darkened toward ink / lightened toward paper)
#   positive / negative: semantic delta colors; fallback = a restrained
#               green/red pair picked by the brand's temperature (accent
#               red-channel >= blue-channel → warm pair, else cool pair).
#               Both fallback pairs clear 4.5:1 on white.
#   accent-2:   second brand color slot; fallback = accent
#   divider-ground / divider-ink: section-divider ground/type; fallback =
#               primary / paper
WARM_POSITIVE, WARM_NEGATIVE = "#2F6B44", "#9E3A2B"
COOL_POSITIVE, COOL_NEGATIVE = "#1E6B52", "#A03B4E"


def load_brand(name):
    path = Path(name)
    if not path.suffix:
        path = BRANDS_DIR / f"{name}.yaml"
    if not path.exists():
        avail = ", ".join(sorted(p.stem for p in BRANDS_DIR.glob("*.yaml"))) or "none"
        raise DeckError(f"brand '{name}' not found at {path} (available: {avail})")
    brand = parse_brand_yaml(path)
    palette = brand.get("palette", {})
    btype = brand.get("type", {})
    for k in ("primary", "ink", "paper", "accent", "muted", "rule"):
        if k not in palette:
            raise DeckError(f"{path}: brand is missing palette.{k}")
        if not re.fullmatch(HEX_RE, str(palette[k])):
            raise DeckError(f"{path}: palette.{k} must be a 6-digit hex, got {palette[k]!r}")
    # optional hex keys — validated only when present
    for k in ("tint", "positive", "negative", "accent-2",
              "divider-ground", "divider-ink"):
        if k in palette and not re.fullmatch(HEX_RE, str(palette[k])):
            raise DeckError(f"{path}: palette.{k} must be a 6-digit hex, got {palette[k]!r}")
    chart = palette.get("chart")
    if chart is not None:
        if not isinstance(chart, dict) or not chart:
            raise DeckError(f"{path}: palette.chart must be a map of 1..4 series colors")
        for k, v in chart.items():
            if k not in ("1", "2", "3", "4"):
                raise DeckError(f"{path}: palette.chart keys must be 1..4, got {k!r}")
            if not re.fullmatch(HEX_RE, str(v)):
                raise DeckError(f"{path}: palette.chart.{k} must be a 6-digit hex, got {v!r}")
    for k in ("display", "body"):
        if k not in btype:
            raise DeckError(f"{path}: brand is missing type.{k}")
    files = btype.get("files")
    if files is not None:
        if not isinstance(files, dict) or not files:
            raise DeckError(f"{path}: type.files must be a map of "
                            "'Family name': path/to/font-file")
        for fam, fpath in files.items():
            if not resolve_asset(fpath).exists():
                raise DeckError(f"{path}: type.files[{fam!r}] not found: {fpath}")
    logo_img = brand.get("logo", {}).get("image")
    if logo_img and not resolve_asset(logo_img).exists():
        raise DeckError(f"{path}: logo.image not found: {logo_img}")
    brand["_path"] = str(path)
    return brand


def resolve_asset(p):
    """Brand asset paths are absolute or kit-relative."""
    path = Path(p).expanduser()
    return path if path.is_absolute() else KIT / path


def tokens_css(brand):
    p, t = brand["palette"], brand["type"]
    accent, muted, ink, paper = p["accent"], p["muted"], p["ink"], p["paper"]
    chart = p.get("chart") or {}
    chart_fallback = {
        "1": accent, "2": muted,
        "3": _mix(muted, ink, 0.50), "4": _mix(muted, paper, 0.35),
    }
    warm = _is_warm(accent)
    positive = p.get("positive") or (WARM_POSITIVE if warm else COOL_POSITIVE)
    negative = p.get("negative") or (WARM_NEGATIVE if warm else COOL_NEGATIVE)
    pairs = [
        ("--c-primary", p["primary"]), ("--c-ink", ink),
        ("--c-paper", paper), ("--c-accent", accent),
        ("--c-muted", muted), ("--c-rule", p["rule"]),
        ("--c-tint", p.get("tint", "#F2F3F5")),
        ("--c-accent-2", p.get("accent-2", accent)),
        ("--c-positive", positive), ("--c-negative", negative),
        ("--c-divider-ground", p.get("divider-ground", p["primary"])),
        ("--c-divider-ink", p.get("divider-ink", paper)),
        ("--f-display", t["display"]), ("--f-body", t["body"]),
        ("--f-mono", t.get("mono", "Menlo, Consolas, monospace")),
    ]
    for n in ("1", "2", "3", "4"):
        pairs.append((f"--c-chart-{n}", chart.get(n, chart_fallback[n])))
    return "\n".join(f"  {k}: {v};" for k, v in pairs)


FONT_FORMATS = {".woff2": "woff2", ".woff": "woff",
                ".ttf": "truetype", ".otf": "opentype"}


def font_faces_css(brand):
    """Optional @font-face injection for licensed faces (type.files).
    Referenced by file:// URI — the HTML is only self-contained when no
    files are given; weights beyond the file's own are browser-synthesized
    unless registered as separate families."""
    files = brand.get("type", {}).get("files")
    if not files:
        return ""
    faces = []
    for fam, fpath in files.items():
        path = resolve_asset(fpath)
        fmt = FONT_FORMATS.get(path.suffix.lower())
        if not fmt:
            raise DeckError(f"{brand['_path']}: type.files[{fam!r}] has an "
                            f"unsupported extension {path.suffix!r} "
                            f"(supported: {', '.join(FONT_FORMATS)})")
        faces.append("@font-face {\n"
                     f"  font-family: '{fam}';\n"
                     f"  src: url('{path.as_uri()}') format('{fmt}');\n"
                     "}")
    return "\n".join(faces) + "\n"


LOGO_MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
             ".svg": "image/svg+xml", ".webp": "image/webp"}


def logo_image_html(brand):
    """logo.image, base64-embedded so the output stays self-contained."""
    img = brand.get("logo", {}).get("image")
    if not img:
        return ""
    path = resolve_asset(img)
    mime = LOGO_MIME.get(path.suffix.lower())
    if not mime:
        raise DeckError(f"{brand['_path']}: logo.image has an unsupported "
                        f"extension {path.suffix!r} (supported: {', '.join(LOGO_MIME)})")
    data = base64.b64encode(path.read_bytes()).decode("ascii")
    alt = html.escape(brand.get("logo", {}).get("text", "") or "logo", quote=True)
    return f"<img class='logo-img' src='data:{mime};base64,{data}' alt='{alt}'>"


# --------------------------------------------------------------------------
# Content parsing
# --------------------------------------------------------------------------

def parse_content(path):
    """Return (meta_dict, [slide_dict]) where each slide has keys, body lines,
    and the source line number of its block."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    meta, i = {}, 0
    # optional frontmatter
    if lines and lines[0].strip() == "---":
        j = 1
        while j < len(lines) and lines[j].strip() != "---":
            line = lines[j].strip()
            if line and not line.startswith("#"):
                if ":" not in line:
                    err(path, j + 1, f"frontmatter line is not 'key: value': {line!r}")
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip()
            j += 1
        if j >= len(lines):
            err(path, 1, "frontmatter '---' never closed")
        i = j + 1

    slides = []
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("```slide"):
            start = i + 1
            j = i + 1
            while j < len(lines) and lines[j].strip() != "```":
                j += 1
            if j >= len(lines):
                err(path, i + 1, "```slide block never closed with ```")
            block = lines[start:j]
            slides.append(parse_slide_block(path, block, start + 1))
            i = j + 1
        elif line and not line.startswith("#") and not line.startswith("<!--"):
            err(path, i + 1,
                f"unexpected content outside a ```slide block: {line!r} "
                "(prose between slides must be a '#' comment line)")
        else:
            i += 1
    if not slides:
        err(path, 1, "no ```slide blocks found")
    return meta, slides


KEY_RE = re.compile(r"^([a-z][a-z-]*):\s*(.*)$")


def parse_slide_block(path, block, first_line):
    keys, body, body_start = {}, [], None
    xp = []  # 'xp-*' experience-layer keys (render_experience.py); repeatable
    in_body = False
    for off, raw in enumerate(block):
        n = first_line + off
        if not in_body:
            if raw.strip() == "---":
                in_body = True
                body_start = n + 1
                continue
            if not raw.strip():
                continue
            m = KEY_RE.match(raw.strip())
            if not m:
                err(path, n,
                    f"expected 'key: value' in slide header, got {raw.strip()!r} "
                    "(start the body with a '---' line)")
            if m.group(1).startswith("xp-"):
                # the PDF renderer ignores xp- keys entirely (spec:
                # doctrine/experience-spec.md §2); collected for reuse
                xp.append((m.group(1), m.group(2).strip()))
                continue
            keys[m.group(1)] = m.group(2).strip()
        else:
            body.append((n, raw))
    arch = keys.get("archetype")
    if not arch:
        err(path, first_line, "slide block is missing 'archetype:'")
    if arch not in ARCHETYPES:
        err(path, first_line,
            f"unknown archetype {arch!r} (valid: {', '.join(ARCHETYPES)})")
    allowed = SLIDE_KEYS[arch]
    for k in keys:
        if k not in allowed:
            err(path, first_line,
                f"key {k!r} is not valid for archetype '{arch}' "
                f"(valid: {', '.join(sorted(allowed))})")
    # trim blank body edges
    while body and not body[0][1].strip():
        body.pop(0)
    while body and not body[-1][1].strip():
        body.pop()
    return {"archetype": arch, "keys": keys, "body": body, "xp": xp,
            "line": first_line, "body_start": body_start}


# --------------------------------------------------------------------------
# Inline + block markdown
# --------------------------------------------------------------------------

def inline_md(text):
    out = html.escape(text, quote=False)
    # typographic apostrophes: straight ' between letters → ’ (code spans untouched)
    out = "".join(
        seg if seg.startswith("`")
        else re.sub(r"(?<=[A-Za-z])'(?=[A-Za-z])", "’", seg)
        for seg in re.split(r"(`[^`]*`)", out))
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"<em>\1</em>", out)
    out = re.sub(r"`(.+?)`", r"<code>\1</code>", out)
    out = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", out)  # links → text
    return out


def wrap_pct(html_text):
    """% glyphs in display numerals render at reduced size, baseline-aligned
    (doctrine §6.3). Comparators (>, <, ~, ±) stay full size — they carry
    meaning. Applied to .rail-value / .ks-num / .kpi-value content."""
    return html_text.replace("%", "<span class='unit'>%</span>")


def parse_blocks(path, body):
    """Body lines → block list: ('bullets', [(text, [subs])]), ('para', text),
    ('heading', text), ('table', header, rows, line)."""
    blocks, i = [], 0
    while i < len(body):
        n, raw = body[i]
        line = raw.rstrip()
        if not line.strip():
            i += 1
            continue
        if line.startswith("## "):
            blocks.append(("heading", line[3:].strip(), n))
            i += 1
        elif line.strip().startswith("|"):
            tbl, i = parse_table(path, body, i)
            blocks.append(tbl)
        elif line.startswith("- "):
            items = []
            while i < len(body):
                n2, raw2 = body[i]
                l2 = raw2.rstrip()
                if l2.startswith("- "):
                    items.append((l2[2:].strip(), [], n2))
                    i += 1
                elif l2.startswith("  - ") or l2.startswith("    - "):
                    if not items:
                        err(path, n2, "sub-bullet with no parent bullet")
                    items[-1][1].append(l2.strip()[2:].strip())
                    i += 1
                elif not l2.strip():
                    i += 1
                    break
                else:
                    break
            blocks.append(("bullets", items, n))
        elif line.strip().startswith("  "):
            err(path, n, f"unrecognized indented line: {line.strip()!r}")
        else:
            blocks.append(("para", line.strip(), n))
            i += 1
    return blocks


def parse_table(path, body, i):
    n0 = body[i][0]
    rows = []
    while i < len(body) and body[i][1].strip().startswith("|"):
        n, raw = body[i]
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        rows.append((n, cells))
        i += 1
    if len(rows) < 3:
        err(path, n0, "table needs a header row, a |---| separator row, and at least one data row")
    if not re.fullmatch(r"[\s|:\-]+", rows[1][1] and "|".join(rows[1][1]) or ""):
        err(path, rows[1][0], "second table row must be a |---| separator")
    header = rows[0][1]
    data = [r for r in rows[2:]]
    width = len(header)
    for n, cells in data:
        # a 2-cell row in a ≥3-column table is a spanning band row: the
        # second cell spans all data columns (navy j-band grammar)
        if len(cells) == 2 and width > 2:
            continue
        if len(cells) != width:
            err(path, n, f"table row has {len(cells)} cells, header has {width}")
    return ("table", header, data, n0), i


NUMERIC_RE = re.compile(r"^[~<>≈+\-$€£]*[\d][\d.,%xX+~<>–\-\s]*\+?$")


def render_blocks(blocks, allow_heading=False):
    out = []
    for b in blocks:
        kind = b[0]
        if kind == "bullets":
            lis = []
            for text, subs, _ in b[1]:
                sub_html = ""
                if subs:
                    sub_html = "<ul>" + "".join(f"<li>{inline_md(s)}</li>" for s in subs) + "</ul>"
                lis.append(f"<li>{inline_md(text)}{sub_html}</li>")
            out.append("<ul>" + "".join(lis) + "</ul>")
        elif kind == "para":
            out.append(f"<p>{inline_md(b[1])}</p>")
        elif kind == "table":
            out.append(render_table(b))
        elif kind == "heading" and allow_heading:
            out.append(f"<div class='col-head'>{inline_md(b[1])}</div>")
    return "\n".join(out)


def render_table(tbl, hl_col=None, large=False):
    """hl_col: 0-based winner column (comparison 'highlight-col:') — gets the
    tint wash; row striping turns off so the wash carries the meaning.
    large: sparse-table scale-up (comparison, ≤5 rows, renderer-decided)."""
    _, header, data, _ = tbl
    ncols = len(header)
    full = [cells for _, cells in data if len(cells) == ncols]
    # right-align columns whose data cells are all numeric-looking
    numcol = []
    for c in range(ncols):
        vals = [cells[c] for cells in full if cells[c].strip()]
        numcol.append(bool(vals) and all(NUMERIC_RE.match(v) for v in vals))

    def cls(c):
        classes = (["num"] if numcol[c] else []) + \
                  (["hl-col"] if c == hl_col else [])
        return f" class='{' '.join(classes)}'" if classes else ""

    ths = "".join(f"<th{cls(c)}>{inline_md(header[c])}</th>" for c in range(ncols))
    trs = []
    for _, cells in data:
        if len(cells) == 2 and ncols > 2:
            # spanning band row: label cell + one navy cell across the data
            # columns (the journey's j-band grammar in table form)
            trs.append(f"<tr class='tr-band'><td>{inline_md(cells[0])}</td>"
                       f"<td class='td-band' colspan='{ncols - 1}'>"
                       f"{inline_md(cells[1])}</td></tr>")
            continue
        tds = "".join(f"<td{cls(c)}>{inline_md(cells[c])}</td>"
                      for c in range(ncols))
        trs.append(f"<tr>{tds}</tr>")
    tbl_cls = "deck-table" + (" deck-table--hl" if hl_col is not None else "") \
              + (" deck-table--large" if large else "")
    return (f"<table class='{tbl_cls}'><thead><tr>" + ths + "</tr></thead>"
            "<tbody>" + "".join(trs) + "</tbody></table>")


# --------------------------------------------------------------------------
# Slide builders
# --------------------------------------------------------------------------

def head_html(slide, deck):
    k = slide["keys"]
    parts = ["<header class='slide-head'>", "<div class='head-rule'></div>"]
    if k.get("kicker"):
        parts.append(f"<div class='kicker'>{inline_md(k['kicker'])}</div>")
    parts.append(f"<h2 class='action-title'>{inline_md(k['title'])}</h2>")
    if k.get("subtitle"):
        parts.append(f"<div class='head-subtitle'>{inline_md(k['subtitle'])}</div>")
    parts.append("</header>")
    return "\n".join(parts)


def takeaway_html(slide):
    t = slide["keys"].get("takeaway")
    if not t:
        return ""
    return ("<div class='takeaway'><span class='takeaway-label'>Takeaway</span>"
            f"<p>{inline_md(t)}</p></div>")


def source_html(slide):
    s = slide["keys"].get("source")
    return f"<div class='source-line'>Source: {inline_md(s)}</div>" if s else ""


def foot_html(deck, page, show_page=True, show_logo=True):
    conf = inline_md(deck["confidentiality"])
    logo = (f"<span class='foot-logo'>{deck['logo_html']}</span>"
            if show_logo else "")
    pg = f"<span class='foot-page'>{page}</span>" if show_page else ""
    return ("<footer class='slide-foot'>"
            f"<span class='foot-conf'>{conf}</span>"
            f"<span class='foot-right'>{logo}{pg}</span>"
            "</footer>")


def require(path, slide, key):
    if not slide["keys"].get(key):
        err(path, slide["line"], f"archetype '{slide['archetype']}' requires '{key}:'")


def require_body(path, slide):
    if not slide["body"]:
        err(path, slide["line"],
            f"archetype '{slide['archetype']}' requires a body "
            "(add a '---' line, then the content)")


def build_title(path, slide, deck, page):
    require(path, slide, "title")
    k = slide["keys"]
    meta_bits = [deck.get(m) for m in ("client", "date", "author")]
    meta_html = "".join(f"<span>{inline_md(m)}</span>" for m in meta_bits if m)
    sub = (f"<div class='title-subtitle'>{inline_md(k['subtitle'])}</div>"
           if k.get("subtitle") else "")
    return (f"<div class='title-logo'>{deck['logo_html']}</div>"
            "<div class='title-block'><div class='title-tag'></div>"
            f"<h1>{inline_md(k['title'])}</h1>{sub}"
            f"<div class='title-meta'>{meta_html}</div></div>"
            # logo already sits top-left on the title slide; keep the footer bare
            + foot_html(deck, page, show_page=False, show_logo=False))


def build_agenda(path, slide, deck, page):
    require_body(path, slide)
    blocks = parse_blocks(path, slide["body"])
    bullets = next((b for b in blocks if b[0] == "bullets"), None)
    if not bullets:
        err(path, slide["body_start"], "agenda body must be a bulleted list")
    items = []
    for idx, (text, subs, n) in enumerate(bullets[1], 1):
        main, _, detail = text.partition("::")
        detail_html = (f"<div class='agenda-detail'>{inline_md(detail.strip())}</div>"
                       if detail else "")
        items.append(f"<div class='agenda-item'><span class='agenda-num'>{idx}</span>"
                     f"<span><span class='agenda-text'>{inline_md(main.strip())}</span>"
                     f"{detail_html}</span></div>")
    slide["keys"].setdefault("title", "Agenda")
    return (head_html(slide, deck)
            + "<div class='slide-body'><div class='agenda-list'>"
            + "".join(items) + "</div></div>" + foot_html(deck, page))


def build_exec_summary(path, slide, deck, page):
    """Pyramid-principle summary: 3-4 numbered findings, answer-first —
    bold serif lead + one supporting line each, hairline separators."""
    require(path, slide, "title")
    require_body(path, slide)
    blocks = parse_blocks(path, slide["body"])
    bullets = next((b for b in blocks if b[0] == "bullets"), None)
    if not bullets:
        err(path, slide["body_start"],
            "exec-summary body must be bullets like '- Finding :: supporting line'")
    items = []
    for idx, (text, _subs, n) in enumerate(bullets[1], 1):
        lead, sep, support = text.partition("::")
        if not sep or not support.strip():
            err(path, n, "exec-summary finding needs 'Lead statement :: "
                         f"supporting line', got {text!r}")
        items.append(f"<div class='exec-item'><span class='exec-num'>{idx}</span>"
                     f"<span><span class='exec-lead'>{inline_md(lead.strip())}</span>"
                     f"<span class='exec-support'>{inline_md(support.strip())}</span>"
                     "</span></div>")
    if not 3 <= len(items) <= 4:
        err(path, slide["body_start"],
            f"exec-summary takes 3-4 findings, found {len(items)}")
    return (head_html(slide, deck)
            + "<div class='slide-body'><div class='exec-list'>"
            + "".join(items) + f"</div>{source_html(slide)}</div>"
            + takeaway_html(slide) + foot_html(deck, page))


def build_divider(path, slide, deck, page, part_no):
    require(path, slide, "title")
    k = slide["keys"]
    label = k.get("label") or f"Part {part_no}"
    sub = (f"<div class='divider-subtitle'>{inline_md(k['subtitle'])}</div>"
           if k.get("subtitle") else "")
    return ("<div class='divider-inner'>"
            f"<div class='divider-label'>{inline_md(label)}</div>"
            f"<h2>{inline_md(k['title'])}</h2>{sub}</div>"
            + foot_html(deck, page))


def build_content(path, slide, deck, page):
    require(path, slide, "title")
    require_body(path, slide)
    body = render_blocks(parse_blocks(path, slide["body"]))
    return (head_html(slide, deck)
            + f"<div class='slide-body'>{body}{source_html(slide)}</div>"
            + takeaway_html(slide) + foot_html(deck, page))


TWO_COL_FLAGS = ("stat-rail", "steps")


def render_stat_rail(path, col):
    """':: stat-rail' column: bullets 'value :: claim' become a ledger of
    large primary-color pulls with one-line claims, hairlines between."""
    bullets = next((b for b in col["blocks"] if b[0] == "bullets"), None)
    stray = next((b for b in col["blocks"] if b[0] != "bullets"), None)
    if not bullets or stray:
        err(path, col["line"],
            f"a ':: stat-rail' column takes only bullets like "
            "'- 95% :: one-line claim'")
    rows = []
    for text, _subs, n in bullets[1]:
        value, sep, claim = text.partition("::")
        if not sep or not value.strip() or not claim.strip():
            err(path, n, f"stat-rail row needs 'value :: claim', got {text!r}")
        # a rail value with no digit is a verbal pull: one scale step down so
        # numbers and words stop competing in one register (craft spec §1.3)
        words = not re.search(r"\d", value)
        cls = "rail-value rail-value--words" if words else "rail-value"
        rows.append("<div class='rail-row'>"
                    f"<div class='{cls}'>{wrap_pct(inline_md(value.strip()))}</div>"
                    f"<div class='rail-claim'>{inline_md(claim.strip())}</div></div>")
    return "<div class='stat-rail'>" + "".join(rows) + "</div>"


def render_steps(path, col):
    """':: steps' column: bullets become stacked tint step cells with drawn
    arrows; a trailing paragraph becomes the bold close caption."""
    bullets = next((b for b in col["blocks"] if b[0] == "bullets"), None)
    if not bullets:
        err(path, col["line"],
            "a ':: steps' column needs bullets (the steps), optionally "
            "followed by a bold close paragraph")
    paras = [b[1] for b in col["blocks"] if b[0] == "para"]
    out = []
    for i, (text, _subs, _n) in enumerate(bullets[1]):
        if i:
            out.append("<div class='step-arrow'></div>")
        out.append(f"<div class='step-cell'>{inline_md(text)}</div>")
    for p in paras:
        out.append(f"<div class='step-close'>{inline_md(p)}</div>")
    return "<div class='step-stack'>" + "".join(out) + "</div>"


def build_two_col(path, slide, deck, page):
    require(path, slide, "title")
    require_body(path, slide)
    blocks = parse_blocks(path, slide["body"])
    cols, current = [], None
    for b in blocks:
        if b[0] == "heading":
            head, _, flag = b[1].partition("::")
            flag = flag.strip().lower()
            if flag and flag not in TWO_COL_FLAGS:
                err(path, b[2], f"unknown column flag {flag!r} "
                                f"(valid: {', '.join(TWO_COL_FLAGS)})")
            current = {"head": head.strip(), "flag": flag, "blocks": [],
                       "line": b[2]}
            cols.append(current)
        elif current is None:
            err(path, b[2], "two-col body must start with a '## Column heading'")
        else:
            current["blocks"].append(b)
    if len(cols) != 2:
        err(path, slide["body_start"],
            f"two-col needs exactly two '## ' headings, found {len(cols)}")
    # 'split: 2-1' — asymmetric column weights (evidence 2fr / implication 1fr
    # per the design doctrine; balanced 1fr/1fr stays the default)
    split = slide["keys"].get("split", "")
    style = ""
    if split:
        m = re.fullmatch(r"([1-9])-([1-9])", split)
        if not m:
            err(path, slide["line"],
                f"'split:' must be two weights like '2-1', got {split!r}")
        style = f" style='grid-template-columns:{m.group(1)}fr {m.group(2)}fr'"

    def col_body(c):
        if c["flag"] == "stat-rail":
            return render_stat_rail(path, c)
        if c["flag"] == "steps":
            return render_steps(path, c)
        return render_blocks(c["blocks"])

    col_html = "".join(
        f"<div><div class='col-head'>{inline_md(c['head'])}</div>"
        f"{col_body(c)}</div>" for c in cols)
    # flagged columns stretch the grid so both columns end together
    grid_cls = "two-col two-col--flex" if any(c["flag"] for c in cols) else "two-col"
    return (head_html(slide, deck)
            + f"<div class='slide-body'><div class='{grid_cls}'{style}>{col_html}</div>"
            + f"{source_html(slide)}</div>" + takeaway_html(slide)
            + foot_html(deck, page))


def build_data(path, slide, deck, page):
    require(path, slide, "title")
    require_body(path, slide)
    k = slide["keys"]
    dense = k.get("dense", "")
    if dense and dense.lower() not in ("true", "false"):
        err(path, slide["line"], f"'dense:' must be true or false, got {dense!r}")
    dense = dense.lower() == "true"
    label_w = k.get("label-width", "")
    if label_w:
        if not label_w.isdigit() or not 120 <= int(label_w) <= 560:
            err(path, slide["line"],
                f"'label-width:' must be a bar-label column width in px "
                f"(120-560), got {label_w!r}")
    blocks = parse_blocks(path, slide["body"])
    stray = next((b for b in blocks if b[0] not in ("table", "bullets")), None)
    if stray:
        err(path, stray[2],
            f"data body only takes a markdown table or bar bullets; got a "
            f"{stray[0]} ({str(stray[1])[:50]!r}) — sources go in a 'source:' header key")
    table = next((b for b in blocks if b[0] == "table"), None)
    bullets = next((b for b in blocks if b[0] == "bullets"), None)
    if table:
        body = render_table(table)
        if label_w:
            err(path, slide["line"], "'label-width:' only applies to bar bodies")
    elif bullets:
        body = render_bars(path, bullets, dense=dense, label_w=label_w)
    else:
        err(path, slide["body_start"],
            "data body must be a markdown table or bar lines like "
            "'- Label :: 60%+ :: highlight'")
    if dense:
        body = f"<div class='data-dense'>{body}</div>"
    return (head_html(slide, deck)
            + f"<div class='slide-body'>{body}{source_html(slide)}</div>"
            + takeaway_html(slide) + foot_html(deck, page))


def render_bars(path, bullets, dense=False, label_w=""):
    bars = []
    for text, _subs, n in bullets[1]:
        parts = [p.strip() for p in text.split("::")]
        if len(parts) < 2:
            err(path, n, f"bar line needs 'Label :: value', got {text!r}")
        label, value = parts[0], parts[1]
        flags = [p.lower() for p in parts[2:]]
        for f in flags:
            if f != "highlight":
                err(path, n, f"unknown bar flag {f!r} (only 'highlight')")
        m = re.search(r"\d+(?:[.,]\d+)?", value)
        if not m:
            err(path, n, f"bar value {value!r} contains no number to scale by")
        bars.append((label, value, float(m.group(0).replace(",", "")),
                     "highlight" in flags))
    peak = max(b[2] for b in bars) or 1.0
    rows = []
    for label, value, num, hl in bars:
        pct = round(num / peak * 78, 1)  # 78% cap leaves room for the value label
        rows.append(
            f"<div class='bar-row{' highlight' if hl else ''}'>"
            f"<div class='bar-label'>{inline_md(label)}</div>"
            f"<div class='bar-track'><div class='bar-fill' style='width:{pct}%'></div>"
            f"<span class='bar-value'>{inline_md(value)}</span></div></div>")
    # few-row exhibits scale up to fill their stage (unless dense backup
    # exhibit); at two bars the chart is the slide and goes hero-scale
    if dense:
        cls = "bar-chart"
    elif len(bars) <= 2:
        cls = "bar-chart bar-chart--xl"
    elif len(bars) == 3:
        cls = "bar-chart bar-chart--large"
    else:
        cls = "bar-chart"
    style = f" style='--bar-label-w:{label_w}px'" if label_w else ""
    return f"<div class='{cls}'{style}>" + "".join(rows) + "</div>"


def build_kpi(path, slide, deck, page):
    """1-3 big stats as the hero — serif display, flat, LEFT-aligned.
    No centering, no gradient, no decoration (the big-number-hero tell)."""
    require(path, slide, "title")
    require_body(path, slide)
    blocks = parse_blocks(path, slide["body"])
    bullets = next((b for b in blocks if b[0] == "bullets"), None)
    if not bullets:
        err(path, slide["body_start"],
            "kpi body must be bullets like '- 95% :: of pilots show no P&L impact'")
    stats, counters = [], []
    for text, _subs, n in bullets[1]:
        parts = [p.strip() for p in text.split("::")]
        flag = parts[-1].lower() if parts and parts[-1].lower() in \
            ("highlight", "counter") else ""
        if flag:
            parts = parts[:-1]
        if len(parts) != 2 or not parts[0] or not parts[1]:
            err(path, n, f"kpi stat needs 'Value :: label', got {text!r}")
        if flag == "counter":
            counters.append((parts[0], parts[1]))
        else:
            stats.append((parts[0], parts[1], flag == "highlight"))
    if not 1 <= len(stats) <= 3:
        err(path, slide["body_start"], f"kpi takes 1-3 stats, found {len(stats)}")
    if sum(1 for s in stats if s[2]) > 1:
        err(path, slide["body_start"], "kpi allows at most one highlighted stat")
    if len(counters) > 1:
        err(path, slide["body_start"], "kpi allows at most one ':: counter' stat")
    if counters:
        # split mode: ONE proportional device — geometry carries the quantity,
        # typography carries the rank (doctrine §6.11). Requires exactly one
        # hero stat + one counter, both percentage shares of one whole.
        if len(stats) != 1:
            err(path, slide["body_start"],
                "':: counter' takes exactly one other stat (the hero)")
        if stats[0][2]:
            err(path, slide["body_start"],
                "no ':: highlight' with ':: counter' — the split device spends "
                "the accent on the counter share")
        def _pct(v, what):
            m = re.search(r"(\d+(?:\.\d+)?)\s*%", v)
            if not m:
                err(path, slide["body_start"],
                    f"split kpi: {what} value {v!r} must contain a percentage")
            return float(m.group(1))
        hero_v, hero_label, _ = stats[0]
        ctr_v, ctr_label = counters[0]
        a, b = _pct(hero_v, "hero"), _pct(ctr_v, "counter")
        if not 98 <= a + b <= 102:
            err(path, slide["body_start"],
                f"split kpi: shares must sum to ~100 (got {a:g} + {b:g})")
        body = (
            "<div class='kpi-split'>"
            "<div class='ks-hero'>"
            f"<div class='ks-num'>{wrap_pct(inline_md(hero_v))}</div>"
            f"<div class='ks-label'>{inline_md(hero_label)}</div></div>"
            f"<div class='ks-bar'><div class='ks-seg ks-seg-a' style='width:{a:g}%'></div>"
            f"<div class='ks-seg ks-seg-b' style='width:{b:g}%'></div></div>"
            f"<div class='ks-note' style='--ks-tick:{100 - b / 2:g}%'>"
            f"<span><strong>{inline_md(ctr_v)}</strong> — {inline_md(ctr_label)}</span>"
            "</div></div>")
        return (head_html(slide, deck) + f"<div class='slide-body'>{body}"
                + f"{source_html(slide)}</div>" + takeaway_html(slide)
                + foot_html(deck, page))
    stat_html = "".join(
        f"<div class='kpi-stat{' highlight' if hl else ''}'>"
        f"<div class='kpi-value'>{wrap_pct(inline_md(value))}</div>"
        f"<div class='kpi-label'>{inline_md(label)}</div></div>"
        for value, label, hl in stats)
    # one stat = the number IS the message: renderer-decided hero scale-up
    row_cls = "kpi-row kpi-row--solo" if len(stats) == 1 else "kpi-row"
    return (head_html(slide, deck)
            + f"<div class='slide-body'><div class='{row_cls}'>{stat_html}</div>"
            + f"{source_html(slide)}</div>" + takeaway_html(slide)
            + foot_html(deck, page))


def build_framework(path, slide, deck, page):
    """2x2: tracked small-caps axis labels, four hairline-grid quadrant cells
    (no fills, no shadows), one highlightable via accent. Cells read TL, TR,
    BL, BR; axis direction is carried in the label text (e.g. 'low → high')."""
    require(path, slide, "title")
    require(path, slide, "x-axis")
    require(path, slide, "y-axis")
    require_body(path, slide)
    blocks = parse_blocks(path, slide["body"])
    cells, current = [], None
    for b in blocks:
        if b[0] == "heading":
            head, _, flag = b[1].partition("::")
            flag = flag.strip().lower()
            if flag and flag != "highlight":
                err(path, b[2], f"unknown quadrant flag {flag!r} (only 'highlight')")
            current = {"head": head.strip(), "hl": flag == "highlight", "paras": []}
            cells.append(current)
        elif b[0] == "para":
            if current is None:
                err(path, b[2], "framework body must start with a '## Quadrant title'")
            current["paras"].append(b[1])
        else:
            err(path, b[2],
                f"framework quadrants take '## title' + 1-2 plain lines; got a {b[0]}")
    if len(cells) != 4:
        err(path, slide["body_start"],
            f"framework needs exactly four '## ' quadrant titles (TL, TR, BL, "
            f"BR), found {len(cells)}")
    if sum(1 for c in cells if c["hl"]) > 1:
        err(path, slide["body_start"], "framework allows at most one highlighted quadrant")
    for c in cells:
        if not 1 <= len(c["paras"]) <= 2:
            err(path, slide["body_start"],
                f"quadrant {c['head']!r} needs 1-2 body lines, found {len(c['paras'])}")
    # Quadrant markers take the chart series only when the brand declares one
    # AND no quadrant is highlighted — one color system per slide: either the
    # series keys the quadrants, or the accent marks the winner, never both
    # (a brand's chart-1 is often its accent, which would double the accent).
    has_hl = any(c["hl"] for c in cells)
    mark = ("<span class='fw-mark'></span>"
            if deck.get("_chart") and not has_hl else "")
    k = slide["keys"]

    def cell_index(name, key):
        for i, c in enumerate(cells):
            if c["head"].lower() == name.strip().lower():
                return i
        err(path, slide["line"], f"'{key}:' names quadrant {name.strip()!r}, "
            f"which is not one of: {', '.join(c['head'] for c in cells)}")

    # 'plot: Quadrant :: label' — a plotted marker inside the named quadrant
    plots = {}
    if k.get("plot"):
        q, sep, label = k["plot"].partition("::")
        if not sep or not label.strip():
            err(path, slide["line"], "'plot:' needs 'Quadrant title :: label'")
        plots[cell_index(q, "plot")] = (
            "<div class='fw-plot'><span class='fw-plot-mark'></span>"
            f"<span>{inline_md(label.strip())}</span></div>")

    # 'target: Quadrant :: label' — the destination marker (accent square).
    # Trajectory = plot (today, primary) + target (destination, accent);
    # never a drawn arrow (doctrine §6.11).
    if k.get("target"):
        q, sep, label = k["target"].partition("::")
        if not sep or not label.strip():
            err(path, slide["line"], "'target:' needs 'Quadrant title :: label'")
        ti = cell_index(q, "target")
        if ti in plots:
            err(path, slide["line"],
                "'plot:' and 'target:' in the same quadrant carries no trajectory")
        plots[ti] = ("<div class='fw-plot fw-plot--target'>"
                     "<span class='fw-plot-mark'></span>"
                     f"<span>{inline_md(label.strip())}</span></div>")

    cell_html = "".join(
        f"<div class='fw-cell{' highlight' if c['hl'] else ''}'>"
        f"<div class='fw-cell-title'>{mark}{inline_md(c['head'])}</div>"
        + "".join(f"<p>{inline_md(t)}</p>" for t in c["paras"])
        + plots.get(i, "")
        + "</div>" for i, c in enumerate(cells))
    fw = ("<div class='framework'>"
          f"<div class='fw-y'>{inline_md(k['y-axis'])}</div>"
          "<div class='fw-main'>"
          f"<div class='fw-grid'>{cell_html}</div>"
          f"<div class='fw-x'>{inline_md(k['x-axis'])}</div>"
          "</div></div>")
    return (head_html(slide, deck)
            + f"<div class='slide-body'>{fw}{source_html(slide)}</div>"
            + takeaway_html(slide) + foot_html(deck, page))


def build_quote(path, slide, deck, page):
    require_body(path, slide)
    blocks = parse_blocks(path, slide["body"])
    paras = [b[1] for b in blocks if b[0] == "para"]
    if not paras:
        err(path, slide["body_start"], "quote body must be plain paragraph text")
    text = " ".join(paras).strip()
    text = text.strip('"“”')
    attr = slide["keys"].get("attribution", "")
    attr_html = (f"<div class='quote-attr'><span>{inline_md(attr)}</span></div>"
                 if attr else "")
    kicker = slide["keys"].get("kicker", "")
    kicker_html = f"<div class='kicker'>{inline_md(kicker)}</div>" if kicker else ""
    # short quotes get full presence; long ones clamp back down
    size_cls = " quote-text--long" if len(text) > 140 else ""
    return ("<div class='quote-block'>"
            f"{kicker_html}"
            f"<div class='quote-text{size_cls}'>“{inline_md(text)}”</div>"
            f"{attr_html}</div>" + foot_html(deck, page))


def build_timeline(path, slide, deck, page):
    require(path, slide, "title")
    require_body(path, slide)
    k = slide["keys"]
    axis_mode = bool(k.get("axis"))
    blocks = parse_blocks(path, slide["body"])
    bullets = next((b for b in blocks if b[0] == "bullets"), None)
    if not bullets:
        err(path, slide["body_start"],
            "timeline body must be bullets like '- Label :: timeframe :: description'")
    phases = []
    for text, _subs, n in bullets[1]:
        parts = [p.strip() for p in text.split("::")]
        # trailing labeled fields: 'span: N' (axis mode width weight) and
        # 'exit: text' (exit deliverable lane row), plus the 'highlight' flag
        hl, span, exit_ = False, None, None
        while len(parts) > 2:
            tail = parts[-1]
            low = tail.lower()
            if low == "highlight":
                hl = True
            elif low.startswith("span:"):
                v = tail[5:].strip()
                if not re.fullmatch(r"\d+(?:\.\d+)?", v) or float(v) <= 0:
                    err(path, n, f"'span:' needs a positive number, got {v!r}")
                span = float(v)
            elif low.startswith("exit:"):
                exit_ = tail[5:].strip()
                if not exit_:
                    err(path, n, "'exit:' needs the deliverable text")
            else:
                break
            parts = parts[:-1]
        if (span is not None or exit_ is not None) and not axis_mode:
            err(path, n, "'span:'/'exit:' fields need 'axis:' on the slide")
        if hl and axis_mode:
            err(path, n, "no 'highlight' in axis mode — the accent belongs "
                         "to the 'gate:' marker")
        if len(parts) == 2:
            label, time, desc = parts[0], "", parts[1]
        elif len(parts) == 3:
            label, time, desc = parts
        else:
            err(path, n, "timeline phase needs 'Label :: description' or "
                         f"'Label :: timeframe :: description', got {text!r}")
        phases.append((label, time, desc, hl, span, exit_))
    if not 2 <= len(phases) <= 6:
        err(path, slide["body_start"],
            f"timeline supports 2-6 phases, found {len(phases)}")
    if axis_mode:
        body = render_phasebar(path, slide, phases)
    else:
        if k.get("gate"):
            err(path, slide["line"], "'gate:' needs 'axis:' on the slide")
        body = "<div class='timeline'>" + "".join(
            f"<div class='tl-phase{' highlight' if hl else ''}'>"
            + (f"<div class='tl-time'>{inline_md(time)}</div>" if time
               else "<div class='tl-time'>&nbsp;</div>")
            + f"<div class='tl-label'>{inline_md(label)}</div>"
            + f"<div class='tl-desc'>{inline_md(desc)}</div></div>"
            for label, time, desc, hl, _s, _e in phases) + "</div>"
    return (head_html(slide, deck)
            + f"<div class='slide-body'>{body}"
            + f"{source_html(slide)}</div>" + takeaway_html(slide)
            + foot_html(deck, page))


def render_phasebar(path, slide, phases):
    """Timeline axis mode: proportional phase bar on a time axis with an
    accent gate marker, exit-deliverable ledger rows below.
    Keys: 'axis: W0 :: M18' (endpoint labels) turns the mode on;
    'gate: 11% :: Week 8 :: callout text' places the accent decision marker.
    Phase lines gain ':: span: N' (width weight — durations drawn to scale)
    and ':: exit: text' (the phase's exit deliverable)."""
    k = slide["keys"]
    ax = [p.strip() for p in k["axis"].split("::")]
    if len(ax) != 2 or not ax[0] or not ax[1]:
        err(path, slide["line"],
            f"'axis:' needs 'start label :: end label', got {k['axis']!r}")
    # span weights are free (11/22/67 or 1/2/6) — the grid normalizes them
    for label, _t, _d, _hl, span, _e in phases:
        if span is None:
            err(path, slide["line"], f"axis mode: phase {label!r} is missing "
                "its ':: span: N' width weight")

    out = ["<div class='phasebar'>", "<div class='pb-axis'>",
           f"<span class='pb-axis-label start'>{inline_md(ax[0])}</span>",
           f"<span class='pb-axis-label end'>{inline_md(ax[1])}</span>",
           "<div class='pb-axis-rule'></div>"]
    if k.get("gate"):
        g = [p.strip() for p in k["gate"].split("::")]
        if len(g) != 3 or not all(g):
            err(path, slide["line"],
                "'gate:' needs 'position% :: label :: callout text'")
        m = re.fullmatch(r"(\d+(?:\.\d+)?)%?", g[0])
        if not m or not 0 < float(m.group(1)) < 100:
            err(path, slide["line"],
                f"gate position must be a percent between 0 and 100, got {g[0]!r}")
        pos = float(m.group(1))
        out.append(f"<div class='pb-gate' style='left:{pos:g}%'></div>")
        out.append(f"<div class='pb-gate-callout' style='left:{pos:g}%'>"
                   f"<span class='gate-label'>{inline_md(g[1])}</span>"
                   f"{inline_md(g[2])}</div>")
    out.append("</div>")

    cols = " ".join(f"{p[4]:g}fr" for p in phases)
    out.append(f"<div class='pb-band' style='grid-template-columns:{cols}'>")
    for i, (label, time, _d, _hl, _s, _e) in enumerate(phases):
        cls = "pb-phase"
        if i == 0:
            cls += " first"
        if i == len(phases) - 1:
            cls += " last"
        time_html = f"<div class='pb-time'>{inline_md(time)}</div>" if time else ""
        out.append(f"<div class='{cls}'>{time_html}"
                   f"<div class='pb-name'>{inline_md(label)}</div></div>")
    out.append("</div>")

    if any(p[5] for p in phases):
        out.append("<div class='pb-lanes'>")
        for label, _t, desc, _hl, _s, exit_ in phases:
            exit_html = (f"<div class='pb-exit'>{inline_md(exit_)}</div>"
                         if exit_ else "<div class='pb-exit empty'>—</div>")
            desc_html = (f"<div class='pb-row-desc'>{inline_md(desc)}</div>"
                         if desc else "")
            out.append(f"<div class='pb-row'>"
                       f"<div class='pb-row-label'>{inline_md(label)}</div>"
                       f"<div>{exit_html}{desc_html}</div></div>")
        out.append("</div>")
    out.append("</div>")
    return "".join(out)


# --- journey: chevron stage band + swim lanes + spanning bands + brackets
#     (spec: doctrine/journey-spec.md — assembled verbatim) ---

J_STAGE_RE = re.compile(r"^(\d+)\.\s+(.+)$")
J_SPAN_RE = re.compile(r"^(\d+)\s*-\s*(\d+)(!?):\s*(.+)$")
J_CELL_RE = re.compile(r"^(\d+):\s*(.+)$")
J_LANE_RE = re.compile(r"^lane:\s*(.+)$")
J_BRACKET_RE = re.compile(r"^bracket:\s*(.*)$")


def j_text(text):
    """House inline markdown plus the journey-local '==stat==' extension."""
    return re.sub(r"==(.+?)==", r"<span class='stat'>\1</span>", inline_md(text))


def build_journey(path, slide, deck, page):
    """Journey map. Line-oriented grammar (not parse_blocks):
    'stages:' + 'N. Name [:: sub]' lines; 'lane: Label' + per-stage 'N: text'
    cells or spanning 'N-M[!]: Label :: text' bands; trailing
    'bracket: N-M :: Head :: text' annotations. No takeaway by design."""
    require(path, slide, "title")
    require_body(path, slide)
    stages, lanes, brackets = [], [], []
    mode, lane = None, None
    for n, raw in slide["body"]:
        line = raw.strip()
        if not line:
            continue
        if line.rstrip(":") == "stages" and line.endswith(":"):
            if stages:
                err(path, n, "duplicate 'stages:' section")
            mode = "stages"
            continue
        m = J_LANE_RE.match(line)
        if m:
            if not stages:
                err(path, n, "'lane:' before 'stages:' — define the stages first")
            if brackets:
                err(path, n, "'lane:' after 'bracket:' — brackets come after all lanes")
            lane = {"label": m.group(1).strip(), "cells": {}, "spans": [],
                    "line": n}
            lanes.append(lane)
            mode = "lane"
            continue
        m = J_BRACKET_RE.match(line)
        if m:
            if not lanes:
                err(path, n, "'bracket:' before any 'lane:'")
            parts = [p.strip() for p in m.group(1).split("::")]
            rng = re.fullmatch(r"(\d+)\s*-\s*(\d+)", parts[0]) if parts else None
            if len(parts) != 3 or not rng or not parts[1] or not parts[2]:
                err(path, n, "bracket needs 'bracket: N-M :: Head :: text'")
            brackets.append((int(rng.group(1)), int(rng.group(2)),
                             parts[1], parts[2], n))
            mode = "bracket"
            continue
        if mode == "stages":
            m = J_STAGE_RE.match(line)
            if not m:
                err(path, n, f"expected 'N. Stage name [:: sub]', got {line!r}")
            num = int(m.group(1))
            if num != len(stages) + 1:
                err(path, n, "stages must be numbered consecutively from 1; "
                             f"expected {len(stages) + 1}, got {num}")
            name, _, sub = m.group(2).partition("::")
            stages.append((name.strip(), sub.strip()))
            continue
        if mode == "lane":
            m = J_SPAN_RE.match(line)
            if m:
                if lane["cells"]:
                    err(path, n, f"lane {lane['label']!r} mixes spanning and "
                                 "per-stage cells")
                a, b, dark = int(m.group(1)), int(m.group(2)), m.group(3) == "!"
                label, sep, text = m.group(4).partition("::")
                if not sep or not label.strip() or not text.strip():
                    err(path, n, "spanning cell needs 'N-M[!]: Label :: text', "
                                 f"got {line!r}")
                if not (1 <= a < b <= len(stages)):
                    err(path, n, f"span {a}-{b} is not a valid stage range "
                                 f"(stages 1-{len(stages)})")
                for a2, b2, *_ in lane["spans"]:
                    if a <= b2 and a2 <= b:
                        err(path, n, f"span {a}-{b} overlaps span {a2}-{b2} "
                                     f"in lane {lane['label']!r}")
                lane["spans"].append((a, b, dark, label.strip(), text.strip()))
                continue
            m = J_CELL_RE.match(line)
            if m:
                if lane["spans"]:
                    err(path, n, f"lane {lane['label']!r} mixes spanning and "
                                 "per-stage cells")
                i = int(m.group(1))
                if not 1 <= i <= len(stages):
                    err(path, n, f"cell stage {i} out of range 1-{len(stages)}")
                if i in lane["cells"]:
                    err(path, n, f"duplicate cell for stage {i} in lane "
                                 f"{lane['label']!r}")
                lane["cells"][i] = m.group(2).strip()
                continue
            err(path, n, f"unrecognized lane line: {line!r} (expected "
                         "'N: text' or 'N-M[!]: Label :: text')")
        err(path, n, f"unrecognized journey line: {line!r} (body opens with "
                     "'stages:', then 'lane:'/'bracket:' sections)")

    nstages = len(stages)
    if not 3 <= nstages <= 6:
        err(path, slide["body_start"] or slide["line"],
            f"journey needs 3-6 stages, found {nstages}")
    if not lanes:
        err(path, slide["body_start"] or slide["line"],
            "journey needs at least one 'lane:'")
    if len(lanes) > 5:
        err(path, lanes[5]["line"],
            f"journey supports at most 5 lanes, found {len(lanes)} — "
            "split the slide")
    for ln in lanes:
        if not ln["cells"] and not ln["spans"]:
            err(path, ln["line"], f"lane {ln['label']!r} has no cells")
    if len(brackets) > 3:
        err(path, brackets[3][4], "journey takes at most 3 brackets")
    for a, b, _h, _t, n in brackets:
        if not (1 <= a <= b <= nstages):
            err(path, n, f"bracket range {a}-{b} is not a valid stage range "
                         f"(stages 1-{nstages})")
    hi = None
    raw_hi = slide["keys"].get("highlight", "")
    if raw_hi:
        if not raw_hi.isdigit() or not 1 <= int(raw_hi) <= nstages:
            err(path, slide["line"],
                f"'highlight:' must be a stage number 1-{nstages}, got {raw_hi!r}")
        hi = int(raw_hi)

    # grid tracks: gutter + one per stage (inline override only when N != 5)
    grid = ("" if nstages == 5 else
            f" style='grid-template-columns:104px repeat({nstages},1fr)'")
    out = ["<div class='journey'>", f"<div class='j-stages'{grid}>"]
    for i, (name, sub) in enumerate(stages, 1):
        cls = "j-stage"
        if i == 1:
            cls += " first"
        if i == nstages:
            cls += " last"
        if i == hi:
            cls += " hi"
        sub_html = f"<div class='j-stage-sub'>{j_text(sub)}</div>" if sub else ""
        out.append(f"<div class='{cls}' style='grid-column:{i + 1}'>"
                   f"<div class='j-stage-num'>Stage {i}</div>"
                   f"<div class='j-stage-name'>{j_text(name)}</div>"
                   f"{sub_html}</div>")
    out.append("</div>")

    out.append(f"<div class='j-lanes'{grid}>")
    out.append("<div class='j-row-rule first'></div>")
    for ln in lanes:
        out.append(f"<div class='j-lane-label'>{j_text(ln['label'])}</div>")
        if ln["spans"]:
            for a, b, dark, label, text in sorted(ln["spans"]):
                band = "j-band dark" if dark else "j-band lit"
                out.append(f"<div class='{band}' "
                           f"style='grid-column: {a + 1} / {b + 2};'>"
                           f"<span class='b-label'>{j_text(label)}</span>"
                           f"{j_text(text)}</div>")
        else:
            for i in range(1, nstages + 1):
                text = ln["cells"].get(i)
                cls = "j-cell" + (" hi-col" if i == hi else "")
                if text is None:
                    out.append(f"<div class='{cls} empty'>—</div>")
                else:
                    out.append(f"<div class='{cls}'>{j_text(text)}</div>")
        out.append("<div class='j-row-rule'></div>")
    out.append("</div>")

    if brackets:
        out.append(f"<div class='j-brackets'{grid}>")
        out.append("<div></div>")
        for a, b, head, text, _n in brackets:
            out.append(f"<div class='j-bracket' "
                       f"style='grid-column: {a + 1} / {b + 2};'>"
                       f"<div class='j-bracket-head'>{j_text(head)}</div>"
                       f"<div class='j-bracket-text'>{j_text(text)}</div></div>")
        out.append("</div>")
    out.append("</div>")

    return (head_html(slide, deck)
            + "<div class='slide-body'>" + "".join(out)
            + f"{source_html(slide)}</div>" + foot_html(deck, page))


# --- workstreams: parallel streams on a week grid, converging on a decision
#     gate (composed per the doctrine's composition amendment — phasebar axis
#     + gate idiom, journey lane grid, tint/dark spanning bands) ---

WS_STREAM_RE = re.compile(r"^stream:\s*(.+)$")
WS_SPAN_RE = re.compile(r"^(\d+)\s*-\s*(\d+)(!?):\s*(.+)$")


def build_workstreams(path, slide, deck, page):
    """Workstreams map. Line-oriented grammar (not parse_blocks):
    'weeks: N' sets the week-column count; each 'stream: Label' is followed
    by exactly one 'A-B[!]: text' bar spanning weeks A..B ('!' = the dark
    converging stream, at most one); 'checkpoint: W :: text' hangs a quiet
    hairline at the end of week W; 'gate: W :: Head :: text' places the
    accent gate line + annotation. '==text==' marks a stat. No takeaway by
    design — the gate annotation carries the message."""
    require(path, slide, "title")
    require(path, slide, "weeks")
    require_body(path, slide)
    k = slide["keys"]
    raw_w = k["weeks"]
    if not raw_w.isdigit() or not 4 <= int(raw_w) <= 12:
        err(path, slide["line"],
            f"'weeks:' must be the week-column count (4-12), got {raw_w!r}")
    nweeks = int(raw_w)

    streams, current = [], None
    for n, raw in slide["body"]:
        line = raw.strip()
        if not line:
            continue
        m = WS_STREAM_RE.match(line)
        if m:
            current = {"label": m.group(1).strip(), "span": None, "line": n}
            streams.append(current)
            continue
        m = WS_SPAN_RE.match(line)
        if m:
            if current is None:
                err(path, n, "'A-B: text' before any 'stream:' — name the "
                             "workstream first")
            if current["span"]:
                err(path, n, f"stream {current['label']!r} already has its "
                             "'A-B:' bar (exactly one per stream)")
            a, b, dark = int(m.group(1)), int(m.group(2)), m.group(3) == "!"
            if not 1 <= a <= b <= nweeks:
                err(path, n, f"bar {a}-{b} is not a valid week range "
                             f"(weeks 1-{nweeks})")
            current["span"] = (a, b, dark, m.group(4).strip())
            continue
        err(path, n, f"unrecognized workstreams line: {line!r} (expected "
                     "'stream: Label' or 'A-B[!]: text')")
    if not 2 <= len(streams) <= 5:
        err(path, slide["body_start"] or slide["line"],
            f"workstreams takes 2-5 streams, found {len(streams)}")
    for s in streams:
        if not s["span"]:
            err(path, s["line"], f"stream {s['label']!r} has no 'A-B: text' bar")
    if sum(1 for s in streams if s["span"][2]) > 1:
        err(path, slide["body_start"] or slide["line"],
            "workstreams allows at most one '!' dark stream — the one that "
            "converges on the gate")

    checkpoint = None
    if k.get("checkpoint"):
        c = [p.strip() for p in k["checkpoint"].split("::")]
        if len(c) != 2 or not all(c) or not c[0].isdigit():
            err(path, slide["line"],
                "'checkpoint:' needs 'W :: text' (end-of-week number + text)")
        cw = int(c[0])
        if not 1 <= cw < nweeks:
            err(path, slide["line"],
                f"checkpoint week must be 1-{nweeks - 1} (the end of week "
                f"{nweeks} is the gate), got {cw}")
        checkpoint = (cw, c[1])

    gate = None
    if k.get("gate"):
        g = [p.strip() for p in k["gate"].split("::")]
        if len(g) != 3 or not all(g) or not g[0].isdigit():
            err(path, slide["line"],
                "'gate:' needs 'W :: Head :: text' (end-of-week number, "
                "tracked head, annotation text)")
        gw = int(g[0])
        if not 1 <= gw <= nweeks:
            err(path, slide["line"],
                f"gate week must be 1-{nweeks}, got {gw}")
        gate = (gw, g[1], g[2])

    def t_pos(w):
        """CSS left position of the end-of-week-w boundary."""
        f = w / nweeks
        return (f"calc(var(--ws-gutter) + "
                f"(100% - var(--ws-gutter))*{f:.4f})")

    grid = (f" style='grid-template-columns:var(--ws-gutter) "
            f"repeat({nweeks},1fr)")
    out = ["<div class='workstreams'>", f"<div class='ws-ruler'{grid}'>",
           "<div></div>"]
    out.extend(f"<div class='ws-week'>W{w}</div>" for w in range(1, nweeks + 1))
    if gate:
        gw = gate[0]
        mark_pos = ("right:0" if gw == nweeks
                    else f"left:{t_pos(gw)};margin-left:-6px")
        out.append(f"<div class='ws-gate-mark' style='{mark_pos}'></div>")
    out.append("</div>")

    out.append("<div class='ws-main'>")
    out.append(f"<div class='ws-lanes'{grid};"
               f"grid-template-rows:repeat({len(streams)},1fr)'>")
    for i, s in enumerate(streams, 1):
        if i > 1:
            out.append(f"<div class='ws-row-rule' style='grid-row:{i}'></div>")
        out.append(f"<div class='ws-lane-label' style='grid-row:{i}'>"
                   f"{j_text(s['label'])}</div>")
        a, b, dark, text = s["span"]
        cls = "ws-band dark" if dark else "ws-band"
        rng = f"Week {a}" if a == b else f"Weeks {a}–{b}"
        out.append(f"<div class='{cls}' style='grid-row:{i};"
                   f"grid-column:{a + 1}/{b + 2}'>"
                   f"<span class='b-label'>{rng}</span>{j_text(text)}</div>")
    out.append("</div>")

    def note_pos(w):
        """Notes hang left of their time line, right-aligned against it."""
        f = (nweeks - w) / nweeks
        return (f"right:calc((100% - var(--ws-gutter))*{f:.4f} + 14px)"
                if w < nweeks else "right:14px")

    notes = []
    if checkpoint:
        cw, ctext = checkpoint
        out.append(f"<div class='ws-vline check' style='left:{t_pos(cw)}'></div>")
        notes.append(f"<div class='ws-note check' style='{note_pos(cw)}'>"
                     f"<span class='ws-note-head'>Week-{cw} checkpoint</span>"
                     f"<span class='ws-note-text'>{j_text(ctext)}</span></div>")
    if gate:
        gw, ghead, gtext = gate
        line_pos = "right:0" if gw == nweeks else f"left:{t_pos(gw)}"
        out.append(f"<div class='ws-vline gate' style='{line_pos}'></div>")
        notes.append(f"<div class='ws-note gate' style='{note_pos(gw)}'>"
                     f"<span class='ws-note-head'>{j_text(ghead)}</span>"
                     f"<span class='ws-note-text'>{j_text(gtext)}</span></div>")
    out.append(f"<div class='ws-notes'>{''.join(notes)}</div>")
    out.append("</div></div>")

    return (head_html(slide, deck)
            + "<div class='slide-body'>" + "".join(out)
            + f"{source_html(slide)}</div>" + foot_html(deck, page))


def build_comparison(path, slide, deck, page):
    require(path, slide, "title")
    require_body(path, slide)
    blocks = parse_blocks(path, slide["body"])
    table = next((b for b in blocks if b[0] == "table"), None)
    if not table:
        err(path, slide["body_start"], "comparison body must contain a markdown table")
    # 'highlight-col: N' — the winner column (1-based, counting the attribute
    # column) takes the tint wash; one local judgment per slide
    hl_col = None
    raw = slide["keys"].get("highlight-col", "")
    if raw:
        ncols = len(table[1])
        if not raw.isdigit() or not 2 <= int(raw) <= ncols:
            err(path, slide["line"],
                f"'highlight-col:' must be a data column number 2-{ncols}, "
                f"got {raw!r}")
        hl_col = int(raw) - 1
    # sparse tables scale up to own the stage (bar-chart--large principle)
    large = len(table[2]) <= 5
    return (head_html(slide, deck)
            + f"<div class='slide-body'>{render_table(table, hl_col, large)}"
            + f"{source_html(slide)}</div>"
            + takeaway_html(slide) + foot_html(deck, page))


def build_closing(path, slide, deck, page):
    require(path, slide, "title")
    k = slide["keys"]
    body = ""
    if slide["body"]:
        blocks = parse_blocks(path, slide["body"])
        bullets = next((b for b in blocks if b[0] == "bullets"), None)
        # '- decision :: owner :: when' bullets become the decision ledger
        # (DECISION | OWNER | WHEN); '—' or blank renders as an honest empty
        if bullets and all("::" in t for t, _s, _n in bullets[1]):
            rows = ["<div class='dl-row dl-head'><span>Decision</span>"
                    "<span>Owner</span><span>When</span></div>"]
            for text, _subs, n in bullets[1]:
                parts = [p.strip() for p in text.split("::")]
                if len(parts) != 3:
                    err(path, n, "decision ledger row needs "
                                 f"'decision :: owner :: when', got {text!r}")
                cells = [f"<span>{inline_md(parts[0])}</span>"]
                for v in parts[1:]:
                    if v in ("", "—", "-"):
                        cells.append("<span class='dl-empty'>—</span>")
                    else:
                        cells.append(f"<span>{inline_md(v)}</span>")
                rows.append("<div class='dl-row dl-item'>" + "".join(cells)
                            + "</div>")
            body = "<div class='decision-ledger'>" + "".join(rows) + "</div>"
        else:
            body = render_blocks(blocks)
    contact = (f"<div class='closing-contact'>{inline_md(k['contact'])}</div>"
               if k.get("contact") else "")
    return ("<div class='closing-block'><div class='title-tag'></div>"
            f"<h2>{inline_md(k['title'])}</h2>{body}{contact}</div>"
            + foot_html(deck, page))


BUILDERS = {
    "title": build_title, "exec-summary": build_exec_summary,
    "agenda": build_agenda, "content": build_content,
    "two-col": build_two_col, "data": build_data, "kpi": build_kpi,
    "framework": build_framework, "quote": build_quote,
    "timeline": build_timeline, "journey": build_journey,
    "workstreams": build_workstreams,
    "comparison": build_comparison, "closing": build_closing,
}


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------

def render(content_path, brand):
    meta, slides = parse_content(content_path)
    if not meta.get("title"):
        raise DeckError(f"{content_path}:1: frontmatter needs at least 'title:'")
    deck = {
        "title": meta["title"],
        "client": meta.get("client", ""),
        "date": meta.get("date", ""),
        "author": meta.get("author", ""),
        "confidentiality": meta.get(
            "confidentiality", "Confidential — draft for discussion"),
        "logo": meta.get("logo") or brand.get("logo", {}).get("text", ""),
        # framework quadrant markers key off an explicit chart series
        "_chart": bool(brand["palette"].get("chart")),
    }
    # logo slot: a frontmatter 'logo:' text override beats the brand image,
    # the brand image (base64-embedded) beats the brand text
    if not meta.get("logo") and brand.get("logo", {}).get("image"):
        deck["logo_html"] = logo_image_html(brand)
    else:
        deck["logo_html"] = inline_md(deck["logo"])
    html_slides, part_no = [], 0
    for page, slide in enumerate(slides, 1):
        arch = slide["archetype"]
        if arch == "section-divider":
            part_no += 1
            inner = build_divider(content_path, slide, deck, page, part_no)
        else:
            inner = BUILDERS[arch](content_path, slide, deck, page)
        note = slide["keys"].get("notes", "")
        note_html = f"<!-- notes: {html.escape(note).replace('--', '-')} -->" if note else ""
        html_slides.append(
            f"<section class='slide slide--{arch}' data-page='{page}'>"
            f"{note_html}\n{inner}\n</section>")

    template = (LAYOUT_DIR / "master.html").read_text(encoding="utf-8")
    css = (LAYOUT_DIR / "deck.css").read_text(encoding="utf-8")
    doc = (template
           .replace("{{TITLE}}", html.escape(deck["title"]))
           .replace("{{FONTS}}", font_faces_css(brand))
           .replace("{{TOKENS}}", tokens_css(brand))
           .replace("{{CSS}}", css)
           .replace("{{SLIDES}}", "\n\n".join(html_slides)))
    return doc, len(slides)


def find_chrome():
    import shutil
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    for name in ("google-chrome", "chromium", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    return None


def print_pdf(html_path, pdf_path):
    chrome = find_chrome()
    if not chrome:
        print("PDF skipped: no Chrome/Chromium found. Install Google Chrome "
              "(or open the HTML and print to PDF manually) — the HTML output "
              f"is ready at {html_path}")
        return False
    cmd = [chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           f"--print-to-pdf={pdf_path}", html_path.as_uri()]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    if result.returncode != 0 or not pdf_path.exists():
        print(f"PDF failed (chrome exit {result.returncode}):\n{result.stderr[-800:]}")
        return False
    return True


def main():
    ap = argparse.ArgumentParser(description="Render a markdown deck to HTML/PDF.")
    ap.add_argument("content", help="content/<deck>.md")
    ap.add_argument("--brand", default="default",
                    help="brand token name in brands/ (or a yaml path)")
    ap.add_argument("--pdf", action="store_true", help="also print to PDF")
    ap.add_argument("-o", "--out", help="output basename override")
    args = ap.parse_args()

    content_path = Path(args.content)
    if not content_path.exists():
        sys.exit(f"error: content file not found: {content_path}")
    try:
        brand = load_brand(args.brand)
        doc, n = render(content_path, brand)
    except DeckError as e:
        sys.exit(f"error: {e}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    brand_name = Path(brand["_path"]).stem
    base = args.out or f"{content_path.stem}--{brand_name}"
    html_path = OUT_DIR / f"{base}.html"
    html_path.write_text(doc, encoding="utf-8")
    print(f"wrote {html_path.relative_to(KIT)} ({n} slides, brand: {brand.get('name', brand_name)})")

    if args.pdf:
        pdf_path = OUT_DIR / f"{base}.pdf"
        if print_pdf(html_path, pdf_path):
            print(f"wrote {pdf_path.relative_to(KIT)}")


if __name__ == "__main__":
    main()
