# QA & Design Review Log

## Round 1 — 2026-07-13

### Functional / a11y QA (Playwright, 12 tests) — 12/12 PASS
Theme controls (both toggles, sync, persistence, reload), tabs (indicator +
full keyboard), accordion, before/after slider, sticky-nav condense +
hamburger, scroll-progress, stat count-up targets, hero choreography
completion, focus-visible rings (8/8 elements), reduced-motion behavior
(final states immediate, zero running ambient animations), zero console
errors, `prefers-color-scheme: dark` default with no stored preference.

### Design review (brand fidelity + craft + WCAG) — findings & resolutions

| # | Severity | Finding | Resolution |
|---|---|---|---|
| 1 | Blocker | Semantic badge/delta text ~3.4:1 on subtle backgrounds (both themes) | Added `--color-*-on-subtle` tokens (Spectrum −1000 step; 5.5:1 light / 4.9:1 dark), rewired tags + delta chips |
| 2 | Blocker | `.adb-nav` animated `height` (motion.md bans layout-property animation) | Shrink rebuilt as transform-only content condense (scale 0.92); layout box constant |
| 3 | Should-fix | Hero/CTA-band headings were `<p>` | Converted to `<h3>` (class-based styles unaffected) |
| 4 | Should-fix | Gallery + kit theme toggles desynced | Both widgets observe `data-theme` mutations and re-derive state from storage |
| 5 | Should-fix | Count-up used literal 1000ms | Reads `--motion-duration-loop` via getComputedStyle |
| 6 | Should-fix | Determinate progress lacked progressbar semantics | `role="progressbar"` + labelled-by + live `aria-valuenow` |
| 7 | Should-fix | Stale pricing-badge screenshots | Full screenshot set regenerated post-fix |
| 8 | Nit | craft-rules "pills = CTAs only" contradicted sanctioned tag/badge/capsule usage | Rule + checklist reworded |
| 9 | Nit | White-on-red CTA 4.55:1 (thin AA margin) | Accepted — documented tradeoff in tokens.css; labels bold ≥16px |
| 10 | Nit | Dark-section accent nearly invisible in dark theme (#060606 on #111111) | Accepted — inherent to global dark mode; noted for site build |

### Verified clean (no findings)
All 10 craft-rules anti-AI-tell checks; hover gating; instant focus rings;
no `ease-in`; no literal hex/ms/bezier in component CSS; tertiary + on-dark
text contrast (4.6–9.3:1); magnetic CTA spring smoothing + gating;
reduced-motion implementation across all animated fragments.
