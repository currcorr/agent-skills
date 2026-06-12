#!/usr/bin/env python3
"""Extract a slide's construction spec: every shape, its geometry, position,
fill, line, and text — documenting HOW a slide is built from shapes so an
agent can study or reproduce the construction. Stdlib only.

Usage:
    python slide_anatomy.py deck.pptx SLIDE_NUMBER [output.md]

Outputs:
  - <out>.md   human-readable construction spec (table + token map + notes)
  - <out>.json machine-readable fixture for spec_diff.py, with per-element
               "mode" ("preserve" | "flex", set at flag time) and a token
               map (literal color -> kit role, set at flag time)
"""

import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"
EMU_PER_IN = 914400


def emu_in(v):
    return round(int(v) / EMU_PER_IN, 2)


def get_xfrm(sp_pr):
    xfrm = sp_pr.find(f"{A}xfrm") if sp_pr is not None else None
    if xfrm is None:
        return None
    off, ext = xfrm.find(f"{A}off"), xfrm.find(f"{A}ext")
    if off is None or ext is None:
        return None
    return {
        "x": int(off.get("x")), "y": int(off.get("y")),
        "cx": int(ext.get("cx")), "cy": int(ext.get("cy")),
        "rot": int(xfrm.get("rot", 0)),
        "choff": xfrm.find(f"{A}chOff"), "chext": xfrm.find(f"{A}chExt"),
    }


def get_fill(sp_pr):
    if sp_pr is None:
        return ""
    solid = sp_pr.find(f"{A}solidFill")
    if solid is None:
        return "none" if sp_pr.find(f"{A}noFill") is not None else ""
    srgb = solid.find(f"{A}srgbClr")
    if srgb is not None:
        return "#" + srgb.get("val").upper()
    scheme = solid.find(f"{A}schemeClr")
    return f"theme:{scheme.get('val')}" if scheme is not None else "?"


def get_line(sp_pr):
    """Outline style: width(pt) color dash, or '' if none."""
    ln = sp_pr.find(f"{A}ln") if sp_pr is not None else None
    if ln is None:
        return ""
    if ln.find(f"{A}noFill") is not None:
        return "none"
    parts = []
    if ln.get("w"):
        parts.append(f"{int(ln.get('w')) / 12700:g}pt")
    solid = ln.find(f"{A}solidFill")
    if solid is not None:
        srgb, scheme = solid.find(f"{A}srgbClr"), solid.find(f"{A}schemeClr")
        if srgb is not None:
            parts.append("#" + srgb.get("val").upper())
        elif scheme is not None:
            parts.append(f"theme:{scheme.get('val')}")
    dash = ln.find(f"{A}prstDash")
    if dash is not None:
        parts.append(dash.get("val"))
    return " ".join(parts) or "default"


def get_table(frame):
    """Summarize a graphicFrame's table: rows x cols + column widths."""
    tbl = frame.find(f".//{A}tbl")
    if tbl is None:
        return None
    cols = [emu_in(c.get("w")) for c in tbl.findall(f"{A}tblGrid/{A}gridCol")]
    rows = len(tbl.findall(f"{A}tr"))
    return f"{rows}r × {len(cols)}c, col widths(in): {', '.join(str(c) for c in cols)}"


