#!/usr/bin/env python3
"""render_experience.py — render a markdown deck as The Experience: one
self-contained interactive HTML document.

Usage:
    python3 render_experience.py content/<deck>.md --brand <name>

Spec: doctrine/experience-spec.md. The CSS/JS below was lifted verbatim
from the two canonical interaction prototypes (the 2x2 self-plot and the
substitution model), templated only where content strings enter. Reuses
render_deck.py's parser and brand loader; the content grammar gains only
optional `xp-` keys, which the PDF renderer ignores. All paths resolve
relative to this file's directory (the kit root).

Output: out/experience--<brand>.html — single file, zero external
requests, works from file://. Progressive enhancement: body starts `nojs`
(the complete argument reads top-to-bottom as one document); the boot script
swaps to `js` (staged, interactive). Content errors fail loudly with
file:line references. Stdlib only.
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import render_deck as rd  # noqa: E402  (parser + brand loader reuse)

KIT = Path(__file__).resolve().parent
OUT_DIR = KIT / "out"

err = rd.err
DeckError = rd.DeckError


# --------------------------------------------------------------------------
# xp- key helpers (parse_slide_block collects them as an ordered list)
# --------------------------------------------------------------------------

def xp_list(slide, key):
    return [v for k, v in slide.get("xp", []) if k == key]


def xp_one(slide, key):
    vals = xp_list(slide, key)
    return vals[0] if vals else None


# --------------------------------------------------------------------------
# Evidence ledger (s16) → drawer data + deterministic auto-linking (spec §4)
# --------------------------------------------------------------------------

LEDGER_HEADER = ["study", "finding", "read-through"]
TOKEN_RE = re.compile(
    r"[~<>]?\d+(?:\.\d+)?(?:\s*[-–]\s*\d+(?:\.\d+)?)?\s*(?:%\+|%|x|\+)")
SLUG_ALIAS = {"mckinsey": "mck", "salesforce": "sf"}


def find_ledger(slides):
    """The appendix ledger: a dense data slide whose table header is
    Study | Finding | Read-through. Returns (index, slide) or (None, None)."""
    for i, s in enumerate(slides):
        if s["archetype"] != "data":
            continue
        if s["keys"].get("dense", "").lower() != "true":
            continue
        blocks = rd.parse_blocks(Path("."), s["body"])
        tbl = next((b for b in blocks if b[0] == "table"), None)
        if not tbl:
            continue
        header = [h.strip().lower() for h in tbl[1]]
        if header == LEDGER_HEADER:
            return i, s
    return None, None


def slug_for(study, token):
    first = re.sub(r"[^a-z0-9]", "", study.split(",")[0].split()[0].lower())
    if "11x" in study.lower():
        return "x11"
    first = SLUG_ALIAS.get(first, first)
    digits = re.sub(r"[^0-9x]", "", token.lower()).rstrip("x") \
        if token.lower().endswith("x") else re.sub(r"[^0-9]", "", token)
    if token.lower().rstrip().endswith("x"):
        digits = re.sub(r"[^0-9]", "", token) + "x"
    return f"{first}-{digits}"


def build_ledger(path, slide):
    """Parse the ledger table → ordered rows [{slug, token, study, finding,
    read}]. Loud error on a row with no numeric token."""
    blocks = rd.parse_blocks(path, slide["body"])
    tbl = next(b for b in blocks if b[0] == "table")
    rows = []
    for n, cells in tbl[2]:
        if len(cells) != 3:
            err(path, n, f"ledger row needs 3 cells, got {len(cells)}")
        study, finding, read = (c.strip() for c in cells)
        m = TOKEN_RE.search(finding)
        if not m:
            err(path, n, f"ledger finding has no numeric token to auto-link: "
                         f"{finding!r}")
        token = m.group(0).strip()
        slug = slug_for(study, token)
        if any(r["slug"] == slug for r in rows):
            err(path, n, f"duplicate ledger slug {slug!r}")
        rows.append({"slug": slug, "token": token, "study": study,
                     "finding": finding, "read": read})
    return rows


# Auto-linker: wraps ledger tokens in visible body/exhibit text with an
# ev button. Skips titles, anchors, buttons, and anything marked no-ev.
SKIP_TAGS = {"h1", "h2", "h3", "button", "a", "script", "style"}
VOID_TAGS = {"img", "br", "hr", "meta", "link", "input", "source", "wbr"}
TAG_RE = re.compile(r"<(/?)([a-zA-Z0-9]+)")


class Linker:
    def __init__(self, ledger):
        self.by_token = {}          # html-escaped token -> slug
        for row in ledger:
            self.by_token[html.escape(row["token"], quote=False)] = row["slug"]
        toks = sorted(self.by_token, key=len, reverse=True)
        self.pat = re.compile(
            r"(?<![\w%~<>–-])("
            + "|".join(re.escape(t) for t in toks)
            + r")(?![\w%+])") if toks else None

    def link(self, html_str, used):
        """Wrap token occurrences in text nodes; returns new html.
        `used` (a list) collects slugs in first-seen order."""
        if not self.pat:
            return html_str
        parts = re.split(r"(<[^>]+>)", html_str)
        out, stack, depth = [], [], 0
        for part in parts:
            if part.startswith("<"):
                m = TAG_RE.match(part)
                if m:
                    closing, tag = m.group(1) == "/", m.group(2).lower()
                    selfclose = part.endswith("/>") or tag in VOID_TAGS
                    if not closing and not selfclose:
                        skip = 1 if (tag in SKIP_TAGS or "no-ev" in part) else 0
                        stack.append(skip)
                        depth += skip
                    elif closing and stack:
                        depth -= stack.pop()
                out.append(part)
                continue
            if depth == 0 and part.strip():
                def wrap(m):
                    slug = self.by_token[m.group(1)]
                    if slug not in used:
                        used.append(slug)
                    return (f"<button type='button' class='ev' "
                            f"data-ev='{slug}'>{m.group(1)}</button>")
                part = self.pat.sub(wrap, part)
            out.append(part)
        return "".join(out)


def j_text_x(text, linker, used):
    """Journey inline text: ==x== marks always link (spec §4); falls back to
    the deck's .stat treatment when the mark has no ledger row."""
    def mark(m):
        tok = m.group(1)
        slug = linker.by_token.get(html.escape(tok, quote=False)) if linker else None
        if slug:
            if slug not in used:
                used.append(slug)
            return (f"<button type='button' class='ev ev-stat' "
                    f"data-ev='{slug}'>{html.escape(tok, quote=False)}</button>")
        return f"<span class='stat'>{html.escape(tok, quote=False)}</span>"
    out = []
    for i, seg in enumerate(re.split(r"==(.+?)==", text)):
        out.append(mark(re.match(r"(.*)", seg)) if i % 2 else rd.inline_md(seg))
    return "".join(out)


# --------------------------------------------------------------------------
# Stage builders. Each returns inner html; auto-linking is applied after.
# --------------------------------------------------------------------------

def stage_head(slide, extra_kicker=None):
    k = slide["keys"]
    parts = ["<header class='st-head'>", "<div class='head-rule'></div>"]
    kicker = extra_kicker or k.get("kicker")
    if kicker:
        parts.append(f"<div class='kicker'>{rd.inline_md(kicker)}</div>")
    parts.append(f"<h2 class='st-title'>{rd.inline_md(k['title'])}</h2>")
    if k.get("subtitle"):
        parts.append(f"<div class='st-sub'>{rd.inline_md(k['subtitle'])}</div>")
    parts.append("</header>")
    return "\n".join(parts)


def source_html(slide, extra=""):
    s = slide["keys"].get("source")
    if not s and not extra:
        return ""
    body = f"Source: {rd.inline_md(s)}" if s else ""
    return f"<div class='source-line no-ev'>{body}{extra}</div>"


def takeaway_html(slide):
    t = slide["keys"].get("takeaway")
    if not t:
        return ""
    return ("<div class='takeaway'><span class='takeaway-label'>Takeaway"
            f"</span><p>{rd.inline_md(t)}</p></div>")


def b_title(path, slide, deck):
    rd.require(path, slide, "title")
    k = slide["keys"]
    meta_bits = [deck.get(m) for m in ("client", "date", "author")]
    meta = "".join(f"<span>{rd.inline_md(m)}</span>" for m in meta_bits if m)
    sub = (f"<div class='t-sub'>{rd.inline_md(k['subtitle'])}</div>"
           if k.get("subtitle") else "")
    return (f"<div class='t-logo'>{deck['logo_html']}</div>"
            "<div class='t-block'><div class='title-tag'></div>"
            f"<h1>{rd.inline_md(k['title'])}</h1>{sub}"
            f"<div class='t-meta'>{meta}</div>"
            "<div class='t-apparatus'>Interactive briefing &middot; 4 acts "
            "&middot; every number opens its source.</div>"
            "<div class='nojs-banner nojs-only'>The interactive version needs "
            "JavaScript. What follows is the complete argument, readable top "
            "to bottom.</div></div>")


def b_exec(path, slide, deck):
    rd.require(path, slide, "title")
    rd.require_body(path, slide)
    blocks = rd.parse_blocks(path, slide["body"])
    bullets = next((b for b in blocks if b[0] == "bullets"), None)
    if not bullets:
        err(path, slide["body_start"], "exec-summary body must be bullets")
    goto = {}
    for v in xp_list(slide, "xp-goto"):
        idx, sep, target = v.partition("::")
        if not sep or not re.fullmatch(r"s\d+", target.strip()):
            err(path, slide["line"], f"xp-goto needs 'N :: sN', got {v!r}")
        goto[int(idx.strip())] = target.strip()
    items = []
    for idx, (text, _subs, n) in enumerate(bullets[1], 1):
        lead, sep, support = text.partition("::")
        if not sep or not support.strip():
            err(path, n, f"exec finding needs 'Lead :: support', got {text!r}")
        tgt = goto.get(idx)
        lead_html = rd.inline_md(lead.strip())
        if tgt:
            lead_html = f"<a class='exec-jump' href='#{tgt}'>{lead_html}</a>"
        go = (f"<a class='exec-go' href='#{tgt}'>See the evidence &#8594;</a>"
              if tgt else "")
        items.append(
            "<div class='exec-item'>"
            f"<span class='exec-num no-ev'>{idx}</span>"
            f"<span class='exec-body'><span class='exec-lead'>{lead_html}</span>"
            f"<span class='exec-support'>{rd.inline_md(support.strip())}</span>"
            f"{go}</span></div>")
    return (stage_head(slide) + "<div class='exec-list'>" + "".join(items)
            + "</div>" + source_html(slide))


def b_divider(path, slide, deck, part_no):
    rd.require(path, slide, "title")
    k = slide["keys"]
    label = k.get("label") or f"Part {part_no}"
    sub = (f"<div class='divider-subtitle'>{rd.inline_md(k['subtitle'])}</div>"
           if k.get("subtitle") else "")
    return ("<div class='divider-inner'>"
            f"<div class='divider-label'>{rd.inline_md(label)}</div>"
            f"<h2>{rd.inline_md(k['title'])}</h2>{sub}</div>")


def parse_kpi_split(path, slide):
    """Replicates build_kpi's ':: counter' split parsing (hero + counter)."""
    blocks = rd.parse_blocks(path, slide["body"])
    bullets = next((b for b in blocks if b[0] == "bullets"), None)
    if not bullets:
        err(path, slide["body_start"], "kpi body must be bullets")
    stats, counters = [], []
    for text, _subs, n in bullets[1]:
        parts = [p.strip() for p in text.split("::")]
        flag = parts[-1].lower() if parts[-1].lower() in ("highlight", "counter") else ""
        if flag:
            parts = parts[:-1]
        if len(parts) != 2:
            err(path, n, f"kpi stat needs 'Value :: label', got {text!r}")
        (counters if flag == "counter" else stats).append((parts[0], parts[1]))
    if len(stats) != 1 or len(counters) != 1:
        err(path, slide["body_start"],
            "the experience kpi stage expects the split device: one hero "
            "stat + one ':: counter' stat")
    def pct(v):
        m = re.search(r"(\d+(?:\.\d+)?)\s*%", v)
        if not m:
            err(path, slide["body_start"], f"split kpi value {v!r} needs a %")
        return float(m.group(1))
    hero_v, hero_label = stats[0]
    ctr_v, ctr_label = counters[0]
    return hero_v, hero_label, ctr_v, ctr_label, pct(hero_v), pct(ctr_v)


def b_kpi(path, slide, deck, linker, used):
    rd.require(path, slide, "title")
    rd.require_body(path, slide)
    hero_v, hero_label, ctr_v, ctr_label, a, b = parse_kpi_split(path, slide)
    deck["_hero_share"] = a
    # the hero numeral is itself the live citation when its token has a row
    m = TOKEN_RE.search(hero_v)
    hero_slug = linker.by_token.get(html.escape(m.group(0), quote=False)) \
        if (m and linker) else None
    hero_html = rd.wrap_pct(rd.inline_md(hero_v))
    if hero_slug:
        if hero_slug not in used:
            used.append(hero_slug)
        hero_html = (f"<button type='button' class='ev ev--hero no-ev' "
                     f"data-ev='{hero_slug}'>{hero_html}</button>")
    note_inner = (f"<strong>{rd.inline_md(ctr_v)}</strong> &mdash; "
                  f"{rd.inline_md(ctr_label)}")
    # xp-drill rows → the magnifier panel (spec §5.4)
    drills = []
    for v in xp_list(slide, "xp-drill"):
        head, sep, body = v.partition("::")
        if not sep or not body.strip():
            err(path, slide["line"], f"xp-drill needs 'Head :: body', got {v!r}")
        body = body.strip()
        srcm = re.search(r"\s*\(([^()]+,\s*\d{4})\)\s*$", body)
        src = srcm.group(1) if srcm else (slide["keys"].get("source") or "")
        if srcm:
            body = body[:srcm.start()]
        drills.append((head.strip(), body, src))
    drill_html = ""
    if drills:
        rows = "".join(
            "<div class='mag-row'>"
            f"<div class='mag-head'>{rd.inline_md(h)}</div>"
            f"<div class='mag-body'>{rd.inline_md(bd)}</div>"
            f"<div class='mag-src no-ev'>{rd.inline_md(s)}</div></div>"
            for h, bd, s in drills)
        drill_html = (
            "<div class='mag' id='mag' role='region' "
            "aria-label='The 5 percent, magnified'>"
            "<div class='mag-flare js-only' id='mag-flare' aria-hidden='true'>"
            "<i class='fl-l'></i><i class='fl-r'></i></div>"
            "<div class='mag-label'>The ~5<span class='pct'>%</span>, magnified</div>"
            "<div class='mag-clause'>What the value creators did differently</div>"
            f"<div class='mag-rows'>{rows}</div></div>")
    note = (
        f"<div class='ks-note' style='--ks-tick:{100 - b / 2:g}%'>"
        f"<button type='button' class='mag-btn js-only' data-mag "
        f"aria-expanded='false' aria-controls='mag'>"
        f"<span class='no-ev'>{note_inner}</span></button>"
        f"<span class='ks-note-static nojs-only'>{note_inner}</span></div>")
    return (stage_head(slide)
            + "<div class='kpi-split'>"
            + "<div class='ks-hero'>"
            + f"<div class='ks-num'>{hero_html}</div>"
            + f"<div class='ks-label'>{rd.inline_md(hero_label)}</div></div>"
            + f"<div class='ks-bar' id='ks-bar'>"
            + f"<div class='ks-seg ks-seg-a' style='width:{a:g}%'></div>"
            + ("<button type='button' class='ks-seg ks-seg-b js-only' "
               f"style='width:{b:g}%' data-mag aria-expanded='false' "
               "aria-controls='mag' aria-label='Open the value-creating "
               "share, magnified'></button>"
               f"<div class='ks-seg ks-seg-b nojs-only' style='width:{b:g}%'>"
               "</div>")
            + "</div>"
            + note + drill_html + "</div>"
            + source_html(slide) + takeaway_html(slide))


