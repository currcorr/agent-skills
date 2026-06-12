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
    "excel-to-evidence",
    "xlsx",                       # workbook mechanics used by excel-to-evidence
    "pptx",                       # .pptx mechanics (unpack/edit/thumbnail/pptxgenjs)
    "frontend-slides",            # HTML presentation techniques used by ey-site
    "humanizer",                  # AI writing-register detection used by the design-rules lint
    "orchestrate-tufte-vdqi",     # chart toolkit router
    "render-tufte-chart",         # chart production (SVG/HTML)
    "assess-graphical-excellence",# chart QA
    # Imported consulting stack (researched 2026-06; all MIT/Apache)
    "management-consulting",      # 42 strategic frameworks, three response modes
    "meeting-minutes",            # strict minutes schema: decisions, owners, dates
    "brand-review",               # voice/terminology governance QA
    "design-critique",            # general visual critique beyond decks
    "ux-copy",                    # interface microcopy for ey-site deliverables
    "internal-comms",             # status reports, 3P updates, leadership comms
    "financial-analyst",          # ratios, DCF, variance, forecast tooling
    "senior-pm",                  # portfolio/program management, RAG, stakeholder maps
    "startup-competitors",        # three-wave competitive intelligence
    "refero-design-research",     # evidence-based design craft guides (+optional MCP)
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
| excel-to-evidence | Workbook → tied-out, traceable exhibits with evidence log |
| xlsx | Spreadsheet read/edit/create machinery used by excel-to-evidence |
| pptx | Low-level .pptx read/edit/create machinery used by ey-deck |
| frontend-slides | HTML presentation techniques used by ey-site |
| humanizer | AI writing-register detection (design rule 25's authority) |
| orchestrate-tufte-vdqi / render-tufte-chart / assess-graphical-excellence | Chart toolkit (route / build / QA) |
| management-consulting | 42 strategic frameworks — the reasoning layer upstream of deliverables |
| meeting-minutes | Strict minutes schema (decisions w/ rationale, owned+dated actions) |
| brand-review / design-critique / ux-copy | Voice governance, visual critique, microcopy QA |
| internal-comms | Status reports, 3P updates, leadership communications |
| financial-analyst / senior-pm | Financial modeling tools; portfolio/program management |
| startup-competitors | Three-wave competitive intelligence with confidence labels |
| refero-design-research | Evidence-based design craft guides (optional Refero MCP) |

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
- pptx / xlsx: (c) Anthropic, governed by your Anthropic agreement (see
  their LICENSE.txt files) — intended for use with Anthropic services.
- frontend-slides: MIT (Zara Zhang).
- Tufte skills: see their folders; render-tufte-chart bundles MIT-licensed
  tufte-css.
- Imported consulting stack: each folder carries its upstream LICENSE
  (Anthropic knowledge-work-plugins, anthropics/skills, github/awesome-copilot,
  borghei/Claude-Skills, ferdinandobons/startup-skill,
  gcamilo/management-consulting, referodesign/refero_skill — all MIT or
  equivalent permissive).

Client templates, logos, and kits you add are confidential — keep the
destination repo private.
"""

PACK_README += r"""
## Keeping skills in sync across Codex and Claude

Make the repo this pack was unzipped into the single source of truth; every
tool reads the same local clone. Edits from any agent: commit → push; other
sessions pick it up at next start.

1. Clone the repo once per machine, e.g. to `~/skills`.
2. Claude Code — symlink skills in:

   ```bash
   mkdir -p ~/.claude/skills
   for d in ~/skills/*/; do ln -sfn "$d" ~/.claude/skills/$(basename "$d"); done
   ```

3. Auto-pull at session start (Claude Code `settings.json`):

   ```json
   {
     "hooks": {
       "SessionStart": [
         { "hooks": [ { "type": "command",
             "command": "git -C ~/skills pull --ff-only --quiet || true" } ] }
       ]
     }
   }
   ```

4. Codex — pull on every launch via a shell wrapper, plus an AGENTS.md line
   as backup:

   ```bash
   codex() { git -C ~/skills pull --ff-only --quiet 2>/dev/null; command codex "$@"; }
   ```

## How agents know when to use these skills

Claude Code auto-discovers skills from their frontmatter descriptions — just
talk ("build me a readout deck", "I like this slide — save it"). Codex needs
a trigger index in each workspace's AGENTS.md (adjust the path):

```markdown
## Skills (~/skills) — read the matching SKILL.md BEFORE starting these tasks
- Any deck/slides/presentation/readout → ~/skills/ey-deck/SKILL.md
- User praises/flags a slide or deck ("save this", "I like the aesthetic/
  headlines") → ~/skills/ey-deck/SKILL.md (template library section)
- Client branding, extract template, restyle for client → ~/skills/ey-brand-kit/SKILL.md
- Interactive site/dashboard/web deliverable → ~/skills/ey-site/SKILL.md
- Review/QA/red-pen a deck → ~/skills/ey-deck-review/SKILL.md
- Synthesize interviews/workshop notes → ~/skills/ey-synthesis/SKILL.md
- Exhibits/charts from a workbook → ~/skills/excel-to-evidence/SKILL.md
- Strategy frameworks/problem structuring → ~/skills/management-consulting/SKILL.md
- Meeting notes → minutes → ~/skills/meeting-minutes/SKILL.md
```

## Automations

`tools/automations.md` (bundled) has three scheduled-agent recipes with
runnable commands: daily skills housekeeping, weekly library digest +
rule-promotion PRs, and the Friday correction review that turns repeated
user corrections into proposed skill/rule edits. All three end in files or
PRs — never a send.
"""

# Non-skill files bundled so the pack stands alone.
EXTRAS = ["tools/automations.md"]


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO / "dist" / "ey-consulting-pack.zip"
    out.parent.mkdir(parents=True, exist_ok=True)

    missing = [s for s in SKILLS if not (REPO / s / "SKILL.md").is_file()]
    if missing:
        sys.exit(f"Missing skills (no SKILL.md): {', '.join(missing)}")

    count = 0
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("ey-consulting-pack/README.md", PACK_README)
        for extra in EXTRAS:
            zf.write(REPO / extra, f"ey-consulting-pack/{extra}")
        for skill in SKILLS:
            for f in sorted((REPO / skill).rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts:
                    zf.write(f, f"ey-consulting-pack/{f.relative_to(REPO)}")
                    count += 1

    print(f"Wrote {out} ({out.stat().st_size / 1e6:.1f} MB, {count} files, {len(SKILLS)} skills)")


if __name__ == "__main__":
    main()
