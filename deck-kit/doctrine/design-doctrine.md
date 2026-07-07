# Deck design doctrine — for any agent designing slides in this system

Status: binding for design work in this kit. Specs win over doctrine when assembling a finished spec; doctrine wins over your instincts everywhere else.

Who this is for: you, the coding/design agent, when you design a NEW slide or archetype (not when rendering existing content). It exists because an earlier version of this system's output was ruled "very clearly AI generated" by a design-literate reviewer despite clean typography. The tells were structural, and they are exactly the defaults an AI designer reaches for. This file is the override. It has since been hardened through four rounds of adversarial design review; the failure signatures found in those rounds are folded in below (§3 and §3b).

The one-line thesis: **consulting decks are graphic, not typographic.** A partner reads structured graphics (journeys, frameworks, spanning bands, annotated exhibits) as evidence that analysis happened. Beautiful text with hairlines reads as a language model with a stylesheet. Typography is the finish; structure is the design.

Worked example of everything below: `doctrine/journey-spec.md` (the journey archetype, designed from a rendered prototype) — see it rendered as the journey slide in `examples/demo-ai-sales-transformation--default.pdf`.

---

## 1. The density doctrine

Density variance is the human fingerprint. The AI tell is not emptiness or fullness — it is *uniformity*: every slide filling the same ~40-50% of the frame in the same silhouette (content top-left, void below, bar at bottom). Kill the uniform silhouette first.

Per-archetype body-zone fill targets (fraction of `.slide-body` height actually occupied):

| class | archetypes | target | note |
|---|---|---|---|
| graphic | journey, workstreams, framework, comparison, data (dense), kpi | >= 70% | the exhibit owns the stage; scale it up, never center-and-float |
| working | content, two-col, agenda, exec-summary | 55-80% | if body ends above 55%, merge the slide or promote to an exhibit |
| breather | quote, section-divider, title, closing | <= 40% | emptiness is the design; do not decorate it |

Deck-level rules:
- At least **one third of content-bearing slides must be graphic-class**. An all-bullets deck fails before anyone sees it.
- Never two consecutive slides with the same silhouette *and* the same fill class. After a dense exhibit, a breather or a differently-shaped working slide.
- Sparse content renders BIGGER (the `bar-chart--large` principle, e.g. 2 bars → 64px tracks), never small-plus-whitespace. If content can't be scaled up honestly, the slide doesn't exist.
- **The positional-void signature:** content occupying the top ~60% of the frame with a framed void below it — the void bounded by the slide's own furniture (footer, takeaway bar), so it reads as a deliberate empty box — is the single most reliable AI-slide silhouette. A void that appears on one slide is a layout bug; the same void appearing on several slides is the system's signature. Hunt it per slide AND per deck.

## 2. Decision procedures (not vibes)

**Shape → archetype.** Ask what the content IS before writing any bullet:
- A process, sequence of stages, or anything with a time/phase axis → `journey`, `timeline`, or `workstreams`, never numbered bullets.
- Two things contrasted attribute-by-attribute → `comparison` table (attributes as rows) — not `two-col` (two-col is for *parallel* arguments, not contrasts).
- One quantity across categories → `data` bars. One quantity that IS the message → `kpi`, huge.
- A claim about position in a space (2 dimensions) → `framework` 2x2.
- Entities with a per-stage or per-dimension breakdown → swim lanes (journey grammar), not nested bullets. Nested bullets deeper than one level = a diagram you refused to draw.
- Only argument-prose with no inherent structure earns `content`.

**Takeaway bar:** omit by default. Include only when the body is an exhibit whose reading is genuinely non-obvious from the action title. If the bar would restate the title, delete the bar. Hard cap: two takeaway bars per five consecutive slides. (The journey and workstreams archetypes reject `takeaway:` outright — annotations on the exhibit carry the message.)