def b_two_col(path, slide, deck):
    rd.require(path, slide, "title")
    rd.require_body(path, slide)
    blocks = rd.parse_blocks(path, slide["body"])
    cols, current = [], None
    for b in blocks:
        if b[0] == "heading":
            head, _, flag = b[1].partition("::")
            current = {"head": head.strip(), "flag": flag.strip().lower(),
                       "blocks": [], "line": b[2]}
            cols.append(current)
        elif current is None:
            err(path, b[2], "two-col body must start with '## Column heading'")
        else:
            current["blocks"].append(b)
    if len(cols) != 2:
        err(path, slide["body_start"], "two-col needs exactly two columns")
    split = slide["keys"].get("split", "")
    style = ""
    if split:
        m = re.fullmatch(r"([1-9])-([1-9])", split)
        if m:
            style = (f" style='grid-template-columns:{m.group(1)}fr "
                     f"{m.group(2)}fr'")
    def col_body(c):
        if c["flag"] == "stat-rail":
            return rd.render_stat_rail(path, c)
        if c["flag"] == "steps":
            return rd.render_steps(path, c)
        return rd.render_blocks(c["blocks"])
    col_html = "".join(
        f"<div><div class='col-head'>{rd.inline_md(c['head'])}</div>"
        f"{col_body(c)}</div>" for c in cols)
    return (stage_head(slide)
            + f"<div class='two-col'{style}>{col_html}</div>"
            + source_html(slide) + takeaway_html(slide))


def b_data(path, slide, deck):
    rd.require(path, slide, "title")
    rd.require_body(path, slide)
    blocks = rd.parse_blocks(path, slide["body"])
    table = next((b for b in blocks if b[0] == "table"), None)
    bullets = next((b for b in blocks if b[0] == "bullets"), None)
    if table:
        body = f"<div class='tbl-wrap'>{rd.render_table(table)}</div>"
    elif bullets:
        body = rd.render_bars(path, bullets)
    else:
        err(path, slide["body_start"], "data body must be a table or bars")
    return (stage_head(slide) + body + source_html(slide)
            + takeaway_html(slide))


# --- journey (spec §5.8) ---------------------------------------------------

def parse_journey(path, slide):
    """Trimmed re-parse of the journey grammar (render_deck.build_journey
    parses inline and renders in one pass; the experience needs the data)."""
    stages, lanes, brackets = [], [], []
    mode, lane = None, None
    for n, raw in slide["body"]:
        line = raw.strip()
        if not line:
            continue
        if line.rstrip(":") == "stages" and line.endswith(":"):
            mode = "stages"
            continue
        m = rd.J_LANE_RE.match(line)
        if m:
            lane = {"label": m.group(1).strip(), "cells": {}, "spans": []}
            lanes.append(lane)
            mode = "lane"
            continue
        m = rd.J_BRACKET_RE.match(line)
        if m:
            parts = [p.strip() for p in m.group(1).split("::")]
            rng = re.fullmatch(r"(\d+)\s*-\s*(\d+)", parts[0])
            brackets.append((int(rng.group(1)), int(rng.group(2)),
                             parts[1], parts[2]))
            continue
        if mode == "stages":
            m = rd.J_STAGE_RE.match(line)
            name, _, sub = m.group(2).partition("::")
            stages.append((name.strip(), sub.strip()))
            continue
        if mode == "lane":
            m = rd.J_SPAN_RE.match(line)
            if m:
                a, bb, dark = int(m.group(1)), int(m.group(2)), m.group(3) == "!"
                label, _, text = m.group(4).partition("::")
                lane["spans"].append((a, bb, dark, label.strip(), text.strip()))
                continue
            m = rd.J_CELL_RE.match(line)
            if m:
                lane["cells"][int(m.group(1))] = m.group(2).strip()
                continue
        err(path, n, f"unrecognized journey line: {line!r}")
    hi = int(slide["keys"].get("highlight") or 0) or None
    return stages, lanes, brackets, hi


def clause_split(text):
    for sep in ("; ", " — "):
        if sep in text:
            a, b = text.split(sep, 1)
            return a, sep + b
    return text, ""


def b_journey(path, slide, deck, linker, used):
    rd.require(path, slide, "title")
    rd.require_body(path, slide)
    stages, lanes, brackets, hi = parse_journey(path, slide)
    n = len(stages)
    deck["_journey_n"] = n
    grid = ("" if n == 5 else
            f" style='grid-template-columns:104px repeat({n},1fr)'")
    jt = lambda t: j_text_x(t, linker, used)  # noqa: E731

    out = ["<div class='j-grid-wrap'><div class='journey' id='journey'>",
           f"<div class='j-stages'{grid}>"]
    for i, (name, sub) in enumerate(stages, 1):
        cls = "j-stage"
        if i == 1:
            cls += " first"
        if i == n:
            cls += " last"
        if i == hi:
            cls += " hi"
        sub_h = f"<div class='j-stage-sub'>{jt(sub)}</div>" if sub else ""
        out.append(
            f"<button type='button' class='{cls}' data-col='{i}' "
            f"style='grid-column:{i + 1}' aria-label='Focus stage {i}, "
            f"{html.escape(name, quote=True)}'>"
            f"<div class='j-stage-num no-ev'>Stage {i}</div>"
            f"<div class='j-stage-name no-ev'>{jt(name)}</div>{sub_h}</button>")
    out.append("</div>")

    # the dark band's adjacent pull: the first sentence of the bracket whose
    # range matches the dark span (spec §5.8)
    dark_pulls = {}
    for a, bb, _head, text in brackets:
        first = text.split(". ")[0].rstrip(".") + "."
        dark_pulls[(a, bb)] = first

    out.append(f"<div class='j-lanes'{grid}>")
    out.append("<div class='j-row-rule first'></div>")
    for ln in lanes:
        out.append(f"<div class='j-lane-label'>{jt(ln['label'])}</div>")
        if ln["spans"]:
            for a, bb, dark, label, text in sorted(ln["spans"]):
                band = "j-band dark" if dark else "j-band lit"
                pull = ""
                if dark and (a, bb) in dark_pulls:
                    pull = (f"<span class='j-pull no-ev'>"
                            f"{jt(dark_pulls[(a, bb)])}</span>")
                out.append(f"<div class='{band}' "
                           f"style='grid-column:{a + 1}/{bb + 2}'>"
                           f"<span class='b-label'>{jt(label)}</span>"
                           f"{jt(text)}{pull}</div>")
        else:
            for i in range(1, n + 1):
                text = ln["cells"].get(i)
                cls = "j-cell" + (" hi-col" if i == hi else "")
                if text is None:
                    out.append(f"<div class='{cls} empty' data-col='{i}'>"
                               "&mdash;</div>")
                else:
                    first, rest = clause_split(text)
                    rest_h = (f"<span class='rest'>{jt(rest)}</span>"
                              if rest else "")
                    out.append(f"<div class='{cls}' data-col='{i}'>"
                               f"<span class='clause'>{jt(first)}</span>"
                               f"{rest_h}</div>")
        out.append("<div class='j-row-rule'></div>")
    out.append("</div>")

    if brackets:
        out.append(f"<div class='j-brackets no-ev'{grid}><div></div>")
        for a, bb, head, text in brackets:
            out.append(f"<div class='j-bracket' "
                       f"style='grid-column:{a + 1}/{bb + 2}'>"
                       f"<div class='j-bracket-head'>{rd.j_text(head)}</div>"
                       f"<div class='j-bracket-text'>{rd.j_text(text)}</div>"
                       "</div>")
        out.append("</div>")
    out.append("</div></div>")

    out.append(
        "<div class='j-nav js-only'>"
        "<button type='button' id='j-prev' aria-label='Previous journey "
        "stage'>&#8592;</button>"
        "<button type='button' id='j-next' aria-label='Next journey stage'>"
        "&#8594;</button>"
        "<span class='j-hint' id='j-hint'>Tap a stage column to walk the "
        "journey in your order; tap it again for the overview.</span></div>")

    # mobile accordion (same state object; spec §5.8)
    acc = ["<div class='j-acc js-only'>"]
    for i, (name, sub) in enumerate(stages, 1):
        sub_h = f"<span class='j-acc-sub'>{jt(sub)}</span>" if sub else ""
        rows = []
        for ln in lanes:
            if ln["spans"]:
                cell = next((f"<span class='b-label'>{jt(lb)}</span>{jt(tx)}"
                             for a, bb, dk, lb, tx in ln["spans"]
                             if a <= i <= bb), "&mdash;")
                dark = any(dk and a <= i <= bb
                           for a, bb, dk, _l, _t in ln["spans"])
                cls = "j-acc-cell dark" if dark else "j-acc-cell"
            else:
                text = ln["cells"].get(i)
                cell = jt(text) if text else "&mdash;"
                cls = "j-acc-cell"
            rows.append(f"<div class='j-acc-lane'>"
                        f"<div class='j-lane-label'>{jt(ln['label'])}</div>"
                        f"<div class='{cls}'>{cell}</div></div>")
        acc.append(
            f"<div class='j-acc-item'>"
            f"<button type='button' class='j-acc-head' data-col='{i}' "
            f"aria-expanded='false'>"
            f"<span class='j-acc-num no-ev'>Stage {i}</span>"
            f"<span class='j-acc-name no-ev'>{jt(name)}</span>{sub_h}</button>"
            f"<div class='j-acc-body'>{''.join(rows)}</div></div>")
    acc.append("</div>")

    return (stage_head(slide) + "".join(out) + "".join(acc)
            + source_html(slide))


# --- comparison + substitution model (spec §5.9; prototype canonical) -------

def parse_model(path, slide):
    raw = xp_one(slide, "xp-model")
    if not raw:
        return None
    parts = [p.strip() for p in raw.split("::")]
    if not parts or parts[0] != "substitution":
        err(path, slide["line"], f"xp-model kind must be 'substitution', "
                                 f"got {parts[0]!r}")
    cfg = {"default": 100, "range": (20, 500, 10), "mults": (1.5, 1.75, 2)}
    for p in parts[1:]:
        k, _, v = p.partition("=")
        k, v = k.strip(), v.strip()
        try:
            if k == "default":
                cfg["default"] = int(v)
            elif k == "range":
                cfg["range"] = tuple(int(x) for x in v.split(","))
            elif k == "mults":
                cfg["mults"] = tuple(float(x) for x in v.split(","))
            else:
                err(path, slide["line"], f"unknown xp-model field {k!r}")
        except ValueError:
            err(path, slide["line"], f"bad xp-model value {p!r}")
    return cfg


MULT_SUBS = ["conservative", "midpoint", "upper bound"]


