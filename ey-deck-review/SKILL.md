---
name: ey-deck-review
description: Automated partner-style red-pen review of a finished deck — scores storyline, design rules, AI tells, and charts, returning page-by-page markup with severities. Use whenever the user asks to review, QA, critique, red-pen, or pressure-test a deck or presentation, asks "is this ready to send?", or before any deck built with ey-deck goes to a client or partner. Works on any .pptx, not just decks this toolkit built.
---

# EY Deck Review

A partner's red pen, systematized. The rubrics live in the toolkit's
existing references — this skill orchestrates them into a structured review.
It does not duplicate the rules; every finding cites its source rule so the
fix is unambiguous.

Rubric sources (read all three before reviewing):
- `ey-deck/references/storyline-guide.md` — argument structure, action titles
- `ey-brand-kit/references/design-rules.md` — layout, color, charts (rules
  1–19), AI tells (rules 20–25)
- `assess-graphical-excellence` — chart-level critique

The review is the deliverable. Report findings; don't edit the deck unless
the user asks. Offer to apply fixes at the end, batched by severity.

## Workflow

### 1. Ingest

- Thumbnails for every slide (`pptx` skill's `thumbnail.py`) — most layout
  findings require *seeing* the slide.
- Text extraction (`python -m markitdown deck.pptx`) for titles and word
  counts.
- Ask which kit/client the deck targets if it isn't obvious; contrast and
  accent findings depend on the kit.

### 2. Storyline pass (the one partners care about most)

Extract every slide title in order and read them as a standalone narrative.

- Does the title sequence make the full argument? (storyline guide: action
  title test)
- Is each title an assertion, not a topic label? Rewrite every weak title in
  the findings — a review that says "title is weak" without offering the
  fixed sentence is half a review.
- Pyramid check: governing thought up front? Sections MECE? Evidence under
  the right section?
- Does the deck end with owned, dated next steps?

### 3. Slide-by-slide pass

For each slide, against design rules 1–19: body text over ~30 words,
misalignment, inconsistent furniture (footers, page numbers, confidentiality
marking), accent overuse (rule 8), contrast failures (rule 15),
color-only encoding (rule 16).

### 4. AI-tells lint

Rules 20–25 explicitly: decorative icons, rounded corners, gradients/neon,
highlight-box grids, uniform layout rhythm, AI writing register. For the
writing register, run the extracted deck text through the `humanizer`
skill's detection patterns (its 24-pattern catalog is the authority;
skip its voice-injection guidance — design rule 25 scopes it). Quote the
offending text/element per finding.

### 5. Chart pass

Route every data exhibit through `assess-graphical-excellence` (lie factor,
chartjunk species, genre fit). Summarize its verdicts into the findings
table rather than pasting full assessments.

### 6. Report

```
## Verdict: <ready | ready after blockers | needs rework>

## Scorecard
| Dimension | Score /10 | One-line basis |
| Storyline | | |
| Design & layout | | |
| Charts | | |
| AI-tells lint | pass/fail | |

## Findings
| # | Slide | Severity | Finding | Rule | Fix |
```

Severities:
- **Blocker** — would embarrass us in front of the client: broken numbers,
  misleading chart, missing confidentiality marking, contrast failure, a
  title the evidence doesn't support.
- **Should-fix** — a partner would mark it: weak title, density, accent
  overuse, AI tell.
- **Polish** — alignment nudges, wording.

Order findings by severity, then slide number. End by offering to apply
fixes (blockers first), and to flag any slide that reviewed exceptionally
well into the template library (`ey-deck/library/`).
