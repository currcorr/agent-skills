---
name: ey-synthesis
description: Turn raw qualitative inputs — interview notes, workshop outputs, transcripts, survey verbatims, sticky-note exports — into evidence-backed findings and a deck-ready outline. Use whenever the user has interview or workshop material and asks to synthesize, find themes, summarize "what we heard", build a findings readout, or prepare a workshop debrief. This is the upstream half of readout decks built with ey-deck.
---

# EY Synthesis

From "what people said" to "what we found, and how sure we are." Output
plugs directly into the `ey-deck` outline format, so synthesis ends one step
before slides begin.

## Workflow

### 1. Inventory and normalize

Catalog every source: who (role, never name), what format (transcript,
notes, stickies, survey), when. Normalize to one statement per line tagged
with a source ID (`[CFO-1]`, `[WS2-ops]`). Keep verbatims verbatim — the
quotes survive all the way to slides, so don't paraphrase at intake.

Note the denominator now: findings will be quantified as "N of M sources"
and M must be defensible.

### 2. Induce themes bottom-up

Cluster statements into candidate themes from the data — do **not** start
from the hypothesis tree and sort quotes into it; that's confirmation bias
wearing a method's clothes. After clustering, *then* map themes against the
engagement's hypotheses and note which are supported, refuted, or
unaddressed. Refuted hypotheses are findings, not failures — they go in the
readout.

Each theme becomes a finding stated as an assertion (action-title-ready):
"Field teams route around the CRM because data entry costs them selling
time", not "CRM adoption issues".

When testing a candidate finding with the user, use the `grilling`
technique: one question at a time, each with your recommended answer ("I read
this as a process problem, not a tooling one — agree?"). It sharpens a fuzzy
theme into a defensible assertion faster than open-ended prompting.

### 3. Build the evidence table

One row per finding:

| Finding (assertion) | Strength | Sources | Best verbatims (2–3) | Counter-evidence |
|---|---|---|---|---|

- **Strength** = breadth × consistency: "14 of 20 interviewees, all
  regions" is strong; "2 of 20, same team" is an anecdote — label it as one.
- **Counter-evidence is mandatory.** If nobody disagreed, say "none found",
  but look first. A finding that survived disagreement is worth more.
- Single-source findings get flagged, not dropped — they may warrant a
  follow-up conversation rather than a slide.

### 4. Confidentiality pass

Attribute by role only. Strip names, identifiable anecdotes, and anything a
small population makes traceable ("the only female VP said…"). When a
verbatim is too identifying to use, keep the finding and replace the quote
with a pattern statement.

### 5. Deliver

Default outputs, in order:

1. **Findings memo** — the evidence table plus a half-page narrative:
   headline finding, what was confirmed/refuted, surprises.
2. **Deck outline** in the `ey-deck` storyline format — governing thought,
   sections = theme groups, one slide per finding using the
   quote/voice-of-customer pattern with the pattern stat, evidence column
   filled from the table. Hand off to `ey-deck` to build.
3. On request: an interactive findings explorer via `ey-site` — filterable
   by theme/role/strength, quotes behind drill-downs. Worth offering when
   the audience will want to interrogate the evidence.

## Quality bars

- Every finding traceable: assertion → sources → verbatims. If a finding
  can't cite its lines, it's an impression, not a finding.
- Themes MECE before they become deck sections.
- Quantify or qualify everything: "many participants" is banned; "11 of 16"
  or "a minority, concentrated in finance" is the standard.