def b_comparison(path, slide, deck, model_cfg=None):
    rd.require(path, slide, "title")
    rd.require_body(path, slide)
    blocks = rd.parse_blocks(path, slide["body"])
    table = next((b for b in blocks if b[0] == "table"), None)
    if not table:
        err(path, slide["body_start"], "comparison body needs a table")
    hl_col = None
    raw = slide["keys"].get("highlight-col", "")
    if raw:
        hl_col = int(raw) - 1
    body = (f"<div class='tbl-wrap'>"
            f"{rd.render_table(table, hl_col, large=len(table[2]) <= 5)}</div>")
    model = ""
    if model_cfg:
        lo, hi_, step = model_cfg["range"]
        n0 = model_cfg["default"]
        mults = model_cfg["mults"]
        m0 = mults[0]
        after0 = -(-n0 // 1)  # placeholder; real math in JS + worked example
        import math as _math
        after0 = _math.ceil(n0 / m0)
        rel0 = n0 - after0
        share0 = after0 / n0
        segs = "".join(
            f"<button type='button' data-m='{m:g}' "
            f"aria-pressed='{'true' if i == 0 else 'false'}'>{m:g}&times;"
            + (f"<span class='seg-sub'>{MULT_SUBS[i]}</span>"
               if len(mults) == 3 else "")
            + "</button>"
            for i, m in enumerate(mults))
        rng_note = (f"The published range: one AE plus AI covers "
                    f"{mults[0]:g}&ndash;{mults[-1]:g}x the book.")
        model = (
            "<div class='sub-model'>"
            "<p class='lede'>AI absorbs the ~70% of rep time that is not "
            "selling, so one AE plus AI covers 1.5&ndash;2x the book. Set "
            "your own team size and where you land in that published range; "
            "the math responds.</p>"
            "<div class='controls js-only'>"
            "<div><div class='ctl-label'>Account executives today</div>"
            "<div class='ctl-row'>"
            f"<div class='ctl-value' id='sub-n-out'>{n0}</div>"
            f"<input type='range' id='sub-n' min='{lo}' max='{hi_}' "
            f"step='{step}' value='{n0}' "
            "aria-label='Account executives today'></div>"
            "<div class='ctl-note'>Your input: drag to your team "
            "size.</div></div>"
            "<div><div class='ctl-label'>Coverage per AE with AI</div>"
            f"<div class='seg' role='group' aria-label='Coverage multiplier "
            f"from the published range'>{segs}</div>"
            f"<div class='ctl-note'>{rng_note}</div></div>"
            "</div>"
            "<div class='model js-only' aria-live='polite'>"
            "<div class='m-row'>"
            "<div class='m-row-label'>Your book today<small>covered by"
            "</small></div>"
            "<div class='m-track'><div class='m-fill' id='bar-today'></div>"
            f"<div class='m-val on-fill' id='val-today'>{n0} AEs</div></div>"
            "</div>"
            "<div class='m-row'>"
            "<div class='m-row-label'>The same book<small>with AI in every "
            "loop</small></div>"
            "<div class='m-track'><div class='m-fill' id='bar-after'></div>"
            "<div class='m-released' id='rel-seg'></div>"
            f"<div class='m-val on-fill' id='val-after'>&asymp;{after0} AEs"
            "</div></div></div>"
            "<div class='m-note-row'><div></div>"
            "<div class='m-note' id='m-note'><span class='no-ev'>"
            f"<strong id='rel-strong'>{rel0} seats released</strong>: "
            f"<span id='rel-text'>&asymp;{after0} AEs plus AI cover the book "
            f"your {n0} cover today, with humans still in every loop</span>"
            "</span></div></div>"
            "<button type='button' class='ev-btn' id='caveat-btn' "
            "aria-expanded='false' aria-controls='ev-drawer'>Why not replace "
            "the reps outright?</button>"
            "</div>"
            f"<p class='sub-worked nojs-only'>Worked example at the "
            f"defaults: {n0} AEs at {m0:g}&times;: &asymp;{after0} cover the "
            f"book; {rel0} seats released. Arithmetic on these inputs, not a "
            "finding.</p>"
            "</div>")
    extra_src = (" <span class='src-honesty'>The seat math above is "
                 "arithmetic on your inputs, not a study finding.</span>"
                 if model_cfg else "")
    return (stage_head(slide) + body + model
            + source_html(slide, extra_src) + takeaway_html(slide))


def b_quote(path, slide, deck):
    rd.require_body(path, slide)
    blocks = rd.parse_blocks(path, slide["body"])
    paras = [b[1] for b in blocks if b[0] == "para"]
    text = " ".join(paras).strip().strip('"“”')
    attr = slide["keys"].get("attribution", "")
    attr_html = (f"<div class='quote-attr'><span>{rd.inline_md(attr)}</span>"
                 "</div>" if attr else "")
    size = " quote-text--long" if len(text) > 140 else ""
    return ("<div class='quote-block'>"
            f"<div class='quote-text{size}'>“{rd.inline_md(text)}”"
            f"</div>{attr_html}</div>")


# --- timeline scrub (spec §5.12) --------------------------------------------

def parse_phases(path, slide):
    blocks = rd.parse_blocks(path, slide["body"])
    bullets = next((b for b in blocks if b[0] == "bullets"), None)
    if not bullets:
        err(path, slide["body_start"], "timeline body must be bullets")
    phases = []
    for text, _subs, n in bullets[1]:
        parts = [p.strip() for p in text.split("::")]
        span, exit_ = None, None
        while len(parts) > 2:
            tail = parts[-1]
            low = tail.lower()
            if low.startswith("span:"):
                span = float(tail[5:].strip())
            elif low.startswith("exit:"):
                exit_ = tail[5:].strip()
            else:
                break
            parts = parts[:-1]
        if len(parts) == 3:
            label, time, desc = parts
        else:
            err(path, n, f"timeline phase needs 'Label :: timeframe :: "
                         f"description', got {text!r}")
        if span is None:
            err(path, n, f"phase {label!r} is missing ':: span: N'")
        phases.append({"name": label, "time": time, "desc": desc,
                       "exit": exit_ or "", "span": span})
    return phases


def b_timeline(path, slide, deck):
    rd.require(path, slide, "title")
    rd.require_body(path, slide)
    k = slide["keys"]
    if not k.get("axis"):
        err(path, slide["line"], "the experience timeline stage needs 'axis:'")
    ax = [p.strip() for p in k["axis"].split("::")]
    phases = parse_phases(path, slide)
    total = sum(p["span"] for p in phases)
    cum = 0.0
    for p in phases:
        p["from"] = round(cum / total * 100, 2)
        cum += p["span"]
        p["to"] = round(cum / total * 100, 2)

    gate_pos, gate_label, gate_text = None, "", ""
    if k.get("gate"):
        g = [p.strip() for p in k["gate"].split("::")]
        gate_pos = float(re.fullmatch(r"(\d+(?:\.\d+)?)%?", g[0]).group(1))
        gate_label, gate_text = g[1], g[2]

    # snap points: axis start, the gate, month boundaries parsed from the
    # phase timeframes, axis end (spec §5.12: W0 / W8 / M3 / M6 / M18)
    months = set()
    for p in phases:
        for m in re.findall(r"(\d+)", p["time"]):
            if p["time"].lower().startswith("month"):
                months.add(int(m))
    total_months = max(months) if months else 0
    snaps = [{"p": 0.0, "label": ax[0]}]
    if gate_pos is not None:
        snaps.append({"p": gate_pos, "label": gate_label})
    for m in sorted(months):
        pos = round(m / total_months * 100, 2) if total_months else 0
        if all(abs(pos - s["p"]) > 1 for s in snaps):
            snaps.append({"p": pos, "label": f"M{m}"})
    if all(abs(100 - s["p"]) > 1 for s in snaps):
        snaps.append({"p": 100.0, "label": ax[1]})
    snaps.sort(key=lambda s: s["p"])

    deck["_phases"] = phases
    deck["_snaps"] = snaps
    deck["_gate"] = {"pos": gate_pos, "label": gate_label, "text": gate_text}

    cols = " ".join(f"{p['span']:g}fr" for p in phases)
    band = []
    for i, p in enumerate(phases):
        cls = "pb-phase"
        if i == 0:
            cls += " first"
        if i == len(phases) - 1:
            cls += " last"
        band.append(f"<div class='{cls}'>"
                    f"<div class='pb-time'>{rd.inline_md(p['time'])}</div>"
                    f"<div class='pb-name'>{rd.inline_md(p['name'])}</div>"
                    "</div>")
    gate_html = ""
    if gate_pos is not None:
        gate_html = (
            f"<div class='pb-gate' style='left:{gate_pos:g}%'></div>"
            f"<div class='pb-gate-callout no-ev' style='left:{gate_pos:g}%'>"
            f"<span class='gate-label'>{rd.inline_md(gate_label)}</span>"
            f"{rd.inline_md(gate_text)}</div>")
    p0 = phases[0]
    exit0 = (f"<div class='ph-exit-row'><span class='ph-exit-label'>Exit"
             f"</span><span class='ph-exit' id='ph-exit'>{p0['exit']}</span>"
             "</div>")
    panel = (
        "<div class='ph-panel js-only' aria-live='polite'>"
        "<div id='ph-inner'>"
        f"<div class='pb-time' id='ph-time'>{rd.inline_md(p0['time'])}</div>"
        f"<div class='ph-name' id='ph-name'>{rd.inline_md(p0['name'])}</div>"
        f"<div class='ph-desc' id='ph-desc'>{rd.inline_md(p0['desc'])}</div>"
        f"{exit0}</div></div>")
    lanes = ["<div class='pb-lanes nojs-only'>"]
    for p in phases:
        lanes.append(
            "<div class='pb-row'>"
            f"<div class='pb-row-label'>{rd.inline_md(p['name'])}</div>"
            f"<div><div class='pb-exit'>{rd.inline_md(p['exit'])}</div>"
            f"<div class='pb-row-desc'>{rd.inline_md(p['desc'])}</div></div>"
            "</div>")
    lanes.append("</div>")
    scrub = (
        "<div class='scrub-wrap'>"
        "<div class='scrub' id='scrub' tabindex='0' role='slider' "
        "data-own-keys aria-label='Program timeline, week zero to month "
        "eighteen. Drag or use arrow keys to move between the snap points.' "
        "aria-valuemin='0' aria-valuemax='100' aria-valuenow='0'>"
        "<div class='pb-axis'>"
        f"<span class='pb-axis-label start'>{rd.inline_md(ax[0])}</span>"
        f"<span class='pb-axis-label end'>{rd.inline_md(ax[1])}</span>"
        f"<div class='pb-axis-rule'></div>{gate_html}</div>"
        f"<div id='pb-track'>"
        f"<div class='pb-band' style='grid-template-columns:{cols}'>"
        + "".join(band) + "</div>"
        "<div class='playhead js-only' id='playhead'>"
        "<div class='ph-handle'></div></div>"
        "</div></div>"
        + panel + "".join(lanes) + "</div>")
    return (stage_head(slide) + scrub + source_html(slide)
            + takeaway_html(slide))


# --- framework self-plot (spec §5.13; prototype canonical) -------------------

def b_framework(path, slide, deck):
    rd.require(path, slide, "title")
    rd.require(path, slide, "x-axis")
    rd.require(path, slide, "y-axis")
    rd.require_body(path, slide)
    k = slide["keys"]
    blocks = rd.parse_blocks(path, slide["body"])
    cells, current = [], None
    for b in blocks:
        if b[0] == "heading":
            head, _, flag = b[1].partition("::")
            current = {"head": head.strip(),
                       "hl": flag.strip().lower() == "highlight", "paras": []}
            cells.append(current)
        elif b[0] == "para" and current is not None:
            current["paras"].append(b[1])
    if len(cells) != 4:
        err(path, slide["body_start"], "framework needs four quadrants")

    def cell_index(name):
        for i, c in enumerate(cells):
            if c["head"].lower() == name.strip().lower():
                return i
        err(path, slide["line"], f"unknown quadrant {name!r}")

    plots = {}
    if k.get("plot"):
        q, _, label = k["plot"].partition("::")
        plots[cell_index(q)] = (
            "<div class='fw-plot'><span class='fw-plot-mark'></span>"
            f"<span>{rd.inline_md(label.strip())}</span></div>")
    if k.get("target"):
        q, _, label = k["target"].partition("::")
        plots[cell_index(q)] = (
            "<div class='fw-plot fw-plot--target'>"
            "<span class='fw-plot-mark'></span>"
            f"<span>{rd.inline_md(label.strip())}</span></div>")

    # readings: xp-read / xp-move / xp-src keyed by quadrant title
    readings = {}
    for key, field in (("xp-read", "read"), ("xp-move", "move"),
                       ("xp-src", "src")):
        for v in xp_list(slide, key):
            q, sep, text = v.partition("::")
            if not sep or not text.strip():
                err(path, slide["line"], f"{key} needs 'Quadrant :: text'")
            qi = cell_index(q)
            title = cells[qi]["head"]
            readings.setdefault(title, {"title": title})[field] = text.strip()
    deck["_readings"] = readings
    deck["_quads"] = [c["head"] for c in cells]
    plot_q = k.get("plot", "").partition("::")[0].strip()
    target_q = k.get("target", "").partition("::")[0].strip()
    deck["_rail_default"] = (
        f"The two markers are ours: most enterprise spend sits in {plot_q} "
        f"today, and the 18-month program lands in {target_q}. The grid is "
        "waiting for a third position: yours.")
    deck["_rail_axes"] = (f"Axes: {k['x-axis'].replace(':', ' —', 1)}"
                          if False else
                          f"Axes: {k['x-axis']} × {k['y-axis']}")

    cell_html = "".join(
        f"<div class='fw-cell{' highlight' if c['hl'] else ''}'>"
        f"<div class='fw-cell-title'>{rd.inline_md(c['head'])}</div>"
        + "".join(f"<p>{rd.inline_md(t)}</p>" for t in c["paras"])
        + plots.get(i, "") + "</div>"
        for i, c in enumerate(cells))
    aria = (f"Two-by-two grid. Horizontal: {k['x-axis']}. Vertical: "
            f"{k['y-axis']}. Press Enter to plot your organization at the "
            "center, then arrow keys to move it.")
    rail = ""
    if xp_one(slide, "xp-plot") == "self":
        rail = (
            "<aside class='rail js-only' id='rail' aria-live='polite'>"
            "<div class='rail-eyebrow'>Your position</div>"
            "<div class='rail-inner' id='rail-inner'>"
            "<div class='rail-q' id='rail-q'>Not plotted yet</div>"
            f"<p id='rail-read'>{html.escape(deck['_rail_default'])}</p>"
            "<div id='rail-move-wrap' hidden>"
            "<div class='rail-move-label'>The move</div>"
            "<p id='rail-move'></p></div></div>"
            f"<div class='rail-src' id='rail-src'>"
            f"{html.escape(deck['_rail_axes'])}</div>"
            "<button type='button' class='rail-clear' id='fw-clear'>Clear "
            "my position</button></aside>")
    hint = ("<div class='fw-hint js-only' id='fw-hint'>Tap anywhere on the "
            "grid to plot where your organization sits today. Drag to "
            "adjust.</div>" if rail else "")
    grid_attrs = (" tabindex='0' role='application' data-own-keys "
                  f"aria-label='{html.escape(aria, quote=True)}'"
                  if rail else "")
    fw = ("<div class='xp-fw'><div>"
          "<div class='framework'>"
          f"<div class='fw-y no-ev'>{rd.inline_md(k['y-axis'])}</div>"
          "<div class='fw-main'>"
          f"<div class='fw-grid no-ev' id='fw-grid'{grid_attrs}>{cell_html}"
          "</div>"
          f"<div class='fw-x no-ev'>{rd.inline_md(k['x-axis'])}</div>"
          f"</div></div>{hint}</div>{rail}</div>")
    return (stage_head(slide) + fw + source_html(slide)
            + takeaway_html(slide))


def b_closing(path, slide, deck):
    rd.require(path, slide, "title")
    k = slide["keys"]
    decisions = []
    body = ""
    if slide["body"]:
        blocks = rd.parse_blocks(path, slide["body"])
        bullets = next((b for b in blocks if b[0] == "bullets"), None)
        if bullets and all("::" in t for t, _s, _n in bullets[1]):
            rows = ["<div class='dl-row dl-head'><span>Decision</span>"
                    "<span>Owner</span><span>When</span></div>"]
            for text, _subs, n in bullets[1]:
                parts = [p.strip() for p in text.split("::")]
                if len(parts) != 3:
                    err(path, n, "decision row needs "
                                 "'decision :: owner :: when'")
                decisions.append(parts[0])
                cells = [f"<span>{rd.inline_md(parts[0])}</span>"]
                for v in parts[1:]:
                    cells.append("<span class='dl-empty'>&mdash;</span>"
                                 if v in ("", "—", "-") else
                                 f"<span>{rd.inline_md(v)}</span>")
                rows.append("<div class='dl-row dl-item'>" + "".join(cells)
                            + "</div>")
            body = ("<div class='decision-ledger'>" + "".join(rows)
                    + "</div>")
        else:
            body = rd.render_blocks(blocks)
    deck["_decisions"] = decisions
    contact = (f"<div class='closing-contact'>{rd.inline_md(k['contact'])}"
               "</div>" if k.get("contact") else "")
    echo = ("<div class='close-echo js-only' id='echo' hidden>"
            "<div class='echo-label'>What you did with this argument</div>"
            "<div id='echo-lines'></div></div>")
    actions = ("<div class='close-actions js-only'>"
               "<button type='button' id='copy-btn'>Copy my read-out"
               "</button>"
               "<button type='button' id='reset-btn'>Start over</button>"
               "</div>")
    return ("<div class='closing-block'><div class='title-tag'></div>"
            f"<h2>{rd.inline_md(k['title'])}</h2>{echo}{body}{actions}"
            f"{contact}</div>")


def b_ledger(path, slide, deck, ledger):
    rd.require(path, slide, "title")
    ths = "".join(f"<th>{h}</th>" for h in ("Study", "Finding",
                                            "Read-through"))
    trs = []
    for row in ledger:
        trs.append(
            f"<tr class='lg-row' id='{row['slug']}'>"
            f"<td>{rd.inline_md(row['study'])}</td>"
            f"<td>{rd.inline_md(row['finding'])}</td>"
            f"<td>{rd.inline_md(row['read'])}</td></tr>")
    tbl = ("<div class='tbl-wrap'><table class='deck-table lg-table'>"
           f"<thead><tr>{ths}</tr></thead><tbody>{''.join(trs)}</tbody>"
           "</table></div>")
    note = ("<div class='lg-note'>Every number in this experience traces to "
            "one of these rows.</div>")
    return stage_head(slide) + tbl + note + source_html(slide)


# --------------------------------------------------------------------------
# Assembly
# --------------------------------------------------------------------------

def group_acts(path, slides):
    """Stages grouped by section-dividers plus the closing slide; short act
    labels from 'xp-act:' (fallback: the divider title)."""
    acts, current = [], {"label": None, "stages": []}
    acts.append(current)
    for i, s in enumerate(slides, 1):
        starts = s["archetype"] == "section-divider" or \
            (s["archetype"] == "closing" and current["label"] is not None)
        if starts:
            label = xp_one(s, "xp-act") or s["keys"].get("title", f"Act")
            current = {"label": label, "stages": []}
            acts.append(current)
        current["stages"].append(i)
    return [a for a in acts if a["stages"]]


def argbar_html(deck, acts, n_stages):
    groups = []
    for gi, a in enumerate(acts):
        ticks = "".join(
            f"<button type='button' class='tick' data-s='{s}' "
            f"aria-label='Stage {s}'></button>" for s in a["stages"])
        label = (f"<button type='button' class='act-label' "
                 f"data-s='{a['stages'][0]}'>{html.escape(a['label'])}"
                 "</button>" if a["label"] else "")
        groups.append(f"<span class='act-group' data-g='{gi}'>{label}"
                      f"<span class='ticks'>{ticks}</span></span>")
    return (
        "<header class='argbar js-only'>"
        f"<div class='argbar-title no-ev'>{html.escape(deck['title'])}</div>"
        f"<div class='argbar-act-now' id='act-now'></div>"
        f"<div class='argbar-acts'>{''.join(groups)}</div>"
        f"<div class='argbar-count'><span id='stage-count'>1</span>"
        f"&thinsp;/&thinsp;{n_stages}</div></header>")


DRAWER_HTML = """
<div class="drawer js-only" id="ev-drawer" role="dialog" aria-modal="false"
     aria-label="Evidence" aria-hidden="true">
  <div class="drawer-inner">
    <button type="button" class="drawer-close" id="ev-close">Close</button>
    <h3 id="ev-head"></h3>
    <p id="ev-body"></p>
    <p class="drawer-caveat" id="ev-caveat" hidden><span class="cv-label">Caveat</span>
      <span id="ev-caveat-text"></span></p>
    <p class="src" id="ev-src"></p>
    <div class="drawer-foot"><a id="ev-ledger-link" href="#s16">Full ledger &#8594;</a></div>
  </div>
</div>
<div class="toast" id="toast" role="status"></div>
<nav class="stagenav js-only" aria-label="Stages">
  <button type="button" id="nav-back">&#8592; Back</button>
  <button type="button" id="nav-next">Next &#8594;</button>
</nav>
"""


def render(content_path, brand):
    meta, slides = rd.parse_content(content_path)
    if not meta.get("title"):
        raise DeckError(f"{content_path}:1: frontmatter needs 'title:'")
    deck = {
        "title": meta["title"],
        "client": meta.get("client", ""),
        "date": meta.get("date", ""),
        "author": meta.get("author", ""),
        "logo": meta.get("logo") or brand.get("logo", {}).get("text", ""),
    }
    deck["logo_html"] = (rd.logo_image_html(brand)
                         if not meta.get("logo")
                         and brand.get("logo", {}).get("image")
                         else rd.inline_md(deck["logo"]))

    ledger_idx, ledger_slide = find_ledger(slides)
    ledger = build_ledger(content_path, ledger_slide) if ledger_slide else []
    linker = Linker(ledger)

    acts = group_acts(content_path, slides)
    stage_act = {}
    for gi, a in enumerate(acts):
        for s in a["stages"]:
            stage_act[s] = gi

    sections, part_no = [], 0
    fn_by_stage = {}
    for i, slide in enumerate(slides, 1):
        arch = slide["archetype"]
        used = []
        beat = ""
        extra_cls = ""
        if arch == "title":
            inner = b_title(content_path, slide, deck)
            autolink = False
        elif arch == "exec-summary":
            inner = b_exec(content_path, slide, deck)
            autolink = True
        elif arch == "section-divider":
            part_no += 1
            inner = b_divider(content_path, slide, deck, part_no)
            autolink = False
        elif arch == "kpi":
            inner = b_kpi(content_path, slide, deck, linker, used)
            autolink = True
            beat = " data-beat='split'"
        elif arch == "two-col":
            inner = b_two_col(content_path, slide, deck)
            autolink = True
        elif arch == "data" and i - 1 == ledger_idx:
            inner = b_ledger(content_path, slide, deck, ledger)
            autolink = False
            extra_cls = " stage--ledger"
        elif arch == "data":
            inner = b_data(content_path, slide, deck)
            autolink = True
            blocks = rd.parse_blocks(content_path, slide["body"])
            if any(b[0] == "bullets" for b in blocks):
                beat = " data-beat='bars'"
        elif arch == "journey":
            inner = b_journey(content_path, slide, deck, linker, used)
            autolink = True
        elif arch == "comparison":
            cfg = parse_model(content_path, slide)
            if cfg:
                deck["_model"] = cfg
            inner = b_comparison(content_path, slide, deck, cfg)
            autolink = True
        elif arch == "quote":
            inner = b_quote(content_path, slide, deck)
            autolink = False
        elif arch == "timeline":
            inner = b_timeline(content_path, slide, deck)
            autolink = True
            beat = " data-beat='phases'"
        elif arch == "framework":
            inner = b_framework(content_path, slide, deck)
            autolink = True
        elif arch == "closing":
            inner = b_closing(content_path, slide, deck)
            autolink = False
            extra_cls = " stage--close"
        else:
            err(content_path, slide["line"],
                f"archetype {arch!r} has no experience stage builder")
        if autolink and ledger:
            inner = linker.link(inner, used)
        # s4's methodological hedge lives in the hero figure's drawer (§4)
        if arch == "kpi" and slide["keys"].get("notes") and used:
            deck.setdefault("_caveats", {})[used[0]] = slide["keys"]["notes"]
        fn_by_stage[i] = used
        # no-JS: drawer content as footnote lines under the source line (§8)
        if used:
            fns = []
            for slug in used:
                row = next((r for r in ledger if r["slug"] == slug), None)
                if row:
                    fns.append(
                        f"<p class='fn'><span class='fn-tok'>{html.escape(row['token'])}"
                        f"</span> &middot; {rd.inline_md(row['finding'])} "
                        f"({rd.inline_md(row['study'])}). "
                        f"{rd.inline_md(row['read'])}.</p>")
            if fns:
                inner += ("<div class='st-fn nojs-only no-ev'>"
                          + "".join(fns) + "</div>")
        close_attr = " data-close='1'" if arch == "closing" else ""
        sections.append(
            f"<section class='stage stage--{arch}{extra_cls}' id='s{i}' "
            f"data-act='{stage_act.get(i, 0)}'{beat}{close_attr}>"
            f"\n{inner}\n</section>")

    # drawer/ledger data for the boot script
    ev = {}
    for row in ledger:
        ev[row["slug"]] = {
            "head": row["finding"], "body": row["read"],
            "src": row["study"], "row": row["slug"],
            "caveat": deck.get("_caveats", {}).get(row["slug"], ""),
        }
    if deck.get("_model"):
        x11 = next((r for r in ledger if r["slug"] == "x11"), None)
        ev["x11-caveat"] = {
            "head": "Pure replacement has already been tried, and its "
                    "economics collapsed",
            "body": "11x, the flagship AI-SDR replacement play, saw ~70–"
                    "80% churn and ARR fall from ~$14M to ~$3M; the survivors "
                    "pivoted to augmentation. Voice-gated role replacement is "
                    "real but slower, and ROI claims there are still vendor-"
                    "reported and unaudited.",
            "src": (x11["study"] if x11
                    else "Company reporting on 11x, 2025–26"),
            "row": x11["slug"] if x11 else "",
        }

    data = {
        "title": deck["title"], "date": deck["date"],
        "stateKey": f"deck-xp:{brand['name']}:{deck['title']}:{deck['date']}",
        "ledgerStage": (ledger_idx + 1) if ledger_idx is not None else 0,
        "ledgerCount": len(ledger),
        "citableCount": len([r for r in ledger if r.get("slug") in ev]),
        "ev": ev,
        "quads": deck.get("_quads", []),
        "readings": deck.get("_readings", {}),
        "railDefault": deck.get("_rail_default", ""),
        "railAxes": deck.get("_rail_axes", ""),
        "model": ({"min": deck["_model"]["range"][0],
                   "max": deck["_model"]["range"][1],
                   "step": deck["_model"]["range"][2],
                   "def": deck["_model"]["default"],
                   "mults": list(deck["_model"]["mults"])}
                  if deck.get("_model") else None),
        "journeyN": deck.get("_journey_n", 0),
        "phases": deck.get("_phases", []),
        "snaps": deck.get("_snaps", []),
        "gate": deck.get("_gate", {}),
        "heroShare": deck.get("_hero_share", 0),
        "decisions": deck.get("_decisions", []),
    }
    data_json = json.dumps(data, ensure_ascii=True).replace("</", "<\\/")

    doc = (PAGE_TEMPLATE
           .replace("{{TITLE}}", html.escape(deck["title"]))
           .replace("{{FONTS}}", rd.font_faces_css(brand))
           .replace("{{TOKENS}}", rd.tokens_css(brand))
           .replace("{{CSS}}", EXP_CSS)
           .replace("{{ARGBAR}}", argbar_html(deck, acts, len(slides)))
           .replace("{{STAGES}}", "\n\n".join(sections))
           .replace("{{CHROME}}", DRAWER_HTML)
           .replace("{{DATA}}", data_json)
           .replace("{{JS}}", EXP_JS))
    return doc, len(slides)


# --------------------------------------------------------------------------
# Templates: page, CSS, JS. Prototype CSS/JS lifted verbatim (spec §6);
# deltas are the shared page furniture and content templating only.
# --------------------------------------------------------------------------

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<style>
{{FONTS}}:root {
{{TOKENS}}
  --track-meta: 0.08em;
  --track-label: 0.11em;
  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
}
{{CSS}}
</style>
</head>
<body class="nojs">
{{ARGBAR}}
<main id="stages">
{{STAGES}}
</main>
{{CHROME}}
<script>
window.XPDATA = {{DATA}};
{{JS}}
</script>
</body>
</html>
"""

EXP_CSS = r"""
/* ==========================================================================
   The Experience — staged interactive rendering of the deck.
   Tokens from the brand yaml; motion tokens per Emil Kowalski STANDARDS
   (mined values). Craft layer: type scale 11/13/16/20/25/31/44/55 + display
   numerals (96 mobile / 200 desktop); spacing 4/8/12/16/24/32/48/64/96.
   ========================================================================== */

* { margin: 0; padding: 0; box-sizing: border-box; border-radius: 0; }
html, body { background: var(--c-paper); }
body { font-family: var(--f-body); color: var(--c-ink);
  -webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility; }
:focus-visible { outline: 2px solid var(--c-ink); outline-offset: 2px; }
button { font: inherit; color: inherit; background: none; border: none;
  cursor: pointer; text-align: inherit; }
a { color: inherit; }
strong { font-weight: 700; } em { font-style: italic; }

/* mode gates: progressive enhancement (spec §8) */
body.js .nojs-only { display: none !important; }
body.nojs .js-only { display: none !important; }

/* ---- wayfinding: argument bar + stage nav (spec §3) ---- */
body.js { padding-top: 48px; }
.argbar { position: fixed; top: 0; left: 0; right: 0; height: 48px;
  background: var(--c-paper); border-bottom: 1px solid var(--c-rule);
  display: flex; align-items: center; gap: 24px; padding: 0 24px; z-index: 30; }
.argbar-title { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-ink); white-space: nowrap; }
.argbar-acts { flex: 1 1 auto; display: flex; justify-content: center;
  align-items: center; gap: 16px; min-width: 0; }
