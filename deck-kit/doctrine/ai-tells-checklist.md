# Adversarial design review — AI-tell + accuracy checklist

**Gate rule:** no design sample reaches the user until a **fresh adversary** (an agent or session that did NOT build it) has run this checklist and returned a per-sample **PASS**. The adversary's job is to *assume the sample is flawed and prove it* — not to approve. If you can run two lenses (a design-eye pass and a second model), do: different models have different blind spots. The deck system in this kit survived four rounds of this gate; assume your defaults are the failure modes listed here.

## Part A — Hunt for AI design tells (any hit = FAIL until fixed)
1. **The 3 slop clusters:** (a) warm cream + high-contrast serif + terracotta; (b) near-black + a single acid-green/vermilion accent; (c) broadsheet hairline-rules + zero-radius + dense newspaper columns. Legit only if the brief *asked* for it. (This kit's default brand deliberately steers clear of (a): white ground not cream, oxblood not terracotta — that distinction is the point.)
2. **Default accents:** generic blue / indigo / violet / purple; a lone "acid" accent on dark. Is the accent a *choice for this subject* or a default?
3. **Gradients:** purple→blue gradients, gradient text, gradient buttons/hero glows.
4. **Elevation-everywhere:** generic soft drop-shadows on every card; uniform "material" elevation.
5. **Radius-everything:** everything rounded 12–16px; pill-shaped everything.
6. **Glassmorphism / backdrop-blur** used decoratively.
7. **Emoji as UI** (in headings, buttons, section markers).
8. **The hero cliché:** big number + small label + gradient accent.
9. **Centered-everything / perfect symmetry** with no tension or hierarchy.
10. **Type has no personality:** Inter/system-only, no deliberate display face, no real pairing.
11. **Identical evenly-spaced card grid;** no rhythm, no variation where content differs.
12. **"01 / 02 / 03" numbering** when the content is not a real sequence.
13. **Over-animation:** fade-in-on-scroll everywhere, hover-scale on everything, gratuitous transitions.
14. **Filler/marketing copy:** "Empower / Seamlessly / Unlock / Elevate"; vague system-named labels; anything not in the material's plain voice.
15. **Rainbow accents with no system;** inconsistent/ad-hoc spacing (not a scale).
16. **Generic decorative icons** (feather/heroicons sprinkled for vibes).
17. **Dark mode used *as* the design idea** rather than a considered choice.
18. **The "AI SaaS landing page" gestalt** overall — would this be mistaken for a generic template?

## Part A+ — copy & systems tells
19. **Copy AI-fingerprints:** em-dash overuse (count them — >~1 per 150 words is a tell), a stock flourish repeated across the piece, headline monotony (same "Colon: sentence" or same structure 3+ times), middot label strings ("X · Y · Z").
20. **Spacing/tracking is ad-hoc, not a token system:** >~4 distinct letter-spacing or margin values doing the same job = per-element eyeballing.
21. **Dead/borrowed CSS from a cloned sibling:** rules that don't apply, state styles that collide (e.g. a highlight wash that a row-striping tint overwrites every other row, a state combination that never fires). Grep for unused selectors; check every pair of background systems that can hit the same element.
22. **The machine-facing output is unpolished:** truncated/mid-word labels in generated output, internal codes leaking into user-visible text.
23. **Bordered/tinted "callout" or "info" boxes:** a rounded rectangle with a 1px border + a background tint used as an aside/note/callout/status box is a dead AI tell — use a hairline rule or inline typeset treatment instead. (Both adversaries missed this once and a human caught it. Hunt every bordered+tinted box that isn't a primary content element.)

## Part A++ — deck-structural tells (from this system's own gate rounds; see doctrine/design-doctrine.md §3b)
24. **The positional void:** content in the top ~60% of the frame with a framed void below it (bounded by footer/bar furniture). One slide = bug; recurring = the system's signature.
25. **A repeated failure signature of any kind** — the same flaw twice across a deck is itself a tell; fix the generator, not the instances.
26. **Equal boxes for unequal things:** phases of unequal duration as equal-width columns, symmetric grids over asymmetric material. Time gets an axis; spans are drawn proportional to duration.
27. **Frameworks/2x2s that plot nothing:** four captioned quadrants with no plotted position or trajectory is labeled empty space.
28. **Annotations restating the title:** takeaway bars, brackets, gate notes, or callouts that repeat the action title are redundancy in furniture form.
29. **Dishonest geometry:** bar spans, phase widths, and marker positions that don't match their stated values when measured. Measure the pixels against the numbers.

## Part B — Accuracy (any failure = FAIL)
- **Reference fidelity:** if a specific brand/site/style was referenced, does the sample capture THAT source's DNA, not a generic version? Name exactly what's right and what's off vs the real thing.
- **Content accuracy:** every fact, number, and attribution in the content is correct against its stated source; every source cited is real; no fabricated stats; plain-English names, no internal codes.
- **Functional accuracy:** the artifact verified by running it, not reading it — for decks: render it, read the embedded `LAYOUT-OK`/`LAYOUT-FAIL` overflow report, and check the PDF page count matches the slide count. Self-contained (zero external refs/fonts unless deliberately using `type.files`). No surviving placeholders.

## Part B+ — measured, not vibed
- **Compute contrast on the actual hexes** for every small text/label (≥4.5:1) and large (≥3:1). Report the numbers. "Premium muted" palettes fail here constantly.
- **Honest geometry, measured:** for each exhibit, compute where each bar/span/marker SHOULD sit from the stated values and compare against the render.
- **Crescendo marked:** is the single most important element (the decision, the gate, the winner) visually distinct, or lost among peers?

## Verdict format (per sample)
`PASS` or `FAIL` + the specific tells found (Part A/A+/A++ #), the accuracy failures (Part B), and the exact fix for each. Re-review after fixes. Only PASS samples go to the user.
