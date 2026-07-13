# Adobe-Style Design System

A high-fidelity, Adobe/Spectrum-2-styled design system for building proposal
websites. Self-contained: no build step, no framework, no dependencies —
open `design-system/index.html` in any browser.

**Not an Adobe product.** Styled after Adobe's public design language
(Spectrum 2); contains no Adobe logo or identity. Token values are verified
against Adobe's open-source `@adobe/spectrum-tokens` package — see
`research/tokens-inventory.md` for per-value provenance.

## What's in the box

| Path | What it is |
|---|---|
| `design-system/index.html` | **Start here** — the living style guide: every component, every state, light/dark theme toggle |
| `kit/tokens.css` | The contract: all colors, type, spacing, radii, shadows, motion as CSS custom properties (light + dark + reduced-motion) |
| `kit/adobe.json` | Brand kit summary (ey-brand-kit schema) — roles, fonts, usage notes |
| `design-system/components/*.html` | Six source fragments: buttons, cards, hero, navigation, data, interactive |
| `design-system/motion.md` | Motion spec: durations, easings, choreography, reduced-motion strategy |
| `design-system/craft-rules.md` | Anti-AI-tell rules — 10 banned patterns + review checklist |
| `design-system/build_gallery.py` | Rebuilds index.html after editing fragments/tokens (`python3 build_gallery.py`, stdlib only) |
| `research/` | Verified token inventory, design-rules brief, raw Spectrum JSON |
| `qa/screenshots/` | Rendered proof: light/dark/mobile captures |

## Building the proposal site from this

1. **Copy `kit/tokens.css` in verbatim** and link it first. Everything else
   consumes it. Never restate a color/duration as a literal — if a token is
   missing, add it to tokens.css.
2. **Lift components from the fragments.** Each `components/*.html` file is
   `<style>` + markup + optional `<script>`, scoped by class prefix
   (`adb-btn`, `adb-card`, `adb-hero`…). Copy the blocks you need; they
   don't depend on the gallery shell.
3. **Follow the three rule docs** — `research/design-rules.md` (layout,
   red rationing, type treatment), `design-system/motion.md` (what moves,
   how fast), `design-system/craft-rules.md` (what never to ship).
4. **Page skeleton:** use the `.adb-section` / `.adb-container` shells from
   `components/navigation.html` for section rhythm; hero → content sections
   → CTA band → footer is the intended composition.
5. **Theme:** pages are light-first. Dark mode works automatically
   (`prefers-color-scheme`) plus explicit `data-theme="light"|"dark"` on
   `<html>`; the theme-toggle component in `components/interactive.html`
   handles switching + persistence.

## Photography

Adobe's scroll experience uses real photography as section backdrops. The
`adb-photosec` component (see the gallery's Photo Sections demo) provides a
full-bleed *pinned* backdrop (content scrolls over a fixed photo) and a
rounded photo panel. Slots take a real `<img>` (object-fit cover) and ship
with a clearly-tagged placeholder — **swap in licensed photography before
shipping**; rules in `research/design-rules.md` §3b (scrims, rhythm,
reduced-motion fallback).

## Fonts

Adobe Clean is proprietary, so the system uses **Source Sans 3** and
**Source Code Pro** — Adobe's own open-source faces. The gallery loads them
from Google Fonts; offline you get the system fallback stack. For a
production site, self-host the woff2 files and keep the same
`--font-sans`/`--font-mono` names.

## The five rules that make it read as Adobe

1. Red (`#EB1000`) in at most 1–2 places per viewport — CTA, small badge,
   or one emphasized headline word. Never backgrounds, body text, or fills.
2. White/near-white surfaces, near-black text; dark sections are a
   deliberate accent (~1 in 4–6 sections) plus the footer.
3. Headlines extrabold-to-black, tight negative tracking, tight
   line-height, in generous whitespace (80–120px section padding).
4. Pill-shaped primary CTAs; rounded corners on all media.
5. Content capped at 1280px; body copy columns at 672px.

Note: `#EB1000` (corporate red) and `#F03823` (Spectrum UI *negative* red)
are different colors with different jobs — never swap them.
