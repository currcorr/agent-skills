# Adobe Web Visual Language — Design Rules Brief

## Method note (read this first)

The plan called for direct WebFetch extraction of HTML/CSS from adobe.com, the Adobe MAX site, and Spectrum 2 announcement posts. **Live page fetching was unavailable for this entire research session** — WebFetch returned HTTP 403 on every target, including adobe.com, spectrum.adobe.com, s2.spectrum.adobe.com, blog.adobe.com, and even a control fetch of example.com, confirming this was a session-wide outbound-fetch failure rather than an adobe.com-specific block. A direct `curl` through the environment's proxy hit the same wall (`CONNECT tunnel failed, response 403`).

WebSearch (a separate channel) did work and surfaced real snippets from Adobe's own Spectrum documentation, the 2023 Spectrum 2 launch coverage (TechCrunch, LogRocket, Adobe's own blog via search snippet), and 2024-2025 rebrand coverage (Creative Bloq on the Mother Design identity refresh). Those are marked **[search-verified]** below with source links. Everything else is marked **[knowledge-based]** — well-established facts about Adobe's design language from pre-training knowledge, not confirmed against live markup this session. Nothing in this brief is marked "verified-by-fetch" because no fetch succeeded.

**Recommendation:** before finalizing pixel-level tokens (hex codes, exact clamp() ranges), someone with working browser/fetch access should confirm against live adobe.com and s2.spectrum.adobe.com computed styles. This brief is safe to build against directionally but treat specific numbers as best-effort estimates, not ground truth.

---

## 1. Typography

**[knowledge-based]** Adobe's corporate marketing typeface is **Adobe Clean**, a proprietary humanist sans (Adobe-internal, not licensable) that reads as a slightly warmer, rounder cousin of Source Sans / Proxima Nova. It is not available for outside use, which is why the target system will substitute **Source Sans 3**.

Source Sans 3 vs. Adobe Clean — adjustments to plan for:
- Source Sans 3 is a touch narrower and more mechanical than Adobe Clean, which has warmer curves and a more humanist skeleton. At display sizes this reads as slightly "colder" — compensate with **tighter tracking is less necessary**; don't over-tighten or it will look cramped rather than confident.
- Source Sans 3 ships a full weight range including Black (900), so headline weight usage (below) maps cleanly — use ExtraBold/Black (800/900) where Adobe Clean Black would appear.
- Adobe Clean's italics and small-caps details won't matter for a marketing system; skip that concern.
- x-height and cap-height ratios are close enough that font-size values below can be reused as-is without a compensating scale factor.

**[knowledge-based]** Marketing headline scale (hero / section headers), typical of adobe.com and campaign pages:
- Hero H1: roughly `clamp(2.5rem, 4.5vw + 1rem, 4.5rem)` → ~40px mobile to ~72px desktop. Large campaign/launch heroes (e.g. MAX, Firefly launches) can go bigger, up to ~80-96px desktop.
- Section H2: `clamp(1.75rem, 2.5vw + 1rem, 2.75rem)` → ~28px to ~44px.
- Card/subsection H3: 20-28px.
- Weight: headlines lean **Bold to Black (700-900)**, rarely regular weight at hero scale. Adobe's marketing voice is confident/bold-forward, not light/thin display type — avoid using light weights (300-400) at large sizes; that reads as competitor (e.g. Apple/Google) territory, not Adobe.
- Tracking: **tight, negative letter-spacing at large sizes** — roughly `-0.01em` to `-0.03em` on hero/H1, tapering to `0em`/neutral by body size. Do not apply negative tracking below ~20px; it hurts legibility at UI/body scale.
- Line-height: tight on display type, **1.0-1.15** for hero headlines (multi-line headlines sit close together), opening up to **1.3-1.4** for H2/H3, and **1.5-1.6** for body copy.
- Body size: 16-18px base, occasionally 20px for marketing "lede" paragraphs under a hero. Line-length capped for readability (roughly 60-75 characters, i.e. body columns rarely exceed ~600-680px wide even inside a 1200px+ container).

## 2. Color usage discipline

