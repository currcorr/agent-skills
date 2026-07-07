#!/usr/bin/env python3
"""deckcheck.py — deterministic craft sweep for the deck system.

The deterministic half of the craft gate: doctrine/design-doctrine.md §6
(gate step §6.10(c)). Run after every render. All paths resolve relative
to this file's directory (the kit root).

Checks (exit non-zero with file:line on any violation):
  1. Type-scale membership (deck.css): every font-size px literal is in
     {11, 13, 16, 20, 25, 31, 44, 55} + free display numerals
     {64, 120, 200, 300}. em/% values exempt.
  2. Tracking membership (deck.css): every letter-spacing value is in
     {var(--track-meta), var(--track-label), -0.01em, -0.015em, 0}.
  3. Spacing tokens (deck.css): every px literal in margin*, padding*,
     gap, grid-gap is in {0, 2, 3, 4, 8, 12, 16, 24, 32, 48, 64, 96}
     (2/3 allowed only as optical nudges); rules between a
     '/* fitted-geometry: spacing exempt */' marker and the next
     section-header comment are skipped.
  4. Numeral face: .rail-value / .kpi-value / .ks-num / .agenda-num /
     .exec-num never set font-family: var(--f-display).
  5. Per-slide HTML checks (out/*.html): (a) em-dash count in
     visible text <= 1, excluding .slide-foot and single-character '—'
     cells (.dl-empty, .j-cell.empty, .pb-exit.empty); (b) every element
     whose class is in the caps-class list has text <= 24 chars (foot-*
     exempt); (c) distinct caps classes present per slide <= 6 (footer
     furniture exempt).

Prints a per-slide summary table (sizes seen, caps tiers, em-dashes)
even on pass. Stdlib only.

Usage: python3 deckcheck.py [--css path/to/deck.css] [html ...]
       (defaults: layout/deck.css + every out/*.html)
"""

import argparse
import re
import sys
from bisect import bisect_right
from html.parser import HTMLParser
from pathlib import Path

KIT = Path(__file__).resolve().parent
CSS_DEFAULT = KIT / "layout" / "deck.css"
OUT_DIR = KIT / "out"

SCALE = {11, 13, 16, 20, 25, 31, 44, 55, 64, 120, 200, 300}
SPACING = {0, 2, 3, 4, 8, 12, 16, 24, 32, 48, 64, 96}
TRACKING = {"var(--track-meta)", "var(--track-label)", "-0.01em",
            "-0.015em", "0"}
NUMERAL_CLASSES = ("rail-value", "kpi-value", "ks-num", "agenda-num",
                   "exec-num")
SPACING_PROP = re.compile(r"^(margin|padding)(-|$)|^(gap|grid-gap|row-gap|column-gap)$")
PX_RE = re.compile(r"(-?\d+(?:\.\d+)?)px")
FITTED_MARK = "fitted-geometry: spacing exempt"
SECTION_HEAD = re.compile(r"/\*\s*[-=]{4,}")

# caps-class list per the spec (5b). 'table th', 'title-meta' spans and
# 'quote-attr span' are contextual; foot-* is footer furniture (exempt).
CAPS_SIMPLE = {
    "kicker", "takeaway-label", "divider-label", "tl-time", "pb-time",
    "pb-axis-label", "pb-row-label", "gate-label", "j-stage-num",
    "j-lane-label", "b-label", "j-bracket-head", "ws-week",
    "ws-lane-label", "ws-note-head",
}
VOID = {"img", "br", "hr", "meta", "link", "input", "source", "area",
        "base", "col", "embed", "track", "wbr"}
CAPS_MAX = 24
TIERS_MAX = 6
EMDASH_MAX = 1


# --------------------------------------------------------------------------
# CSS side (checks 1-4)
# --------------------------------------------------------------------------

def blank_comments(css):
    """Replace comment contents with spaces so offsets/lines survive."""
    return re.sub(r"/\*.*?\*/",
                  lambda m: re.sub(r"[^\n]", " ", m.group(0)), css,
                  flags=re.S)


def fitted_regions(css):
    """(start, end) offsets exempt from the spacing check: from each
    fitted-geometry marker to the next section-header comment (or EOF)."""
    regions = []
    for m in re.finditer(re.escape(FITTED_MARK), css):
        nxt = SECTION_HEAD.search(css, m.end())
        regions.append((m.start(), nxt.start() if nxt else len(css)))
    return regions


