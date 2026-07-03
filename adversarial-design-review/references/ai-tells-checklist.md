# AI design tells — the 23-item hunt list

Load this during Part A of `adversarial-design-review`. Any hit is a FAIL until
fixed; a tell is only legitimate when the brief explicitly asked for it. Report
each by number with the exact fix.

Deck/site sibling: `ey-brand-kit/references/design-rules.md` rules 20–28 cover
the same ground for client decks and sites — this list is the executable version
for any rendered design.

## Layout, color, and surface

1. **The three slop clusters.** (a) warm cream + high-contrast serif + terracotta;
   (b) near-black + a single acid-green/vermilion accent; (c) broadsheet
   hairline-rules + zero-radius + dense newspaper columns. Legit only if the brief
   asked for it.
2. **Default accents.** Generic blue / indigo / violet / purple; a lone "acid"
   accent on dark. Is the accent a choice *for this subject*, or a default?
3. **Gradients.** Purple→blue gradients, gradient text, gradient buttons/hero glows.
4. **Elevation everywhere.** Generic soft drop-shadows on every card; uniform
   "material" elevation.
5. **Radius everything.** Everything rounded 12–16px; pill-shaped everything.
6. **Glassmorphism / backdrop-blur** used decoratively.
7. **Emoji as UI** (in headings, buttons, section markers).
8. **The hero cliché.** Big number + small label + gradient accent (the named
   template answer).
9. **Centered-everything / perfect symmetry** with no tension or hierarchy.
10. **Type has no personality.** Inter/system-only, no deliberate display face, no
    real pairing.
11. **Identical evenly-spaced card grid.** No rhythm, no variation where content
    differs.
12. **"01 / 02 / 03" numbering** when the content is not a real sequence.
13. **Over-animation.** Fade-in-on-scroll everywhere, hover-scale on everything,
    gratuitous transitions.
14. **Filler / marketing copy.** "Empower / Seamlessly / Unlock / Elevate"; vague
    system-named labels; anything not in the interface's plain voice.
15. **Rainbow accents with no system;** inconsistent/ad-hoc spacing (not a scale).
16. **Generic decorative icons** (feather/heroicons sprinkled for vibes).
17. **Dark mode used *as* the design idea** rather than a considered choice.
18. **The "AI SaaS landing page" gestalt.** Would the whole thing be mistaken for a
    generic template?

## Copy and systems tells

19. **Copy AI-fingerprints.** Em-dash overuse (count them — >~1 per 150 words is a
    tell), a stock flourish repeated across the page, headline monotony (same
    "Colon: sentence" or same structure 3+ times), middot label strings
    ("X · Y · Z"). The `humanizer` skill is the authority for the writing-register
    tells — run its detection patterns over all copy rather than restating them
    here.
20. **Spacing/tracking is ad-hoc, not a token system.** >~4 distinct
    letter-spacing or margin values doing the same job = per-element eyeballing.
    Define ~3 tracking tokens and reuse.
21. **Dead/borrowed CSS from a cloned sibling.** Rules that don't apply, state
    styles that collide (a `.on.bad` that never fires, a border-style that clashes
    with `.on`). Grep for unused selectors; delete what doesn't apply.
22. **Bordered/tinted "callout" or "info" boxes.** A rounded rectangle with a 1px
    border + a background tint used as an aside/note/callout/status box is a dead
    AI tell — use a hairline rule or inline typeset treatment instead. Hunt every
    bordered+tinted box that isn't a primary content card (both adversaries missed
    the Safari-note and reactions boxes on the Masters sample).
23. **The machine-facing output is unpolished.** Truncated/mid-word labels in a
    copied or sent payload, codes leaking into it. Anything a human sees — even a
    copied string — is design surface; hand-write short labels.