**[search-verified, with a flagged discrepancy]** Search results surfaced two different "official" Adobe red hex values depending on source and era: `#FA0C00`/`#FA0F00` (cited by brand-color aggregator sites as the current corporate red) and `#EB1000` (the value given in this task's own brief, which also circulates as an Adobe red reference, plausibly a Spectrum token value or a slightly older brand-guideline number). **Flag: pick one canonical hex and apply it consistently rather than mixing** — for a Source-Sans-based Adobe-styled system, `#EB1000` (as specified in the task) is a reasonable working value; if a stricter brand match matters later, verify against a live fetch of Adobe's current brand guidelines page, since aggregator sites disagree.

**[search-verified]** Adobe's own guidance, paraphrased from brand-guideline coverage: *"Red is reserved for the logo or associated products... should not be used as a flood or type color."* Adobe treats red as a **primary corporate color used only in deliberate, accent ways that elevate it to 'special' status** — not a background or fill color. Source: [Adobe brand color coverage, BrandColorCode.com](https://www.brandcolorcode.com/adobe).

**[search-verified]** Adobe's 2024-2025 identity refresh (Mother Design) is described as *"tidying up"* the palette toward a tighter focus on **red + black + white**, i.e. reducing incidental color use in brand contexts rather than expanding it. Source: [Creative Bloq, "Adobe quietly rebrands, tweaking its iconic logo"](https://www.creativebloq.com/design/branding/adobe-rebrand).

Concrete rationing rule for builders **[knowledge-based, synthesizing the above]**:
- Red appears only as: (a) the logo mark, (b) primary CTA button fill or a CTA text/icon accent, (c) small indicator dots/underlines/tags (e.g. "New" badges), (d) occasional single-word emphasis inside a headline. It should never be more than roughly **1-2 elements per viewport/section**.
- Red **never** appears as: a section background, a body-text color, a large image/media fill, a card background, or an icon set's base color (icons are typically neutral gray/black or on-brand secondary hues, not red).
- Dominant surface palette is **white / near-white** (`#FFFFFF`, `#FAFAFA`/`#F5F5F5` for subtle section differentiation).
- Text is **near-black**, not pure black — roughly `#2C2C2C` for body copy, sometimes darker (`#1A1A1A`/`#131313`) for headlines, which softens the WCAG-max-contrast starkness while staying very dark.
- Gray hierarchy for secondary text/borders/dividers: a 4-6 step gray ramp, e.g. `#464646` (secondary text) → `#6E6E6E` (tertiary/meta text) → `#B3B3B3` (disabled/placeholder) → `#E1E1E1`/`#EAEAEA` (borders, dividers, subtle card backgrounds).
- **Dark sections** (near-black or deep charcoal backgrounds, `#0A0A0A`-`#1E1E1E` range) are used sparingly and rhythmically — typically to bracket a page (e.g. a dark footer, or one dark "hero" section for a flagship launch/event like MAX or Firefly) rather than alternating light/dark every section. Treat dark sections as a **special-occasion accent**, roughly 1 in every 4-6 sections on a long marketing page, not a 50/50 alternation.
- **[search-verified]** Spectrum 2's *product* (application UI, not marketing-site) color system was rebuilt around a broader brand hue set — Orange, Celery, Cyan, Indigo, Fuchsia, Magenta — used for sub-brand and semantic color (Photoshop blue, Illustrator orange, etc.), while red stays reserved for brand/logo/critical-action moments. This is a UI-system nuance; the marketing-site rule above (red = rare accent) still holds for a marketing-facing design system. Source: [LogRocket, "Introducing Spectrum 2"](https://blog.logrocket.com/ux-design/spectrum-2-adobes-revamped-design-system/); [Adobe Blog Spectrum 2 announcement](https://blog.adobe.com/en/publish/2023/12/12/adobe-unveils-spectrum-2-design-system-reimagining-user-experience-over-100-adobe-applications).

## 3. Layout

**[search-verified]** Adobe's own Spectrum grid documentation confirms a **12-column responsive grid**, with two grid modes: a *fluid* grid (100% width, for app/workflow UI) and a **fixed grid with a capped max-width for content-specific/marketing pages** — this fixed mode is the relevant one for a marketing design system. Gutters are fixed pixel values that step up at breakpoints (documentation cites values like 16px/24px). Source: [Spectrum — Responsive grid](https://spectrum.adobe.com/page/responsive-grid/).

**[knowledge-based]** Concrete numbers to build against:
- Max content width: **~1200-1280px** for body/text-centric content, occasionally up to **~1440px** for wide visual/hero sections or full-bleed image galleries. Keep text columns narrower than the full container even when the container is wide.
- Section vertical padding rhythm: generous — roughly **80-120px** top/bottom padding per section on desktop, collapsing to **48-64px** on mobile. This generous whitespace is a core part of the "premium software brand" feel; cramped sections read as off-brand.
- Hero composition: two dominant patterns —
  1. **Left-aligned text + right-side product shot/video** (most common for product marketing pages — Creative Cloud, individual app pages): headline + subhead + CTA stacked left, roughly 40-50% of width, large visual filling the remainder.
  2. **Centered text over/under a large hero image or gradient background** (more common for campaign/event pages like MAX, or brand-moment pages): headline and CTA centered, often over a full-bleed visual.
- Cards: rounded corners (**12-16px radius** typical), soft/low-opacity drop shadows rather than hard borders, image or icon on top with text below, internal padding roughly **24-32px**. Grids of cards are typically 3-column on desktop, collapsing to 1-2 column on mobile.
- Image treatment: **rounded corners on essentially all media** (product screenshots, thumbnails, video embeds) — this is a consistent, checkable signature. Radius scales with element size (small thumbnail ~8px, large hero visual ~16-24px). Full-bleed edge-to-edge imagery is used more sparingly, mostly in campaign heroes.
- Whitespace ratio: marketing sections favor **content occupying well under half the vertical rhythm**, with the rest as padding/whitespace — dense, tightly-packed sections are not the Adobe pattern.

## 3b. Photography in the scroll experience

**[user-verified against live adobe.com]** Adobe uses real photography as
section backgrounds during the scroll experience — full-bleed photographic
moments between flat-color content sections, with content scrolling over
them. Rules for this system:

- **Real photos, not CSS scenery.** Photo slots ship with clearly-marked
  placeholders; production pages must swap in licensed photography (people
  at work, product-in-context, campaign imagery). A gradient is never a
  substitute in a photo slot.
- **Two treatments:** (1) full-bleed pinned backdrop — the photo stays fixed
  while content scrolls over it (one per page is plenty; it's a "brand
  moment", used like the dark section); (2) rounded photo panel
  (`--radius-xxl`) inside a normal section, matching the rounded-media rule.
- **Text never sits directly on a photo.** Always through a scrim token
  (`--scrim-photo`, `--scrim-photo-strong`, `--scrim-photo-left`) with
  `--color-text-on-media`; headline + one line + optional CTA, kept to the
  scrimmed region.
- **Rhythm:** photo sections count toward the same "special occasion" budget
  as dark sections — roughly 1 photographic backdrop per 4-6 sections. They
  pair naturally: photo moment → light content → dark section.
- **Motion:** the pinned effect itself is the motion; no additional zoom/pan
  by default. Under `prefers-reduced-motion` the photo becomes a normally
  scrolling absolute layer.

## 4. Component idioms

**[search-verified]** Spectrum 2 (Adobe's product-UI design system, launched Dec 2023) explicitly moved components toward being **"lighter, bolder, and rounder"** — described in launch coverage as introducing more rounded elements, thicker icon strokes, and brighter color use across 100+ Adobe applications. Sources: [Adobe Blog](https://blog.adobe.com/en/publish/2023/12/12/adobe-unveils-spectrum-2-design-system-reimagining-user-experience-over-100-adobe-applications), [adobe.design — Introducing Spectrum 2](https://adobe.design/stories/design-for-scale/introducing-spectrum-2).

**[knowledge-based]** Buttons: the trend line (both product UI via Spectrum 2 and newer marketing-site CTAs) is toward **fully rounded / pill-shaped primary buttons** (`border-radius: 999px` / full stadium shape), a shift from Spectrum 1's smaller-radius (~4-8px) rounded rectangles. For a new Adobe-styled system, **default to pill buttons for primary CTAs** — this is the more current, more distinctively "Adobe 2024+" signature than the older rounded-rect. Secondary/tertiary buttons (text links, outline buttons) can keep a smaller radius or no fill.

**[knowledge-based]** Navigation bar: a **thin, sticky top bar** (~48-64px tall) — logo mark at far left, primary nav items (often a "For Business / Individuals / Students" segmentation) left-of-center or center, with a search icon, sign-in, and a primary CTA button clustered right. Background is typically white/near-white with a subtle bottom border or shadow on scroll (not a heavy drop shadow). Collapses to a hamburger + drawer on mobile.

**[knowledge-based]** Card hover behavior: subtle — a slight elevation increase (shadow deepens) and/or a small vertical lift (translateY of a few px), sometimes a subtle scale-up on contained imagery. Adobe does not favor aggressive hover color-inversions or large scale jumps; hover states are restrained, reinforcing the "confident, not flashy" feel.

**[knowledge-based]** Footer structure: **multi-column link groups** (typically 4-6 columns: e.g. "Products," "Learn & Support," "Company," "Adobe accounts," etc.), a persistent dark or near-black background is common for the footer specifically (one of the few consistent uses of a dark section), region/language selector, social icons, and a bottom legal bar (copyright, privacy links, cookie preferences) in small type.

## 5. The "Adobe feel" — five checkable rules

1. **Red shows up in at most 1-2 places per viewport**, and never as a background, body-text color, or large fill — only logo, primary CTA, or a small accent/badge.
2. **Surfaces are white/near-white with near-black (not pure-black) text**; dark/near-black sections are a deliberate, occasional accent (roughly 1 in 4-6 sections), not a 50/50 alternation.
3. **Headlines are bold-to-black weight with tight negative tracking and tight line-height**, sitting in generous whitespace — if a hero section feels "light-weight" or cramped, it's off-brand in one of two opposite directions.
4. **All media has rounded corners**; primary CTAs are pill-shaped (fully rounded), not sharp rectangles.
5. **Section rhythm is generous** — roughly 80-120px vertical padding per section on desktop, content capped around 1200-1280px wide even when the outer background runs full-bleed.
