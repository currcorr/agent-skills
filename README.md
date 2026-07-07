# Agent Skills

Curated skills for Codex, Claude Code, and OpenClaw agents.

Each subdirectory contains a SKILL.md and any supporting files.

## EY consulting toolkit

Three skills that work as a system for client deliverables:

- **ey-brand-kit** — per-client brand kits (JSON tokens). Extracts colors,
  fonts, and layout maps from any client .pptx template; converts kits to CSS
  variables; holds the overarching design rules. Start here.
- **ey-deck** — storyline-first PowerPoint decks from a consulting slide
  pattern library, rendered through the active kit (uses the `pptx` skill for
  file mechanics).
- **ey-site** — zero-dependency interactive HTML deliverables (reports,
  dashboards, workshop sites) styled from the same kit, so decks and sites
  always match.
- **ey-synthesis** — interview/workshop material → evidence-backed findings
  → deck-ready outline (the upstream half of readout decks).
- **ey-deck-review** — partner-style red-pen review of any finished deck:
  storyline, design rules, AI-tells lint, chart QA, severity-ranked findings.
- **excel-to-evidence** — workbook → tied-out exhibits: locate the series,
  verify it ties out, draft the so-what, render via Tufte, log provenance.

Plus an imported consulting stack (researched June 2026, each folder carries
its upstream license): `management-consulting` (42 strategy frameworks),
`meeting-minutes`, `brand-review`, `design-critique`, `ux-copy`,
`internal-comms`, `financial-analyst`, `senior-pm`, `startup-competitors`,
and `refero-design-research`.

Also imported: `canvas-design` (Anthropic, July 2026) — static poster/art
pieces (PNG/PDF) with 54 bundled OFL fonts; pairs with `ey-brand-kit` for
client-styled one-pagers and cover art. New in-house: `deep-research` —
decision-grade, multi-source, adversarially verified research reports with
citations (quick lookups stay with `perplexity`/`last30days`).

Design-build gate (in-house):

- **adversarial-design-review** — fresh-adversary gate for any rendered design
  (HTML page, site, artifact): hunts 23 AI design tells, verifies content +
  functional accuracy (runs the JS), applies measured gates (computed contrast,
  375px signature test, crescendo check). The mandatory final pass after
  `frontend-design`/`ey-site`/`canvas-design`/`interactive-brief`.
- **interactive-brief** — self-contained interactive HTML artifacts consumed on
  a phone from an attachment that collect the reader's structured reactions and
  send them back via pre-filled iMessage or clipboard (briefs, review decks,
  decision cards).
- **taste** — imported design-taste reference library (July 2026, licensed +
  attributed): Leonxlnx taste-skill v2 (web anti-slop), pbakaus/impeccable
  craft chapters (typeset/layout/colorize/polish/craft), Emil Kowalski motion
  standards. Web/HTML + motion layers only; decks stay governed by `deck-kit`.

Orchestration (in-house):

- **large-program-orchestration** — the multi-session program pattern (from
  Ryan Carson's 40-session migration): frozen immutable manifest, risk-ordered
  waves of file-disjoint work packages, fresh-context gates between waves,
  parent writes zero code. Includes the loop-scale ladder (turn/goal/time/
  proactive) for work below program scale.

Bundle all of it (plus dependency skills) for transfer with
`python tools/build_ey_pack.py`.

Swapping the kit restyles every deliverable — nothing outside `kits/` may
hard-code a color or font. Scripts are Python stdlib only and the skills are
tool-agnostic: from Codex or another agent, point it at the relevant SKILL.md
(e.g. "follow agent-skills/ey-deck/SKILL.md") or symlink the skill folders
into the tool's skills directory.

## Keeping skills in sync across Codex and Claude

The skills repo on GitHub is the single source of truth; every tool reads
the same local clone of it. Any agent that edits a skill commits and pushes;
every other agent picks up the change at its next session start.

**Setup per machine/environment:**

1. Clone this repo once, e.g. to `~/skills`.
2. Point Claude Code at it — symlink the skill folders into
   `~/.claude/skills/` (personal) or `<project>/.claude/skills/` (per-repo):

   ```bash
   mkdir -p ~/.claude/skills
   for d in ~/skills/*/; do
     [ -f "$d/SKILL.md" ] && ln -sfn "$d" ~/.claude/skills/$(basename "$d")
   done
   ```

3. Point Codex at the same clone (its skills directory, or an AGENTS.md
   line: "for decks, follow ~/skills/ey-deck/SKILL.md").
4. Auto-pull at session start so changes propagate without thinking about
   it — in Claude Code's `settings.json`:

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

   For Claude Code on the web, clone the repo in the environment's setup
   script instead — a fresh clone is always current.

5. The reverse direction (Codex picking up Claude's pushes) uses the same
   pull, triggered on the Codex side. Most deterministic: wrap the CLI so
   every launch pulls first — in `~/.bashrc`/`~/.zshrc`:

   ```bash
   codex() { git -C ~/skills pull --ff-only --quiet 2>/dev/null; command codex "$@"; }
   ```

   Belt-and-suspenders: also put a line in AGENTS.md ("before using any
   skill from ~/skills, run `git -C ~/skills pull --ff-only`") so remote or
   non-wrapped Codex sessions self-update. The wrapper is harness-level and
   always fires; the AGENTS.md line depends on the agent following it.

**Iteration loop:** edit a skill from either tool → commit → push. New
sessions everywhere see it. Two caveats: skill descriptions load at session
*start*, so a running session won't see a mid-session push until restarted;
and if more than one person starts pushing, switch from direct pushes to
branches + PRs.

**How agents know when to use these skills:** Claude Code loads every
skill's frontmatter `description` at session start and triggers on matching
requests — no need to name a skill, just talk ("build me a readout deck",
"I like this slide — save it"). Codex doesn't auto-discover skill
descriptions, so its AGENTS.md must carry the trigger index. Paste this
into engagement workspaces' AGENTS.md (adjust the path):

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
