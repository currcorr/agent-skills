---
name: ey-deck
description: Build consulting-grade PowerPoint decks rapidly — storyline first, branded via a client kit, using a library of proven consulting slide patterns. Use whenever the user asks for a deck, slides, presentation, proposal, steering-committee pack, status report, or readout for client or internal EY work, including restyling an existing deck for a new client. ALSO use whenever the user flags or praises any slide or deck — "save this slide", "keep this layout", "I like this deck's headlines/aesthetic/messaging", "add this to my template library" — to capture it in the template library, even when no new deck is being built. Works with or without a client .pptx template.
---

# EY Deck

Storyline → patterns → render. The deck's content is designed before any
slide is touched, the look comes entirely from a brand kit, and the slides
themselves are assembled from a pattern library — so the same deck can be
restyled for a different client by swapping the kit.

Dependencies (same repo): `ey-brand-kit` for styling and design rules,
`pptx` for low-level .pptx mechanics.

## Workflow

### 1. Storyline first — no slides yet

If the deck is a findings readout from interviews or workshops, run
`ey-synthesis` first — it produces the evidence-backed outline this step
needs. Read [references/storyline-guide.md](references/storyline-guide.md). Produce
a one-page outline: governing thought, then one line per slide where each
line is that slide's **action title** (a complete sentence stating the
takeaway). Confirm the storyline with the user before building anything —
revising an outline is minutes, revising a built deck is hours.

### 2. Resolve the brand kit

Use the `ey-brand-kit` skill. If the user supplied a client template, extract
a kit from it; otherwise use `ey-brand-kit/kits/ey-default.json` or an
existing client kit. Read `ey-brand-kit/references/design-rules.md` — those
rules bind every slide.

### 3. Pick a pattern per slide

[references/slide-patterns.md](references/slide-patterns.md) catalogs the
consulting patterns (exec summary, 2x2, roadmap, harvey-ball comparison,
KPI dashboard, …) with layout specs and when-to-use guidance. Check
[library/INDEX.md](library/INDEX.md) first — a flagged real slide that fits
beats a pattern built from scratch. Annotate the outline with one pattern
(or library entry) per slide.

### 4. Render

For slides whose evidence lives in a workbook or model, build the exhibits
with `excel-to-evidence` first — it ties numbers out to the source and
produces the evidence log QA will want.

Two paths, chosen by whether a client .pptx template exists:

- **Template path (preferred when `pptx.templatePath` is set in the kit):**
  follow the `pptx` skill's editing workflow — duplicate template slides per
  the kit's `layoutMap`, replace placeholder content. This inherits masters,
  footers, and fonts exactly, which is what "matching the client template"
  actually requires. Note that in practice most content slides use a basic
  layout (title + body, or blank) and are **constructed freehand from
  shapes, text boxes, and objects** — the layout supplies only the title
  placeholder and furniture.

  When constructing freehand, route by slide type:
  - **Data-driven slides** (charts, tables, timelines, dashboards — anything
    whose element count varies with the data): generate **parametrically**
    — Tufte scripts for charts, pptxgenjs/table generation from kit tokens.
    An exemplar spec built for 5 bars does not adapt safely to 9; code does.
  - **Compositional slides** (frameworks, callout layouts, comparison
    builds, section structures): rebuild from **construction specs** in
    `library/anatomy/` — exact positions, sizes, fills, grouping, plus
    craft notes saying what to preserve and what can flex. Rebuilding from
    a spec beats improvising geometry.
  - Hybrids (a chart inside a composed layout) use both: spec for the
    composition and zones, parametric generation for the data element
    placed into its zone.

  To study how any existing slide is built, run
  `scripts/slide_anatomy.py deck.pptx <slide#>`.
- **From-scratch path:** follow the `pptx` skill's pptxgenjs workflow, but
  take every color and font from the kit's `colors.roles` and `typography`
  blocks. Never hard-code hex values in the generation code — define
  variables from the kit at the top so a kit swap restyles the deck.

### 5. Verify before delivering

**Closed loop for rebuilt slides:** any slide rebuilt from a library
construction spec gets verified mechanically before visual review:

```bash
python scripts/spec_diff.py library/anatomy/<entry>.json out.pptx <slide#> --kit <kit.json>
```

Tier 1 diffs geometry (strict for `preserve` elements, invariants for
`flex`) and verifies colors by kit *role* via the spec's token map — so the
same spec validates any client restyle. Tier 2 checks machine-checkable
design rules (margins, accent-area ≤ ~10%, minimum text size). Fix blockers
and re-run; cap at 3 fix iterations, then surface remaining findings to the
user. Only when clean, do the visual pass below (tier 3: overflow, font
substitution, balance — what XML can't express). Parametric slides have no
target spec: tier 2 + visual pass only.

- Render thumbnails (`pptx` skill's `thumbnail.py`) and inspect every slide:
  overflow, alignment, orphaned placeholders.
- Read the action titles top to bottom — do they tell the story on their own?
- Check footer/page numbers/confidentiality marking on every slide.
- Spot-check contrast pairs against design rule 15.
- Run the AI-tells lint (design rules 20–28): no decorative icons, no
  rounded corners, no gradients, no grids of equal highlight boxes, no
  filler vocabulary. Fix every hit before delivering.
- For data slides, sanity-check charts against rules 11–14; if a chart came
  from client material, run `assess-graphical-excellence` on it.
- For client-facing decks, finish with a full `ey-deck-review` pass — it
  runs these checks systematically and returns severity-ranked findings.

## Restyling an existing deck for a new client

1. Extract or load the new client's kit (`ey-brand-kit`).
2. Template path: move slide content onto the new template's layouts via the
   `pptx` editing workflow. From-scratch path: re-run generation with the new
   kit.
3. Re-verify rules 8 (accent scarcity) and 15 (contrast) — palettes break
   these silently.

## Template library

When the user flags a slide they like ("save this slide", "keep this layout",
"add slide 7 to the library"), follow the capture workflow in
[library/README.md](library/README.md): store the source deck, render a
thumbnail, add an INDEX.md row with why it earned the flag, and offer to
promote it to a named pattern. After delivering any deck, if a slide drew
explicit praise during review, proactively offer to flag it.

When the user flags a **whole deck** for a quality ("I like how this deck
uses headlines", "I like this one's aesthetic"), that's a deck exemplar —
follow the distillation workflow in library/README.md and index it in
[library/EXEMPLARS.md](library/EXEMPLARS.md). Consult EXEMPLARS.md during
step 1 (messaging/structure exemplars) and step 4 (aesthetic exemplars);
exemplars steer choices within the design rules and active kit, never
against them.

## Speed defaults

When the user wants a deck fast and gives no contrary instruction: 16:9,
title + agenda + exec summary + content sections + next steps + appendix,
EY default kit, one pattern per content slide, sources as bottom-left
captions. Ask only about storyline substance, not formatting.