.act-group { display: flex; align-items: center; gap: 4px; }
.act-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); padding: 16px 4px; white-space: nowrap;
  transition: color 120ms var(--ease-out); }
.act-group.on .act-label { color: var(--c-ink); }
.ticks { display: flex; }
.tick { width: 16px; height: 48px; display: flex; align-items: center;
  justify-content: center; padding: 0; }
.tick::before { content: ""; width: 6px; height: 6px;
  background: var(--c-rule); transition: background 120ms var(--ease-out); }
.tick.seen::before { background: var(--c-primary); }
.tick.cur::before { background: var(--c-ink); }
.argbar-count { font-size: 11px; color: var(--c-muted);
  font-variant-numeric: tabular-nums; white-space: nowrap; }
.argbar-act-now { display: none; font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-ink); white-space: nowrap; }

.stagenav { position: fixed; right: 24px; bottom: 24px; display: flex;
  gap: 8px; z-index: 30; }
.stagenav button { min-width: 48px; min-height: 48px; padding: 8px 24px;
  border: 1px solid var(--c-ink); background: var(--c-paper);
  font-size: 13px; font-weight: 700;
  transition: background 120ms var(--ease-out); }
.stagenav button:active { background: var(--c-tint); }
.stagenav button[disabled] { border-color: var(--c-rule);
  color: var(--c-rule); cursor: default; }

/* ---- stage shell ---- */
.stage { max-width: 1180px; margin: 0 auto; padding: 48px 64px 96px; }
body.js .stage { display: none; }
body.js .stage.active { display: block;
  animation: stage-in 200ms var(--ease-out); }
@keyframes stage-in { from { opacity: 0; transform: translateY(4px); } }
body.nojs .stage { border-bottom: 1px solid var(--c-rule); }

.head-rule { position: relative; border-top: 1px solid var(--c-rule);
  margin-bottom: 16px; }
.head-rule::before { content: ""; position: absolute; top: -1px; left: 0;
  width: 44px; height: 7px; background: var(--c-accent); }
.kicker { font-size: 13px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); margin-bottom: 8px; }
.st-title { font-family: var(--f-display); font-size: 31px;
  line-height: 1.22; font-weight: 700; max-width: 980px;
  text-wrap: balance; }
.st-sub { font-size: 16px; line-height: 1.5; color: var(--c-muted);
  max-width: 860px; margin-top: 8px; }
.source-line { font-size: 11px; color: var(--c-muted); margin-top: 48px;
  border-top: 1px solid var(--c-rule); padding-top: 16px; }
.takeaway { border-top: 1px solid var(--c-ink); margin-top: 32px;
  padding-top: 16px; display: flex; align-items: baseline; gap: 24px; }
.takeaway-label { flex: none; font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); }
.takeaway p { font-size: 16px; font-weight: 700; line-height: 1.4;
  max-width: 900px; }
.stat { font-weight: 700; color: var(--c-primary); }

/* ---- evidence-on-demand: live citations (spec §4) ---- */
button.ev { display: inline; padding: 0; font: inherit; color: inherit;
  letter-spacing: inherit; text-decoration: underline;
  text-decoration-style: dotted; text-decoration-color: var(--c-muted);
  text-decoration-thickness: 1px; text-underline-offset: 4px; }
button.ev-stat { font-weight: 700; color: var(--c-primary); }
.j-band.dark button.ev-stat { color: var(--c-paper);
  text-decoration-color: var(--c-paper); }
@media (hover: hover) and (pointer: fine) {
  button.ev:hover { text-decoration-color: var(--c-ink); }
}
.ev--hero { text-decoration-thickness: 4px; text-underline-offset: 16px;
  text-decoration-color: var(--c-rule); }
body.nojs button.ev { text-decoration: none; pointer-events: none;
  cursor: text; }

.drawer { position: fixed; left: 0; right: 0; bottom: 0;
  background: var(--c-paper); border-top: 2px solid var(--c-accent);
  padding: 24px 64px 32px; transform: translateY(100%);
  transition: transform 240ms var(--ease-drawer); visibility: hidden;
  z-index: 35; }
.drawer.open { transform: translateY(0); visibility: visible; }
.drawer-inner { max-width: 1052px; margin: 0 auto; position: relative; }
.drawer h3 { font-size: 20px; font-weight: 700; margin-bottom: 8px;
  max-width: 860px; }
.drawer p { font-size: 16px; line-height: 1.5; max-width: 760px;
  margin-bottom: 8px; }
.drawer .drawer-caveat { font-size: 13px; line-height: 1.5;
  color: var(--c-ink); border-left: 2px solid var(--c-rule);
  padding-left: 12px; }
.cv-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); margin-right: 8px; }
.drawer .src { font-size: 13px; color: var(--c-muted); }
.drawer-close { position: absolute; top: 0; right: 0; font-size: 13px;
  font-weight: 700; color: var(--c-muted); text-decoration: underline;
  text-underline-offset: 3px; padding: 8px; }
.drawer-foot { margin-top: 12px; }
.drawer-foot a { font-size: 13px; font-weight: 700;
  color: var(--c-primary); text-decoration: none; }

