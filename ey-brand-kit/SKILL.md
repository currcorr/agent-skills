---
name: ey-brand-kit
description: Create, extract, and apply client brand kits (colors, fonts, logos, PPT layout maps) for consulting deliverables. Use whenever the user mentions a client PowerPoint template, matching a client's branding, "make it look like the client's deck", restyling a deliverable for a different client, EY branding, or before building any deck or site with ey-deck or ey-site. Also use to extract theme colors and fonts from any .pptx file.
---

# EY Brand Kit

A brand kit is a single JSON file that captures everything needed to style a
deliverable for one client: colors, typography, logo, and a map of the slide
layouts in their PowerPoint template. Decks (`ey-deck`) and interactive sites
(`ey-site`) both consume the same kit, so one extraction restyles everything.

Tool-agnostic: plain markdown + Python stdlib scripts. Works from Claude Code,
Codex CLI, or any agent that can run Python.

## Sources of truth (in precedence order)

1. **Client's own template/guidelines** — for client-branded deliverables,
   the extracted client .pptx always wins.
2. **Brand-standards MCP server** — if any connected MCP server exposes
   brand standards, design assets, or template libraries (common on EY work
   accounts), query it before relying on anything baked into this repo. Use
   it to populate or validate kit colors, fonts, logo assets, and approved
   templates — and to refresh `kits/ey-default.json`, which is only a
   placeholder built from public information.
3. **Kits in `kits/`** — previously confirmed extractions.
4. **`kits/ey-default.json`** — last resort.

When an MCP source supplied values, record it in the kit's `meta.source` so
provenance is auditable.

## Workflow

1. **Find or create the kit.** Check `kits/` for an existing kit for this
   client. If a brand-standards MCP server is connected, pull authoritative
   values from it (see precedence above). If none exists and the user has a
   client .pptx template:

   ```bash
   python scripts/extract_kit.py ClientTemplate.pptx kits/client-name.json
   ```

   This pulls the theme color scheme, font scheme, slide size, and layout
   names directly from the file's XML. No client template? Start from
   `kits/ey-default.json` and adjust.

2. **Review with the user.** Show the extracted colors (as a small HTML swatch
   page or a table with hex codes) and the layout map. Extraction gets the raw
   theme right, but humans should confirm which accent is "the" brand color
   and which layouts to use for title/section/content slides. Fill in the
   `roles` block based on their answers.

3. **Apply it.**
   - Decks: pass the kit path to the `ey-deck` workflow. The kit's
     `pptx.templatePath` and `pptx.layoutMap` drive template-based editing;
     `colors`/`typography` drive from-scratch generation.
   - Sites: generate CSS variables and inject into the HTML head:

     ```bash
     python scripts/kit_to_css.py kits/client-name.json > client-name.css
     ```

4. **Commit the kit** to `kits/` so the next engagement reuses it.

## Kit anatomy

See [references/kit-schema.md](references/kit-schema.md) for the full schema
with field-by-field notes. Summary:

| Block | Contents |
|-------|----------|
| `meta` | Client name, source template, date extracted |
| `colors` | Raw theme palette + semantic `roles` (primary, accent, background, text, chart series) |
| `typography` | Heading/body font families with web-safe fallbacks, size scale |
| `logo` | Path(s) to logo assets, clear-space and placement notes |
| `pptx` | Template path, slide size, `layoutMap` (role → layout index/name) |
| `notes` | Free-text brand rules that don't fit structured fields |

## Design rules

[references/design-rules.md](references/design-rules.md) holds the overarching
design rules that apply to **every** deliverable regardless of client kit —
hierarchy, density, Tufte-grounded chart rules (backed by the
`orchestrate-tufte-vdqi` / `render-tufte-chart` / `assess-graphical-excellence`
skills in this repo), accessibility, and a mandatory lint for common AI
design tells (rules 20–25). Read it before building anything
with `ey-deck` or `ey-site`. Client kit settings override colors and fonts;
they never override these rules.

## Cautions

- Client templates and logos are usually confidential. Keep kits in private
  repos only, and never embed client assets in anything published externally.
- Fonts named in a client theme (e.g. proprietary corporate fonts) often are
  not installed where the deck renders. Always record a fallback stack; the
  extractor inserts sensible defaults, but verify.
- EY's own font (EY Interstate) is licensed — reference it by name with
  Arial/Helvetica fallbacks rather than bundling font files.
