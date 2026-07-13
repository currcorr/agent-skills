# Motion Specification — Adobe/Spectrum 2-styled Design System

Status: draft for orchestrator gate (Phase 0). Feeds `kit/tokens.css` (motion tokens)
and `design-system/motion.md`. Written so a component builder can implement without
judgment calls — every rule has an exact value.

## Sources & precedence

1. **Spectrum 2 component tokens** — pulled directly from the `adobe/spectrum-css`
   source (`tokens/custom/global-vars.css`, plus usage across `components/*/index.css`),
   verified via GitHub code search on 2026-07-13 (`spectrum.adobe.com/page/motion/`
   returned HTTP 403 through the environment's proxy and could not be fetched directly;
   the token values below are the actual CSS custom properties Spectrum ships, not a
   paraphrase of the marketing page). This is ground truth for durations, easing curve
   math, and how Adobe's own components wire them up.
2. **`taste/references/emil/*`** — Emil Kowalski's animation standards. Per the task
   brief, **emil wins on every judgment call Spectrum's raw tokens don't make** — i.e.
   when to animate at all, frequency gating, `ease-in` bans, stagger timing, spring
   feel, performance discipline, and reduced-motion behavior. Spectrum ships tokens,
   not a philosophy; emil supplies the philosophy.
3. Where the two genuinely conflict (see §1.3), emil's rule is applied and the
   Spectrum default is noted as "not used here, and why."

---

## 1. Token table

### 1.1 Durations

Verified Spectrum ladder (`--spectrum-animation-duration-*`, values in `tokens/custom/global-vars.css`).
Renamed to system tokens for this kit; component builders use the `--motion-*` names only
— never a raw `ms` literal in component CSS.

| System token | Value | Spectrum source token | Tier | Use |
|---|---|---|---|---|
| `--motion-duration-instant` | `0ms` | `--spectrum-animation-duration-0` | 0 | Reduced-motion target; instant state snaps (focus ring) |
| `--motion-duration-100` | `130ms` | `--spectrum-animation-duration-100` | micro | Button/press feedback, checkbox/radio/switch toggle, color swatches, tooltips, focus-adjacent transitions |
| `--motion-duration-200` | `160ms` | `--spectrum-animation-duration-200` | small | Hover state changes (color, border, shadow), tag/badge, tray exit |
| `--motion-duration-300` | `190ms` | `--spectrum-animation-duration-300` | small-medium | Underlay/scrim exit, dropdown/menu close |
| `--motion-duration-400` | `220ms` | `--spectrum-animation-duration-400` | medium | Dropdowns/selects opening, popovers, card hover lift settle |
| `--motion-duration-500` | `250ms` | `--spectrum-animation-duration-500` | medium | Tray/panel entry, accordion expand |
| `--motion-duration-600` | `300ms` | `--spectrum-animation-duration-600` | medium-large | Underlay/scrim entry, modal-adjacent chrome — **this is the emil UI ceiling (300ms); nothing interactive/UI exceeds this** |
| `--motion-duration-700` | `350ms` | `--spectrum-animation-duration-700` | large | Reserved; not used in this kit's interactive components |
| `--motion-duration-800` | `400ms` | `--spectrum-animation-duration-800` | large | Reserved; not used in this kit's interactive components |
| `--motion-duration-900` | `450ms` | `--spectrum-animation-duration-900` | large | Modal open/close (occasional-frequency component; emil table allows 200–500ms here) |
| `--motion-duration-1000` | `500ms` | `--spectrum-animation-duration-1000` | xl | Ceiling for any single modal/drawer transition |
| `--motion-duration-scroll-reveal` | `550ms` | *(not a Spectrum token — marketing/explanatory tier)* | scroll | Section/card entrance choreography (§3); emil explicitly allows longer durations here |
| `--motion-duration-loop` | `1000ms` | `--spectrum-animation-duration-2000` | ambient | One full cycle of an ambient/looping animation (progress indeterminate, gradient drift) |