.toast { position: fixed; left: 50%; bottom: 96px;
  transform: translateX(-50%); background: var(--c-ink);
  color: var(--c-paper); padding: 12px 16px; font-size: 13px;
  font-weight: 700; opacity: 0; transition: opacity 200ms var(--ease-out);
  pointer-events: none; z-index: 40; max-width: 88vw; }
.toast.on { opacity: 1; }

/* ---- s1 title ---- */
.stage--title .t-logo { font-size: 16px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-primary); }
.title-tag { width: 72px; height: 10px; background: var(--c-accent);
  margin-bottom: 24px; }
.stage--title .t-block { margin-top: 96px; }
.stage--title h1 { font-family: var(--f-display); font-size: 55px;
  line-height: 1.12; font-weight: 700; max-width: 900px;
  margin-bottom: 16px; }
.t-sub { font-size: 20px; line-height: 1.45; color: var(--c-muted);
  max-width: 760px; }
.t-meta { display: flex; margin-top: 48px; font-size: 11px;
  letter-spacing: var(--track-meta); text-transform: uppercase;
  color: var(--c-muted); }
.t-meta span { padding: 0 16px; border-left: 1px solid var(--c-rule); }
.t-meta span:first-child { padding-left: 0; border-left: none; }
.t-apparatus { margin-top: 24px; font-size: 13px; color: var(--c-muted); }
.nojs-banner { border: 1px solid var(--c-ink); padding: 16px;
  margin-top: 32px; font-size: 16px; line-height: 1.5; max-width: 640px; }

/* ---- s2 exec summary: the argument map (spec §5.2) ---- */
.exec-list { max-width: 1080px; margin-top: 24px; }
.exec-item { display: flex; align-items: baseline; gap: 32px;
  padding: 16px 0; border-bottom: 1px solid var(--c-rule); }
.exec-item:first-child { border-top: 1px solid var(--c-ink); }
.exec-num { flex: none; width: 40px; font-size: 25px; font-weight: 700;
  color: var(--c-muted); text-align: right;
  font-variant-numeric: lining-nums tabular-nums; }
.exec-lead { display: block; font-family: var(--f-display);
  font-size: 20px; line-height: 1.3; font-weight: 700; }
a.exec-jump { text-decoration: none; }
@media (hover: hover) and (pointer: fine) {
  a.exec-jump:hover { text-decoration: underline;
    text-underline-offset: 4px; }
}
.exec-support { display: block; font-size: 13px; line-height: 1.45;
  color: var(--c-ink); margin-top: 4px; max-width: 920px; }
.exec-go { display: inline-block; margin-top: 8px; padding: 8px 0;
  font-size: 13px; font-weight: 700; color: var(--c-primary);
  text-decoration: none; }

/* ---- act openers (dividers) ---- */
.stage--section-divider { max-width: none; padding: 0;
  background: var(--c-divider-ground); color: var(--c-divider-ink); }
.stage--section-divider .divider-inner { max-width: 1180px;
  margin: 0 auto; padding: 96px 64px; }
body.js .stage--section-divider.active { display: flex;
  align-items: center; min-height: calc(100vh - 48px); }
body.js .stage--section-divider .divider-inner { width: 100%; }
.divider-label { font-size: 13px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-divider-ink); opacity: 0.72; padding-bottom: 16px;
  margin-bottom: 24px; width: 320px;
  border-bottom: 1px solid color-mix(in srgb, var(--c-divider-ink) 35%, transparent); }
.stage--section-divider h2 { font-family: var(--f-display);
  font-size: 44px; line-height: 1.15; font-weight: 700; max-width: 940px;
  text-wrap: balance; }
.divider-subtitle { font-size: 20px; line-height: 1.45; margin-top: 16px;
  max-width: 820px; opacity: 0.82; }

/* ---- s4 kpi split + the sliver drill (spec §5.4) ---- */
.kpi-split { margin-top: 32px; max-width: 1100px; }
.ks-hero { display: flex; align-items: baseline; gap: 48px; }
.ks-num { font-family: var(--f-body); font-size: 200px; line-height: 0.78;
  font-weight: 700; letter-spacing: -0.015em; color: var(--c-primary);
  font-variant-numeric: lining-nums tabular-nums; }
.ks-num .unit { font-size: 0.55em; letter-spacing: 0; }
.ks-label { font-size: 20px; line-height: 1.35; max-width: 560px; }
.ks-bar { display: flex; gap: 2px; width: 100%; height: 112px;
  margin-top: 48px; }
.ks-seg { transform-origin: left center; }
.ks-seg-a { background: var(--c-primary); }
.ks-seg-b { background: var(--c-accent); }
button.ks-seg-b { position: relative; padding: 0; }
button.ks-seg-b::after { content: ""; position: absolute;
  inset: -8px -16px; }
.ks-note { position: relative; width: 100%; padding-top: 16px;
  display: flex; justify-content: flex-end; }
.ks-note::before { content: ""; position: absolute; top: 0;
  left: var(--ks-tick, 97.5%); height: 12px;
  border-left: 1px solid var(--c-ink); }
.ks-note span { font-size: 16px; line-height: 1.4; text-align: right; }
.ks-note strong { font-weight: 700; color: var(--c-accent); }
.mag-btn { padding: 0; }
.mag-btn > span { display: inline-block; text-decoration: underline;
  text-decoration-style: dotted; text-decoration-color: var(--c-muted);
  text-decoration-thickness: 1px; text-underline-offset: 4px; }
@media (hover: hover) and (pointer: fine) {
  .mag-btn:hover > span { text-decoration-color: var(--c-ink); }
}
.mag { display: none; position: relative; margin-top: 24px;
  border-top: 1px solid var(--c-ink); padding-top: 24px; }
.mag.open { display: block; animation: panel-in 200ms var(--ease-out); }
body.nojs .mag { display: block; }
@keyframes panel-in { from { opacity: 0; transform: translateY(8px); } }
.mag-flare { position: absolute; left: 0; right: 0; bottom: 100%;
  height: 24px; pointer-events: none; }
.mag-flare .fl-l { position: absolute; top: 0; left: 0; width: 0;
  border-top: 1px solid var(--c-rule); transform-origin: left center; }
.mag-flare .fl-r { position: absolute; top: 0; bottom: 0; right: 0;
  border-left: 1px solid var(--c-rule); }
.mag-label { font-size: 13px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); }
.mag-label .pct { text-transform: none; }
.mag-clause { font-size: 16px; margin-top: 4px; }
.mag-rows { display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 48px; margin-top: 24px; }
.mag-head { font-size: 20px; font-weight: 700; line-height: 1.3; }
.mag-body { font-size: 16px; line-height: 1.5; margin-top: 8px; }
.mag-src { font-size: 13px; color: var(--c-muted); margin-top: 8px; }

/* the s4 beat: split segments draw once, 95 then 5 (spec §5.4) */
.stage.beat[data-beat="split"] .ks-seg-a {
  animation: draw-x 500ms var(--ease-out) backwards; }
.stage.beat[data-beat="split"] .ks-seg-b {
  animation: draw-x 500ms var(--ease-out) 80ms backwards; }
@keyframes draw-x { from { transform: scaleX(0); } }

/* ---- s5 two-col: stat rail + steps ---- */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 48px;
  margin-top: 32px; }
.col-head { font-size: 20px; font-weight: 700; padding-bottom: 8px;
  border-bottom: 1px solid var(--c-ink); margin-bottom: 16px; }
.two-col ul { list-style: none; }
.two-col ul > li { position: relative; font-size: 16px; line-height: 1.45;
  padding-left: 24px; margin-bottom: 12px; }
.two-col ul > li::before { content: ""; position: absolute; left: 2px;
  top: 0.52em; width: 6px; height: 6px; background: var(--c-ink); }
.two-col p { font-size: 16px; line-height: 1.5; margin-bottom: 12px; }
.stat-rail { display: flex; flex-direction: column; }
.rail-row { display: grid; grid-template-columns: 220px 1fr; gap: 24px;
  align-items: center; padding: 16px 0; }
.rail-row + .rail-row { border-top: 1px solid var(--c-rule); }
.rail-value { font-family: var(--f-body); font-size: 44px;
  line-height: 1.05; font-weight: 700; letter-spacing: -0.01em;
  color: var(--c-primary); font-variant-numeric: lining-nums tabular-nums; }
.rail-value .unit { font-size: 0.58em; letter-spacing: 0; }
.rail-value--words { font-size: 31px; line-height: 1.1; }
.rail-claim { font-size: 16px; line-height: 1.45; }
.step-stack { display: flex; flex-direction: column; }
.step-cell { background: var(--c-tint); padding: 16px; font-size: 16px;
  line-height: 1.4; }
.step-arrow { align-self: center; width: 0; height: 0;
  border-left: 8px solid transparent; border-right: 8px solid transparent;
  border-top: 8px solid var(--c-ink); margin: 8px 0; }
.step-close { padding-top: 16px; font-size: 16px; font-weight: 700;
  line-height: 1.4; }

/* ---- s6 bars ---- */
.bar-chart { max-width: 1020px; margin-top: 32px; }
.bar-row { display: grid;
  grid-template-columns: var(--bar-label-w, 300px) 1fr;
  align-items: center; margin-bottom: 16px; }
.bar-label { font-size: 16px; line-height: 1.3; padding-right: 24px;
  text-align: right; }
.bar-track { position: relative; border-left: 1.5px solid var(--c-ink);
  height: 38px; display: flex; align-items: center; }
.bar-fill { height: 30px; background: var(--c-muted); flex: none;
  transform-origin: left center; }
.bar-row.highlight .bar-fill { background: var(--c-accent); }
.bar-value { font-size: 16px; font-weight: 700; margin-left: 12px;
  font-variant-numeric: tabular-nums; }
.bar-row.highlight .bar-value { color: var(--c-accent); }
.bar-chart--large .bar-row { margin-bottom: 32px; }
.bar-chart--large .bar-track { height: 64px; }
.bar-chart--large .bar-fill { height: 52px; }
.bar-chart--large .bar-value { font-size: 20px; }
.bar-chart--xl { max-width: 1100px; margin-top: 48px; }
.bar-chart--xl .bar-row { margin-bottom: 48px; }
.bar-chart--xl .bar-row:last-child { margin-bottom: 0; }
.bar-chart--xl .bar-track { height: 176px; }
.bar-chart--xl .bar-fill { height: 156px; }
.bar-chart--xl .bar-label { font-size: 20px; line-height: 1.35; }
.bar-chart--xl .bar-value { font-size: 31px; margin-left: 16px; }
.stage.beat[data-beat="bars"] .bar-fill {
  animation: draw-x 500ms var(--ease-out) backwards; }
.stage.beat[data-beat="bars"] .bar-row:nth-child(2) .bar-fill {
  animation-delay: 80ms; }
.stage.beat[data-beat="bars"] .bar-row:nth-child(3) .bar-fill {
  animation-delay: 160ms; }

/* ---- tables ---- */
.tbl-wrap { margin-top: 24px; }
table.deck-table { border-collapse: collapse; width: 100%;
  max-width: 1120px; }
table.deck-table th { font-size: 13px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  text-align: left; border-top: 1px solid var(--c-ink);
  border-bottom: 1px solid var(--c-ink); padding: 12px 16px 12px 0; }
table.deck-table td { font-size: 16px; line-height: 1.4;
  padding: 12px 16px 12px 0; border-bottom: 1px solid var(--c-rule);
  vertical-align: top; }
table.deck-table td:first-child { font-weight: 700; }
table.deck-table tr:nth-child(even) td { background: var(--c-tint); }
table.deck-table--large td { line-height: 1.45;
  padding: 24px 16px 24px 0; }
table.deck-table tr.tr-band td { background: none; border-bottom: none; }
table.deck-table tr.tr-band td.td-band { background: var(--c-primary);
  color: var(--c-paper); font-weight: 700; padding-left: 16px;
  padding-right: 16px; }
table.deck-table tr.tr-band td.td-band button.ev { color: var(--c-paper);
  text-decoration-color: var(--c-paper); }
table.deck-table--hl tbody tr:nth-child(even) td:not(.hl-col) {
  background: none; }
table.deck-table--hl th.hl-col, table.deck-table--hl td.hl-col {
  background: var(--c-tint); padding-left: 16px; }
table.deck-table--hl th.hl-col { border-top: 2px solid var(--c-ink); }

/* ---- s8 journey: explorable (spec §5.8) ---- */
.j-grid-wrap { margin-top: 32px; }
.journey { width: 100%; }
.j-stages { display: grid; grid-template-columns: 104px repeat(5, 1fr); }
.j-stage { grid-row: 1; position: relative; background: var(--c-tint);
  padding: 9px 12px 10px 24px; width: 100%; display: block;
  clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%,
    calc(100% - 10px) 100%, 0 100%, 10px 50%); }
.j-stage.first { clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%,
  calc(100% - 10px) 100%, 0 100%); padding-left: 14px; }
.j-stage.last { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%,
  10px 50%); }
body.js .j-stage { cursor: pointer; }
.j-stage-num { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); }
.j-stage-name { font-size: 16px; font-weight: 700; margin-top: 2px; }
.j-stage-sub { font-size: 11px; color: var(--c-muted); margin-top: 2px; }
.j-stage.hi { background: var(--c-accent); }
.j-stage.hi .j-stage-num, .j-stage.hi .j-stage-sub {
  color: var(--c-paper); opacity: 0.85; }
.j-stage.hi .j-stage-name { color: var(--c-paper); }
body.js .j-stage.seen::after { content: ""; position: absolute; top: 10px;
  right: 18px; width: 6px; height: 6px; background: var(--c-ink); }
body.js .j-stage.hi.seen::after { background: var(--c-paper); }
.j-lanes { display: grid; grid-template-columns: 104px repeat(5, 1fr);
  margin-top: 14px; }
.j-lane-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); padding: 10px 14px 10px 0; line-height: 1.45; }
.j-cell { font-size: 13px; line-height: 1.35; padding: 10px 16px 12px 0; }
body.js .j-cell { cursor: pointer; }
.j-row-rule { grid-column: 1 / -1; border-top: 1px solid var(--c-rule); }
.j-row-rule.first { border-top: 1px solid var(--c-ink); }
.j-cell .stat { font-weight: 700; color: var(--c-primary); }
.j-cell.empty { color: var(--c-rule); }
.j-cell.hi-col { background: var(--c-tint); padding-left: 10px;
  padding-right: 12px; margin-right: 2px; }
body.js .j-cell.mini .rest { display: none; }
.j-band { font-size: 11px; line-height: 1.4; padding: 8px 16px 9px 10px; }
.j-band .b-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  display: block; margin-bottom: 2px; }
.j-band.dark { background: var(--c-primary); color: var(--c-paper);
  margin-right: 2px; }
.j-band.dark .b-label { color: var(--c-paper); opacity: 0.8; }
.j-band.lit { border-top: 1px solid var(--c-ink); }
.j-pull { display: none; margin-top: 8px; font-weight: 700; }
.journey[data-focus="1"] .j-pull, .journey[data-focus="2"] .j-pull,
.journey[data-focus="3"] .j-pull { display: block; }
.j-brackets { display: grid; grid-template-columns: 104px repeat(5, 1fr);
  margin-top: 16px; }
.j-bracket { position: relative; padding-top: 10px; margin-right: 8px; }
.j-bracket + .j-bracket { margin-left: 8px; margin-right: 0; }
.j-bracket::before { content: ""; position: absolute; top: 0; left: 0;
  right: 0; height: 7px; border-left: 1px solid var(--c-ink);
  border-right: 1px solid var(--c-ink); border-top: 1px solid var(--c-ink); }