def get_text(el):
    """Concatenate runs; report dominant size/bold."""
    parts, sizes, bolds = [], [], []
    for para in el.findall(f".//{A}p"):
        runs = [r for r in para.findall(f"{A}r")]
        text = "".join((r.findtext(f"{A}t") or "") for r in runs)
        if text.strip():
            parts.append(text.strip())
        for r in runs:
            rpr = r.find(f"{A}rPr")
            if rpr is not None:
                if rpr.get("sz"):
                    sizes.append(int(rpr.get("sz")) // 100)
                if rpr.get("b") == "1":
                    bolds.append(True)
    text = " / ".join(parts)
    if len(text) > 80:
        text = text[:77] + "…"
    meta = []
    if sizes:
        meta.append(f"{max(set(sizes), key=sizes.count)}pt")
    if bolds:
        meta.append("bold")
    return text, " ".join(meta)


def walk(tree_el, transform, rows, depth=0):
    """transform maps raw child coords -> absolute EMU: (ox, oy, sx, sy)."""
    ox, oy, sx, sy = transform
    for el in tree_el:
        tag = el.tag.split("}")[1]
        if tag not in ("sp", "pic", "graphicFrame", "grpSp", "cxnSp"):
            continue
        nv = el.find(f".//{P}cNvPr")
        name = nv.get("name") if nv is not None else ""
        ph = el.find(f".//{P}ph")
        sp_pr = el.find(f"{P}spPr") or el.find(f"{P}grpSpPr")
        xf = get_xfrm(sp_pr) if sp_pr is not None else None
        if xf is None and tag == "graphicFrame":
            xf = get_xfrm(el)
        kind = {"sp": "shape", "pic": "image", "graphicFrame": "table/chart",
                "grpSp": "group", "cxnSp": "connector"}[tag]
        geom = el.find(f".//{A}prstGeom")
        if geom is not None and tag == "sp":
            kind = geom.get("prst")
        placeholder = ph.get("type", "body") if ph is not None else ""
        row = {"depth": depth, "kind": kind, "name": name,
               "placeholder": placeholder,
               "fill": get_fill(sp_pr), "line": get_line(sp_pr)}
        if xf:
            row.update(x=round(ox + xf["x"] * sx), y=round(oy + xf["y"] * sy),
                       w=round(xf["cx"] * sx), h=round(xf["cy"] * sy),
                       rot=round(xf["rot"] / 60000, 1) if xf["rot"] else 0)
        tx = el.find(f"{P}txBody")
        row["text"], row["textmeta"] = get_text(tx) if tx is not None else ("", "")
        if tag == "graphicFrame":
            tbl = get_table(el)
            if tbl:
                row["kind"], row["text"] = "table", tbl
        rows.append(row)
        if tag == "grpSp" and xf is not None:
            choff, chext = xf["choff"], xf["chext"]
            cx0 = int(choff.get("x")) if choff is not None else xf["x"]
            cy0 = int(choff.get("y")) if choff is not None else xf["y"]
            cw = int(chext.get("cx")) if chext is not None else xf["cx"]
            ch = int(chext.get("cy")) if chext is not None else xf["cy"]
            gsx = (xf["cx"] / cw if cw else 1) * sx
            gsy = (xf["cy"] / ch if ch else 1) * sy
            gox = ox + xf["x"] * sx - cx0 * gsx
            goy = oy + xf["y"] * sy - cy0 * gsy
            walk(el, (gox, goy, gsx, gsy), rows, depth + 1)


def get_theme(zf):
    """First theme's color scheme as {slot: #HEX} for resolving theme: refs."""
    names = sorted(n for n in zf.namelist() if re.match(r"ppt/theme/theme\d+\.xml", n))
    if not names:
        return {}
    root = ET.fromstring(zf.read(names[0]))
    scheme = root.find(f".//{A}clrScheme")
    colors = {}
    if scheme is not None:
        for child in scheme:
            tag = child.tag.split("}")[1]
            srgb = child.find(f"{A}srgbClr")
            sysclr = child.find(f"{A}sysClr")
            if srgb is not None:
                colors[tag] = "#" + srgb.get("val").upper()
            elif sysclr is not None and sysclr.get("lastClr"):
                colors[tag] = "#" + sysclr.get("lastClr").upper()
    # scheme refs in shapes use tx/bg aliases for dk/lt
    for alias, slot in (("tx1", "dk1"), ("bg1", "lt1"), ("tx2", "dk2"), ("bg2", "lt2")):
        if slot in colors:
            colors.setdefault(alias, colors[slot])
    return colors


def extract(src, n):
    """Return the spec as a dict (positions in EMU). Importable by spec_diff."""
    src = Path(src)
    with zipfile.ZipFile(src) as zf:
        theme = get_theme(zf)
        pres = ET.fromstring(zf.read("ppt/presentation.xml"))
        sz = pres.find(f"{P}sldSz")
        W, H = int(sz.get("cx")), int(sz.get("cy"))
        slide_name = f"ppt/slides/slide{n}.xml"
        if slide_name not in zf.namelist():
            avail = sorted(s for s in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml", s))
            raise SystemExit(f"{slide_name} not found. Deck has {len(avail)} slides.")
        root = ET.fromstring(zf.read(slide_name))
        layout = ""
        rel = f"ppt/slides/_rels/slide{n}.xml.rels"
        if rel in zf.namelist():
            m = re.search(r'Target="\.\./slideLayouts/(slideLayout\d+)\.xml"', zf.read(rel).decode())
            if m:
                lay = ET.fromstring(zf.read(f"ppt/slideLayouts/{m.group(1)}.xml"))
                csld = lay.find(f"{P}cSld")
                layout = csld.get("name", "") if csld is not None else ""

    rows = []
    walk(root.find(f"{P}cSld/{P}spTree"), (0, 0, 1, 1), rows)
    for i, r in enumerate(rows, 1):
        r["z"] = i
        r.setdefault("mode", "")  # set at flag time: "preserve" | "flex"

    tokens = {}
    for r in rows:
        for val in (r["fill"], r["line"]):
            for tok in val.split():
                if tok.startswith("#") or tok.startswith("theme:"):
                    tokens.setdefault(tok, "")  # role filled at flag time

    return {"source": src.name, "slide": n, "layout": layout,
            "canvas": {"w": W, "h": H}, "theme": theme,
            "elements": rows, "token_map": tokens}


def to_markdown(spec):
    W, H = spec["canvas"]["w"], spec["canvas"]["h"]
    rows = spec["elements"]
    lines = [
        f"# Construction spec — {spec['source']}, slide {spec['slide']}",
        f"Canvas: {emu_in(W)} x {emu_in(H)} in · Layout: \"{spec['layout'] or 'unknown'}\" · {len(rows)} elements (z-order, top to bottom of table = back to front)",
        "",
        "| z | Element | Name | Pos x,y (in) | Size w×h (in) | x,y (%) | Fill | Line | Text |",
        "|---|---------|------|--------------|---------------|---------|------|------|------|",
    ]
    for r in rows:
        indent = "↳ " * r["depth"]
        kind = r["kind"] + (f" [placeholder:{r['placeholder']}]" if r["placeholder"] else "")
        if "x" in r:
            pos = f"{r['x']/EMU_PER_IN:.2f}, {r['y']/EMU_PER_IN:.2f}"
            size = f"{r['w']/EMU_PER_IN:.2f} × {r['h']/EMU_PER_IN:.2f}"
            pct = f"{100*r['x']/W:.0f}, {100*r['y']/H:.0f}"
            if r.get("rot"):
                size += f" rot{r['rot']}°"
        else:
            pos = size = pct = "—"
        text = r["text"] + (f" ({r['textmeta']})" if r["textmeta"] else "")
        lines.append(f"| {r['z']} | {indent}{kind} | {r['name']} | {pos} | {size} | {pct} | {r['fill']} | {r['line']} | {text} |")

    lines += [
        "",
        "## Token map — literal value → kit role (fill in at flag time, in the .json)",
        "",
        "| Value | Kit role |",
        "|-------|----------|",
    ]
    for val in spec["token_map"]:
        lines.append(f"| {val} | |")
    if not spec["token_map"]:
        lines.append("| _no explicit colors found (all inherited from layout/master)_ | |")

    lines += [
        "",
        "## Construction notes (fill in at flag time)",
        "",
        "- **Per-element mode:** _set \"mode\" to preserve|flex for each element in the .json — the verifier depends on it_",
        "- **Alignment grid:** _column boundaries / margins everything snaps to_",
        "- **Spacing rhythm:** _the repeated gaps and padding unit_",
        "- **Visual zones:** _which elements form which zones (title / evidence / so-what…)_",
        "- **Hierarchy:** _what reads first, second, third — and why_",
        "- **Preserve:** _what must not change when reusing (proportions, zone order…)_",
        "- **Can flex:** _what adapts safely (element counts, zone widths, text length…)_",
        "- **Why it works:** _the craft judgment, one or two sentences_",
        "",
    ]
    return "\n".join(lines)


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    src, n = Path(sys.argv[1]), int(sys.argv[2])
    out = Path(sys.argv[3]) if len(sys.argv) > 3 else src.with_name(f"{src.stem}-slide{n}-anatomy.md")
    spec = extract(src, n)
    out.write_text(to_markdown(spec))
    json_out = out.with_suffix(".json")
    json_out.write_text(json.dumps(spec, indent=1) + "\n")
    print(f"Wrote {out} and {json_out} ({len(spec['elements'])} elements)")
    print("Flag-time TODO in the .json: set per-element \"mode\" and the token_map roles.")


if __name__ == "__main__":
    main()