def iter_rules(css_blanked):
    """Yield (selector, body, body_offset). @media wrappers are unwrapped;
    other at-rules with braces (@page, @font-face) are treated as rules."""
    rules, buf_start, pos, n = [], 0, 0, len(css_blanked)
    while pos < n:
        ch = css_blanked[pos]
        if ch == "{":
            selector = css_blanked[buf_start:pos].strip()
            if selector.startswith("@media"):
                buf_start = pos + 1  # unwrap: children scan as top-level
            else:
                close = css_blanked.find("}", pos)
                if close == -1:
                    break
                rules.append((selector, css_blanked[pos + 1:close], pos + 1))
                pos = close
                buf_start = pos + 1
        elif ch == "}":
            buf_start = pos + 1
        pos += 1
    return rules


def check_css(css_path, violations):
    """Run checks 1-4. Returns (rules_with_sizes, stats) for the summary."""
    raw = css_path.read_text(encoding="utf-8")
    exempt = fitted_regions(raw)
    css = blank_comments(raw)
    newlines = [m.start() for m in re.finditer(r"\n", css)]

    def line_of(off):
        return bisect_right(newlines, off - 1) + 1

    def is_exempt(off):
        return any(a <= off < b for a, b in exempt)

    sized_selectors = []      # (classes, tags, sizes) for the summary
    seen_sizes, seen_spacing, seen_tracking = set(), set(), set()

    for selector, body, body_off in iter_rules(css):
        rule_sizes = []
        for m in re.finditer(r"([-\w]+)\s*:\s*([^;{}]+)", body):
            prop = m.group(1).strip().lower()
            value = m.group(2).strip()
            off = body_off + m.start()
            loc = f"{css_path}:{line_of(off)}"
            if prop.startswith("--"):
                continue
            if prop == "font-size":
                for px in PX_RE.findall(value):
                    v = float(px)
                    v = int(v) if v == int(v) else v
                    seen_sizes.add(v)
                    rule_sizes.append(v)
                    if v not in SCALE:
                        violations.append(
                            f"{loc}: font-size {px}px off the locked scale "
                            f"({selector})")
            elif prop == "letter-spacing":
                seen_tracking.add(value)
                if value not in TRACKING:
                    violations.append(
                        f"{loc}: letter-spacing {value!r} not a tracking "
                        f"token ({selector})")
            elif SPACING_PROP.match(prop):
                if is_exempt(off):
                    continue
                for px in PX_RE.findall(value):
                    v = float(px)
                    v = int(v) if v == int(v) else v
                    seen_spacing.add(v)
                    if v not in SPACING:
                        violations.append(
                            f"{loc}: {prop} {px}px off the spacing tokens "
                            f"({selector})")
            elif prop == "font-family":
                if ("var(--f-display)" in value and
                        any(f".{c}" in selector for c in NUMERAL_CLASSES)):
                    violations.append(
                        f"{loc}: {selector} sets the serif display face on "
                        "a numeral class (doctrine §6.3)")
        if rule_sizes:
            classes = set(re.findall(r"\.([\w-]+)", selector))
            tags = set(re.findall(r"(?<![\w.#:-])([a-z][a-z0-9]*)", selector)) \
                - {"before", "after", "hover", "root", "not", "nth"}
            sized_selectors.append((classes, tags, rule_sizes))

    stats = {"sizes": seen_sizes, "spacing": seen_spacing,
             "tracking": seen_tracking}
    return sized_selectors, stats


# --------------------------------------------------------------------------
# HTML side (check 5)
# --------------------------------------------------------------------------

