# Goal loops and loss-function development for deliverables

How to use `/goal` (Claude Code and Codex both have it) with this toolkit.
The short version: goals work here because the toolkit has machine-checkable
verifiers — `spec_diff.py` exit codes, lint verdicts. A goal without an
instrument is a vibe; ours have instruments.

## Two kinds of loop — don't confuse them

1. **Spec-driven (inner loop):** a finite finish line. "Build the deck;
   verifier passes." Most deliverable work is this. `/goal` just saves you
   prompting each fix round.
2. **Loss-function (outer loop):** a target to descend toward across many
   cycles, scored against an eval set too big to memorize. Use for building
   *capability* (e.g. the snippet normalizer), not for one deliverable.

## Ready-to-use goal conditions (inner loop)

- Deck build:
  `/goal draft.pptx built per the approved outline; spec_diff exits 0 for every slide rebuilt from a library fixture; ey-deck-review reports no blockers — or findings surfaced after 3 fix attempts`
- Client restyle:
  `/goal deck restyled: spec_diff clean with --kit <client>.json on all fixture slides; accent-share and min-text-size checks pass — or findings surfaced after 3 attempts`
- Site build:
  `/goal site.html contains all outline sections, passes the AI-tells lint (design rules 20-28), no overflow at 390px and 1440px`
- Evidence refresh:
  `/goal every evidence-log row re-tied against the updated workbook; changed headline values and affected slide titles listed`

Always include the escape hatch ("or findings surfaced after N attempts") —
an impossible fixture must end in a report, not an infinite burn.

## Loss-function anatomy for this toolkit (outer loop)

Per LFD practice: target, constraints, instruments, forced entropy.

**Target.** Big enough that enumeration doesn't pay, and blind: held-out
slides/decks the agent never sees during the run, scored only between
cycles. The template library (fixtures + craft notes + kits) is the eval
set — it is also the moat: anyone can clone a deck skill; nobody else can
score against your flagged ground truth. Every flag grows the eval.

**Constraints (and their #1 violation).** Wall-clock and token budgets;
stdlib-only; and above all: **the verifier and the fixtures are
read-only.** The cheapest way to make spec_diff pass is to edit spec_diff
or the fixture. Fence it: fixtures + verifier in a directory the run
cannot write, hash-checked at scoring time.

**Instruments.** Have: spec_diff (exit codes, severities), rule checks
(accent share, margins, text size), thumbnails. Missing (build before
serious outer loops): a **pixel-diff tool** for render comparison — LLM
judges approve 12px spacing errors; only a pixel diff catches them — and
per-cycle time/token accounting the agent can query.

**Forced entropy.** Require an iteration log (hypothesis → expected failure
→ result per cycle) and an overfit reflection each cycle: "am I
generalizing, or memorizing the eval?" If the metric stalls, the next cycle
must change approach, not turn the same knob harder.

## Known cheat modes in this domain, and fences

| Cheat | Fence |
|---|---|
| Edit verifier/fixture tolerances to pass | Read-only + hash check at scoring |
| Delete hard elements instead of handling them | Already fenced: missing preserve-elements are blockers |
| Per-slide special cases keyed to filenames | Held-out blind slides; overfit reflection |
| Optimize to the lint, ship sterile slides | Out of scope by design: loops verify fidelity and rules; taste stays human (library flags) |

## The first real outer-loop candidate: the snippet normalizer

The agreed next build (owned by the pattern-miner side, callable by all) is
a textbook LFD run:

- **Eval:** N flagged slides × M destination templates/kits. Loss = total
  spec_diff findings (weighted by severity) on normalize round-trips, plus
  the acceptance test: same-canvas round-trip must be CLEAN.
- **Blind:** hold out a third of the slides; score between cycles only.
- **Constraints:** stdlib only; may not modify slide_anatomy/spec_diff or
  any fixture; token + wall-clock budget.
- **Goal:** `/goal normalize_snippet.py achieves zero blockers across the
  visible eval; then report held-out score — do not optimize against
  held-out items`.

## Cautions

- Conditions must be exit codes and file checks — never "looks good" (the
  evaluator either loops forever or passes slop).
- Tier 3 stays advisory: a verifier-clean deck still gets human eyes before
  any client sees it.
- Sit with the first cycle of any long run; confirm the harness is actually
  being used. Then walk away.
- Client data in unattended loops follows the same confidentiality rules as
  any automation (see automations.md guardrails).
