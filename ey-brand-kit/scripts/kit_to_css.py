#!/usr/bin/env python3
"""Convert a brand kit JSON into CSS custom properties.

Usage:
    python kit_to_css.py kits/client.json > client.css

Emits a :root block with --color-*, --font-*, and --text-* variables that
ey-site templates consume. Point sizes from the kit scale are converted to
rem (1pt ~= 1.333px, base 16px).
"""

import json
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    kit = json.loads(Path(sys.argv[1]).read_text())

    lines = [f"/* Generated from {kit.get('meta', {}).get('name', 'kit')} — do not hand-edit colors here */", ":root {"]

    for name, val in kit.get("colors", {}).get("roles", {}).items():
        if name == "chart":
            for i, c in enumerate(val, 1):
                lines.append(f"  --color-chart-{i}: {c};")
        else:
            lines.append(f"  --color-{name.replace('_', '-')}: {val};")

    typo = kit.get("typography", {})
    for role in ("heading", "body"):
        f = typo.get(role)
        if f:
            stack = f'"{f["family"]}", {f.get("fallback", "sans-serif")}'
            lines.append(f"  --font-{role}: {stack};")
            lines.append(f"  --weight-{role}: {f.get('weight', 400)};")

    for name, pt in typo.get("scale", {}).items():
        rem = round(pt * 1.333 / 16, 3)
        lines.append(f"  --text-{name}: {rem}rem;")

    lines.append("}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
