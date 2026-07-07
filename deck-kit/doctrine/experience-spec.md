# The Experience — executable spec for `render_experience.py`

Status: binding for the kit's second renderer. **The interaction design is decided and prototype-verified; build against it, don't re-design it.** The interactive exhibits were designed as standalone prototypes, interaction-tested in headless Chrome (desktop 1280 + mobile 390, before/after states shot), and their HTML/CSS/JS was then lifted verbatim into `render_experience.py`'s templates — the prototypes themselves are not shipped in the kit; the renderer embeds them.

**The prototype CSS/JS inside `render_experience.py` is canonical. The only permitted deltas are the shared page furniture (wayfinding chrome, stage container) and templating of the content strings.** Every bug below was already fixed during prototyping; do not reintroduce them: text selection during grid drag (`user-select:none` on `.fw-grid`), marker/cell-text collision (paper halo chip on `.you`), reading-panel strobe on drag (swap only on quadrant *change*), released-label overflow on mobile (the under-bar tick note, never an in-track absolute label), the tick gap (`.m-note-row{margin-top:-16px}`), `:last-of-type` does not select by class.

---

## 0. Law

The owner's rule, verbatim: **"Don't mistake animation for interactivity."**

- **Interaction** = the client ACTS and the artifact RESPONDS. That is the meal.
- **Animation** = seasoning. Every animated thing must be either (a) a response to a client action or (b) the stage's single narrative beat. Anything else gets cut.
- The wow-test for every stage: **what did the client DO here that they couldn't do with the PDF?** If the honest answer is "watched," the stage ships static.

## 1. Narrative frame — staged argument with free navigation (decided)

The experience is a sequence of **stages**, one per slide of the content file, grouped into the deck's acts plus front/back matter. One stage on screen at a time (JS mode). Native scrolling *within* a stage when content exceeds the viewport. **No scroll-triggered choreography of any kind. The page never moves except when the client navigates or scrolls natively.**

Why staged, not scroll-narrative:
1. Presenter-led in-room use needs discrete beats and keyboard advance (←/→), same muscle as a deck.
2. Scroll-narratives structurally invite scroll-triggered reveals — precisely the animation-mistaken-for-interactivity failure.
3. The interactive exhibits need the client to *stop and act*; a scroll flow encourages skimming past them.

The hybrid concessions: free navigation (jump anywhere via the argument bar or exec-summary links; nothing is gated), hash deep-links per stage (`#s4`), and the no-JS document is one continuous scroll (§8).

### Stage map of the shipped demo (16 stages, 1:1 with content blocks)

| # | id | slide archetype | interactive class |
|---|----|-----------------|-------------------|
| 1 | s1 | title | static |
| 2 | s2 | exec-summary | **argument map** (claim → jump) |
| 3 | s3 | section-divider | act opener, static |
| 4 | s4 | kpi (split) | **sliver drill** + beat |
| 5 | s5 | two-col stat-rail | evidence-on-demand |
| 6 | s6 | data (bars) | evidence-on-demand + beat |
| 7 | s7 | section-divider | act opener, static |
| 8 | s8 | journey | **explorable journey** |
| 9 | s9 | comparison + `xp-model` | **substitution model** (prototyped) |
| 10 | s10 | quote | static |
| 11 | s11 | section-divider | act opener, static |
| 12 | s12 | timeline | **time scrub** + beat |
| 13 | s13 | framework + `xp-plot` | **self-plot 2x2** (prototyped) |
| 14 | s14 | comparison | evidence-on-demand |
| 15 | s15 | closing | **personalized close** (reads state) |
| 16 | s16 | data (dense) | evidence ledger (drawer target) |

## 2. Architecture