**Rule:** UI (anything the user directly operates — buttons, toggles, menus, tooltips)
never exceeds `--motion-duration-600` (300ms), per emil's sub-300ms UI rule. Only
occasional-frequency overlay components (modal, tray) and non-interactive
scroll/ambient motion may go longer.

### 1.2 Easings

Verified Spectrum easing tokens (same source file):

| System token | Cubic-bezier | Spectrum source | Use |
|---|---|---|---|
| `--motion-ease-linear` | `cubic-bezier(0, 0, 1, 1)` | `--spectrum-animation-linear` | Constant-speed motion only: marquees, indeterminate progress, gradient drift |
| `--motion-ease-in-out` | `cubic-bezier(0.45, 0, 0.4, 1)` | `--spectrum-animation-ease-in-out` | Elements already on screen moving from A to B (tabs indicator, drag reposition, layout shifts) — matches the PLAN.md estimate exactly |
| `--motion-ease-out` | `cubic-bezier(0, 0, 0.4, 1)` | `--spectrum-animation-ease-out` | Default entrances for **small, frequent, component-level** motion (buttons, toggles, tags) — the literal curve Spectrum's own button/link/actionbutton CSS ships |
| `--motion-ease-out-strong` | `cubic-bezier(0.23, 1, 0.32, 1)` | *(emil override — not a Spectrum token)* | Entrances for **larger, less-frequent, marketing-weight** motion: hero reveals, scroll-reveal choreography, card entrance on first view. Spectrum's own `ease-out` (`0,0,0.4,1`) is tuned for tiny component transitions and reads as flat/weak at hero scale; emil's standard explicitly calls built-in-strength eases "too weak" and prescribes a stronger custom curve for exactly this case |
| `--motion-ease-spring` | `cubic-bezier(0.34, 1.56, 0.64, 1)` | *(emil override — approximates a subtle spring, bounce ≈0.15)* | Micro-interaction "alive" feel: icon/badge pop-in, magnetic CTA settle, count-up finish tick. Keep to small elements only — never cards/panels/layout-scale motion |
| `--motion-ease-drawer` | `cubic-bezier(0.32, 0.72, 0, 1)` | *(emil, iOS/Ionic-derived)* | Reserved for any future drawer/sheet component |

**Not adopted:** `--spectrum-animation-ease-in`, `cubic-bezier(0.5, 0, 1, 1)`. Spectrum
itself uses this on one internal case (modal confirm-dialog exit fade). Per emil's
non-negotiable standard #3 ("never `ease-in` on UI — it delays the exact moment the
user is watching"), this kit does not use `ease-in` anywhere. All exits use
`--motion-ease-out` or `--motion-ease-out-strong` at a shorter duration than the
matching entrance (see §3 asymmetric timing).

### 1.3 Explicit Spectrum-vs-emil conflicts and the resolution used

| Where they conflict | Spectrum default | Emil rule | Resolution used in this kit |
|---|---|---|---|
| Exit easing on overlays (modal confirm, underlay) | `ease-in` | Never `ease-in` on UI | Use `--motion-ease-out` on exit too, at a shorter duration than entry (asymmetric timing carries the "deliberate exit" feeling instead) |
| Curve strength for large/marketing motion | Component `ease-out` (`0,0,0.4,1`), same curve at every scale | Built-in-strength eases are "too weak"; use a stronger custom curve | New `--motion-ease-out-strong` token added for hero/scroll-reveal scale; Spectrum's native `ease-out` reserved for small component-level motion |
| Spring/bounce feel | No spring tokens in Spectrum CSS | Springs for "alive" elements, bounce 0.1–0.3 | New `--motion-ease-spring` token added, scoped to micro-interactions only |

---

## 2. Interaction motion rules

All values below use tokens from §1. No literal `ms`/bezier values in implementation.

### Hover (gate every rule below behind `@media (hover: hover) and (pointer: fine)`)

