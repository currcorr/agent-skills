#!/usr/bin/env python3
"""Bundle the EY consulting toolkit and its dependency skills into one zip
for transfer to another GitHub org / machine.

Usage (from repo root):
    python tools/build_ey_pack.py [output.zip]

Default output: dist/ey-consulting-pack.zip
"""

import sys
import zipfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Core toolkit + every skill the toolkit's SKILL.md files reference.
SKILLS = [
    "ey-brand-kit",
    "ey-deck",
    "ey-deck-review",
    "ey-site",
    "ey-synthesis",
    "pptx",                       # .pptx mechanics (unpack/edit/thumbnail/pptxgenjs)
    "frontend-slides",            # HTML presentation techniques used by ey-site
    "orchestrate-tufte-vdqi",     # chart toolkit router
    "render-tufte-chart",         # chart production (SVG/HTML)
    "assess-graphical-excellence" # chart QA
]

PACK_README = f"""# EY Consulting Pack

Self-contained skill pack for building client deliverables: branded
PowerPoint decks and interactive HTML sites, restylable per client via brand
kits, with Tufte-grounded charts. Assembled {date.today().isoformat()} from
the agent-skills repo.

## Contents

| Skill | Role |
|-------|------|
| ey-brand-kit | Per-client brand kits, .pptx theme extraction, kit→CSS, design rules (start here) |
| ey-deck | Storyline-first consulting decks + pattern library + template library |
| ey-deck-review | Partner-style red-pen review: storyline, design rules, AI tells, charts |
| ey-site | Kit-styled zero-dependency interactive HTML deliverables |
| ey-synthesis | Interview/workshop material → evidence-backed findings → deck outline |
| pptx | Low-level .pptx read/edit/create machinery used by ey-deck |
| frontend-slides | HTML presentation techniques used by ey-site |
| orchestrate-tufte-vdqi / render-tufte-chart / assess-graphical-excellence | Chart toolkit (route / build / QA) |

## Install

Each folder is a standard Agent Skill (SKILL.md + resources). Options:

- **Claude Code, per-repo:** copy the folders into `<repo>/.claude/skills/`.
- **Claude Code, personal:** copy into `~/.claude/skills/`.
- **Codex or other agents:** keep the folders anywhere in the workspace and
  point the agent at them (e.g. in AGENTS.md: "for decks, follow
  skills/ey-deck/SKILL.md"), or use the tool's own skills directory.

Scripts are Python 3 stdlib only — no pip installs needed for the EY skills.
The pptx and Tufte skills list their own requirements in their SKILL.md
files (e.g. LibreOffice for thumbnails, Node/pptxgenjs for from-scratch
generation).

## First tasks after install

1. Refresh `ey-brand-kit/kits/ey-default.json` from your brand-standards MCP
   server (the bundled kit is a public-information placeholder).
2. Add a real EY .pptx template, set `pptx.templatePath`, and run
   `ey-brand-kit/scripts/extract_kit.py` on it to fill the layout map.
3. Start flagging good slides into `ey-deck/library/` so the template
   library compounds.

## Licenses

- ey-brand-kit / ey-deck / ey-site: created for this repo, no restrictions.
- pptx: (c) Anthropic, governed by your Anthropic agreement (see
  pptx/LICENSE.txt) — intended for use with Anthropic services.
- frontend-slides: MIT (Zara Zhang).
- Tufte skills: see their folders; render-tufte-chart bundles MIT-licensed
  tufte-css.

Client templates, logos, and kits you add are confidential — keep the
destination repo private.
"""


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "dist" / "ey-consulting-pack.zip"
    out.parent.mkdir(parents=True, exist_ok=True)

    missing = [s for s in SKILLS if not (REPO / s / "SKILL.md").is_file()]
    if missing:
        sys.exit(f"Missing skills (no SKILL.md): {', '.join(missing)}")

    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("ey-consulting-pack/README.md", PACK_README)
        for skill in SKILLS:
            for f in sorted((REPO / skill).rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts:
                    zf.write(f, f"ey-consulting-pack/{f.relative_to(REPO)}")
                    count += 1

    print(f"Wrote {out} ({out.stat().st_size / 1e6:.1f} MB, {count} files, {len(SKILLS)} skills)")


if __name__ == "__main__":
    main()
