# Adobe-Style Proposal Website — Execution Plan

**Goal:** A high-fidelity proposal website in Adobe's visual language, built on a
reusable Adobe design system (tokens + components + motion), with interactive and
motion elements throughout. Orchestrated by the main agent; executed with Sonnet
subagents wherever the work is parallelizable and well-specified.

**Repo fit:** This mirrors the existing `ey-brand-kit` → `ey-site` pattern:
a brand kit (JSON + CSS tokens) is the single source of truth, and the site
consumes it. Quality gates reuse `taste`, `brand-review`,
`adversarial-design-review`, `assess-graphical-excellence`, and `webapp-testing`.

---

## Ground truth: what "Adobe attributes" means

Adobe's public design system is **Spectrum 2**. Its published, verifiable
attributes anchor the whole build — no guessing at "Adobe-ish":

| Attribute | Source of truth |
|---|---|
| Color (Adobe Red `#EB1000`, gray ramps, semantic colors, light/dark) | `adobe/spectrum-tokens` (GitHub, open source) |
| Typography | Adobe Clean is **proprietary** — substitute **Source Sans 3 / Source Serif 4** (Adobe's own open-source faces, on Google Fonts). Closest legal match by design lineage. |
| Spacing / sizing / corner radius | Spectrum dimension tokens (Spectrum 2 uses noticeably rounder corners: 8–16px) |
| Elevation & shadow | Spectrum drop-shadow tokens |
| Motion | Spectrum motion tokens: short durations (130–500ms), spectrum ease-in-out curves; plus the `taste/references/emil` animation standards already in this repo |
| Layout feel | Generous whitespace, 12-col grid, large editorial headlines, red used sparingly as accent — adobe.com and Adobe MAX sites as visual reference |

**Guardrail:** the site is *in the style of* Adobe, not impersonating Adobe. No
Adobe logo, no claim of origin. This is the same client-branding stance as the
EY skills.

---

## Deliverable layout

```
adobe-proposal/
  PLAN.md                     ← this file
  kit/
    adobe.json                ← brand kit (ey-brand-kit schema)
    tokens.css                ← CSS custom properties, light + dark
  design-system/
    index.html                ← living style guide / component gallery
    components/               ← one HTML+CSS+JS snippet file per component
    motion.md                 ← motion spec: durations, easings, choreography rules
  site/
    index.html                ← the proposal site (self-contained, single file)
    assets/
  qa/
    screenshots/              ← Playwright captures per breakpoint
    review-log.md             ← findings from each review gate + resolutions
```

**Stack decision: self-contained static HTML/CSS/vanilla-JS, no build step.**
Rationale: matches `ey-site`'s proven template pattern, is portable (openable
anywhere, publishable, emailable), and removes toolchain failure modes from
subagent work. Motion via CSS transitions/keyframes + IntersectionObserver +
small vanilla JS — Spectrum-grade motion does not need a framework. If the
proposal later needs an app-like feature (configurator, live pricing), that
section gets an isolated `<script type="module">`, not a framework migration.

---

## Phases and subagent allocation

Model policy: **Sonnet** for research fan-out, token transcription, component
and section builds, and screenshot QA — parallel, well-specified, contract-driven
work. **Main agent (orchestrator)** keeps the judgment work: the design-system
contract, integration, and final design review verdicts.

### Phase 0 — Research & brand kit (parallel, ~3 Sonnet subagents)

1. **Token researcher** — pull real values from `adobe/spectrum-tokens` and
   Spectrum 2 docs: color ramps, red accent values, type scale, spacing scale,
   radii, shadows, motion durations/easings. Output: raw token inventory (JSON).
2. **Visual-language researcher** — study adobe.com / Adobe MAX / Spectrum 2
   announcement pages: layout patterns, hero treatments, how red is rationed,
   card and nav idioms, dark-section rhythm. Output: written design-rules brief
   with concrete measurements ("hero headline ~72–96px, -2% tracking…").
3. **Motion researcher** — Spectrum motion guidelines + `taste/emil` standards:
   what animates, what never animates, entrance choreography, hover physics.
   Output: `design-system/motion.md` draft.

**Orchestrator gate:** merge into `kit/adobe.json` (ey-brand-kit schema) and
`kit/tokens.css`. This is the contract every later subagent receives verbatim.

### Phase 1 — Design system build (parallel, ~5–6 Sonnet subagents)

Each subagent gets: `tokens.css`, the design-rules brief, `motion.md`, and one
component bundle. They may only use token variables — no literal hex/px values.