.j-bracket-head { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  margin-top: 4px; }
.j-bracket-text { font-size: 11px; line-height: 1.4; margin-top: 3px;
  max-width: 560px; }
/* the 150ms content swap on focus change (reflow accepted, no FLIP) */
.j-stage, .j-cell, .j-band { transition: opacity 150ms var(--ease-out); }
.journey.j-swap .j-stage, .journey.j-swap .j-cell,
.journey.j-swap .j-band { opacity: 0; }
.j-nav { display: flex; align-items: center; gap: 8px; margin-top: 16px; }
.j-nav button { min-width: 48px; min-height: 44px;
  border: 1px solid var(--c-ink); font-weight: 700; text-align: center;
  transition: background 120ms var(--ease-out); }
.j-nav button:active { background: var(--c-tint); }
.j-hint { font-size: 13px; color: var(--c-muted); margin-left: 8px; }
.j-acc { display: none; margin-top: 24px; }
.j-acc-item { border-top: 1px solid var(--c-rule); }
.j-acc-item:first-child { border-top: 1px solid var(--c-ink); }
.j-acc-head { width: 100%; display: block; padding: 12px 0;
  min-height: 48px; }
.j-acc-num { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); display: block; }
.j-acc-name { font-size: 16px; font-weight: 700; }
.j-acc-sub { font-size: 13px; color: var(--c-muted); margin-left: 8px; }
.j-acc-body { display: none; padding: 0 0 16px; }
.j-acc-item.open .j-acc-body { display: block; }
.j-acc-lane { margin-top: 12px; }
.j-acc-cell { font-size: 13px; line-height: 1.45; margin-top: 4px; }
.j-acc-cell.dark { background: var(--c-primary); color: var(--c-paper);
  padding: 8px 12px; }
.j-acc-cell.dark .b-label { color: var(--c-paper); opacity: 0.8;
  font-size: 11px; font-weight: 700; letter-spacing: var(--track-label);
  text-transform: uppercase; display: block; margin-bottom: 2px; }
.j-acc-cell .b-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  display: block; margin-bottom: 2px; }

/* ---- s9 substitution model (prototype canonical, lifted verbatim) ---- */
.sub-model .lede { font-size: 16px; line-height: 1.5; max-width: 760px;
  margin-top: 32px; }
.controls { display: grid; grid-template-columns: 1fr 1fr; gap: 48px;
  margin-top: 32px; border-top: 1px solid var(--c-ink); padding-top: 24px; }
.ctl-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); margin-bottom: 12px; }
.ctl-row { display: flex; align-items: baseline; gap: 24px; }
.ctl-value { font-size: 44px; font-weight: 700; color: var(--c-primary);
  letter-spacing: -0.01em; font-variant-numeric: lining-nums tabular-nums;
  min-width: 120px; }
input[type=range] { flex: 1 1 auto; -webkit-appearance: none;
  appearance: none; height: 32px; background: transparent; cursor: pointer;
  align-self: center; }
input[type=range]::-webkit-slider-runnable-track { height: 2px;
  background: var(--c-rule); }
input[type=range]::-webkit-slider-thumb { -webkit-appearance: none;
  width: 16px; height: 16px; background: var(--c-primary);
  margin-top: -7px; }
input[type=range]::-moz-range-track { height: 2px;
  background: var(--c-rule); }
input[type=range]::-moz-range-thumb { width: 16px; height: 16px;
  background: var(--c-primary); border: none; border-radius: 0; }
.seg { display: flex; gap: 8px; }
.seg button { flex: 1; min-height: 48px; padding: 8px 12px;
  border: 1px solid var(--c-ink); font-size: 16px; font-weight: 700;
  font-variant-numeric: lining-nums tabular-nums; text-align: center;
  transition: background 120ms var(--ease-out),
    color 120ms var(--ease-out); }
.seg button .seg-sub { display: block; font-size: 11px; font-weight: 400;
  letter-spacing: 0; color: var(--c-muted); margin-top: 2px; }
.seg button[aria-pressed=true] { background: var(--c-ink);
  color: var(--c-paper); }
.seg button[aria-pressed=true] .seg-sub { color: var(--c-paper); }
.seg button:active { background: var(--c-tint); }
.ctl-note { font-size: 13px; color: var(--c-muted); margin-top: 12px; }
.model { margin-top: 48px; }
.m-row { display: grid; grid-template-columns: 220px 1fr; gap: 24px;
  align-items: center; margin-bottom: 16px; }
.m-row-label { font-size: 16px; line-height: 1.35; text-align: right; }
.m-row-label small { display: block; font-size: 13px;
  color: var(--c-muted); }
.m-track { position: relative; height: 56px; }
.m-fill { position: absolute; inset: 0; background: var(--c-primary);
  transform-origin: left center;
  transition: transform 250ms var(--ease-in-out); }
.m-released { position: absolute; top: 0; bottom: 0;
  background: var(--c-tint); border: 1px solid var(--c-rule);
  transition: left 250ms var(--ease-in-out),
    width 250ms var(--ease-in-out); }
.m-val { position: absolute; top: 50%; transform: translateY(-50%);
  white-space: nowrap; font-size: 20px; font-weight: 700;
  font-variant-numeric: lining-nums tabular-nums; }
.m-val.on-fill { color: var(--c-paper); left: 16px; }
.m-note-row { display: grid; grid-template-columns: 220px 1fr; gap: 24px;
  margin-top: -16px; }
.m-note { position: relative; padding-top: 16px; display: flex;
  justify-content: flex-end; }
.m-note::before { content: ""; position: absolute; top: 0;
  left: var(--m-tick, 83.5%); height: 12px;
  border-left: 1px solid var(--c-ink);
  transition: left 250ms var(--ease-in-out); }
.m-note span { font-size: 16px; line-height: 1.4; text-align: right;
  max-width: 560px; }
.m-note strong { font-size: 20px; font-weight: 700;
  color: var(--c-accent); font-variant-numeric: lining-nums tabular-nums; }
.ev-btn { display: inline-block; margin-top: 24px; padding: 8px 0;
  font-size: 13px; font-weight: 700; color: var(--c-primary);
  text-decoration: underline; text-decoration-style: dotted;
  text-underline-offset: 4px; }
.sub-worked { font-size: 16px; line-height: 1.5; margin-top: 24px;
  max-width: 760px; }
.src-honesty { font-weight: 700; }

/* ---- s10 quote ---- */
.stage--quote .quote-block { max-width: 1080px; padding: 96px 0; }
.quote-text { font-family: var(--f-display); font-size: 44px;
  line-height: 1.3; font-weight: 400; text-indent: -0.45em; }
.quote-text--long { font-size: 31px; line-height: 1.35; }
.quote-attr { margin-top: 32px; }
.quote-attr::before { content: ""; display: block; width: 44px;
  height: 3px; background: var(--c-accent); margin-bottom: 16px; }
.quote-attr span { font-size: 13px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); }

/* ---- s12 timeline: the scrub (spec §5.12) ---- */
.scrub-wrap { margin-top: 48px; }
.scrub { position: relative; touch-action: none; }
body.js .scrub { cursor: pointer; }
.pb-axis { position: relative; height: 32px; }
.pb-axis-rule { position: absolute; left: 0; right: 0; bottom: 0;
  border-top: 1.5px solid var(--c-ink); }
.pb-axis-label { position: absolute; bottom: 10px; font-size: 11px;
  font-weight: 700; letter-spacing: var(--track-label);
  text-transform: uppercase; color: var(--c-muted); }
.pb-axis-label.start { left: 0; }
.pb-axis-label.end { right: 0; }
.pb-gate { position: absolute; bottom: -7px; width: 13px; height: 13px;
  margin-left: -6px; background: var(--c-accent); z-index: 1; }
.scrub.gate-on .pb-gate { outline: 2px solid var(--c-accent);
  outline-offset: 2px; }
.pb-gate-callout { position: absolute; bottom: 10px; margin-left: 16px;
  font-size: 13px; white-space: nowrap; }
.pb-gate-callout .gate-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  margin-right: 10px; }
.scrub.gate-on .pb-gate-callout .gate-label { color: var(--c-accent); }
#pb-track { position: relative; }
.pb-band { display: grid; }
.pb-phase { position: relative; background: var(--c-tint);
  padding: 12px 12px 12px 24px; transform-origin: left center;
  clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%,
    calc(100% - 10px) 100%, 0 100%, 10px 50%); }
.pb-phase.first { clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%,
  calc(100% - 10px) 100%, 0 100%); padding-left: 16px; }
.pb-phase.last { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%,
  10px 50%); }
.pb-time { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); }
.pb-name { font-family: var(--f-display); font-size: 20px;
  font-weight: 700; margin-top: 3px; }
.stage.beat[data-beat="phases"] .pb-phase {
  animation: draw-x 250ms var(--ease-out) backwards; }
.stage.beat[data-beat="phases"] .pb-phase:nth-child(2) {
  animation-delay: 125ms; }
.stage.beat[data-beat="phases"] .pb-phase:nth-child(3) {
  animation-delay: 250ms; }
.playhead { position: absolute; top: -10px; bottom: -22px; left: 0;
  width: 0; border-left: 2px solid var(--c-ink); z-index: 2;
  transition: left 250ms var(--ease-in-out); }
.scrub.dragging .playhead { transition: none; }
.ph-handle { position: absolute; bottom: 0; left: -9px; width: 16px;
  height: 16px; background: var(--c-ink); }
.ph-panel { margin-top: 48px; border-top: 1px solid var(--c-ink);
  padding-top: 16px; max-width: 760px; }
#ph-inner { transition: opacity 150ms var(--ease-out); }
#ph-inner.swap { opacity: 0; }
.ph-name { font-size: 20px; font-weight: 700; margin-top: 4px; }
.ph-desc { font-size: 16px; line-height: 1.5; margin-top: 8px; }
.ph-exit-row { margin-top: 16px; border-top: 1px solid var(--c-rule);
  padding-top: 12px; }
.ph-exit-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-accent); margin-right: 12px; }
.ph-exit { font-size: 16px; font-weight: 700; }
.pb-lanes { display: flex; flex-direction: column; margin-top: 32px; }
.pb-row { display: grid; grid-template-columns: 200px 1fr;
  align-items: center; border-top: 1px solid var(--c-rule);
  padding: 16px 0; }
.pb-row:first-child { border-top: 1px solid var(--c-ink); }
.pb-row-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); padding-right: 16px; line-height: 1.5; }
.pb-exit { font-size: 20px; font-weight: 700; line-height: 1.35; }
.pb-row-desc { font-size: 13px; line-height: 1.45; margin-top: 4px;
  max-width: 880px; }

/* ---- s13 the 2x2 self-plot (prototype canonical, lifted verbatim) ---- */
.xp-fw { display: grid; grid-template-columns: 1fr 340px; gap: 48px;
  margin-top: 32px; align-items: start; }
.framework { display: flex; gap: 8px; }
.fw-y { flex: none; writing-mode: vertical-rl; transform: rotate(180deg);
  text-align: center; padding-left: 12px; font-size: 13px;
  color: var(--c-muted); }
.fw-main { flex: 1 1 auto; min-width: 0; display: flex;
  flex-direction: column; }
.fw-x { text-align: center; padding: 12px 0 4px 0; font-size: 13px;
  color: var(--c-muted); }
.fw-grid { position: relative; display: grid;
  grid-template-columns: 1fr 1fr; grid-template-rows: 1fr 1fr;
  height: 480px; }
body.js .fw-grid { cursor: crosshair; touch-action: none;
  user-select: none; -webkit-user-select: none; }
.fw-cell { padding: 24px 24px 16px 24px; overflow: hidden; display: flex;
  flex-direction: column; justify-content: flex-start; }
.fw-cell:nth-child(1) { border-right: 1px solid var(--c-rule);
  border-bottom: 1px solid var(--c-rule); }
.fw-cell:nth-child(2) { border-bottom: 1px solid var(--c-rule); }
.fw-cell:nth-child(3) { border-right: 1px solid var(--c-rule); }
.fw-cell.highlight { background: var(--c-tint); }
.fw-cell-title { font-size: 20px; font-weight: 700; margin-bottom: 8px; }
.fw-cell p { font-size: 16px; line-height: 1.45; max-width: 460px; }
.fw-plot { display: flex; align-items: center; gap: 8px;
  margin-top: auto; padding-top: 16px; font-size: 13px;
  font-weight: 700; }
.fw-plot-mark { flex: none; width: 10px; height: 10px;
  background: var(--c-primary); }
.fw-plot--target .fw-plot-mark { background: var(--c-accent); }
.fw-hint { margin-top: 8px; font-size: 13px; color: var(--c-muted); }
.you { position: absolute; display: flex; align-items: center; gap: 8px;
  transform: translate(-8px, -8px); font-size: 13px; font-weight: 700;
  color: var(--c-ink); pointer-events: none; white-space: nowrap;
  background: var(--c-paper); padding: 3px 8px 3px 3px;
  outline: 1px solid var(--c-rule); }
.you.flip { padding: 3px 3px 3px 8px; }
.you-mark { flex: none; width: 14px; height: 14px;
  background: var(--c-paper); border: 2.5px solid var(--c-ink); }
.you.flip { flex-direction: row-reverse;
  transform: translate(calc(-100% + 8px), -8px); }
.you.enter { animation: place 200ms var(--ease-out); }
@keyframes place { from { opacity: 0;
  transform: translate(-8px, -8px) scale(0.9); } to { opacity: 1; } }
.you.flip.enter { animation: placef 200ms var(--ease-out); }
@keyframes placef { from { opacity: 0;
  transform: translate(calc(-100% + 8px), -8px) scale(0.9); }
  to { opacity: 1; } }
.rail { border-top: 1px solid var(--c-ink); padding-top: 16px;
  min-height: 480px; display: flex; flex-direction: column; }
.rail-eyebrow { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); margin-bottom: 12px; }
.rail-inner { transition: opacity 150ms var(--ease-out); }
.rail-inner.swap { opacity: 0; }
.rail-q { font-size: 20px; font-weight: 700; margin-bottom: 8px; }
.rail-q .q-mark { display: inline-block; width: 12px; height: 12px;
  margin-right: 8px; background: var(--c-paper);
  border: 2.5px solid var(--c-ink); vertical-align: baseline; }
.rail p { font-size: 16px; line-height: 1.5; margin-bottom: 16px; }
.rail-move-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-accent); margin: 8px 0 8px; padding-top: 16px;
  border-top: 1px solid var(--c-rule); }
.rail-src { font-size: 13px; color: var(--c-muted); margin-top: auto;
  padding-top: 24px; }
.rail-clear { margin-top: 12px; align-self: flex-start; font-size: 13px;
  font-weight: 700; color: var(--c-muted); text-decoration: underline;
  text-underline-offset: 3px; padding: 8px 0; display: none; }
.rail.placed .rail-clear { display: block; }

/* ---- s15 the personalized close (spec §5.15) ---- */
.stage--closing .closing-block { max-width: 1000px; padding-top: 48px; }
.stage--closing h2 { font-family: var(--f-display); font-size: 44px;
  line-height: 1.15; font-weight: 700; max-width: 940px;
  margin-bottom: 32px; text-wrap: balance; }
.close-echo { border-top: 1px solid var(--c-ink); margin-bottom: 32px;
  padding-top: 16px; max-width: 860px; }
.echo-label { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  color: var(--c-muted); }
.echo-line { font-size: 16px; line-height: 1.5; margin-top: 8px; }
.echo-move { display: block; font-size: 13px; line-height: 1.5;
  margin-top: 4px; }