- `python3 render_experience.py content/<deck>.md --brand <brand>` → `out/experience--<brand>.html`. **Single self-contained file, zero external requests, works from `file://`** (no fetch, no modules, no CDN, no webfonts beyond the brand stacks) — sharing it means opening or sending the file, nothing to serve. Imports and reuses `render_deck.py`'s parser and brand loader; the content grammar is never forked.
- Same brand yaml tokens (`brands/*.yaml`) → the same CSS custom properties as the deck (`--c-*`, `--f-*`, `--track-*`), plus the motion tokens (§7).
- **Content grammar extension — `xp-` keys, all optional, all ignored by `render_deck.py`** (the PDF renderer collects and discards them; adding them never changes the PDF):
  - `xp-goto: N :: sID` (exec-summary) — maps claim N to its evidence stage.
  - `xp-act: Label` (section-divider or first slide of an act) — names the act in the argument bar.
  - `xp-drill: Head :: body text` (repeatable, kpi split only) — rows of the sliver drill panel.
  - `xp-model: substitution :: default=100 :: range=20,500,10 :: mults=1.5,1.75,2` (comparison) — enables the model block; mults must sit inside the published range stated in the slide's own copy.
  - `xp-plot: self` (framework) — enables the self-plot layer + reading rail. Reading copy per quadrant: `xp-read: Quadrant :: reading` and `xp-move: Quadrant :: the move` (repeatable), `xp-src: Quadrant :: source line` — fact-checked and em-dash-rationed like all visible copy.
- **State** (`try/catch`-guarded localStorage, key `deck-xp:<deck-title>:<date>`):
  ```js
  state = { stage: 0, visited: {}, plot: {x, y, quadrant} | null,
            model: {n, m} | null, evOpened: {}, journeyStage: null }
  ```
  Persist on every mutation. The closing stage reads it (§5.15). "Clear" affordances reset their own piece; the closing offers a full reset — **and a reset must zero the in-memory state object before clearing storage** (any later save() re-persists the live object; "Start over" that doesn't start over is a trust breach in a shared-screen room).
- Body starts `class="nojs"`; the boot script swaps to `js` (progressive enhancement, §8).

The shipped `content/demo-ai-sales-transformation.md` carries all of these keys — it is the worked reference for the grammar. **Only `xp-` lines differ from a PDF-only content file; nothing the PDF renders changes.**

## 3. Wayfinding

- **Argument bar** (fixed top, 48px, paper ground, hairline bottom rule): left = deck short title (11px caps, `--track-label`); center = the act labels, each with per-stage tick squares (6px): current = ink, visited = `--c-primary` at rest, unvisited = `--c-rule`. Ticks and act labels are click targets (44px hit areas). Right = "n / 16".
- **Stage nav**: bottom-right Back / Next buttons (48px min, 1px ink border, rectilinear). Keyboard: ←/→ stage, Esc closes any drawer/panel, Home/End first/last stage.
- Stage transition: outgoing fades, incoming fades in with a 4px rise — 200ms `--ease-out`, that is all. **Never a slide/push/zoom transition** (that is a slideshow pretending).
- Hash routing: each stage sets `location.hash`; loading with a hash opens that stage. Exec-summary claim links are plain `#s4`-style anchors so they work in no-JS too.
- Mobile (<900px): act labels collapse to the current act name + the tick strip; Back/Next become a full-width bottom bar (`env(safe-area-inset-bottom)`).

## 4. Evidence-on-demand (one component, used everywhere)

Every sourced figure in the experience is a **live citation**:

- Markup: `<button class="ev" data-ev="mit-95">95%</button>` — ink text, dotted underline (`text-decoration-style:dotted`, `text-underline-offset:4px`), no other decoration. Never on more than the figure itself.
- Response: a bottom **drawer**: paper ground, 2px accent top rule, head 20px bold, body 16px/1.5, source line 13px muted; slides up 240ms `cubic-bezier(0.32,0.72,0,1)`; Esc or Close dismisses; focus moves in and back. One drawer element, re-filled per citation.
- Drawer content comes from the **appendix ledger** (the dense data slide): the renderer parses the appendix table into rows with slug ids holding study / finding / read-through. A `notes:` hedge on a slide renders inside its figure's drawer as the caveat line — this is where methodological honesty lives.
- Each drawer footer: "Full ledger →" linking the ledger stage; the target row gets a static `:target` tint (no animation).
- Auto-linking rule (deterministic): for each ledger row, extract its numeric token; on every stage, wrap occurrences of that token in visible body/exhibit text (not titles, not the ledger itself) in an `ev` button. `==x==` marks in content always link.
- The wow here: the PDF asserts; the experience lets the client **pull the receipt** — including the caveats that would otherwise be buried.

## 5. Per-stage interaction specs

Format per stage: CLIENT DOES → ARTIFACT RESPONDS; then build notes.

**5.1 s1 Title.** Nothing interactive. Title/subtitle/meta per deck title slide, plus one apparatus line (13px muted): "Interactive briefing · 4 acts · every number opens its source." No animation.

**5.2 s2 Exec summary — the argument map.** CLIENT: taps any of the four claims → RESPONDS: jumps to the stage carrying that evidence (the `xp-goto` map). Each claim row gets a quiet "see the evidence →" affordance (13px, primary, appears statically — not on hover-only). Figures in claim support text are `ev` buttons. No other motion.

**5.3/5.7/5.11 Act openers.** The divider slide rendered full-viewport (primary ground, paper type, per deck divider spec). Static. They give the room a breath; the argument bar marks the act change.

**5.4 s4 The 95/5 — sliver drill.** Renders the deck's split device exactly (hero 95% numeral, proportional split bar, counter tick-note — the `ks-*` CSS). BEAT (the stage's one): on first entry, the two segments draw left-to-right once — `scaleX` 0→1, `transform-origin:left`, 500ms `--ease-out`, 95 then 5 with an 80ms offset. CLIENT: taps the 5-sliver or the counter note (sliver hit area extended to ≥44px with a transparent `::after`; the note text carries the dotted affordance) → RESPONDS: a **magnifier panel** opens below the note: label line "The ~5%, magnified — what the value creators did differently" (13px caps tier + clause sentence-case), then the `xp-drill` rows (head 20px bold / body 16px ink / source 13px muted), each figure an `ev` button. Panel enters 200ms opacity + 8px rise, `--ease-out`. Two hairline leader lines from the sliver's edges to the panel's top corners flare the magnification honestly — **the bar's geometry never changes; magnification happens in the panel, never on the data.** Tap again / Esc closes.

