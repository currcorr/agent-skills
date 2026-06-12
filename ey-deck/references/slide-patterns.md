# Consulting Slide Pattern Library

Each pattern: when to use it, its layout, and rendering notes. All colors and
fonts come from the active brand kit's `roles` — patterns reference tokens
(`accent`, `muted`, `chart[0]`…), never hex values. Design rules
(`ey-brand-kit/references/design-rules.md`) apply to all patterns.

## Framing patterns

### Executive summary
- **Use:** slide 2 of every deck.
- **Layout:** governing thought as a bold banner across the top third; below,
  3–5 numbered support statements, each one line + one proof point.
- **Notes:** this slide is written last, after the evidence exists.

### Agenda / section tracker
- **Use:** agenda after exec summary; repeat as tracker at each section break.
- **Layout:** numbered section list; on tracker repeats, current section in
  `accent` treatment, completed sections in `muted`.

### Section divider
- **Use:** every section start. Kit's `section` layout if templated,
  otherwise `backgroundDark` full-bleed with the section assertion in
  `textOnDark`.

### Next steps / decisions
- **Use:** last content slide, always.
- **Layout:** three-column table — action, owner, date. Decisions needed get
  an `accent` marker. No deck ends without owners and dates.

## Comparison patterns

### 2x2 matrix
- **Use:** positioning options/vendors/initiatives on two independent
  dimensions.
- **Layout:** square plot area left or center, axis labels at ends, items as
  labeled dots; recommended quadrant tinted with `accent` at low opacity.
  Callout box right with the so-what.
- **Notes:** ≤ 12 items; if both axes are scores you invented, say how in the
  source note.

### Harvey-ball comparison table
- **Use:** options scored against criteria (vendor selection, build-vs-buy).
- **Layout:** criteria as rows, options as columns, 0/¼/½/¾/full circles
  (render as pie-slice shapes or Unicode ◔◑◕●). Recommended option's column
  header in `accent`. Total/recommendation row at bottom.
- **Notes:** ≤ 7 criteria, ≤ 5 options. Weight criteria explicitly if they
  aren't equal.

### Before/after (from–to)
- **Use:** target operating model, process redesign.
- **Layout:** two columns ("Today" muted, "Future" accented) with arrow
  between; 4–6 paired rows, parallel grammar in each pair.

## Quantitative patterns

For any actual chart, use the Tufte toolkit in this repo:
`render-tufte-chart` to build it (its scripts emit clean SVG — convert to
PNG/EMF for slides), `assess-graphical-excellence` to QA charts inherited
from client material. The patterns below define the slide around the chart;
the chart itself obeys design rules 11–14.

### Waterfall
- **Use:** bridging two numbers (cost baseline → target, EBITDA bridge).
- **Layout:** start and end bars in `primary`, increases `positive`,
  decreases `negative`, connector lines in `border`. Label every bar with
  its value; title states the bridge's message.

### KPI dashboard
- **Use:** status reporting, value tracking.
- **Layout:** grid of metric cards — big number, label, delta vs. target
  with directional marker. RAG only via `positive`/`negative`/`muted` roles,
  paired with ▲▼ glyphs (rule 16: never color alone).
- **Notes:** ≤ 8 cards; each needs a target or trend or it's trivia.

### Highlighted-bar chart
- **Use:** any single-series comparison proving the title.
- **Layout:** bars sorted by value, the bar that proves the title in
  `accent`, all others `muted`. Direct labels, no legend, no y-axis if
  labels carry the values.

### Value driver tree
- **Use:** showing where value comes from — bridging a headline KPI to the
  initiatives that move it.
- **Layout:** KPI at far left (e.g. EBITDA uplift), decomposed left-to-right
  into drivers with +/× operators on the connectors; leaf nodes name the
  initiative and its sized value. The biggest lever gets the `accent`
  treatment; connectors in `border`.
- **Notes:** values at each level must sum/multiply correctly — check the
  arithmetic before rendering.

### Issue / hypothesis tree
- **Use:** structuring a problem at engagement start, or showing what's been
  proven by readout time.
- **Layout:** root question at left, MECE branches right across 2–3 levels.
  In hypothesis mode, mark each leaf confirmed/refuted/testing with
  `positive`/`negative`/`muted` plus a glyph (✓ ✗ …) per rule 16.

## Time patterns

### Roadmap / horizon plan
- **Use:** implementation plans, transformation waves.
- **Layout:** time across the top (quarters/halves), workstreams as rows,
  initiatives as rectangular bars in `chart` colors by workstream; milestones
  as diamonds in `accent`. "Today" as a vertical line.
- **Notes:** ≤ 6 workstreams; detail plans go to appendix, not into smaller
  fonts.

### Maturity ladder
- **Use:** current-vs-target capability maturity.
- **Layout:** 4–5 ascending steps left to right; "today" marker in `muted`,
  "target" in `accent`, with the gap labeled.

## Structure patterns

### Framework / pillars
- **Use:** explaining an approach or operating model.
- **Layout:** 3–5 pillar boxes under a roof banner (the objective), a
  foundation bar beneath (enablers). One line + 2–3 sub-bullets per pillar.
- **Notes:** the roof states an outcome, not "Our framework".

### Process flow
- **Use:** current/future state processes, methodologies.
- **Layout:** chevrons left to right, ≤ 6 steps, step name + one descriptor;
  pain points or changes flagged beneath in `negative`/`accent` markers.

### RACI matrix
- **Use:** clarifying who does what in a new operating model or program.
- **Layout:** activities as rows, roles as columns, single letters R/A/C/I in
  cells; A cells get the `accent` treatment. Exactly one A per row — if a row
  has zero or two, that's a finding, not a formatting problem.
- **Notes:** ≤ 12 activities per slide; group by phase and split if longer.

### Risk heatmap
- **Use:** risk registers, steering-committee risk decisions.
- **Layout:** likelihood × impact grid (3x3 or 5x5) with a quiet tint ramp —
  `muted` at low, `negative` only in the top-right corner band, never a
  traffic-light rainbow. Risks as numbered dots; a table beside the grid
  lists number, risk, mitigation, owner. Position carries the data (rule
  16); the tint is secondary.

### Quote / voice of the customer
- **Use:** interview or survey findings, change-readiness evidence.
- **Layout:** 1–3 verbatim quotes in large body type with attribution by
  role (never name), plus the pattern stat beside them ("14 of 20
  interviewees raised this"). No giant decorative quotation-mark glyph —
  that's an AI tell (rule 20); a thin `accent` rule above each quote is
  enough.

### Org / governance chart
- **Use:** target org, program governance.
- **Layout:** boxes by level, reporting lines in `border`; new/changed roles
  in `accent` outline. Decision bodies get meeting cadence in the box.

## Pattern selection cheat sheet

| The slide's message is about… | Pattern |
|---|---|
| The whole story | Executive summary |
| Which option wins | Harvey-ball table or 2x2 |
| How big / what drives a number | Waterfall or highlighted-bar |
| How we get there | Roadmap |
| What changes | Before/after |
| How we'll work | Framework, process flow, governance, RACI |
| Are we on track | KPI dashboard |
| What's driving the problem | Issue / hypothesis tree |
| Where the value is | Value driver tree |
| What could go wrong | Risk heatmap |
| What people told us | Quote / voice of the customer |
| What we need from you | Next steps / decisions |

Before reaching for a generic pattern, check the template library
([../library/INDEX.md](../library/INDEX.md)) for a flagged real slide that
already solves the same problem — copying a proven slide beats rebuilding it.
