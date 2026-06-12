---
name: ey-site
description: Build interactive client-facing websites and microsites for consulting work — interactive reports, workshop sites, dashboards, prototypes, results explorers — styled from the same brand kit as the decks. Use whenever the user wants an interactive site, web version of a deck, clickable prototype, microsite, or HTML deliverable for client or EY work, or wants to "make this deck interactive".
---

# EY Site

Single-file, zero-dependency interactive HTML deliverables, styled entirely
by CSS variables generated from a brand kit — the same kit that styles the
client's deck, so deck and site always match.

Dependencies (same repo): `ey-brand-kit` for the kit, CSS generation, and
design rules. For presentation-style sites (slide-by-slide), also read
`frontend-slides` for animation and viewport techniques.

## Workflow

### 1. Resolve the brand kit and rules

Use `ey-brand-kit` to find/extract the client kit, then generate the styles:

```bash
python ../ey-brand-kit/scripts/kit_to_css.py kits/client.json
```

Paste the emitted `:root` block into the template's `/* KIT VARIABLES */`
slot. Read `ey-brand-kit/references/design-rules.md` — rules 8, 15, 17
(accent scarcity, contrast, accessibility) are the ones sites most often
break.

### 2. Pick the site shape

| Shape | Use for | Structure |
|---|---|---|
| **Interactive report** | Deck content that benefits from drill-down | Sticky section nav + scrollable sections, expandable detail |
| **Dashboard** | KPIs, value tracking | Card grid + filterable charts |
| **Workshop site** | Agendas, pre-reads, live exercises | Tabbed pages, embedded forms/canvases |
| **Prototype** | Demonstrating a future-state tool/journey | Clickable screens with realistic dummy data |

Start every shape from [assets/site-template.html](assets/site-template.html)
— it has the token plumbing, layout primitives, and accessibility baseline
wired up.

### 3. Build

- **Single HTML file, no CDN dependencies.** Client IT blocks external
  resources, and deliverables get emailed. Inline all CSS/JS; charts as
  inline SVG. Build charts with the `render-tufte-chart` skill — its scripts
  emit standalone SVG that pastes straight into the page; recolor strokes/
  fills with the kit's `--color-chart-*` variables.
- **Only token styling.** Every color/font through `var(--color-*)` /
  `var(--font-*)`. A kit swap must restyle the site with zero markup edits.
- **Slide patterns translate.** The `ey-deck` pattern library
  (`ey-deck/references/slide-patterns.md`) maps to site sections: KPI
  dashboard → card grid, roadmap → horizontal scroll timeline, harvey-ball
  table → interactive comparison with hover detail. Interactivity should add
  drill-down depth a static slide can't, not decoration.
- **Confidentiality:** same footer marking as the deck, plus a
  `<meta name="robots" content="noindex">` and a reminder to the user that
  hosting anywhere public requires client approval.

### 4. Verify

- Open in a browser (or render a screenshot) and check at 1440px and 390px
  widths — client partners will open it on phones.
- Keyboard-walk the interactions; check focus visibility.
- Print preview: an interactive report should still print sanely to PDF.
- Contrast-check text/background pairs from the kit (rule 15).
- Run the AI-tells lint (design rules 20–25). Sites are the worst offenders:
  check specifically for border-radius creep, gradient backgrounds, icon
  grids, and equal-weight card rows. The template ships square-cornered and
  flat — keep it that way.

## Restyling for a new client

Regenerate the CSS block from the new kit and replace the `:root` section.
If nothing else needs editing, the site was built correctly. Then re-check
contrast and accent scarcity.