| Subagent | Components |
|---|---|
| A | Buttons (all variants/states), links, tags/badges |
| B | Cards (content, stat, pricing), hover elevation + tilt micro-interaction |
| C | Navigation (sticky header w/ scroll shrink), footer, section shells |
| D | Hero patterns (headline reveal, gradient/red accent treatments), CTA band |
| E | Data display: timeline, stepper, comparison table, stat counters (animated count-up) |
| F | Interactive: tabs, accordion, before/after slider, scroll-progress indicator |

**Orchestrator gate:** assemble `design-system/index.html` (the gallery),
normalize inconsistencies, run the `brand-review` skill against the kit, fix.
The gallery is reviewed *before* any site work starts — cheaper to fix a button
once than in seven sections.

### Phase 2 — Content (1 Sonnet subagent + user input)

Draft proposal narrative structure: Hero → Problem → Proposed solution →
Approach & timeline → Team → Investment → Next steps/CTA. Real content comes
from the user; until then, the subagent writes credible domain-appropriate
placeholder copy with correct information hierarchy (never lorem ipsum — copy
length drives layout truthfully).
**Open question for user:** what is the proposal actually for, and who reads it?

### Phase 3 — Site assembly (parallel, ~7 Sonnet subagents, then integration)

One subagent per section, each receiving the *same* contract (tokens + gallery
components + motion spec + its content block). Sections are built as standalone
fragments with a strict interface: root `<section id>`, only token variables,
self-registering IntersectionObserver reveals.

Motion/interaction budget per the spec — signature moves:
- Hero: staggered headline mask-reveal on load, subtle red gradient drift
- Scroll: per-section entrance choreography (translate+fade, 120ms stagger)
- Stats: count-up on first view; timeline: progressive line draw
- Nav: shrink-on-scroll, active-section highlighting, smooth anchor scroll
- Hover: card lift + shadow bloom at Spectrum durations; magnetic CTA button
- Global: scroll-progress bar, `prefers-reduced-motion` honored everywhere

**Orchestrator integration pass (not delegated):** stitch fragments into
`site/index.html`, unify spacing rhythm between sections, dedupe JS, one
choreography timeline, performance sanity (no layout thrash, transforms only).

### Phase 4 — QA and design-review loop (parallel Sonnet + orchestrator verdicts)

1. **Screenshot agent** — `webapp-testing`/Playwright captures at 390/768/1440px,
   light + dark, plus mid-animation states → `qa/screenshots/`.
2. **Review gates**, run as three parallel Sonnet reviewers with distinct lenses,
   findings logged to `qa/review-log.md`:
   - `brand-review`: does it actually read as Adobe/Spectrum?
   - `adversarial-design-review` + `assess-graphical-excellence`: craft defects —
     spacing drift, type-scale violations, contrast, motion jank
   - Accessibility: WCAG contrast (red-on-white is borderline — verify),
     keyboard nav, focus states, reduced-motion
3. **Orchestrator adjudicates** findings (kill false positives), Sonnet fixers
   apply confirmed ones, re-screenshot. Loop until a pass produces no new
   confirmed findings (loop-until-dry, max 3 rounds).

### Phase 5 — Ship

Commit the full tree to this branch, push. Optional follow-ups: publish a
preview, or promote `kit/` + `design-system/` into a proper `adobe-kit` skill
alongside the EY family so future Adobe-branded deliverables reuse it.

---

## Sequencing summary

```
Phase 0  research ×3 (parallel Sonnet)      ─┐
Phase 0g kit contract (orchestrator)         ← everything downstream depends on this
Phase 1  components ×6 (parallel Sonnet)    ─┐
Phase 1g gallery + brand-review (orch.)      ← second hard gate
Phase 2  content ×1 (Sonnet, can overlap Phase 1)
Phase 3  sections ×7 (parallel Sonnet)
Phase 3g integration (orchestrator)
Phase 4  QA loop (Sonnet screenshots/reviewers, orchestrator verdicts) ×≤3
Phase 5  ship
```

~18–20 Sonnet subagent runs total; the two hard gates (kit contract, gallery
review) are what keep 13 parallel builders from diverging.

## Risks

- **Font legality:** Adobe Clean cannot be embedded. Source Sans 3 is the
  correct substitute and is itself an Adobe face — this is a feature, not a hack.
- **Red overuse:** the fastest way to look *not*-Adobe is too much red. The
  design-rules brief will set an explicit ration (accent + CTA only).
- **Impersonation line:** style yes, logo/identity no. Reviewer lens includes this.
- **Content vacuum:** without the real proposal subject, Phase 2 ships
  placeholders; layout is content-truthful so swapping copy later is low-risk.
