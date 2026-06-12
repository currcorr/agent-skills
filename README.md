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

Swapping the kit restyles every deliverable — nothing outside `kits/` may
hard-code a color or font. Scripts are Python stdlib only and the skills are
tool-agnostic: from Codex or another agent, point it at the relevant SKILL.md
(e.g. "follow agent-skills/ey-deck/SKILL.md") or symlink the skill folders
into the tool's skills directory.