.decision-ledger { max-width: 1000px; }
.dl-row { display: grid; grid-template-columns: 1fr 150px 130px;
  gap: 24px; align-items: baseline; padding: 16px 0;
  border-bottom: 1px solid var(--c-rule); }
.dl-row.dl-head { font-size: 11px; font-weight: 700;
  letter-spacing: var(--track-label); text-transform: uppercase;
  padding: 0 0 8px 0; border-bottom: 1px solid var(--c-ink); }
.dl-item span { font-size: 20px; line-height: 1.45; }
.dl-item .dl-empty { color: var(--c-rule); }
.close-actions { margin-top: 48px; display: flex; gap: 16px; }
.close-actions button { min-height: 48px; padding: 12px 24px;
  border: 1px solid var(--c-ink); background: var(--c-paper);
  font-size: 13px; font-weight: 700; text-align: center;
  transition: background 120ms var(--ease-out); }
.close-actions button:active { background: var(--c-tint); }
#reset-btn { border-color: var(--c-rule); color: var(--c-muted); }
.closing-contact { margin-top: 32px; font-size: 13px;
  letter-spacing: var(--track-meta); text-transform: uppercase;
  color: var(--c-muted); }

/* ---- s16 the ledger ---- */
.lg-table td { font-size: 13px; line-height: 1.35;
  padding: 8px 12px 8px 0; }
.lg-table th { font-size: 11px; padding: 8px 12px 8px 0; }
.lg-row:target td, .lg-row.is-target td {
  background: var(--c-tint) !important; }
.lg-note { font-size: 13px; color: var(--c-muted); margin-top: 24px; }

/* ---- no-JS footnotes (the drawers, printed) ---- */
.st-fn { margin-top: 16px; }
.fn { font-size: 13px; line-height: 1.5; margin-top: 8px;
  max-width: 860px; }
.fn-tok { font-weight: 700; }

/* ---- reduced motion: transform motion off, ≤150ms opacity swaps kept ---- */
@media (prefers-reduced-motion: reduce) {
  * { animation: none !important; }
  .drawer, .playhead, .m-fill, .m-released, .m-note::before,
  .seg button, .stagenav button, .close-actions button, .j-nav button,
  .tick::before, .act-label { transition: none !important; }
}

/* ---- mobile (<900px): deck scale maps down, on-scale (spec §9) ---- */
@media screen and (max-width: 899px) {
  .stage { padding: 24px 16px 64px; }
  .st-title { font-size: 25px; }
  .stage--title h1 { font-size: 31px; }
  .stage--title .t-block { margin-top: 48px; }
  .t-sub { font-size: 16px; }
  .t-meta { flex-wrap: wrap; }
  .stage--section-divider .divider-inner { padding: 64px 16px; }
  .stage--section-divider h2 { font-size: 31px; }
  .divider-subtitle { font-size: 16px; }
  .stage--closing h2 { font-size: 31px; }
  .exec-num { width: 24px; font-size: 20px; }
  .exec-item { gap: 16px; }
  .ks-hero { flex-direction: column; align-items: flex-start; gap: 16px; }
  .ks-num { font-size: 96px; line-height: 0.88; }
  .ks-label { font-size: 16px; }
  .ks-bar { height: 64px; margin-top: 32px; }
  .ev--hero { text-underline-offset: 8px; }
  .mag-rows { grid-template-columns: 1fr; gap: 24px; }
  .two-col { grid-template-columns: 1fr !important; gap: 32px; }
  .rail-row { grid-template-columns: 1fr; gap: 4px; padding: 12px 0; }
  .rail-value { font-size: 31px; }
  .rail-value--words { font-size: 25px; }
  .bar-row, .bar-chart--xl .bar-row { grid-template-columns: 1fr; }
  .bar-label, .bar-chart--xl .bar-label { text-align: left;
    padding: 0 0 4px 0; font-size: 16px; }
  .bar-chart--xl .bar-track { height: 96px; }
  .bar-chart--xl .bar-fill { height: 80px; }
  .bar-chart--xl .bar-value { font-size: 20px; }
  .tbl-wrap { overflow-x: auto; margin-left: -16px; margin-right: -16px;
    padding: 0 16px; }
  .tbl-wrap table { min-width: 680px; }
  table.deck-table--large td { padding: 12px 16px 12px 0; }
  .j-grid-wrap { overflow-x: auto; margin-left: -16px;
    margin-right: -16px; padding: 0 16px; }
  .j-grid-wrap .journey { min-width: 820px; }
  body.js .j-grid-wrap, body.js .j-nav { display: none; }
  body.js .j-acc { display: block; }
  .controls { grid-template-columns: 1fr; gap: 24px; }
  .m-row, .m-note-row { grid-template-columns: 1fr; gap: 8px; }
  .m-note-row { margin-top: 0; }
  .m-row-label { text-align: left; }
  .m-val { font-size: 16px; }
  .quote-text { font-size: 31px; }
  .quote-text--long { font-size: 25px; }
  .stage--quote .quote-block { padding: 48px 0; }
  .pb-gate-callout { white-space: normal; max-width: 55%; }
  .pb-name { font-size: 16px; }
  .pb-row { grid-template-columns: 1fr; gap: 4px; }
  .xp-fw { grid-template-columns: 1fr; gap: 24px; }
  .fw-grid { height: 400px; }
  .fw-cell { padding: 12px; }
  .fw-cell-title { font-size: 16px; }
  .fw-cell p { display: none; }
  .fw-plot { font-size: 11px; gap: 6px; }
  .rail { min-height: 0; }
  .dl-row { grid-template-columns: 1fr 90px 70px; gap: 8px; }
  .dl-item span { font-size: 16px; }
  .drawer { padding: 16px 16px 24px; }
  .argbar { padding: 0 8px; gap: 8px; }
  .argbar-title, .argbar .act-label { display: none; }
  .argbar-act-now { display: block; overflow: hidden;
    text-overflow: ellipsis; max-width: 96px; }
  .argbar-acts { gap: 4px; justify-content: flex-start; overflow: hidden; }
  .act-group { gap: 0; }
  .tick { width: 12px; }
  body.js { padding-bottom: 96px; }
  .stagenav { left: 0; right: 0; bottom: 0;
    padding: 8px 16px calc(8px + env(safe-area-inset-bottom));
    background: var(--c-paper); border-top: 1px solid var(--c-ink); }
  .stagenav button { flex: 1 1 0; }
  .toast { bottom: calc(96px + env(safe-area-inset-bottom)); }
  .close-actions { flex-direction: column; }
}

