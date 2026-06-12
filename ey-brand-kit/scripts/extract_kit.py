#!/usr/bin/env python3
"""Extract a brand kit JSON from a .pptx template.

Pulls the theme color scheme, font scheme, slide size, and slide layout
names straight from the OOXML — no third-party dependencies.

Usage:
    python extract_kit.py ClientTemplate.pptx [output.json]

Prints the layout list so a human can assign roles in pptx.layoutMap.
"""

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"

# Approximations for theme colors defined as system colors
SYS_COLOR_DEFAULTS = {"windowText": "000000", "window": "FFFFFF"}

FALLBACK = "Arial, Helvetica, sans-serif"


def color_value(parent):
    srgb = parent.find(f"{{{A}}}srgbClr")
    if srgb is not None:
        return "#" + srgb.get("val").upper()
    sysclr = parent.find(f"{{{A}}}sysClr")
    if sysclr is not None:
        val = sysclr.get("lastClr") or SYS_COLOR_DEFAULTS.get(sysclr.get("val"), "000000")
        return "#" + val.upper()
    return None


def extract_theme(zf):
    theme_names = sorted(n for n in zf.namelist() if re.match(r"ppt/theme/theme\d+\.xml", n))
    if not theme_names:
        sys.exit("No theme found in file — is this a valid .pptx?")
    root = ET.fromstring(zf.read(theme_names[0]))

    colors = {}
    scheme = root.find(f".//{{{A}}}clrScheme")
    if scheme is not None:
        for child in scheme:
            tag = child.tag.split("}")[1]
            val = color_value(child)
            if val:
                colors[tag] = val

    fonts = {}
    fscheme = root.find(f".//{{{A}}}fontScheme")
    if fscheme is not None:
        for role, el in (("heading", "majorFont"), ("body", "minorFont")):
            latin = fscheme.find(f"{{{A}}}{el}/{{{A}}}latin")
            if latin is not None and latin.get("typeface"):
                fonts[role] = latin.get("typeface")
    return colors, fonts


def extract_slide_size(zf):
    root = ET.fromstring(zf.read("ppt/presentation.xml"))
    sz = root.find(f"{{{P}}}sldSz")
    if sz is None:
        return None
    cx, cy = int(sz.get("cx")), int(sz.get("cy"))
    ratio = cx / cy
    label = "16:9" if abs(ratio - 16 / 9) < 0.05 else "4:3" if abs(ratio - 4 / 3) < 0.05 else f"{cx}x{cy} EMU"
    return label


def extract_layouts(zf):
    names = sorted(
        (n for n in zf.namelist() if re.match(r"ppt/slideLayouts/slideLayout\d+\.xml", n)),
        key=lambda n: int(re.search(r"(\d+)", n).group(1)),
    )
    layouts = []
    for i, name in enumerate(names):
        root = ET.fromstring(zf.read(name))
        csld = root.find(f"{{{P}}}cSld")
        layouts.append({"index": i, "name": (csld.get("name") if csld is not None else "") or f"Layout {i + 1}"})
    return layouts


def guess_layout_map(layouts):
    """Best-effort role assignment from layout names; humans should verify."""
    patterns = {
        "title": r"title slide|cover",
        "section": r"section|divider|chapter",
        "content": r"title and content|content|body",
        "twoCol": r"two content|two column|comparison",
        "blank": r"blank",
        "closing": r"thank|closing|back cover|end",
    }
    mapping = {}
    for role, pat in patterns.items():
        for lay in layouts:
            if re.search(pat, lay["name"], re.IGNORECASE):
                mapping[role] = {"index": lay["index"], "name": lay["name"]}
                break
    return mapping


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else src.with_suffix(".kit.json")

    with zipfile.ZipFile(src) as zf:
        colors, fonts = extract_theme(zf)
        slide_size = extract_slide_size(zf)
        layouts = extract_layouts(zf)

    accents = [colors.get(f"accent{i}") for i in range(1, 7) if colors.get(f"accent{i}")]
    kit = {
        "meta": {
            "name": src.stem.lower().replace(" ", "-"),
            "client": "",
            "source": src.name,
            "extracted": date.today().isoformat(),
            "confidential": True,
        },
        "colors": {
            "theme": colors,
            "roles": {
                "primary": colors.get("dk2") or colors.get("dk1", "#000000"),
                "accent": accents[0] if accents else "#000000",
                "background": colors.get("lt1", "#FFFFFF"),
                "backgroundDark": colors.get("dk2") or colors.get("dk1", "#000000"),
                "text": colors.get("dk1", "#000000"),
                "textOnDark": colors.get("lt1", "#FFFFFF"),
                "muted": accents[2] if len(accents) > 2 else "#747480",
                "border": accents[3] if len(accents) > 3 else "#C4C4CD",
                "positive": "#168736",
                "negative": "#B9251C",
                "chart": accents or ["#000000"],
            },
        },
        "typography": {
            "heading": {"family": fonts.get("heading", "Arial"), "fallback": FALLBACK, "weight": 700},
            "body": {"family": fonts.get("body", "Arial"), "fallback": FALLBACK, "weight": 400},
            "scale": {"title": 40, "h1": 28, "h2": 20, "body": 14, "caption": 10},
        },
        "logo": {"primary": "", "onDark": "", "placement": "", "clearSpace": ""},
        "pptx": {
            "templatePath": str(src),
            "slideSize": slide_size,
            "layoutMap": guess_layout_map(layouts),
        },
        "notes": [],
    }

    out.write_text(json.dumps(kit, indent=2) + "\n")
    print(f"Kit written to {out}\n")
    print(f"Slide size: {slide_size}")
    print(f"Theme fonts: heading={fonts.get('heading')}, body={fonts.get('body')}")
    print("\nAll layouts in template (assign roles in pptx.layoutMap):")
    for lay in layouts:
        print(f"  [{lay['index']:2d}] {lay['name']}")
    print("\nReview colors.roles and layoutMap with the user — extraction is a first draft.")


if __name__ == "__main__":
    main()