**5.5 s5 Evidence rail.** The two-col stat-rail layout (rail values 44px sans bold lining; verbal pulls at the words tier). CLIENT: taps any rail value → RESPONDS: its `ev` drawer. Nothing else moves.

**5.6 s6 Bars.** The data archetype. BEAT: bars draw once on first entry, `scaleX` 500ms `--ease-out`, 80ms stagger. Values are `ev` buttons. Nothing else.

**5.8 s8 The journey — explorable.** The five-stage × four-lane grid per the deck slide, with the bracket row and the dark band. CLIENT: taps a stage column (header or cells; whole column is one target) → RESPONDS: that column focuses — grid columns re-template so the focused column gets ~2fr with full cell text, unfocused columns compress to ~0.7fr showing only their lane-cell first clauses (CSS `grid-template-columns` swap + a 150ms opacity swap on cell content; accept the reflow, no FLIP theater); the stage header marks visited (small ink tick). The dark band: while a focused stage sits under it, the band's label and cell render at full emphasis with the bracket text pulled adjacent — the client *standing in* those stages and seeing the firm blind is the beat, and it is client-driven, so it costs nothing from the animation budget. Prev/next stage arrows inside the exhibit (44px). `==stat==` marks are `ev` buttons. Tapping the focused column again returns to overview. Mobile: columns become an accordion (one stage open at a time, lanes stacked inside; same state object).

**5.9 s9 Substitution model — prototyped, canonical.** The comparison table renders above (per deck), then the model block. CLIENT: drags the AE slider (the `xp-model` range) and picks a multiplier from the published range → RESPONDS: the two proportional bars re-size (`scaleX`, 250ms `--ease-in-out`), the released-capacity tint segment and its tick-note re-anchor, and the note re-states the arithmetic: "**{released} seats released** — ≈{after} AEs plus AI cover the book your {n} cover today, with humans still in every loop." Math is `after = ceil(n/m)` — arithmetic only, and the source line says so: *"The seat math above is arithmetic on your inputs, not a study finding."* (Honesty rule: client inputs never dress up as research.) The caveat button opens its drawer. Writes `state.model = {n, m}`.