| Element | Property | From → To | Duration | Easing |
|---|---|---|---|---|
| Card | `transform`, `box-shadow` | `translateY(0)` → `translateY(-4px)`; resting shadow → elevated shadow (bloom, larger blur/spread, same opacity family) | `--motion-duration-400` (220ms) | `--motion-ease-out` |
| Button (primary/secondary) | `background`, `border-color`, `box-shadow` | resting → hover fill/border tokens | `--motion-duration-100` (130ms) | `--motion-ease-out` — this is Spectrum's literal `basebutton.css` wiring |
| Link / nav item | `color` | resting → hover color token | `--motion-duration-100` (130ms) | `--motion-ease-in-out` — matches Spectrum's `link/index.css` |
| Tag / badge | `background`, `color` | resting → hover | `--motion-duration-100` (130ms) | `--motion-ease-out` |
| Magnetic CTA (decorative, hero only) | `transform` | cursor-follow offset, capped ±8px | spring-driven (JS), not duration-based — see §4 for spring config | `--motion-ease-spring` equivalent if implemented in CSS fallback |

Never animate `width`/`height`/`top`/`left` for a hover lift — always `transform:
translateY()`. Never add hover motion to elements that also appear in a
keyboard-navigated list without also handling `:focus-visible` the same way (state
indication must not depend on pointer-only hover).

### Press / active

