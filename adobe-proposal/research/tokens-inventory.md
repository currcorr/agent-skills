# Adobe Spectrum Design Token Inventory (Verified)

Compiled 2026-07-13. All "VERIFIED" values were fetched directly from Adobe's
open-source token source files and cross-checked by parsing the raw JSON
(not paraphrased by a summarizing model). Anything not confirmed this way is
explicitly marked "UNVERIFIED".

## Sources actually reached

1. **`adobe/spectrum-design-data`** (GitHub repo — note: `adobe/spectrum-tokens`
   was renamed to `adobe/spectrum-design-data` in 2025; the old repo is now a
   redirect placeholder). Package `@adobe/spectrum-tokens` on npm, version
   **14.14.0** (`dist-tags.latest` as of fetch time), tarball pulled from
   `https://registry.npmjs.org/@adobe/spectrum-tokens/-/spectrum-tokens-14.14.0.tgz`.
   This is the canonical machine-readable Spectrum 2 token source. Files parsed
   directly as JSON:
   - `packages/tokens/src/color-palette.json` (372 tokens — base color ramps, light/dark/wireframe sets)
   - `packages/tokens/src/semantic-color-palette.json` (94 tokens — positive/negative/notice/informative/accent semantic ramps)
   - `packages/tokens/src/color-aliases.json` (170 tokens — background layers, component-state colors, drop-shadow colors)
   - `packages/tokens/src/color-component.json` (73 tokens)
   - `packages/tokens/src/typography.json` (312 tokens — type scale, weights, line-heights, letter-spacing)
   - `packages/tokens/src/layout.json` (359 tokens — spacing, corner-radius, component-height, drop-shadow geometry)
   - `packages/tokens/src/layout-component.json` (1010 tokens — per-component dimensions)
   - `packages/tokens/src/icons.json` (not deeply mined; icon sizing only)

   Confirmed via GitHub directory listing that these 8 files are the **entire**
   contents of `packages/tokens/src/` — there is no separate motion/duration/
   easing/elevation/spacing JSON file in this package.

2. **`@spectrum-css/vars`** (npm, version **9.0.8**) — Spectrum **1** (classic)
   CSS custom-property source, used only for motion/duration/easing because
   Spectrum 2's token repo does not yet publish motion tokens in JSON. Flagged
   per-value below as "Spectrum 1, not S2-confirmed."