**Laying out N items — anti-symmetric-grid rules:**
- N equal items in equal boxes is almost always a lie; content is never equal. Give the item that matters most more room, the highlight, or a spanning treatment — and mark it (accent, wash, bracket).
- **Unequal things must never render as equal boxes.** The hard case is time: phases of different length drawn as equal columns is a quiet falsehood. Time gets an axis, and spans are drawn proportional to duration (the timeline archetype's `axis:` + `span:` mode exists exactly for this). The same rule generalizes: if the underlying quantities differ, the geometry must differ.
- Prefer asymmetric splits when the two sides differ in kind: evidence 2fr / implication 1fr, not 1fr/1fr. Balanced 3v3 bullet columns are a tell; 4v2 that follows the actual weight of the material is design.
- Empty cells in a matrix are rendered honestly (em-dash in `--c-rule`), never padded with filler text to look complete. Fully-populated equal-length matrices smell generated.
- **One local judgment per slide**: exactly one element that deliberately breaks the slide's own grid — a spanning cell, a highlighted column, a bracket, an asymmetric split. Zero = template; two or more = noise.

**Accent budget (per slide):** accent appears on the head-rule tag + at most ONE meaningful element (highlighted stage/bar/cell/label). Accent must MEAN something — "this is where the deal is decided" — never "this needed color." If you can't say what the accent marks in one sentence, remove it. Structural darks use `--c-primary`; stats use `.stat` (bold primary); everything else is ink/muted/rule.

## 3. Forbidden moves (the deck-specific AI tells)

Each with the correct alternative — these are the defaults you will reach for; don't.

1. **Takeaway bar restating the action title.** → Omit the bar; the title is the takeaway. If an exhibit needs a read, annotate the exhibit (bracket, callout) at the point of evidence.
2. **Bullets for anything that has structure** (stages, lanes, contrasts, flows). → Draw the structure: chevrons, lanes, comparison rows, 2x2. Bullets are the last resort, max ~5, one nesting level.
3. **Content rendered at natural size, floating in the top half.** → Scale the exhibit to own the stage, or merge/kill the slide. No slide ships with an accidental empty lower third.
4. **Equal boxes for unequal things** (N symmetric columns/cards, 1fr everywhere, 3v3 bullet balance, equal-width phases of unequal duration). → Weight the layout by the material; give time an axis with proportional spans; highlight the one that matters; let cells be empty.
5. **Filled SmartArt-style chevrons / colored boxes with icons.** → Quiet tint chevron cells with angular paper seams (journey spec geometry); ONE accent stage; no icons, no emoji, ever. Semantic marking is done by lanes, labels, and position — not glyphs.
6. **Spending accent for decoration** (accent headers, accent rules everywhere, multicolor categories). → One accent meaning per slide. Category distinction uses structure (position, spans, weight), not a palette.
7. **Same silhouette three slides running.** → Re-sequence or re-shape: alternate exhibit / breather / table; vary where the mass sits in the frame.
8. **Softening the system** — shadows, gradients, rounded corners, tinted panels for "cards." → The discipline is paper, ink, hairlines, square corners. Depth comes from ink density (tint → rule → muted → ink → primary), never from effects.
9. **Repeating furniture invented for one slide onto every slide** (the death-by-consistency failure: brackets on everything, washes on everything). → Devices earn their place per slide; a device used on every slide becomes furniture and stops meaning anything.
10. **Force-fitting content into the nearest archetype.** → Compose from primitives instead (see the composition amendment below).

## 3b. Failure signatures from the adversarial gate (four rounds, learned the hard way)

These are the patterns a fresh adversary actually caught in this system's own output. Treat your defaults as guilty of each until the rendered screenshot proves otherwise.

1. **A repeated failure signature is itself the tell.** Any flaw that shows up twice across a deck — the same void, the same redundant annotation, the same misweighted grid — stops being a local mistake and becomes a machine fingerprint. Fixing instances is not enough; find and fix the generator (the CSS rule, the builder default, the habit).
2. **The positional void:** content in the top ~60% with a framed void below (see §1). The frame (footer, bar) makes the emptiness read designed-but-dead. Scale the exhibit, merge the slide, or reclass it as a breather.
3. **Frameworks/2x2s must PLOT something.** Four captioned quadrants is a labeled empty space — SmartArt with better typography. A 2x2 earns its place only when it plots a position ("we/they/the spend sits HERE") or a trajectory (today's position plus the destination the program moves it to). The framework archetype's `plot:` (today, primary mark) and `target:` (destination, accent mark on the washed quadrant) keys exist for exactly this; a framework slide using neither should be challenged. Trajectory is two plotted positions, never a drawn arrow (§6.11, and the arrow lesson below).
4. **Annotations that restate the title are takeaway-bar-equivalents.** The takeaway-bar rule (§2) generalizes to every annotation device: a bracket, gate note, or callout that says what the action title already says is the same redundancy in nicer clothes. Every annotation must add a reading the title doesn't carry.
5. **Geometry must be honest.** Bar spans, phase widths, and gate positions are measured against the stated values — a bar labeled 60% must be drawn at the 60% proportion of its scale; a week-8 gate on an 18-month axis sits at ~11%, not "about a quarter in." The adversary will measure your pixels against your numbers; do it first.
6. **Winner-washes must survive zebra striping.** State styles collide, especially in cloned/extended CSS: a highlight wash (`hl-col`, `hi-col`) that visually vanishes wherever a row-striping tint lands on the same cell means the winner column reads as noise every other row. Whenever two background-color systems can hit the same cell, define the precedence explicitly (striping turns OFF where a wash carries meaning) and check the render for the collision. Generalize: grep cloned CSS for state combinations that never fire or fight each other.

## 4. Reference anchors — "make it feel like THESE"

- **The journey slide** in `examples/demo-ai-sales-transformation--default.pdf` (the "shortlist is fixed before the first conversation" slide) — the target grade. Note what makes it read designed: chevron band with one accent stage; column wash falling from the accent stage; lanes of visibly different height and density; honestly empty cells; a dark spanning band that carries the argument; brackets instead of a takeaway bar; every number placed where it belongs in the structure.
- **The workstreams slide** in `examples/validation-first-8-weeks--default.pdf` — what composing from primitives looks like: four parallel streams of unequal span on a week grid, one dark converging stream, a quiet checkpoint hairline, the accent spent once on the decision gate, the gate annotation carrying the message instead of a takeaway bar.
- **The 2-bar data slide** in the demo PDF ("agentic AI pays only when the process is redesigned end to end") — one message, exhibit scaled to own the stage, accent on the winning bar, spans honest to the stated values.
- **The comparison slides** in the demo PDF — correct use of a table for a two-way contrast; the winner column wash with striping precedence handled; a spanning band row carrying the net-effect claim.
- **Anti-reference:** any slide that is tidy bullets under a serif headline, symmetric columns, a takeaway restating the title, and a half-empty frame. If your new slide resembles that silhouette, start over.

## 5. Self-check gate (run on EVERY slide before showing the user)

Render the slide (headless Chrome screenshot at 1280x720 — test by running, not imagining) and answer ALL of these. Any failure = iterate, don't ship:

1. **Structure test:** Cover the title. Does the body's *shape* alone tell you what kind of thinking happened (sequence, contrast, position, magnitude)? If the shape is "rows of text," it fails.
2. **Density check (measure, don't feel):** body-zone fill within the class target from §1? No accidental void below the content — especially the framed positional void (§3b.2)? (`master.html`'s overflow-report catches overflow; under-fill you must eyeball or measure from the screenshot.)
3. **Accent audit:** count accent occurrences. Tag + one meaningful element, and you can state the accent's meaning in one sentence. More = fail.
4. **Symmetry audit:** find the one deliberate grid-break (span, highlight, asymmetric split, annotation). None = template smell. More than one competing = noise. And check the inverse: nothing unequal rendered equal (equal boxes for unequal durations/quantities = fail).
5. **Annotation redundancy:** if a takeaway bar, bracket, gate note, or callout exists, does it say something the title doesn't? If not, delete it (§3b.4).
6. **Honest-geometry check:** measure every bar span, phase width, and marker position against its stated value (§3b.5). A labeled 60% drawn at 45% is a fail even if it "looks right."
7. **State-collision check:** if the slide uses a meaning-bearing wash (winner column, highlight cell), verify it survives row striping and any other background system on the same cells (§3b.6).
8. **Furniture check:** is every repeated element (rules, labels, brackets, washes) doing semantic work on THIS slide, or is it there because the last slide had it?
9. **Flip test (deck level):** screenshot the deck as thumbnails; do any three consecutive slides share a silhouette? Does any failure signature repeat (§3b.1)? Re-shape or re-sequence.
10. **The partner test:** would a design-literate partner flipping past this at one second per slide think a human made a local decision here? Name the decision they'd notice. If you can't name it, there isn't one.

Ship only what passes 1-10 in the rendered screenshot — never from the HTML source in your head.

---

## Doctrine amendment — composition over layouts (Curran Corrigan, 2026-07-06)

The owner's guidance, verbatim: *"A consulting team will need extreme flexibility in slidework — it is always created with shapes, tables, etc., not SmartArt or predefined layouts. That being said you will often reuse a layout as a starting point. The key is don't rely on layouts."*

**Rule: archetypes are starting points, never cages.** A locked archetype menu is SmartArt at a higher altitude — the exact tell this doctrine exists to kill. When the thinking has a shape no archetype fits, COMPOSE the slide from the system's primitives (tint cells, hairlines, chevrons, spanning bands, brackets, tracked labels, ledger rows, callouts) — the journey archetype was itself composed this way, and the workstreams archetype (see `content/validation-first-8-weeks.md`) is the worked proof that composing under this rule passes the gate.

**Implications:**
1. The designer's first question is "what structure does THIS thought have?", not "which archetype is closest?" Force-fitting content into the nearest archetype is a forbidden move (§3 #10).
2. Archetypes earn their place as reusable starting points — fork one and bend it freely; the tokens + furniture + tells-gate are the invariants, not the layout.
3. A composed slide must end up as renderable and self-editable as an archetyped one: give it a content grammar and a builder (the workstreams archetype is the template for how — axis + gate idiom from the timeline, lane grid from the journey, spanning bands from both).

## Lesson — question the device before iterating its geometry (2026-07-07)

The 2x2's trajectory arrow went through FOUR geometry iterations (anchoring, collision-avoidance, label placement) and passed the adversarial gate — and the owner rejected the slide "mostly because of the use of that arrow." The device itself was wrong; no amount of placement fixes a wrong element. (The framework archetype's `arrow:` key was removed and replaced by `target:` as a result.)

**Rule:** when an element needs repeated geometry/collision iterations to sit comfortably on a slide, STOP — that's the slide telling you the element doesn't belong. Ask first: does this device exist in real consulting pages? (Trajectory arrows across 2x2s mostly don't; a plotted position + a marked destination already carry "from here to there.") Iterate placement only AFTER the device has earned its existence.

Corollary for reviewers: gates must ask "should this element exist?" before "is this element well-placed?"

## 6. Craft layer — the register beneath structure

Structure decides what the slide is; craft decides whether it feels engineered.
"Unseen details compound": no single rule below is individually visible, and a
design-literate reader feels all of them at once. All values are executable;
most are checked by `deckcheck.py` (the kit's deterministic craft sweep), not
by judgment.

**6.1 Type scale.** All type comes from 11 / 13 / 16 / 20 / 25 / 31 / 44 / 55px
(+ display numerals ≥64 free: 64/120/200/300 in use). No off-scale sizes, ever.
Mapping: 11 labels/sources/footer, 13 captions/kickers/cell annotations, 16
body & cell text, 20 exhibit-internal heads and leads, 25 numbered-index tier,
31 action title, 44 divider/quote tier, 55 deck title. A slide should use ≤5
steps (footer furniture exempt).

**6.2 Hierarchy contrast.** Adjacent levels inside one block differ by ≥1 full
scale step PLUS one other dimension (weight Bold↔Regular — never
Medium↔Regular — or ink↔muted). Weight-only hierarchy at ~1.1:1 size is the
flatness tell.

**6.3 Numerals.** Any numeral ≥20px: body sans, bold, lining + tabular figures
— never the serif display face (Georgia has only old-style figures; digits of
uneven height read bookish, not engineered). Serif is for words. The % and
currency glyphs render at 55–60% of the digit size, baseline-aligned (not
superscripted). Comparators (>, <, ~, ±) stay full size — they carry meaning.

**6.4 Spacing scale & rhythm.** Spacing tokens: 4/8/12/16/24/32/48/64/96px
only (strokes, marker geometry, and <4px optical nudges exempt; fitted
exhibit sections are marked in deck.css). Within-group gap ≤ ⅓ of
between-group gap — equal spacing everywhere carries no grouping information.

**6.5 Leading & measure.** Body/cell text 1.4–1.5; titles 1.1–1.25; nothing
multi-line below 1.35. Measure ≤75ch; captions ≤90ch hard stop.
`text-wrap: balance` on headings and multi-line labels.

**6.6 Caps discipline.** Two tracking tokens only: `--track-meta: 0.08em`,
`--track-label: 0.11em`. Caps only for labels ≤3 words AND ≤24 characters;
anything longer is sentence case at the same size. Budget: ≤6 tracked-caps
tiers per slide, where a repeating rail of like-for-like labels (stage
numbers, lane labels, table headers) counts as ONE tier; footer furniture
exempt. KPI labels and 2x2 axis captions are clauses → sentence case, never
caps.

**6.7 Alignment (optical, verified on the render).** Two horizontally
adjacent peer elements share exactly one of: cap-line, baseline, or anchoring
hairline (flex `align-items: baseline` for single-line pairs; uniform
padding-top + flex-start for stacked cells). Every hairline starts and ends
on a column or content edge — never mid-air. Geometric centering is a
starting point; if a 200% crop shows it off, nudge it.

**6.8 Color craft.** Neutrals stay slate-tinted toward primary (protect in
new brand files: 0.005–0.015 chroma of the brand hue, one temperature per
deck). Muted is metadata-only (sources, axis captions, footer); content-
bearing secondary text is ink at a smaller scale step. Never gray text on
accent/primary fills — paper or a tint of the fill's own hue. Body contrast
≥4.5:1.

**6.9 Copy craft.** ≤1 em-dash per slide body (footer and honest-empty `—`
cells exempt). Source lines carry citation, n, date — nothing else;
methodological hedges go to `notes:`. Never invent a pseudo-stat (a hedge or
adjective dressed as a rail value); if the value has no number and no noun,
it is not evidence. Copy self-audit before ship: re-read every visible
string; rewrite anything fake-precise or LLM-thoughtful.

**6.10 Craft gate (extends §5; run after the structure checks).**
(a) 200% crops in three places — a numeral, a text block, one alignment seam
— and READ them (a screenshot you didn't read doesn't count);
(b) squint test: primary/secondary/groupings still rank;
(c) `deckcheck.py` passes (scale membership, spacing tokens, tracking
tokens, caps length + tier count, em-dash ration, numeral face);
(d) device-existence question, before any placement iteration: does this
element exist on real consulting pages? (See the arrow lesson — if a device
needs repeated geometry fixes, the device is wrong.)

**6.11 Quantities are drawn, ranks are typeset.** When two numbers form one
statistic (a share of a whole, a before/after), their SIZE relationship must
be geometrically honest: one proportional device (split bar, scaled bars),
never two display numerals at an arbitrary type-size ratio. Typography ranks
(hero vs support); geometry measures. Corollary: trajectory on a 2x2 is two
plotted positions (today: primary mark; destination: accent mark on the
washed quadrant), never a drawn arrow.

### 6.A Do-not-import list (web-idiom rules that do NOT transfer)

- Motion/interaction anything: easing, springs, hover/focus/loading states,
  touch targets. Static print idiom. (The experience renderer inverts exactly
  these lines — see `doctrine/experience-spec.md` §9 — and nothing else.)
- Responsive/adaptive: breakpoints, `clamp()` fluid type, container queries.
  The page is fixed 1280×720.
- Web platform hygiene: FOUT, Core Web Vitals, dark mode, z-index scales,
  icon libraries (icons stay banned outright).
- Web-marketing furniture: hero stacks, CTAs, logo walls, bento grids.
  Analogize the *rationing* ideas only.
- Inverted defaults: the web's absolute em-dash ban → decks *ration* (§6.9);
  "never pure #FFFFFF" → our white paper ground is the deliberate anti-cream
  move; keep it.

## Lessons — the experience gate (2026-07-07, from gating the second renderer)

These came out of the adversarial gate on `render_experience.py`'s interactive
output (spec: `doctrine/experience-spec.md`); they bind any interactive
artifact built in this system:

1. **State resets must zero memory before clearing storage** — any later save() re-persists the live object; "Start over" that doesn't start over is a trust breach in a shared-screen room.
2. **Scope mobile media queries to `screen`** — print width (~A4 794px) silently inherits `max-width` mobile rules and amputates content; `@media screen and (max-width:...)` is the default discipline for any artifact that must also print.
3. **Honest denominators** — "you opened N of the 10 sources" must count only what is actually citable in-artifact; a denominator the user can never reach is a small lie.
4. **The interactivity audit works as a gate**: every transition traced to a listener; 3 sanctioned narrative beats; zero autonomous motion — this is the enforceable form of "don't mistake animation for interactivity."