| Element | Rule |
|---|---|
| Any pressable element (button, card-as-link, tab, tag) | `transform: scale(0.98)` on `:active`. Duration `--motion-duration-100` (130ms — sits inside emil's 100–160ms press-feedback window), `--motion-ease-out`. Scale must stay in the 0.95–0.98 band (emil "subtle" rule) — this kit standardizes on 0.98 for large elements (cards, buttons ≥ 40px tall) and 0.97 for small elements (icon buttons, tags) so bigger targets don't look like they're deforming. |
| Combined with hover lift | Press overrides hover: `:active` transform wins over the `-4px` hover translate (i.e. `scale(0.98)` applied on top of, not instead of, any existing translate — compose them: `translateY(-4px) scale(0.98)`). |

### Focus

**No animation, ever.** Focus rings snap in at `--motion-duration-instant` (0ms) /
`transition: none`. Rationale: focus is a keyboard-driven, high-frequency,
accessibility-critical state (emil frequency table: keyboard-initiated actions get
"no animation, ever"); any delay between keypress and visible ring is a regression a
screen-reader/keyboard user feels immediately. The one exception is a `box-shadow`
that is already present at 0 opacity and only needs a **color/opacity swap**, which is
still instant (0ms) — not a soft fade-in.

```css
:focus-visible {
  outline: none;
  box-shadow: 0 0 0 2px var(--motion-focus-ring-color, var(--spectrum-focus-indicator-color));
  transition: none;
}
```

---

## 3. Entrance choreography

### Scroll-reveal pattern (sections, cards, list items)

- Initial state: `opacity: 0; transform: translateY(24px);`
- Final state: `opacity: 1; transform: translateY(0);`
- Duration: `--motion-duration-scroll-reveal` (550ms, within emil's explicit
  "marketing/explanatory can be longer" allowance — well above the 300ms UI ceiling
  because this is not an interactive control)
- Easing: `--motion-ease-out-strong` (`cubic-bezier(0.23, 1, 0.32, 1)`)
- Stagger: `80–120ms` between sibling elements in the same group (top of the emil
  30–80ms band, widened slightly because these are large editorial blocks, not list
  rows — use 80ms for tight groups like a 3-stat row, 120ms for spaced groups like
  hero sub-elements)
- **Each element animates once.** Use `IntersectionObserver` with `once: true`
  semantics (unobserve after first trigger) — re-triggering a reveal every time a
  user scrolls past is a frequency violation (this becomes a "tens of times/day"
  motion for anyone scrolling back and forth, which emil's table says to reduce or
  remove).
- Never `scale(0)` for any card/element variant of this pattern — if a reveal
  variant uses scale, start at `scale(0.96)` + opacity, not `scale(0)`.

### Hero load sequence

1. Fires on page load, not on scroll (hero is already in view) — use
   `@starting-style` (or the `data-mounted` fallback) rather than
   `IntersectionObserver`.
2. Order: eyebrow/label → headline (mask-reveal or fade+translateY) → subhead →
   CTA row → supporting visual. Each step staggered `100–150ms` after the previous.
3. Headline: `opacity: 0 → 1`, `translateY(16px) → 0`, `--motion-duration-scroll-reveal`
   (550ms), `--motion-ease-out-strong`. If mask-revealing per word/line, treat each
   line as its own staggered sibling per the scroll-reveal stagger rule (80–120ms).
4. Total sequence budget: keep the full hero choreography under ~1.2s from first
   paint to last element settled, so the page doesn't feel like it's still "loading"
   when a user tries to click the CTA. The CTA button itself must be interactive
   (not `pointer-events: none`) even mid-sequence — never block interaction while
   entrance animation plays (emil: stagger is decorative, never blocking).
5. Ambient red-gradient drift (if used behind the hero) starts concurrently and
   loops per §4 — it does not gate or delay the content choreography.

---

## 4. Continuous / ambient motion rules

### Allowed

- **Slow gradient drift** behind hero/section backgrounds: `background-position`
  animated via `transform: translate()` on a background layer (not the
  `background-position` property itself — that's not GPU-accelerated), `--motion-ease-linear`,
  one full cycle at `--motion-duration-loop` (1000ms) or slower — in practice use
  8–20s per cycle for drift so it reads as ambient, not as an obvious loop. Must
  never change brightness/contrast enough to affect text legibility on top of it.
- **Indeterminate progress indicators**: linear, looping, `--motion-ease-in-out` per
  Spectrum's own `progressbar` token wiring, 1000ms+ per cycle.
- **Idle/skeleton shimmer** on loading placeholders: linear sweep, looping, low
  contrast delta.

### Hard bans

- **No infinite bouncing/pulsing** on any persistent UI chrome (nav items, badges,
  icons) — this is exactly the "it looks cool but the user sees it 100+ times/day"
  case emil's frequency table blocks outright.
- **No parallax that fights scroll direction or scroll velocity** — if a background
  layer moves opposite to or slower/faster than user scroll input in a way that
  makes content feel like it's lagging the pointer/trackpad, remove it. Parallax
  layers must move in the same direction as scroll, at a bounded speed ratio
  (0.5–0.9× of scroll speed for background layers), never inverted.
- **Nothing animates inside body-text reading areas** while a user is plausibly
  reading — no moving backgrounds, no shimmer, no drifting gradients behind or
  overlapping paragraph text/long-form copy blocks. Ambient motion is confined to
  hero backgrounds, section dividers, and decorative chrome outside the text
  measure.
- **No looping animation without a way to stop it** effectively — ambient motion
  must fully respect `prefers-reduced-motion` (§6), which functions as the "pause"
  control for users who need it.
- **No animation tied 1:1 to raw mouse position** without spring smoothing (emil:
  direct mouse-tied values feel artificial) — any mouse-tracking decorative effect
  (magnetic CTA, tilt-on-hover) must interpolate through a spring, not snap to
  cursor coordinates every frame.

---

## 5. Performance rules

1. **Animate `transform` and `opacity` only.** No `width`, `height`, `top`, `left`,
   `margin`, `padding` in any transition/animation/keyframe in this kit. Card hover
   lift, entrance translateY, press scale, stagger — all `transform`. Shadow "bloom"
   on hover animates `box-shadow` (paint-only, not layout — acceptable per emil's
   distinction between layout-triggering and paint-only properties; still prefer
   pairing it with a `transform` change rather than shadow alone so the motion
   reads on the GPU-composited layer).
2. **No `transition: all`.** Every transition/animation names its exact properties.
3. **Don't drive child transforms via a CSS custom property on a shared parent** —
   e.g. a card-grid container must not set `--hover-offset` on itself expecting
   children to read it; each card sets its own `transform` directly. This avoids a
   style-recalc storm across every sibling on one card's hover.
4. **`will-change` discipline:**
   - Apply `will-change: transform` (or `transform, opacity`) only on elements
     about to animate imminently — e.g. add it on `mouseenter`/on
     `IntersectionObserver` entry just before the transition starts, remove it once
     the transition ends (`transitionend`).
   - Never apply `will-change` globally or leave it permanently set on
     always-visible elements (cards at rest, nav items) — it forces a persistent
     compositor layer and costs memory/paint budget for zero benefit while idle.
   - Do not stack `will-change` on more than a handful of concurrently-animating
     elements (e.g. don't set it on all 12 cards in a grid at once "just in case" —
     only the ones actively transitioning).
5. **CSS for predetermined motion, JS/WAAPI for dynamic/interruptible motion.**
   Scroll-reveal, hover, press, stagger = CSS transitions/`@starting-style`.
   Magnetic CTA, drag, anything gesture-driven = WAAPI or a spring library, so it
   stays interruptible and doesn't restart from zero when redirected mid-flight.
6. **No Framer/animation-library shorthand `x`/`y`/`scale` props if a JS animation
   library is ever introduced** — always animate the full `transform` string so the
   browser hardware-accelerates it.

### Canonical IntersectionObserver pattern (scroll-reveal, once-only)

```js
const revealObserver = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    entry.target.style.willChange = 'transform, opacity';
    entry.target.classList.add('is-revealed');
    entry.target.addEventListener('transitionend', () => {
      entry.target.style.willChange = '';
    }, { once: true });
    revealObserver.unobserve(entry.target); // fire once only
  }
}, { threshold: 0.15, rootMargin: '-80px 0px' });

document.querySelectorAll('[data-reveal]').forEach((el) => revealObserver.observe(el));
```

Matching CSS:

```css
[data-reveal] {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity var(--motion-duration-scroll-reveal) var(--motion-ease-out-strong),
              transform var(--motion-duration-scroll-reveal) var(--motion-ease-out-strong);
}
[data-reveal].is-revealed {
  opacity: 1;
  transform: translateY(0);
}
[data-reveal="stagger"] > * { transition-delay: calc(var(--reveal-index, 0) * 100ms); }
```

(`--reveal-index` set per-child inline via `style="--reveal-index: 2"` at markup time —
a static value set once, not updated per frame, so it does not trigger the
"CSS-variable-on-parent recalc storm" emil warns against.)

---

## 6. `prefers-reduced-motion` fallback strategy

Two-layer strategy: CSS token override (covers all transition-based motion
automatically) + JS short-circuit (covers IntersectionObserver/JS-driven motion and
anything that would otherwise re-trigger).

### CSS

```css
@media (prefers-reduced-motion: reduce) {
  :root {
    /* Collapse every duration to effectively-instant. Not literally 0ms:
       a 1ms transition still fires `transitionend`, so JS that depends on
       that event (will-change cleanup, sequencing) doesn't break. */
    --motion-duration-instant: 0ms;
    --motion-duration-100: 1ms;
    --motion-duration-200: 1ms;
    --motion-duration-300: 1ms;
    --motion-duration-400: 1ms;
    --motion-duration-500: 1ms;
    --motion-duration-600: 1ms;
    --motion-duration-700: 1ms;
    --motion-duration-800: 1ms;
    --motion-duration-900: 1ms;
    --motion-duration-1000: 1ms;
    --motion-duration-scroll-reveal: 1ms;
    --motion-duration-loop: 1ms;
  }

  /* Belt-and-suspenders: kill transform-based movement outright, keep
     opacity/color (emil: reduced motion means gentler, not zero — comprehension-aiding
     fades stay, movement goes). */
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
  }

  [data-reveal] {
    transform: none !important; /* no translateY entrance; opacity fade still runs at 1ms */
  }

  .hover-lift:hover,
  .press-scale:active {
    transform: none !important; /* no lift, no press-scale movement */
  }

  .ambient-drift,
  .marquee,
  .parallax-layer {
    animation: none !important;
    transform: none !important;
  }
}
```

This mirrors Spectrum's own approach (their Storybook `reduce-motion` decorator sets
every `--spectrum-animation-duration-*` token to `0ms` under a reduced-motion state) —
this kit uses `1ms` instead of `0ms` specifically so dependent `transitionend`
listeners still fire (see JS layer below).

### JS

```js
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

function applyRevealState(el) {
  el.classList.add('is-revealed'); // final state immediately, no transition class dance
}

if (prefersReducedMotion.matches) {
  // Short-circuit: make everything visible immediately, skip observing entirely.
  document.querySelectorAll('[data-reveal]').forEach(applyRevealState);
} else {
  // ... normal IntersectionObserver setup from §5 ...
}

// React to a live OS-level toggle mid-session (rare, but don't leave a stale state).
prefersReducedMotion.addEventListener('change', (e) => {
  if (e.matches) document.querySelectorAll('[data-reveal]').forEach(applyRevealState);
});
```

Rules this encodes:

- Everything that would have been hidden pre-reveal (`opacity: 0`) becomes visible
  immediately — content is never gated behind motion that's been turned off.
- Transitions collapse to ~1ms, not deleted outright, so any code relying on
  `transitionend` (the `will-change` cleanup in §5) keeps working.
- Observers **short-circuit**: under reduced motion, skip
  `IntersectionObserver.observe()` entirely and set final state synchronously,
  rather than letting the observer fire and run a 1ms transition on every element —
  cheaper and removes any chance of a flash.
- Ambient/looping motion (gradient drift, marquee, parallax) is fully disabled, not
  slowed — emil's "gentler, not zero" applies to comprehension-aiding transitions
  (fades, color), not to decorative ambient loops that serve no functional purpose.

---

## 7. Motion review checklist (10-point, derived from `taste/references/emil/review-animations.md`)

Use this to gate every component/section before it ships. A single "no" is a block
unless justified in writing.

1. **Justified.** Does this animation answer "why does it animate" — spatial
   consistency, state indication, feedback, explanation, or preventing a jarring
   snap? If the only answer is "it looks cool" and the element is seen often, delete
   it.
2. **Frequency-appropriate.** Is anything animating on a keyboard-initiated or
   100+/day action (nav clicks, keyboard shortcuts)? If yes, remove the animation
   entirely — no exceptions.
3. **No `ease-in` on UI.** Grep the diff for `ease-in` (not `ease-in-out`) on any
   interactive element. Any hit is a block; swap to `--motion-ease-out` (or
   `-strong`) plus asymmetric timing if the "deliberate" feeling needs preserving.
4. **Sub-300ms UI ceiling.** Every interactive-element duration ≤
   `--motion-duration-600` (300ms). Only modals/trays/scroll-reveal/ambient may
   exceed it, and each such case has a one-line justification.
5. **No `scale(0)` entrances, ever.** Every scale-based entrance starts at
   `scale(0.9–0.98)` + `opacity: 0`, never `scale(0)`.
6. **Origin-aware, trigger-anchored motion.** Any popover/dropdown/tooltip scales
   from `transform-origin` matching its trigger, not `center`. (Modals are the one
   exception — centered is correct for them.)
7. **GPU-only properties.** No `width`/`height`/`top`/`left`/`margin`/`padding` in
   any transition/animation/keyframe. `transform` + `opacity` (and paint-only
   `box-shadow`/`color`/`background-color`) only.
8. **Interruptible where it needs to be.** Anything rapidly re-triggerable (toasts,
   toggles, hover states fired repeatedly) uses CSS transitions or a spring, not
   `@keyframes` that restart from zero.
9. **Reduced motion + hover gating both present.** `prefers-reduced-motion` handling
   exists for every new movement-based animation (§6), and every `:hover` rule with
   a `transform` is wrapped in `@media (hover: hover) and (pointer: fine)`.
10. **Cohesion and stagger.** Does the timing/easing match the element's weight and
    the rest of the system (component-scale = Spectrum tokens, hero/marketing-scale
    = `-strong` curve)? Do sibling groups stagger 30–120ms instead of appearing all
    at once? Would deleting the animation feel better than keeping it as-is — if
    genuinely unsure, that's the answer.

Every finding raised against this checklist should be written as a
`| Before | After | Why |` markdown table row (per `review-animations.md`'s required
output format), not a prose list — keep review output consistent with the rest of
the emil-derived tooling in this repo.