**5.10 s10 Quote.** Static. Full-stage, per deck quote spec.

**5.12 s12 Timeline — the scrub.** The phase bar with spans exactly proportional (deck geometry) and the gate marker. BEAT: on first entry the segments draw left-to-right once (500ms total, `--ease-out`) — the program's proportions are the message. CLIENT: drags the playhead (2px ink line, 16px square handle, pointer-captured) or taps anywhere on the bar → RESPONDS: playhead snaps on release to the nearest milestone (snap = 150ms `--ease-out` settle); the detail panel below swaps (150ms fade, swap-on-change-only) to the active phase: name, timeframe, description, **exit criterion** rendered as the panel's anchor line. At the gate the gate state activates: accent gate marker + the gate's callout text. Keyboard: ←/→ between snap points when the bar has focus. What the client does that the PDF can't: *feel* the phase proportions by dragging through them.

**5.13 s13 The 2x2 self-plot — prototyped, canonical.** Grid left, reading rail right (stacked on mobile, cell prose hidden — the rail does the talking). Today marker (primary square) and target marker (accent square) render per the deck. CLIENT: taps anywhere on the grid (or Enter + arrows — full keyboard path) → RESPONDS: their marker (outlined ink square + "You" paper chip) places with a 200ms scale-0.9 entrance; the rail swaps (150ms, on quadrant change only) to the quadrant's `xp-read` + **The move** (accent label tier, the `xp-move`) + source. Drag adjusts continuously; pointer capture held. "Clear my position" resets. Writes `state.plot`. **No drawn line between markers — doctrine §6.11: trajectory is plotted positions, never a drawn arrow.** The client drawing their own gap against today/target IS the exhibit.

**5.14 s14 Comparison table.** Static table per deck (highlight column); every figure an `ev` button. No time-toggle toy — the title already does that work.

**5.15 s15 The close — personalized (the consequence loop).** Reads `state`. If the client acted, a block above the decisions, "What you did with this argument" (13px caps label tier), up to three echo lines, each only if its state exists:
- plot: "You placed your organization in **{quadrant}**." (+ if quadrant ≠ the target quadrant, its `xp-move` line)
- model: "At your numbers, ≈{after} of {n} AE seats cover today's book at {m}× — {released} seats released through productivity."
- evidence: "You opened {k} of the {total} sources behind this argument." — **the denominator counts only what is actually citable in-artifact**; a denominator the user can never reach is a small lie.
Then the decisions verbatim from content. Below: **"Copy my read-out"** — clipboard payload (execCommand fallback chain): deck title/date, the echo lines, the decisions; toast "Copied — paste it into the follow-up." And "Start over" (full state reset, `window.confirm`, memory zeroed before storage cleared). If state is empty: decisions only, no empty-state scaffolding.

**5.16 s16 The ledger.** The appendix table rendered dense per deck, each row `id`-anchored, `:target` row tinted. This stage is also the drawer data source (§4). Closing line (13px muted): "Every number in this experience traces to one of these rows."

## 6. The two prototyped pieces — embedded verbatim

The 2x2 self-plot and the substitution model are the canonical implementations: tokens, type sizes, spacing, easings, ARIA (role="application" grid with keyboard path, `aria-live="polite"` response regions, `aria-pressed` segments, drawer focus management), reduced-motion blocks, and the mobile breakpoints are all final inside `render_experience.py`. Template the content strings; change nothing structural.

## 7. Motion doctrine

Tokens (mined from shipped best-practice motion standards, not invented):

```css
--ease-out: cubic-bezier(0.23, 1, 0.32, 1);      /* responses, entrances */
--ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);  /* on-screen morphs: bar re-size, playhead settle */
--ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);   /* the evidence drawer */
```

| thing | duration |
|---|---|
| press feedback (buttons/chips) | 120ms |
| panel/reading content swap | 150ms |
| marker placement, drill/panel entrance | 200ms |
| stage transition | 200ms |
| evidence drawer | 240ms |
| model bar re-size, playhead snap | 250ms |
| narrative beat (geometry draw) | 500ms, once per session |

