---
name: excel-to-evidence
description: Turn Excel models and data extracts into deck-ready exhibits with full source traceability — locate the series, reshape it, verify it ties out, draft the so-what, render the chart, and log provenance. Use whenever the user wants slides, charts, or exhibits built from a workbook, model, benchmark file, or survey data, or asks "make a slide from this spreadsheet", or needs numbers in a deck to tie back to a model. The upstream data half of quantitative slides built with ey-deck.
---

# Excel to Evidence

The extraction and tie-out layer between models and slides. The slow,
error-prone step in deck production is going from a 30-tab workbook to the
exhibit that proves a slide title — and the expensive failure is a number on
a slide that nobody can trace back to the model. This skill makes
"workbook → exhibit" one move and makes every exhibit auditable.

Dependencies (same repo): `xlsx` for workbook mechanics, `render-tufte-chart`
for output, `ey-brand-kit` for the chart palette, `ey-deck` for the slide
around the exhibit.

## Workflow

### 1. Locate the series

Map the workbook first (tab names, header rows, units) before hunting for
data. Given the message to prove ("show the cost gap by category vs.
peers"), identify the candidate tab/range. If two tabs could plausibly be
the source — e.g. a raw data tab and a summary tab that disagree — stop and
ask which is authoritative rather than picking silently.

### 2. Extract and reshape

- Aggregate to the level the message needs, not the level the model keeps.
- Sort to the message (design rule 12); time keeps natural order.
- Carry units explicitly from the source headers ("$mm", "FTEs"). If the
  source doesn't state units, that's a question for the model owner, not a
  guess.
- Currency across multiple years gets deflated to real terms
  (`assess-graphical-excellence/scripts/deflate.py`) and labeled
  "real <base-year> <currency>".

### 3. Tie out — zero tolerance

Before anything renders:

- Recompute totals/subtotals from the extracted rows; they must match the
  workbook's own totals exactly.
- Cross-check the headline number against any other tab that states it
  (summary tabs, dashboards). A discrepancy is a **blocker finding to
  report**, never something to average over or pick the prettier value from.
- Note workbook health issues encountered (formula errors, hardcodes inside
  formula ranges) even when they don't touch the extracted range — the model
  owner needs to know.

### 4. Draft the so-what

Write the candidate action title the data actually supports, with the
number in it: "Indirect spend drives 60% of the cost gap to peers."

**Integrity rule:** if the user wanted the slide to say X and the data
supports Y, say so explicitly and propose the title the data supports. A
deck title the model can't back is a blocker (`ey-deck-review` severity
language), and it's cheaper to surface now than in front of the client.

### 5. Render

Through `render-tufte-chart`, genre chosen by data shape (its Part C
table): one series over time → line, category comparison → highlighted bar,
bridge → waterfall (hand-built per the `ey-deck` pattern), ≤ 20 numbers →
consider a table instead of a chart. Colors from the active kit's
`roles.chart`; the bar that proves the title gets `accent`, the rest
`muted`.

### 6. Log provenance

Every exhibit carries two records:

- **On the slide/page:** source note, bottom-left, caption size:
  `Source: <workbook>, '<tab>'!<range>, extracted <date>; <transformations>`.
- **In the evidence log** (`evidence-log.md` next to the deck): one row per
  exhibit so QA can tie out the whole deck in one pass:

| Exhibit | Slide | Workbook | Tab!Range | Transformations | Headline value | Tied out |
|---|---|---|---|---|---|---|

"Transformations" lists everything done to the raw cells (aggregated by
region, deflated to 2024 USD, sorted desc). An exhibit whose row can't be
filled completely doesn't ship.

## When the model changes

Models change mid-engagement. On "the model was updated, refresh the
exhibits": re-run extraction for every evidence-log row pointing at that
workbook, diff headline values old → new, report which slides' titles are
affected — a changed number can invalidate an action title, and that's a
storyline edit, not just a chart swap.
