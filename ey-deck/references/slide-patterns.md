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
| How we'll work | Framework, process flow, governance |
| Are we on track | KPI dashboard |
| What we need from you | Next steps / decisions |