/* ---- print: the no-JS document with page breaks between acts (§8) ---- */
@media print {
  body, body.js { padding: 0; }
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .argbar, .stagenav, .drawer, .toast, .js-only { display: none !important; }
  body.js .nojs-only, .nojs-only { display: block !important; }
  body.js span.nojs-only, span.nojs-only,
  body.js .ks-note-static, .ks-note-static { display: inline !important; }
  body.js .j-grid-wrap, .j-grid-wrap { display: block !important; }
  .j-grid-wrap .journey { min-width: 0; }
  body.js .stage { display: block !important; animation: none !important; }
  .stage--section-divider { page-break-before: always; }
  .stage--closing { page-break-before: always; }
  button.ev { text-decoration: none; }
  .stage { max-width: none; padding: 32px 0; }
}
"""

EXP_JS = r"""
(function () {
  'use strict';
  var D = window.XPDATA;
  document.body.classList.remove('nojs');
  document.body.classList.add('js');

  function $(s, r) { return (r || document).querySelector(s); }
  function $$(s, r) { return [].slice.call((r || document).querySelectorAll(s)); }
  var stages = $$('.stage'), N = stages.length;
  var reduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---- state (Economist-brief pattern; try/catch-guarded) ---- */
  var state = { stage: 0, visited: {}, plot: null, model: null,
                evOpened: {}, journeyStage: null };
  try {
    var st0 = JSON.parse(localStorage.getItem(D.stateKey) || 'null');
    if (st0 && typeof st0 === 'object')
      for (var k in state) if (st0[k] !== undefined) state[k] = st0[k];
  } catch (e) {}
  function save() {
    try { localStorage.setItem(D.stateKey, JSON.stringify(state)); }
    catch (e) {}
  }

  /* ---- evidence drawer (one element, re-filled per citation; §4) ---- */
  var drawer = $('#ev-drawer'), evReturn = null;
  function openEv(slug) {
    var e = D.ev[slug];
    if (!e) return;
    $('#ev-head').textContent = e.head;
    $('#ev-body').textContent = e.body;
    var cv = $('#ev-caveat');
    cv.hidden = !e.caveat;
    if (e.caveat) $('#ev-caveat-text').textContent = e.caveat;
    $('#ev-src').textContent = 'Source: ' + e.src;
    var link = $('#ev-ledger-link');
    link.href = '#' + (e.row || 's' + D.ledgerStage);
    evReturn = document.activeElement;
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
    if (e.row) { state.evOpened[e.row] = 1; save(); }
    $('#ev-close').focus();
  }
  function closeDrawer() {
    if (!drawer.classList.contains('open')) return;
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    if (evReturn && evReturn.focus) { try { evReturn.focus(); } catch (e) {} }
    evReturn = null;
  }
  $('#ev-close').addEventListener('click', closeDrawer);
  document.addEventListener('click', function (ev) {
    var b = ev.target.closest && ev.target.closest('button.ev');
    if (b && b.dataset.ev) openEv(b.dataset.ev);
  });
  $('#ev-ledger-link').addEventListener('click', function () {
    drawer.classList.remove('open');
    drawer.setAttribute('aria-hidden', 'true');
    evReturn = null;
  });

  /* ---- wayfinding: activate / argument bar / hash routing (§3) ---- */
  var cur = -1;
  var backBtn = $('#nav-back'), nextBtn = $('#nav-next');
  function updateBar() {
    $$('.tick').forEach(function (t) {
      var s = +t.dataset.s;
      t.classList.toggle('cur', s === cur + 1);
      t.classList.toggle('seen', !!state.visited['s' + s] && s !== cur + 1);
    });
    var act = stages[cur].dataset.act;
    $$('.act-group').forEach(function (g) {
      g.classList.toggle('on', g.dataset.g === act);
    });
    var actLabel = $('.act-group[data-g="' + act + '"] .act-label');
    $('#act-now').textContent = actLabel ? actLabel.textContent : D.title;
    $('#stage-count').textContent = cur + 1;
    backBtn.disabled = cur === 0;
    nextBtn.disabled = cur === N - 1;
  }
  function activate(i, setHash) {
    if (i < 0) i = 0;
    if (i > N - 1) i = N - 1;
    if (i === cur) return;
    if (cur >= 0) {
      stages[cur].classList.remove('active');
      stages[cur].classList.remove('beat');
    }
    cur = i;
    var st = stages[i], sid = 's' + (i + 1);
    if (st.dataset.beat && !state.visited[sid] && !reduced)
      st.classList.add('beat');
    state.visited[sid] = 1;
    state.stage = i;
    save();
    st.classList.add('active');
    window.scrollTo(0, 0);
    updateBar();
    closeDrawer();
    if (setHash !== false && location.hash !== '#' + sid) {
      try { history.replaceState(null, '', '#' + sid); }
      catch (e) { location.hash = sid; }
    }
    if (st.dataset.close) buildEcho();
  }
  function markRow(slug) {
    $$('.lg-row.is-target').forEach(function (r) {
      r.classList.remove('is-target');
    });
    var row = document.getElementById(slug);
    if (row) {
      row.classList.add('is-target');
      row.scrollIntoView({ block: 'center' });
    }
  }
  function route() {
    var h = location.hash.replace('#', '');
    if (/^s\d+$/.test(h)) { activate(+h.slice(1) - 1, false); return true; }
    if (h && D.ev[h] && D.ledgerStage) {
      activate(D.ledgerStage - 1, false);
      markRow(h);
      return true;
    }
    return false;
  }
  window.addEventListener('hashchange', route);
  document.addEventListener('click', function (e) {
    var t = e.target.closest && e.target.closest('[data-s]');
    if (t) activate(+t.dataset.s - 1);
  });
  backBtn.addEventListener('click', function () { activate(cur - 1); });
  nextBtn.addEventListener('click', function () { activate(cur + 1); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
      if (drawer.classList.contains('open')) { closeDrawer(); return; }
      if (mag && mag.classList.contains('open')) { setMag(false); return; }
      return;
    }
    var t = e.target, tag = t && t.tagName ? t.tagName.toLowerCase() : '';
    if (tag === 'input' || tag === 'textarea' || tag === 'select' ||
        (t && t.isContentEditable)) return;
    if (t && t.closest && t.closest('[data-own-keys]') &&
        (e.key === 'ArrowLeft' || e.key === 'ArrowRight' ||
         e.key === 'ArrowUp' || e.key === 'ArrowDown' ||
         e.key === 'Enter')) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); activate(cur + 1); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); activate(cur - 1); }
    else if (e.key === 'Home') { e.preventDefault(); activate(0); }
    else if (e.key === 'End') { e.preventDefault(); activate(N - 1); }
  });

  /* ---- s4: the sliver drill / magnifier (§5.4) ---- */
  var mag = $('#mag');
  var magBtns = $$('[data-mag]');
  function flare() {
    var f = $('#mag-flare'), bar = $('#ks-bar');
    if (!f || !bar) return;
    var W = f.clientWidth, H = f.clientHeight;
    var x0 = W * (D.heroShare / 100);
    var l = $('.fl-l', f);
    l.style.left = x0 + 'px';
    l.style.width = Math.hypot(x0, H) + 'px';
    l.style.transform =
      'rotate(' + (Math.atan2(H, -x0) * 180 / Math.PI) + 'deg)';
  }
  function setMag(on) {
    if (!mag) return;
    mag.classList.toggle('open', on);
    magBtns.forEach(function (b) {
      b.setAttribute('aria-expanded', on ? 'true' : 'false');
    });
    if (on) flare();
  }
  magBtns.forEach(function (b) {
    b.addEventListener('click', function () {
      setMag(!mag.classList.contains('open'));
    });
  });

  /* ---- s8: the explorable journey (§5.8) ---- */
  (function () {
    var root = $('#journey');
    if (!root) return;
    var grids = $$('.j-stages, .j-lanes, .j-brackets', root);
    var n = D.journeyN, focusK = 0;
    function apply(k) {
      root.dataset.focus = k || '';
      var t = '104px';
      if (k) { for (var i = 1; i <= n; i++) t += i === k ? ' 2.2fr' : ' 0.7fr'; }
      else t += ' repeat(' + n + ',1fr)';
      grids.forEach(function (g) { g.style.gridTemplateColumns = t; });
      $$('.j-stage', root).forEach(function (s) {
        var c = +s.dataset.col;
        s.classList.toggle('focus', c === k);
        if (k && c === k) s.classList.add('seen');
      });
      $$('.j-cell[data-col]', root).forEach(function (c) {
        c.classList.toggle('mini', !!k && +c.dataset.col !== k);
      });
      $$('.j-acc-item').forEach(function (it, idx) {
        var on = (idx + 1) === k;
        it.classList.toggle('open', on);
        $('.j-acc-head', it).setAttribute('aria-expanded',
          on ? 'true' : 'false');
      });
      var hint = $('#j-hint');
      if (hint) hint.textContent = k
        ? 'Stage ' + k + ' of ' + n +
          ' focused. Tap it again for the overview.'
        : 'Tap a stage column to walk the journey in your order; tap it ' +
          'again for the overview.';
    }
    function setFocus(k) {
      focusK = k;
      state.journeyStage = k || null;
      save();
      root.classList.add('j-swap');
      setTimeout(function () {
        apply(k);
        root.classList.remove('j-swap');
      }, 150);
    }
    root.addEventListener('click', function (e) {
      if (e.target.closest && e.target.closest('button.ev')) return;
      var col = e.target.closest && e.target.closest('[data-col]');
      if (!col) return;
      var c = +col.dataset.col;
      setFocus(c === focusK ? 0 : c);
    });
    $$('.j-acc-head').forEach(function (h) {
      h.addEventListener('click', function () {
        var c = +h.dataset.col;
        setFocus(c === focusK ? 0 : c);
      });
    });
    var prev = $('#j-prev'), next = $('#j-next');
    if (prev) prev.addEventListener('click', function () {
      setFocus(focusK ? (focusK > 1 ? focusK - 1 : n) : n);
    });
    if (next) next.addEventListener('click', function () {
      setFocus(focusK ? (focusK < n ? focusK + 1 : 1) : 1);
    });
    if (state.journeyStage) { focusK = state.journeyStage; apply(focusK); }
  })();

  /* ---- s9: the substitution model (prototype JS, lifted verbatim) ---- */
  (function () {
    var nIn = $('#sub-n');
    if (!nIn) return;
    var n = D.model.def, m = D.model.mults[0];
    if (state.model && state.model.n && state.model.m) {
      n = state.model.n; m = state.model.m;
    }
    var nOut = $('#sub-n-out'),
        segBtns = $$('.seg button'),
        barToday = $('#bar-today'), barAfter = $('#bar-after'),
        relSeg = $('#rel-seg'),
        valToday = $('#val-today'), valAfter = $('#val-after'),
        note = $('#m-note'),
        relStrong = $('#rel-strong'), relText = $('#rel-text');
    function fmt(x) { return x.toLocaleString('en-US'); }
    function render() {
      // Honest arithmetic only: at coverage m, the same book needs ceil(n/m).
      var after = Math.ceil(n / m), released = n - after, share = after / n;
      barToday.style.transform = 'scaleX(1)';
      barAfter.style.transform = 'scaleX(' + share + ')';
      relSeg.style.left = 'calc(' + (share * 100) + '% + 2px)';
      relSeg.style.width = 'calc(' + ((1 - share) * 100) + '% - 2px)';
      valToday.textContent = fmt(n) + ' AEs';
      valAfter.textContent = '≈' + fmt(after) + ' AEs';
      note.style.setProperty('--m-tick', (share * 100 + (1 - share) * 50) + '%');
      relStrong.textContent = fmt(released) + ' seats released';
      relText.textContent = '≈' + fmt(after) +
        ' AEs plus AI cover the book your ' + fmt(n) +
        ' cover today, with humans still in every loop';
    }
    function persist() { state.model = { n: n, m: m }; save(); }
    nIn.value = n;
    nOut.textContent = fmt(n);
    segBtns.forEach(function (x) {
      x.setAttribute('aria-pressed', +x.dataset.m === m ? 'true' : 'false');
    });
    nIn.addEventListener('input', function () {
      n = +nIn.value;
      nOut.textContent = fmt(n);
      render();
      persist();
    });
    segBtns.forEach(function (b) {
      b.addEventListener('click', function () {
        m = +b.dataset.m;
        segBtns.forEach(function (x) {
          x.setAttribute('aria-pressed', x === b ? 'true' : 'false');
        });
        render();
        persist();
      });
    });
    var cav = $('#caveat-btn');
    if (cav) cav.addEventListener('click', function () {
      openEv('x11-caveat');
    });
    render();
  })();

  /* ---- s12: the time scrub (§5.12) ---- */
  (function () {
    var scrub = $('#scrub');
    if (!scrub) return;
    var ph = $('#playhead'), inner = $('#ph-inner');
    var snaps = D.snaps, phases = D.phases, gate = D.gate;
    var pos = 0, curKey = 'p0', dragging = false, rect = null;
    var bounds = phases.map(function (p) { return p.to; });
    function keyFor(p, snapped) {
      if (snapped && gate.pos != null && Math.abs(p - gate.pos) < 0.5)
        return 'gate';
      for (var i = 0; i < bounds.length; i++)
        if (p < bounds[i] || i === bounds.length - 1) return 'p' + i;
      return 'p' + (bounds.length - 1);
    }
    function fill(key) {
      var name = $('#ph-name'), time = $('#ph-time'),
          desc = $('#ph-desc'), exitRow = $('.ph-exit-row'),
          exit = $('#ph-exit');
      if (key === 'gate') {
        time.textContent = gate.label + ' · decision gate';
        name.textContent = 'First funded redesign decision, not a report';
        desc.textContent = 'The assessment converts into a funded ' +
          'decision here; the accent gate on the axis marks it.';
        exitRow.hidden = false;
        exit.textContent = phases[0].exit;
        return;
      }
      var p = phases[+key.slice(1)];
      time.textContent = p.time;
      name.textContent = p.name;
      desc.textContent = p.desc;
      exitRow.hidden = !p.exit;
      exit.textContent = p.exit;
    }
    function paint(p, snapped) {
      pos = p;
      ph.style.left = p + '%';
      var key = keyFor(p, snapped);
      scrub.classList.toggle('gate-on', key === 'gate');
      scrub.setAttribute('aria-valuenow', Math.round(p));
      if (key !== curKey) {
        curKey = key;
        inner.classList.add('swap');
        setTimeout(function () {
          fill(key);
          inner.classList.remove('swap');
        }, 150);
      }
    }
    function pFrom(e) {
      return Math.min(100, Math.max(0,
        (e.clientX - rect.left) / rect.width * 100));
    }
    function snap() {
      var best = snaps[0];
      snaps.forEach(function (s) {
        if (Math.abs(s.p - pos) < Math.abs(best.p - pos)) best = s;
      });
      paint(best.p, true);
    }
    scrub.addEventListener('pointerdown', function (e) {
      dragging = true;
      rect = $('#pb-track').getBoundingClientRect();
      scrub.classList.add('dragging');
      try { scrub.setPointerCapture(e.pointerId); } catch (er) {}
      paint(pFrom(e), false);
      e.preventDefault();
    });
    scrub.addEventListener('pointermove', function (e) {
      if (dragging) paint(pFrom(e), false);
    });
    function up() {
      if (!dragging) return;
      dragging = false;
      scrub.classList.remove('dragging');
      snap();
    }
    scrub.addEventListener('pointerup', up);
    scrub.addEventListener('pointercancel', up);
    scrub.addEventListener('keydown', function (e) {
      var idx = 0, bd = Infinity;
      snaps.forEach(function (s, i) {
        if (Math.abs(s.p - pos) < bd) { bd = Math.abs(s.p - pos); idx = i; }
      });
      if (e.key === 'ArrowRight') idx = Math.min(snaps.length - 1, idx + 1);
      else if (e.key === 'ArrowLeft') idx = Math.max(0, idx - 1);
      else return;
      e.preventDefault();
      paint(snaps[idx].p, true);
    });
  })();

  /* ---- s13: the 2x2 self-plot (prototype JS, lifted verbatim) ---- */
  (function () {
    var grid = $('#fw-grid'), rail = $('#rail');
    if (!grid || !rail) return;
    var inner = $('#rail-inner'), qEl = $('#rail-q'),
        readEl = $('#rail-read'), moveWrap = $('#rail-move-wrap'),
        moveEl = $('#rail-move'), srcEl = $('#rail-src'),
        hint = $('#fw-hint'), clearBtn = $('#fw-clear');
    var mark = null, pos = null;
    var QUADS = D.quads; // cell order TL, TR, BL, BR
    function quadrant(p) {
      return p.y < 50 ? (p.x < 50 ? QUADS[0] : QUADS[1])
                      : (p.x < 50 ? QUADS[2] : QUADS[3]);
    }
    function render(first) {
      if (!pos) return;
      var q = quadrant(pos), r = D.readings[q];
      if (!mark) {
        mark = document.createElement('div');
        mark.className = 'you';
        mark.innerHTML = '<span class="you-mark"></span><span>You</span>';
        grid.appendChild(mark);
      }
      mark.style.left = pos.x + '%';
      mark.style.top = pos.y + '%';
      mark.classList.toggle('flip', pos.x > 84);
      if (first) {
        mark.classList.remove('enter');
        void mark.offsetWidth;
        mark.classList.add('enter');
      }
      // swap the rail reading only when the quadrant changes (drags inside
      // a quadrant must not strobe the panel)
      if (rail.dataset.q !== q) {
        rail.dataset.q = q;
        inner.classList.add('swap');
        setTimeout(function () {
          qEl.innerHTML = '<span class="q-mark"></span>' +
            (r ? r.title : q);
          readEl.textContent = r ? r.read : '';
          moveWrap.hidden = !(r && r.move);
          moveEl.textContent = r ? r.move : '';
          srcEl.textContent = r && r.src ? 'Source: ' + r.src : '';
          inner.classList.remove('swap');
        }, 150);
      }
      rail.classList.add('placed');
      if (hint) hint.textContent =
        'Drag the marker, or tap again to move it.';
      state.plot = { x: Math.round(pos.x * 10) / 10,
                     y: Math.round(pos.y * 10) / 10, quadrant: q };
      save();
    }
    function place(ev) {
      var b = grid.getBoundingClientRect();
      pos = { x: Math.min(97, Math.max(3, (ev.clientX - b.left) / b.width * 100)),
              y: Math.min(97, Math.max(3, (ev.clientY - b.top) / b.height * 100)) };
      render(ev.type === 'pointerdown');
    }
    var dragging = false;
    grid.addEventListener('pointerdown', function (e) {
      if (e.target.closest && e.target.closest('button.ev')) return;
      dragging = true;
      try { grid.setPointerCapture(e.pointerId); } catch (er) {}
      place(e);
    });
    grid.addEventListener('pointermove', function (e) {
      if (dragging) place(e);
    });
    grid.addEventListener('pointerup', function () { dragging = false; });
    grid.addEventListener('pointercancel', function () { dragging = false; });
    grid.addEventListener('keydown', function (e) {
      var step = 2.5;
      if (e.key === 'Enter' && !pos) {
        pos = { x: 50, y: 50 };
        render(true);
        e.preventDefault();
        return;
      }
      if (!pos) return;
      if (e.key === 'ArrowLeft') pos.x = Math.max(3, pos.x - step);
      else if (e.key === 'ArrowRight') pos.x = Math.min(97, pos.x + step);
      else if (e.key === 'ArrowUp') pos.y = Math.max(3, pos.y - step);
      else if (e.key === 'ArrowDown') pos.y = Math.min(97, pos.y + step);
      else return;
      e.preventDefault();
      render(false);
    });
    clearBtn.addEventListener('click', function () {
      if (mark) { mark.remove(); mark = null; }
      pos = null;
      delete rail.dataset.q;
      rail.classList.remove('placed');
      qEl.textContent = 'Not plotted yet';
      readEl.textContent = D.railDefault;
      moveWrap.hidden = true;
      srcEl.textContent = D.railAxes;
      if (hint) hint.textContent = 'Tap anywhere on the grid to plot ' +
        'where your organization sits today. Drag to adjust.';
      state.plot = null;
      save();
    });
    if (state.plot && typeof state.plot.x === 'number') {
      pos = { x: state.plot.x, y: state.plot.y };
      render(false);
    }
  })();

  /* ---- s15: the personalized close (§5.15) ---- */
  var echoLines = [];
  function buildEcho() {
    var box = $('#echo');
    if (!box) return;
    var lines = [], html = '';
    if (state.plot && state.plot.quadrant) {
      var q = state.plot.quadrant, r = D.readings[q];
      var target = D.quads[1];
      var line = 'You placed your organization in ' + q + '.';
      var move = (r && r.move && q !== target) ? r.move : '';
      lines.push(line + (move ? ' The move: ' + move : ''));
      html += '<p class="echo-line">You placed your organization in ' +
        '<strong>' + q + '</strong>.' +
        (move ? ' <span class="echo-move">' + move + '</span>' : '') +
        '</p>';
    }
    if (state.model && state.model.n) {
      var n = state.model.n, m = state.model.m;
      var after = Math.ceil(n / m), rel = n - after;
      var l2 = 'At your numbers, ≈' + after + ' of ' + n +
        ' AE seats cover today’s book at ' + m +
        '× — ' + rel + ' seats released through productivity.';
      lines.push(l2);
      html += '<p class="echo-line">' + l2 + '</p>';
    }
    var kk = Object.keys(state.evOpened).length;
    if (kk) {
      var l3 = 'You opened ' + kk + ' of the ' + (D.citableCount || D.ledgerCount) +
        ' sources behind this argument.';
      lines.push(l3);
      html += '<p class="echo-line">' + l3 + '</p>';
    }
    echoLines = lines;
    box.hidden = !lines.length;
    $('#echo-lines').innerHTML = html;
  }
  var toastEl = $('#toast'), toastT = null;
  function toast(msg) {
    toastEl.textContent = msg;
    toastEl.classList.add('on');
    clearTimeout(toastT);
    toastT = setTimeout(function () { toastEl.classList.remove('on'); }, 2600);
  }
  function copy(text) {
    function ok() { toast('Copied — paste it into the follow-up.'); }
    function fallback() {
      try {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
        ok();
      } catch (e) {
        toast('Copy failed — select the decisions above and copy.');
      }
    }
    if (navigator.clipboard && window.isSecureContext)
      navigator.clipboard.writeText(text).then(ok, fallback);
    else fallback();
  }
  var copyBtn = $('#copy-btn');
  if (copyBtn) copyBtn.addEventListener('click', function () {
    buildEcho();
    var txt = D.title + ' — ' + D.date + '\n';
    if (echoLines.length)
      txt += '\nWhat you did with this argument:\n' +
        echoLines.map(function (l) { return '• ' + l; }).join('\n') + '\n';
    txt += '\nDecisions we need from this group:\n' +
      D.decisions.map(function (d, i) { return (i + 1) + '. ' + d; }).join('\n');
    copy(txt);
  });
  var resetBtn = $('#reset-btn');
  if (resetBtn) resetBtn.addEventListener('click', function () {
    if (!window.confirm('Start over? This clears your plotted position, ' +
        'your model inputs, and your progress.')) return;
    state = { stage: 0, visited: {}, plot: null, model: null,
              evOpened: {}, journeyStage: null };   /* zero BEFORE clearing —
              the hashchange below re-saves, so it must re-save emptiness (gate B1) */
    try { localStorage.removeItem(D.stateKey); } catch (e) {}
    location.hash = '#s1';
    location.reload();
  });

  /* ---- boot: hash wins; else resume from state ---- */
  if (!route()) activate(state.stage || 0, true);
})();
"""


def main():
    ap = argparse.ArgumentParser(
        description="Render a markdown deck as the interactive Experience.")
    ap.add_argument("content", help="content/<deck>.md")
    ap.add_argument("--brand", default="default")
    ap.add_argument("-o", "--out", help="output basename override")
    args = ap.parse_args()
    content_path = Path(args.content)
    if not content_path.exists():
        sys.exit(f"error: content file not found: {content_path}")
    try:
        brand = rd.load_brand(args.brand)
        doc, n = render(content_path, brand)
    except DeckError as e:
        sys.exit(f"error: {e}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    brand_name = Path(brand["_path"]).stem
    base = args.out or f"experience--{brand_name}"
    out = OUT_DIR / f"{base}.html"
    out.write_text(doc, encoding="utf-8")
    print(f"wrote {out.relative_to(KIT)} ({n} stages, "
          f"brand: {brand.get('name', brand_name)})")


if __name__ == "__main__":
    main()
