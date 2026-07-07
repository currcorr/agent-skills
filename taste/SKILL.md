---
name: taste
description: "Curated design-taste reference library for web/HTML artifacts — the additive parts of the 2026 'taste skill' suite (Leonxlnx taste-skill v2, pbakaus/impeccable craft chapters, Emil Kowalski motion standards), vetted and licensed. Load when building or polishing landing pages, portfolios, interactive HTML deliverables, or motion/animation work — the layers deck-kit's doctrine does not cover. NOT a slide skill: for static decks use deck-kit (its doctrine §6 already encodes the deck-relevant extraction of these sources)."
license: "MIT (this router); references carry their upstream licenses (MIT / Apache-2.0) — see attribution table"
---

# Taste — imported craft references for web artifacts

Curated copies of the additive parts of the installable "taste skill" suite
(the 2026 anti-slop ecosystem: tasteskill.dev, impeccable.style,
emilkowalski/skills). Imported 2026-07-07 after a mining pass
(`ops/reviews/deck-craft-upgrade.md` in the vault) extracted the
**deck-relevant** values into `deck-kit/doctrine/design-doctrine.md` §6. What
lives here is what that extraction deliberately left out: the **web-idiom and
motion layers**, which apply to interactive HTML work, not static slides.

## Routing — which authority governs what

| Artifact | Authority |
|---|---|
| Static consulting deck (PDF/pptx idiom) | `deck-kit` doctrine §6 — do NOT import web-isms from here into decks |
| Landing page, portfolio, marketing site | `references/taste-skill-frontend.md` (generation-side) + `adversarial-design-review` (review-side) |
| Product UI / dashboard / app-shell craft | `references/impeccable/*` chapters |
| Motion, easing, micro-interactions (incl. the deck Experience track) | `references/emil/*` |

## References — load on demand, not all at once

**`references/taste-skill-frontend.md`** (1,200 lines — Leonxlnx
`design-taste-frontend` v2). Generation-side anti-slop for landing pages,
portfolios, redesigns. Load when *building* a page from a brief: §0 brief
inference, §2 brief→design-system map, §11 audit-first redesign protocol,
§14 hard pre-flight checklist. Its catalog of empirically-observed LLM
defaults ("production-test tells") complements `adversarial-design-review`'s
23-tell checklist — this one prevents at build time, that one catches at
review time. Do not apply its web-copy absolutes (em-dash ban, never-pure-
white) to decks; the deck doctrine deliberately inverts both.

**`references/impeccable/`** (Paul Bakaus, Apache-2.0) — the five craft
chapters that go deeper than the doctrine's extraction, for product-UI and
site work:
- `typeset.md` — type scales, vertical rhythm, weight contrast, tracking
  bands, optical compensation for light-on-dark.
- `layout.md` — 4pt spacing scale, grouping rhythm, hierarchy dimensions,
  optical alignment, squint test.
- `colorize.md` — tinted neutrals, OKLCH stepping, 60-30-10 by visual
  weight, never-gray-on-color.
- `polish.md` — the distinct final pass: baseline grid, widows/orphans,
  per-element consistency, "a screenshot you didn't read doesn't count".
- `craft.md` — the full shape→direction→build→inspect flow with its
  do-not-compress user gates.
Not copied: impeccable's other 18 command chapters and its deterministic
detector (`antipatterns.mjs`) — the detector is coupled to their npx CLI
engine; the house analog is `deck-kit/deckcheck.py`. Install the real thing
from impeccable.style if you want the CI detector.

**`references/emil/`** (Emil Kowalski, MIT) — the motion layer nothing else
in this repo covers. Load for the deck-kit **Experience track** (interactive
HTML renderer), `interactive-brief`, `ey-site`, or any UI that moves:
- `design-engineering.md` — the philosophy ("unseen details compound",
  cohesion, asymmetric emphasis) + animation decision framework.
- `review-animations.md` + `animation-standards.md` — strict review pass
  with exact durations, cubic-beziers, and frequency tables.
- `animation-vocabulary.md` — named motion patterns to reach for.
Remember the experience-spec's own law still governs deck experiences:
*don't mistake animation for interactivity*.

## What was vetted and skipped (don't re-import)

- **ui-ux-pro-max** (MIT) — 67-style/161-palette CSV lookup DB. Mining
  verdict: product-UI breadth play, least useful of the suite; its two
  transferable ideas (deterministic lookup tables; type floors) are already
  in the doctrine. Skipped.
- **taste-skill's deck-relevant rules** — already extracted into deck-kit
  doctrine §6 (eyebrow/caps budget, hierarchy via weight+color, one palette
  temperature, copy self-audit). Not duplicated here.
- **html2pptx.app** — proprietary SaaS (Terms: all rights reserved; skill
  files carry no license; requires a paid API key). Not copyable into this
  repo. If wanted, install per-machine via the vendor's own installer:
  `npx skills add https://html2pptx.app -a claude-code`.

## Attribution

| Source | Author | License | Copied @ |
|---|---|---|---|
| github.com/Leonxlnx/taste-skill | Leon (@Leonxlnx) | MIT (`references/LICENSE-taste-skill`) | b177427, 2026-07-05 |
| github.com/pbakaus/impeccable | Paul Bakaus | Apache-2.0 (`references/impeccable/LICENSE`) | 7190295, 2026-07-07 |
| github.com/emilkowalski/skills | Emil Kowalski | MIT (`references/emil/LICENSE` — upstream file names Matt Pocock; copied verbatim) | 1274a05, 2026-07-01 |

All copies are unmodified except a provenance header comment at the top of
each file. Upstreams move fast (taste-skill v2 is explicitly experimental) —
re-pull before trusting a rule that seems stale, and read before wiring any
third-party ruleset into client-facing work.