3. **`spectrum.adobe.com` / `s2.spectrum.adobe.com`** — **UNREACHABLE**. All
   requests to `*.adobe.com` (and `en.wikipedia.org`, tested as a control) were
   rejected at the network egress layer with `403` ("gateway answered 403 to
   CONNECT — policy denial"), i.e. this session's sandbox blocks that host
   outright. `api.github.com` was also blocked (different error: "GitHub
   access to this repository is not enabled for this session"). Everything
   documentation-page-only (prose explanations, rationale, screenshots) is
   therefore **not verified** in this pass — only what exists in the JSON/CSS
   token files above.

Working files (raw downloads) are kept alongside this report in
`/home/user/agent-skills/adobe-proposal/research/*.json` for re-derivation.

---

## 1. Color

### 1.1 Gray ramp — VERIFIED (`color-palette.json`, `gray-*`, sets.light / sets.dark)

| Token | Light | Dark |
|---|---|---|
| gray-25  | rgb(255, 255, 255) | rgb(17, 17, 17) |
| gray-50  | rgb(248, 248, 248) | rgb(27, 27, 27) |
| gray-75  | rgb(243, 243, 243) | rgb(34, 34, 34) |
| gray-100 | rgb(233, 233, 233) | rgb(44, 44, 44) |
| gray-200 | rgb(225, 225, 225) | rgb(50, 50, 50) |
| gray-300 | rgb(218, 218, 218) | rgb(57, 57, 57) |
| gray-400 | rgb(198, 198, 198) | rgb(68, 68, 68) |
| gray-500 | rgb(143, 143, 143) | rgb(109, 109, 109) |
| gray-600 | rgb(113, 113, 113) | rgb(138, 138, 138) |
| gray-700 | rgb(80, 80, 80)   | rgb(175, 175, 175) |
| gray-800 | rgb(41, 41, 41)   | rgb(219, 219, 219) |
| gray-900 | rgb(19, 19, 19)   | rgb(242, 242, 242) |
| gray-1000| rgb(0, 0, 0)      | rgb(255, 255, 255) |

Note: Spectrum 2's gray scale runs **25 → 1000** (13 steps), not the
classic Spectrum 1 gray-50→gray-900 (9 steps). `gray-1000` light = pure
black, dark = pure white (these are the ramp endpoints, distinct from the
`black`/`white` primitive tokens below).

Primitives — VERIFIED: `black` = `rgb(0, 0, 0)`, `white` = `rgb(255, 255, 255)` (both flat, no light/dark sets).

### 1.2 Red ramp — VERIFIED (`color-palette.json`, `red-*`)

Spectrum 2 extended the ramp from 13 to **16 steps** (100–1600, incrementing
by 100), replacing the old 900-cap scale.

| Token | Light | Dark |
|---|---|---|
| red-100  | rgb(255, 246, 245) | rgb(54, 10, 3) |
| red-200  | rgb(255, 235, 232) | rgb(68, 13, 5) |
| red-300  | rgb(255, 214, 209) | rgb(87, 17, 7) |
| red-400  | rgb(255, 188, 180) | rgb(115, 24, 11) |
| red-500  | rgb(255, 157, 145) | rgb(147, 31, 17) |
| red-600  | rgb(255, 118, 101) | rgb(177, 38, 23) |
| red-700  | rgb(255, 81, 61)  | rgb(205, 46, 29) |
| red-800  | rgb(240, 56, 35)  | rgb(223, 52, 34) |
| red-900  | rgb(215, 50, 32)  | rgb(252, 67, 46) |
| red-1000 | rgb(183, 40, 24)  | rgb(255, 103, 86) |
| red-1100 | rgb(156, 33, 19)  | rgb(255, 134, 120) |
| red-1200 | rgb(129, 27, 14)  | rgb(255, 167, 157) |
| red-1300 | rgb(104, 21, 10)  | rgb(255, 196, 189) |
| red-1400 | rgb(80, 16, 6)    | rgb(255, 222, 219) |
| red-1500 | rgb(59, 11, 4)    | rgb(255, 242, 240) |
| red-1600 | rgb(29, 5, 2)     | rgb(255, 255, 255) |

`red-800` (light) = `rgb(240, 56, 35)` ≈ `#F03823` is the UI "negative" red
(see §1.4) — **this is not the same as Adobe's corporate brand-mark red.**

**Adobe corporate red `#EB1000`** — **UNVERIFIED**. Not present anywhere in
the fetched token files (they define the *product UI* red ramp, not the
corporate logo mark). Web search for third-party confirmation (adobe.com
itself was unreachable) returned inconsistent unofficial values (e.g.
`#ED2224` cited by brand-color aggregator sites) — none authoritative. Treat
`#EB1000` as **unconfirmed knowledge, flag before using it** in any deliverable.

### 1.3 Blue ramp — VERIFIED (`color-palette.json`, `blue-*`; this is Spectrum 2's default "informative"/"accent" hue)

| Token | Light | Dark |
|---|---|---|
| blue-100  | rgb(245, 249, 255) | rgb(14, 23, 63) |
| blue-200  | rgb(229, 240, 254) | rgb(15, 28, 82) |
| blue-300  | rgb(203, 226, 254) | rgb(12, 33, 117) |
| blue-400  | rgb(172, 207, 253) | rgb(18, 45, 154) |
| blue-500  | rgb(142, 185, 252) | rgb(26, 58, 195) |
| blue-600  | rgb(114, 158, 253) | rgb(37, 73, 229) |
| blue-700  | rgb(93, 137, 255)  | rgb(52, 91, 248) |
| blue-800  | rgb(75, 117, 255)  | rgb(64, 105, 253) |
| blue-900  | rgb(59, 99, 251)   | rgb(86, 129, 255) |
| blue-1000 | rgb(39, 77, 234)   | rgb(105, 149, 254) |
| blue-1100 | rgb(29, 62, 207)   | rgb(124, 169, 252) |
| blue-1200 | rgb(21, 50, 173)   | rgb(152, 192, 252) |
| blue-1300 | rgb(16, 40, 140)   | rgb(181, 213, 253) |
| blue-1400 | rgb(12, 31, 105)   | rgb(213, 231, 254) |
| blue-1500 | rgb(14, 24, 67)    | rgb(238, 245, 255) |
| blue-1600 | rgb(7, 11, 30)     | rgb(255, 255, 255) |

### 1.4 Semantic colors — VERIFIED (`semantic-color-palette.json` aliases resolved against `color-palette.json`)

Semantic ramps are **aliases** onto the base hue ramps (not independent
values): `positive-color-*` → `green-*`, `negative-color-*` → `red-*`,
`informative-color-*` → `blue-*`, `notice-color-*` → `orange-*`.

Representative "-800" step (the step most commonly used for default
icon/text/border semantic color):

| Semantic | Light | Dark | Aliases to |
|---|---|---|---|
| positive-color-800    | rgb(7, 147, 85)   | rgb(6, 136, 80)   | `{green-800}` |
| negative-color-800    | rgb(240, 56, 35)  | rgb(223, 52, 34)  | `{red-800}` |
| informative-color-800 | rgb(75, 117, 255) | rgb(64, 105, 253) | `{blue-800}` |
| notice-color-800      | rgb(212, 91, 0)   | rgb(199, 82, 0)   | `{orange-800}` |
| accent-color-800       | rgb(75, 117, 255) | rgb(64, 105, 253) | `{blue-800}` (same as informative — default accent hue is blue) |

Icon colors (`icon-color-*`, resolve through `*-visual-color` aliases):

| Token | Light | Dark |
|---|---|---|
| icon-color-negative    | rgb(240, 56, 35)  | rgb(252, 67, 46) |
| icon-color-positive    | rgb(7, 147, 85)   | rgb(9, 157, 89) |
| icon-color-informative | rgb(75, 117, 255) | rgb(86, 129, 255) |
| icon-color-notice      | rgb(212, 91, 0)   | rgb(224, 100, 0) |
| icon-color-neutral     | rgb(143, 143, 143)| rgb(138, 138, 138) |

Subtle semantic backgrounds (`*-subtle-background-color-default`, from `color-aliases.json`):

| Token | Light | Dark |
|---|---|---|
| positive-subtle-background-color-default    | rgb(215, 247, 225) | rgb(0, 51, 38) |
| negative-subtle-background-color-default    | rgb(255, 235, 232) | rgb(87, 17, 7) |
| informative-subtle-background-color-default | rgb(229, 240, 254) | rgb(12, 33, 117) |
| notice-subtle-background-color-default      | rgb(255, 236, 207) | rgb(80, 27, 0) |

Full green ramp (positive) and orange ramp (notice), for reference — VERIFIED:

| Step | green light | green dark | orange light | orange dark |
|---|---|---|---|---|
| 100  | rgb(237,252,241) | rgb(0,30,23)  | rgb(255,246,231) | rgb(49,16,0) |
| 200  | rgb(215,247,225) | rgb(0,38,29)  | rgb(255,236,207) | rgb(61,21,0) |
| 300  | rgb(173,238,197) | rgb(0,51,38)  | rgb(255,218,158) | rgb(80,27,0) |
| 400  | rgb(107,227,162) | rgb(0,68,48)  | rgb(255,193,94)  | rgb(106,36,0) |
| 500  | rgb(43,209,125)  | rgb(2,87,58)  | rgb(255,162,19)  | rgb(135,47,0) |
| 600  | rgb(18,184,103)  | rgb(3,106,67) | rgb(252,125,0)   | rgb(162,59,0) |
| 700  | rgb(11,164,93)   | rgb(4,124,75) | rgb(232,106,0)   | rgb(185,73,0) |
| 800  | rgb(7,147,85)    | rgb(6,136,80) | rgb(212,91,0)    | rgb(199,82,0) |
| 900  | rgb(5,131,78)    | rgb(9,157,89) | rgb(194,78,0)    | rgb(224,100,0) |
| 1000 | rgb(3,110,69)    | rgb(14,175,98)| rgb(167,62,0)    | rgb(243,117,0) |

### 1.5 Background layers — VERIFIED (`color-aliases.json`)

| Token | Light | Dark |
|---|---|---|
| background-base-color       | rgb(255, 255, 255) | rgb(17, 17, 17) |
| background-layer-1-color    | rgb(248, 248, 248) | rgb(27, 27, 27) |
| background-layer-2-color    | rgb(255, 255, 255) | rgb(34, 34, 34) |
| background-elevated-color   | rgb(255, 255, 255) | rgb(34, 34, 34) |
| background-pasteboard-color | rgb(233, 233, 233) | rgb(17, 17, 17) |

(`background-base-color` = `gray-25`, `background-layer-1-color` = `gray-50`,
`background-layer-2`/`elevated` = `gray-75` in dark mode — confirms the
layer ramp is literally the gray scale walked one step at a time.)

---

## 2. Typography — VERIFIED (`typography.json`)

### 2.1 Type scale — font sizes

Base numeric scale (`font-size-N`), each token has separate **desktop** and
**mobile** values:

| Token | Desktop | Mobile |
|---|---|---|
| font-size-25   | 10px | — |
| font-size-50   | 11px | — |
| font-size-75   | 12px | — |
| font-size-100  | 14px | — |
| font-size-200  | 16px | — |
| font-size-300  | 18px | — |
| font-size-400  | 20px | — |
| font-size-500  | 22px | — |
| font-size-600  | 25px | — |
| font-size-700  | 28px | — |
| font-size-800  | 32px | — |
| font-size-900  | 36px | — |
| font-size-1000 | 40px | — |
| font-size-1100 | 45px | — |
| font-size-1200 | 51px | — |
| font-size-1300 | 58px | — |
| font-size-1400 | 65px | — |
| font-size-1500 | 73px | — |

Heading scale (`heading-size-*`, aliases onto `font-size-N`, desktop / mobile):

| Token | Desktop | Mobile |
|---|---|---|
| heading-size-xxxxl | 73px | 88px |
| heading-size-xxxl  | 58px | 70px |
| heading-size-xxl   | 45px | 55px |
| heading-size-xl    | 36px | 44px |
| heading-size-l     | 28px | 34px |
| heading-size-m     | 22px | 27px |
| heading-size-s     | 20px | 24px |
| heading-size-xs    | 18px | 22px |
| heading-size-xxs   | 14px | 17px *(marked `"deprecated": true` in source)* |

Body scale (`body-size-*`):

| Token | Desktop | Mobile |
|---|---|---|
| body-size-xxxl | 25px | 31px |
| body-size-xxl  | 22px | 27px |
| body-size-xl   | 20px | 24px |
| body-size-l    | 18px | 22px |
| body-size-m    | 16px | 19px |
| body-size-s    | 14px | 17px |
| body-size-xs   | 12px | 15px |
| body-size-xxs  | 11px | 13px |

Detail scale (`detail-size-*`) and code scale (`code-size-*`):

| Token | Desktop | Mobile |
|---|---|---|
| detail-size-xl | 18px | 22px |
| detail-size-l  | 16px | 19px |
| detail-size-m  | 14px | 17px |
| detail-size-s  | 12px | 15px |
| detail-size-xs | 11px | 13px |
| code-size-xl   | 20px | 24px |
| code-size-l    | 18px | 22px |
| code-size-m    | 16px | 19px |
| code-size-s    | 14px | 17px |

### 2.2 Weights — VERIFIED

Weight tokens resolve to **named variable-font instances**, not raw CSS
numbers: `light-font-weight` = "light", `regular-font-weight` = "regular",
`medium-font-weight` = "medium", `bold-font-weight` = "bold",
`extra-bold-font-weight` = "extra-bold", `black-font-weight` = "black".
Heading default weight = `extra-bold` (sans-serif); heavy variant = `black`.

### 2.3 Line-heights — VERIFIED

- `line-height-100` = **1.3** (used by `heading-line-height`, `detail-line-height`)
- `line-height-200` = **1.5** (used by `body-line-height`, `code-line-height`)
- Full font-size-matched line-height scale (`line-height-font-size-N`, px, desktop):
  25→12px, 50→14px, 75→16px, 100→18px, 200→20px, 300→22px, 400→24px,
  500→26px, 600→30px, 700→32px, 800→36px, 900→42px, 1000→46px, 1100→52px,
  1200→58px, 1300→66px, 1400→74px, 1500→84px.

### 2.4 Letter-spacing — VERIFIED

- `letter-spacing` (base/heading/body) = **0em**
- `detail-letter-spacing` = **0.06em**

### 2.5 Font families — VERIFIED

- Sans-serif (default): **Adobe Clean Spectrum VF**
- Serif: **Adobe Clean Serif**
- CJK: **Adobe Clean Han**
- Code/monospace: **Source Code Pro**

---

## 3. Dimension / Spacing / Corner Radius — VERIFIED (`layout.json`)

### 3.1 Spacing scale

| Token | Value |
|---|---|
| spacing-25  | 1px |
| spacing-50  | 2px |
| spacing-75  | 4px |
| spacing-85  | 6px |
| spacing-100 | 8px |
| spacing-200 | 12px |
| spacing-300 | 16px |
| spacing-350 | 20px |
| spacing-400 | 24px |
| spacing-500 | 32px |
| spacing-600 | 40px |
| spacing-700 | 48px |
| spacing-800 | 64px |
| spacing-900 | 80px |
| spacing-1000| 96px |

### 3.2 Component heights (desktop / mobile)

| Token | Desktop | Mobile |
|---|---|---|
| component-height-50  | 20px | 26px |
| component-height-75  | 24px | 30px |
| component-height-100 | 32px | 40px |
| component-height-200 | 40px | 50px |
| component-height-300 | 48px | 60px |
| component-height-400 | 56px | 70px |
| component-height-500 | 64px | 80px |

### 3.3 Corner radius — Spectrum 2's rounder scale

| Token | Value |
|---|---|
| corner-radius-0    | 0px |
| corner-radius-75   | 3px |
| corner-radius-100  | 4px |
| corner-radius-200  | 5px |
| corner-radius-300  | 6px |
| corner-radius-400  | 7px |
| corner-radius-500  | 8px |
| corner-radius-600  | 9px |
| corner-radius-700  | 10px |
| corner-radius-800  | 16px |
| corner-radius-1000 | 0.5 *(unitless ratio → 50%, used for full/pill radius)* |

Named semantic defaults (aliases):
- `corner-radius-none` → `{corner-radius-0}` = 0px
- `corner-radius-small-default` → `{corner-radius-100}` = 4px
- `corner-radius-medium-default` → `{corner-radius-500}` = 8px
- `corner-radius-large-default` → `{corner-radius-700}` = 10px
- `corner-radius-extra-large-default` → `{corner-radius-800}` = 16px
- `corner-radius-full` → `{corner-radius-1000}` = 0.5 (50%, pill/circle)

There are also `corner-radius-small-size-*` / `corner-radius-medium-size-*`
t-shirt-size variants (extra-small/small/medium/large/extra-large) in the
file for per-component sizing, not itemized here — see
`research/layout.json` for the full set.

---

## 4. Elevation / Drop Shadow — VERIFIED (`layout.json` geometry + `color-aliases.json` color/opacity)

Geometry (x/y offset and blur radius; x is 0 for all elevation levels — shadows are purely vertical + blur):

| Level | x | y | blur |
|---|---|---|---|
| 100 (base, e.g. `drop-shadow-emphasized-default-*`) | 0px | 1px | 6px |
| 200 (elevated / hover, e.g. `drop-shadow-elevated-*`, `drop-shadow-emphasized-hover-*`) | 0px | 2px | 8px |
| 300 (dragged, e.g. `drop-shadow-dragged-*`) | 0px | 6px | 16px |

Color/opacity (`color-aliases.json`, `drop-shadow-color-*`, rgba, per mode):

| Level | Light | Dark | Wireframe |
|---|---|---|---|
| drop-shadow-color-100 (base)     | rgba(0,0,0,0.12) | rgba(0,0,0,0.36) | rgba(0,0,0,0.12) |
| drop-shadow-color-200 (elevated) | rgba(0,0,0,0.16) | rgba(0,0,0,0.48) | rgba(0,0,0,0.16) |
| drop-shadow-color-300 (dragged)  | rgba(0,0,0,0.20) | rgba(0,0,0,0.60) | rgba(0,0,0,0.20) |
| drop-shadow-ambient-color        | rgba(0,0,0,0.08) | rgba(0,0,0,0.24) | rgba(0,0,0,0.08) |

So, combined, e.g. **default/resting elevation** = `0px 1px 6px rgba(0,0,0,0.12)` (light) /
`rgba(0,0,0,0.36)` (dark); **elevated/hover** = `0px 2px 8px rgba(0,0,0,0.16)` (light) /
`rgba(0,0,0,0.48)` (dark); **dragged** = `0px 6px 16px rgba(0,0,0,0.20)` (light) /
`rgba(0,0,0,0.60)` (dark).

Android-specific: `android-elevation` = **2dp** (single flat value, no per-level scale found in this file).

---

## 5. Motion — duration VERIFIED but from Spectrum 1, not S2-confirmed; easing same caveat

**Important caveat:** `packages/tokens/src/` in the current Spectrum 2 token
package (`@adobe/spectrum-tokens` 14.14.0) contains **no** motion/duration/
easing files — confirmed by grepping all 8 JSON files for
"duration"/"cubic-bezier"/"easing" (zero matches) and by the GitHub directory
listing showing only the 8 files enumerated in the Sources section above.
`spectrum.adobe.com`/`s2.spectrum.adobe.com` motion documentation pages could
not be reached (network policy blocks `*.adobe.com` in this session).

The values below come from **`@spectrum-css/vars` v9.0.8** (npm registry,
`dist/spectrum-global.css`), which is **Spectrum 1 (classic)**, fetched
directly and grepped — real, exact, published values, but **not verified as
carried over unchanged into Spectrum 2's token set**. Treat as a
strong-but-unconfirmed reference point pending an accessible S2 motion doc.

Duration (`--spectrum-global-animation-duration-*`):

| Token | Value |
|---|---|
| duration-0    | 0ms |
| duration-100  | 130ms |
| duration-200  | 160ms |
| duration-300  | 190ms |
| duration-400  | 220ms |
| duration-500  | 250ms |
| duration-600  | 300ms |
| duration-700  | 350ms |
| duration-800  | 400ms |
| duration-900  | 450ms |
| duration-1000 | 500ms |
| duration-2000 | 1000ms |
| duration-4000 | 2000ms |

Easing (`--spectrum-global-animation-*`):

| Token | cubic-bezier |
|---|---|
| linear      | `cubic-bezier(0, 0, 1, 1)` |
| ease-in-out | `cubic-bezier(.45, 0, .40, 1)` |
| ease-in     | `cubic-bezier(.50, 0, 1, 1)` |
| ease-out    | `cubic-bezier(0, 0, 0.40, 1)` |
| ease-linear | `cubic-bezier(0, 0, 1, 1)` |

Spot-check from the S2 React components package (`@react-spectrum/s2` v1.5.1,
npm) shows a couple of hand-coded durations in component CSS
(`Toast.module.css`): `400ms`, `300ms`, `600ms` — consistent with the S1
duration scale (400ms = duration-800, 300ms = duration-600) but these are
inline component values, not confirmed to trace back to named S2 duration
tokens.

---

## Summary of verification status

| Category | Status |
|---|---|
| Gray ramp (25–1000, light+dark) | VERIFIED — `color-palette.json` |
| Red ramp (100–1600, light+dark) | VERIFIED — `color-palette.json` |
| Blue ramp (100–1600, light+dark) | VERIFIED — `color-palette.json` |
| Green/Orange ramps | VERIFIED — `color-palette.json` |
| Semantic positive/negative/notice/informative/accent | VERIFIED — `semantic-color-palette.json` (aliases resolved) |
| Background layers (base/layer-1/layer-2/elevated/pasteboard) | VERIFIED — `color-aliases.json` |
| Adobe corporate brand red `#EB1000` | **UNVERIFIED** — not in token files; adobe.com unreachable; third-party sites disagree |
| Typography scale (sizes, desktop+mobile) | VERIFIED — `typography.json` |
| Font weights (named, not numeric) | VERIFIED — `typography.json` |
| Line-heights, letter-spacing | VERIFIED — `typography.json` |
| Font families | VERIFIED — `typography.json` |
| Spacing scale | VERIFIED — `layout.json` |
| Component heights | VERIFIED — `layout.json` |
| Corner radius scale + named defaults | VERIFIED — `layout.json` |
| Drop-shadow geometry (x/y/blur) | VERIFIED — `layout.json` |
| Drop-shadow color/opacity | VERIFIED — `color-aliases.json` |
| Motion duration tokens | PARTIALLY VERIFIED — real values, but from Spectrum **1** (`@spectrum-css/vars`), not confirmed as current in S2 |
| Motion easing curves | PARTIALLY VERIFIED — same caveat as above |
| Spectrum docs pages (spectrum.adobe.com, s2.spectrum.adobe.com) | **UNREACHABLE** this session (network policy blocks `*.adobe.com`) |