Rules:
- **Everything under 300ms except the ≤5 narrative beats** (the shipped demo ships 3: s4 split draw, s6 bars draw, s12 phase draw). Beats play once per session (`state.visited`), render final-state on revisit and under reduced motion.
- Never `ease-in`. Never `scale(0)` (enter from 0.9–0.97 + opacity). Only `transform` and `opacity` animate; bar quantities via `scaleX` with labels outside the fill. CSS transitions, not keyframes, for anything re-triggerable (interruptible).
- **The never-animates list:** text and headings (no typing, no counting-up numerals — values swap instantly), anything on scroll, anything on hover-only (hover may tint, never move; gate hover with `(hover:hover) and (pointer:fine)`), bullets/list staggers, the wayfinding ticks, loops/marquees/pulses of any kind, page load beyond the current stage's single beat.
- `prefers-reduced-motion: reduce`: transform motion off everywhere, opacity swaps ≤150ms retained, beats render final state.

## 8. No-JS fallback + print

`body.nojs`: every stage `display:block` in document order — the complete argument reads top-to-bottom as one document. Banner under the title: "The interactive version needs JavaScript. What follows is the complete argument, readable top to bottom." Hidden: argument bar, nav, sliders, segmented buttons, drill/caveat buttons, "clear" links. Shown instead (renderer emits both; CSS picks): the static split device with counter note + the drill rows as a static list; the comparison table plus one worked example at the model defaults ("arithmetic, not a finding"); the fully expanded journey grid (deck layout); all phase details listed with exits; the 2x2 with today/target markers only; decisions un-personalized; drawer content rendered as footnote lines under each stage's source line. Print stylesheet = the no-JS view with page-breaks between acts — and **mobile media queries are scoped to `screen`** (print width ~A4 794px silently inherits bare `max-width` rules and amputates content; `@media screen and (max-width:...)` is the default discipline for any artifact that must also print). **The no-JS document must pass the deck's own craft gate on its static rendering.**

## 9. Craft carry-over (and what inverts)

- Type scale, spacing tokens, tracking tokens, caps budget (≤6 tiers/stage), numeral rules (≥20px = body sans bold lining, units at 0.55–0.58em), muted-is-metadata-only, ≤1 em-dash per stage body, accent budget (one meaning per stage) — all per `doctrine/design-doctrine.md` §6, enforced on the experience's DOM.
- Doctrine §6.A inverts **only** its responsive and interaction lines for this medium: breakpoints, fluid layout, hover/focus/touch states are required here (44px targets, visible focus, `env(safe-area-inset-*)`). Still banned, unchanged: icons, gradients, shadows-as-style, parallax, scroll-jacking, cream grounds, dark-mode variants.
- Desktop type = deck scale verbatim; <900px: 31→25 title tier, 44→31 value tier, 200-class display numerals →96 (stay on-scale).

## 10. GATE — the medium's own adversarial checks (run all four, evidence required)

1. **Wow-test, per interactive stage:** state in one sentence what the client DID that the PDF cannot. For the shipped demo: s2 jumped the argument · s4 pulled the 5% open · s8 walked the journey in their order · s9 ran their own numbers · s12 dragged through the program · s13 plotted themselves · s15 took their read-out away · everywhere opened sources. Any stage whose sentence is "watched X happen" fails and ships static.
2. **Interactivity-not-animation audit:** enumerate every CSS transition/animation in the shipped file (grep `transition|animation|@keyframes`). Each maps to a client action or is one of the ≤5 once-per-session beats. Anything else is deleted. Publish the count table in the gate note.
3. **Anti-tech-demo:** zero network requests after load (DevTools evidence); no scroll listeners driving visuals (grep `scroll` — allowed only for `scrollTo` on stage change); no parallax/gradient/icon/blur-glass/3D/cursor effects/sound; works from `file://`; one HTML file; opens in <1s.
4. **Honesty + craft:** all geometry data-true (split widths, phase spans, model bars = the arithmetic); client inputs never blend into published figures (the "arithmetic, not a finding" line present); every figure's drawer content matches the ledger; caveats reachable within one tap of their figures. Craft sweep (§9) on every stage's static render; keyboard-only full pass; 390px and 1440px shots per stage; no-JS full-document read-through.
