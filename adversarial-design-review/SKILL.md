---
name: adversarial-design-review
description: Adversarial fresh-eyes review that gates a rendered design (HTML page, site, artifact, interactive brief) before it ships — hunts AI design tells, verifies content + functional accuracy, applies measured gates (computed contrast on actual hexes, 375px signature test, JS executed against a mock DOM, crescendo check). Use when asked to review/gate/pressure-test a built design, to check whether something 'looks AI-generated', or as the mandatory final pass after frontend-design/ey-site/canvas-design/interactive-brief. For .pptx use ey-deck-review; for chart critique use assess-graphical-excellence; for mockup usability use design-critique.
license: MIT
---

# Adversarial Design Review

The final gate before a rendered design reaches the person who asked for it. The
reviewer's job is **not** to approve — it is to assume the design is flawed and
prove it. Ship nothing that has not returned a per-sample **PASS**.

Sibling authority for decks/sites: `ey-brand-kit/references/design-rules.md`
rules 20–28 cover the same tells from the client-deliverable side; this skill is
the executable gate for anything rendered.

## The gate rule

- **Reviewer ≠ builder.** A fresh adversary who did not build the sample runs the
  passes. Someone reviewing their own work grades on a curve; the tells they
  chose are invisible to them.
- **Assume it's flawed and hunt.** "Prove it's broken," not "confirm it's fine."
- **Two lenses where available.** A design adversary (aesthetics, tells,
  faithfulness) and a cross-model adversary (correctness, edge cases, the
  send-back mechanism). Different blind spots — both missed a bordered callout
  box on the Masters sample; running both narrows the gap.

## Three passes — any FAIL blocks the ship

### Part A — hunt AI design tells

Walk every item in [`references/ai-tells-checklist.md`](references/ai-tells-checklist.md)
(23 tells, 1–23). Any hit is a FAIL until fixed. A tell is only legitimate if the
brief explicitly asked for it. Report each hit by number with the exact fix.

### Part B — accuracy (verify, do not vibe)

- **Real-site fidelity.** If the brief references a specific site (Economist,
  Bloomberg, Linear, Palantir, FT, Masters), does it capture *that* site's DNA,
  not a generic version? Name what's right and what's off versus the real thing.
- **Content accuracy.** Facts, numbers, and attributions are correct (e.g.
  Bridgewater not BlackRock; no fabricated stats); every source URL is real;
  plain-English names only, no internal codes leaking into copy.
- **Functional accuracy — RUN the JS, don't read it.** Execute the interaction
  against a mock DOM: swiper, reactions on/off, localStorage resume, sanitized
  payload, iOS `sms:&body=` send, clipboard fallback. String-coercion and render
  bugs only appear when executed. Self-contained (zero external refs/fonts).
  Progressive enhancement (readable with JS off). No surviving placeholders.

### Part B+ — measured gates (report the numbers)

- **Compute contrast on the actual hexes.** Small text/labels ≥ 4.5:1, large
  ≥ 3:1. Report the ratios. "Premium muted" palettes fail this constantly
  (antique-gold on cream measured 2.65:1).
- **Signature element at 375px.** Does the memorable device (board, ticker,
  leaderboard, price sheet) hold its form on a phone, or wrap/overflow into a
  generic table? Test it at width, not in your head.
- **Crescendo marked.** Is the single most important element (the decision) made
  visually distinct, or lost among equal-weight peers?

## Verdict format (per sample)

```
PASS | FAIL
Tells found: #<n> — <what> — <exact fix>   (Part A)
Accuracy:    <failure> — <exact fix>        (Part B)
Measured:    contrast <ratio>, 375px <hold/break>, crescendo <marked/lost>  (Part B+)
```

Only PASS samples go to the requester. **Re-review after fixes** — a fix often
introduces a new tell (dead CSS from a clone, a fresh em-dash cluster). The gate
runs again on the corrected sample, not once.
