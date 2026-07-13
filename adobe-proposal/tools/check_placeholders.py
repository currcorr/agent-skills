#!/usr/bin/env python3
"""Placeholder gate for pages built from this design system.

Usage:
    python3 tools/check_placeholders.py path/to/page.html [more.html ...]

Exit 0  = clean: no placeholder content found, page can ship.
Exit 1  = placeholders remain — the report lists each one with its line.

What it catches (in order of severity):
  1. data-placeholder attributes    — media/photo slots still holding
     stand-in gradients or the tagged placeholder SVG. Every one must be
     replaced with real licensed imagery (or, for "media-optional", either
     replaced or consciously kept — see CLAUDE.md).
  2. data-sample-content on <body>  — the page is still the demo document;
     a real proposal page must not carry this marker.
  3. Sample-brand strings           — "Northbeam" (the fictional demo
     brand) and the visible "swap for licensed photography" tag.
  4. PLACEHOLDER comment markers    — <!-- PLACEHOLDER ... --> notes left
     by builders.

Gallery/demo files (design-system/index.html, components/*.html) are
SUPPOSED to contain placeholders — run this only against pages you intend
to ship.
"""
import re
import sys
from pathlib import Path

CHECKS = [
    ("data-placeholder slot", re.compile(r'data-placeholder="(?!media-optional)[^"]*"')),
    ("data-placeholder (optional — replace or consciously keep)",
     re.compile(r'data-placeholder="media-optional"')),
    ("sample-content body marker", re.compile(r'data-sample-content=')),
    ("sample brand string", re.compile(r'Northbeam')),
    ("placeholder swap tag", re.compile(r'swap for licensed photography', re.I)),
    ("PLACEHOLDER comment", re.compile(r'<!--[^>]*PLACEHOLDER', re.I)),
]

HARD = {"data-placeholder slot", "sample-content body marker",
        "sample brand string", "placeholder swap tag", "PLACEHOLDER comment"}


def scan(path: Path):
    findings = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        for label, rx in CHECKS:
            for m in rx.finditer(line):
                findings.append((label, lineno, line.strip()[:100]))
    return findings


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    hard_total = 0
    for arg in argv[1:]:
        path = Path(arg)
        if not path.exists():
            print(f"MISSING FILE: {path}")
            hard_total += 1
            continue
        findings = scan(path)
        hard = [f for f in findings if f[0] in HARD]
        soft = [f for f in findings if f[0] not in HARD]
        print(f"\n== {path} — {len(hard)} blocking, {len(soft)} advisory")
        for label, lineno, snippet in findings:
            tag = "BLOCK" if label in HARD else "note "
            print(f"  [{tag}] L{lineno:>5} {label}: {snippet}")
        hard_total += len(hard)
    if hard_total:
        print(f"\nNOT SHIPPABLE: {hard_total} blocking placeholder(s) remain.")
        return 1
    print("\nClean — no blocking placeholders.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