class SlideScan(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.slides = []
        self.cur = None
        self.stack = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        ad = dict(attrs)
        classes = set((ad.get("class") or "").split())
        parent = self.stack[-1] if self.stack else None
        if tag == "section" and "slide" in classes:
            arch = next((c[len("slide--"):] for c in classes
                         if c.startswith("slide--")), "")
            self.cur = {"page": ad.get("data-page", "?"), "arch": arch,
                        "classes": set(), "tags": set(), "tiers": set(),
                        "caps": [], "emdash": 0}
            self.slides.append(self.cur)
        entry = {
            "tag": tag,
            "in_foot": bool(parent and parent["in_foot"])
                       or "slide-foot" in classes,
            "suppress": bool(parent and parent["suppress"])
                        or "dl-empty" in classes
                        or ("empty" in classes and
                            ("j-cell" in classes or "pb-exit" in classes)),
            "in_meta": bool(parent and parent["in_meta"])
                       or "title-meta" in classes,
            "in_attr": bool(parent and parent["in_attr"])
                       or "quote-attr" in classes,
            "caps_buf": None,
        }
        if self.cur is not None:
            self.cur["classes"] |= classes
            self.cur["tags"].add(tag)
            key = None
            if entry["in_foot"] or any(c.startswith("foot-") for c in classes):
                key = None          # footer furniture exempt
            elif classes & CAPS_SIMPLE:
                key = sorted(classes & CAPS_SIMPLE)[0]
            elif tag == "th":
                key = "table th"
            elif tag == "span" and entry["in_meta"]:
                key = "title-meta"
            elif tag == "span" and entry["in_attr"]:
                key = "quote-attr span"
            if key:
                entry["caps_buf"] = (key, [])
        self.stack.append(entry)

    def handle_data(self, data):
        if self.cur is None or not self.stack:
            return
        top = self.stack[-1]
        if not top["in_foot"] and not top["suppress"]:
            self.cur["emdash"] += data.count("—")
        for e in self.stack:
            if e["caps_buf"] is not None:
                e["caps_buf"][1].append(data)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        while self.stack:
            e = self.stack.pop()
            if e["caps_buf"] is not None and self.cur is not None:
                key, parts = e["caps_buf"]
                text = re.sub(r"\s+", " ", "".join(parts)).strip()
                self.cur["tiers"].add(key)
                self.cur["caps"].append((key, text))
            if e["tag"] == tag:
                if tag == "section" and self.cur is not None:
                    self.cur = None
                break


def check_html(html_path, violations):
    scan = SlideScan()
    scan.feed(html_path.read_text(encoding="utf-8"))
    for s in scan.slides:
        where = f"{html_path.name} slide {s['page']}"
        if s["emdash"] > EMDASH_MAX:
            violations.append(
                f"{html_path}: slide {s['page']}: {s['emdash']} em-dashes in "
                f"visible text (ration is {EMDASH_MAX})")
        for key, text in s["caps"]:
            if len(text) > CAPS_MAX:
                violations.append(
                    f"{html_path}: slide {s['page']}: {key} caps string "
                    f"{text!r} is {len(text)} chars (max {CAPS_MAX})")
        if len(s["tiers"]) > TIERS_MAX:
            violations.append(
                f"{html_path}: slide {s['page']}: {len(s['tiers'])} caps "
                f"tiers ({', '.join(sorted(s['tiers']))}); max {TIERS_MAX}")
    return scan.slides


def slide_sizes(slide, sized_selectors):
    out = set()
    for classes, tags, sizes in sized_selectors:
        if classes and not classes & slide["classes"]:
            continue
        if not classes and not tags & slide["tags"]:
            continue
        out.update(sizes)
    return out


def fmt_nums(nums):
    return ",".join(str(v) for v in sorted(nums))


def main():
    ap = argparse.ArgumentParser(description="Deterministic craft sweep.")
    ap.add_argument("html", nargs="*", help="rendered decks (default: out/*.html)")
    ap.add_argument("--css", default=str(CSS_DEFAULT))
    args = ap.parse_args()

    css_path = Path(args.css)
    html_paths = ([Path(p) for p in args.html] if args.html
                  else sorted(OUT_DIR.glob("*.html")))
    violations = []
    sized_selectors, stats = check_css(css_path, violations)

    print(f"deckcheck — {css_path.relative_to(KIT) if css_path.is_relative_to(KIT) else css_path}")
    print(f"  font sizes seen: {fmt_nums(stats['sizes'])}")
    print(f"  spacing px seen: {fmt_nums(stats['spacing'])}")
    print(f"  tracking seen:   {', '.join(sorted(stats['tracking']))}")

    for hp in html_paths:
        slides = check_html(hp, violations)
        print(f"\n{hp.name}")
        print(f"  {'slide':<6}{'archetype':<18}{'caps tiers':<11}"
              f"{'em-dash':<8}sizes seen")
        for s in slides:
            print(f"  {s['page']:<6}{s['arch']:<18}{len(s['tiers']):<11}"
                  f"{s['emdash']:<8}{fmt_nums(slide_sizes(s, sized_selectors))}")

    if violations:
        print(f"\nDECKCHECK-FAIL ({len(violations)} violations)")
        for v in violations:
            print(f"  {v}")
        sys.exit(1)
    print("\nDECKCHECK-OK")


if __name__ == "__main__":
    main()
