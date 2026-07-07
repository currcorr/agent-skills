# Deck journey archetype — the worked composition example

> **Why this file is in the kit.** The `journey` archetype is already built into `render_deck.py` and `layout/deck.css` — you don't need this spec to use it (the block grammar is in README.md). It is here as the **worked example of how a slide gets designed in this system**: diagnosis of what reads AI-generated → design rationale with every choice argued → content grammar → verbatim CSS → exact markup → integration steps. When you design a new archetype or compose a bespoke slide, produce this. Every choice below was rendered and eye-checked in a prototype before being specced — design by running, not imagining.

The founding critique this spec answered, from a design-literate reviewer of the system's earlier all-typographic demo: "Could be worse on the design but still very clearly AI generated." Part 1 explains why. Part 2 is the fix's first installment: the `journey` archetype, specced verbatim from a working prototype. Where this file and an assembling agent's instinct disagree, this file wins.

---

## Part 1 — Why the earlier demo read AI-generated (ranked)

All twelve slides of the earlier demo were rendered in two brands and reviewed as images.

**1. The system was typographic, not graphic.** Eleven of twelve slides were text under a serif headline. The only exhibit form in the whole deck was a horizontal bar ledger, used twice, identically. Real consulting pages encode the *thinking* in structure: journey maps, process chevrons, swim lanes, 2x2s, annotated frameworks, spanning brackets. A partner reads structure as evidence of analysis; tidy hairlines around bullets read as "a language model laid out its paragraph." This is the root cause; the rest are aggravators.

**2. Uniform slide rhythm — every slide had the same density map.** Content huddled in the top 40% of the frame; the lower half was void; the takeaway bar floated at the bottom. Six slides shared this exact silhouette. Flip through fast and every page is the *same page*. Human decks alternate: a dense exhibit, a breather, a wall-of-table, a single number. Density variance IS the human fingerprint.

**3. The takeaway bar on everything, restating the action title.** The title already stated the so-what as a full sentence, then a labeled TAKEAWAY bar said it again in bold. Same position, same label, six slides running. Double-stating the message in fixed furniture is the single most template-smelling pattern there is.

**4. Exhibits didn't own their stage.** A 2-bar chart occupied a 250px strip and left 300px of white below; a 3-phase timeline was three text columns with 11px squares and a half-slide of air under it. Generated layouts render content at its natural size and stop; designed layouts size the exhibit to the frame (or admit the slide is half-empty and merge it away).

**5. No local judgment anywhere — perfect symmetry, no annotation layer.** The two-col slide balanced 3v3 bullets; nothing spanned columns; there were no callouts, no brackets, no "this cell is the point" marks, no deliberately empty cells. Every element obeyed the global grid and no element showed a decision made for *this slide only*. Humans leave fingerprints: a highlighted column, an asymmetric split, an annotation that cuts across the structure.

(Confirmed across brands: the second-brand render shared all five tells — it was the layout system, not the skin.)

---

## Part 2 — The `journey` archetype

### Design rationale (decisions and why)

- **Stage band: flat chevron cells, not filled SmartArt chevrons and not plain columns.** Chevrons are *the* consulting journey idiom, but PowerPoint's default filled-chevron strip is itself an AI/template tell. Resolution: quiet tint-filled cells clipped to chevron geometry, separated by constant 10px angular paper seams, sitting on the same grid as the lanes below (pixel-exact column alignment — prototyped both ways; flex-overlap interlock drifts up to ~5px against the lanes, grid + notch-both-sides does not). Direction reads from the seams; ink discipline holds.
- **One accent stage = the moment that matters.** Exactly one stage may carry the accent fill (paper text on `--c-accent`), consistent with the house rule's "one highlighted bar/phase." Its column continues downward as a `--c-tint` wash through every lane, so the moment reads as a full-height column, not a colored box.
- **Swim lanes with deliberately varied density.** Lanes are grid rows under the stage band: full-width hairline rules (first rule in ink, table-style), 104px label gutter with tracked-uppercase micro-labels. Cells hold 1-3 short lines; **empty cells render an em-dash in `--c-rule`** — visibly, honestly empty. A journey map with every cell filled to equal length is tell #5 again.
- **Spanning band lane.** A lane whose cells span multiple stages (in the demo: Seller visibility, "Dark" spanning stages 1-3 as a filled `--c-primary` band with paper text vs "Visible" spanning 4-5 on paper with an ink top rule). Spanning cells are the strongest anti-uniform-grid move on the slide and carry the analytical claim graphically.
- **Bracket annotations, not a takeaway bar.** Below the lanes, upward-opening U-brackets (1px ink) span stage ranges with a tracked-caps head + muted detail line. The brackets ARE the so-what, placed where the evidence is. **The journey slide omits the takeaway bar by default** (see prescriptions).
- **Emotion/friction curve: cut.** For a partner-selection journey the insight is the visibility divide, not sentiment; a curve would be decoration. The band lane + brackets encode the same judgment with more precision. (The lane grammar below supports adding a sentiment lane as text if content ever earns it.)
- **Pain/friction marking: a lane, not icons.** "What decides it" is its own lane; the lane label does the semantic work. No emoji, no icon fonts, no per-cell glyphs. Stats inside cells use the house `.stat` treatment (bold, `--c-primary`).
- **Accent discipline on this slide:** accent = the head-rule tag + the one highlighted stage. Nothing else. Primary (slate/navy) = the dark band + stats. Ink = brackets and rules.

### Content block grammar (what the author writes)

````
```slide
archetype: journey
kicker: How buyers choose
title: The shortlist is fixed before the first conversation: buyers now run three of five stages on AI research alone
highlight: 3
source: G2 buyer survey, n=1,076, March 2026; Gartner 2026 projections; house five-phase buying journey
---
stages:
1. Awareness :: problem sensing
2. Understand need :: solution mapping
3. Define criteria :: the shortlist forms
4. Evaluate options :: first seller contact
5. Validate & select :: commit

lane: Buyer actions
1: Senses underperformance; runs educational research to frame the problem
2: Names the problem; asks an AI assistant to map solutions and candidate partners
3: Sets selection criteria; has AI score the market and draft the shortlist
4: Invites the shortlist to respond; compares proposals with decision makers
5: Validates references and commercials; signs

lane: Where they look
1: Peer networks, industry press
2: ==51%== start with an AI chatbot, not Google — up from 29% in 2025
3: AI-synthesized vendor comparisons; analyst notes as tie-breakers
4: Your partners, proposals, orals
5: References, procurement

lane: Seller visibility
1-3!: Dark :: No calls, no RFIs — the firm cannot see this work happening
4-5: Visible :: First contact arrives with the shortlist already fixed

lane: What decides it
2: Whether the machine can find and cite your point of view
3: ==69%== chose a different vendor than planned on AI guidance; ~33% bought a previously unfamiliar firm
5: Whether stage-4 claims survive procurement's own AI check

bracket: 1-3 :: Pre-contact zone :: ~70% of the journey is complete before a seller knows the deal exists. Being findable and citable to the buyer's AI is now the top of the funnel.
bracket: 4-5 :: Traditional selling starts here :: Against criteria and a shortlist the firm did not shape.
```
````

**Parse rules (renderer):**

- `stages:` opens the stage list; each following `N. Name` or `N. Name :: sub` line defines stage N (3-6 stages valid; error outside that range). `Name` → `.j-stage-name`; text after `::` → `.j-stage-sub` (optional, omitted if absent). The label `Stage N` is generated, not written.
- `highlight: N` (header key, optional) — stage N gets the accent chevron and its lane cells get the `hi-col` wash. Absent → no accent stage, no wash. Error if N is not a defined stage.
- `lane: Label` opens a lane. Lane label breaks to multiple lines at word boundaries automatically (the CSS gutter is 104px); author writes it plainly.
- Inside a lane, `N: text` fills the cell for stage N. **Omitted stage numbers become empty cells** (`.j-cell.empty`, rendered as `—`). Duplicate N in one lane = error with file:line.
- `N-M: Label :: text` — a spanning cell from stage N through M, rendered as `.j-band` with `grid-column: {N+1} / {M+2}` (gutter is track 1). The part before `::` becomes the `.b-label` micro-caps; after it the body text. A `!` suffix on the range (`1-3!:`) renders the filled treatment (`.j-band.dark`); without `!` the quiet treatment (`.j-band.lit`). A lane mixing spanning and per-stage cells is an error (keeps the geometry sane).
- `bracket: N-M :: Head :: text` (0-3 allowed, after the lanes) — U-bracket spanning stages N-M; `Head` → `.j-bracket-head`, `text` → `.j-bracket-text`. No brackets → the bracket zone is omitted entirely.
- Inline markdown per house `inline_md()`, plus one journey-local extension: `==text==` → `<span class="stat">text</span>`.
- `takeaway:` is **not** an accepted key for `journey` (SLIDE_KEYS omits it — fails loudly, by design; the brackets carry the message). `source:` and `subtitle:` accepted as usual.
- Degradation: minimum viable block is `stages:` + one lane; everything else is optional. 4 or 6 stages just change the track count (`repeat(N, 1fr)`).
- Validation: at least one lane required; lane count 2-5 (6+ will not fit at these type sizes — error, suggest splitting the slide).

### Verbatim CSS (lives in `layout/deck.css` under the `/* ---- journey ---- */` section)

The renderer emits a `style="grid-template-columns:104px repeat(N,1fr)"` inline override on `.j-stages`, `.j-lanes`, `.j-brackets` only when N != 5.

```css
/* ---- journey: stages + swim lanes + brackets ---- */

.journey { width: 100%; }

/* stage band: flat chevron cells on the same grid as the lanes below.
   Each cell is notched 10px on both slanted edges, producing a constant
   10px angular paper seam between stages while grid tracks stay exact. */
.j-stages { display: grid; grid-template-columns: 104px repeat(5, 1fr); }
.j-stage {
  grid-row: 1;
  position: relative;
  background: var(--c-tint);
  padding: 9px 12px 10px 24px;
  clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%, calc(100% - 10px) 100%, 0 100%, 10px 50%);
}
.j-stage.first { clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 50%, calc(100% - 10px) 100%, 0 100%); padding-left: 14px; }
.j-stage.last  { clip-path: polygon(0 0, 100% 0, 100% 100%, 0 100%, 10px 50%); }
.j-stage-num { font-size: 10px; font-weight: 700; letter-spacing: var(--track-label); text-transform: uppercase; color: var(--c-muted); }
.j-stage-name { font-size: 15px; font-weight: 700; margin-top: 2px; }
.j-stage-sub { font-size: 10.5px; color: var(--c-muted); margin-top: 2px; }
.j-stage.hi { background: var(--c-accent); }
.j-stage.hi .j-stage-num, .j-stage.hi .j-stage-sub { color: var(--c-paper); opacity: 0.85; }
.j-stage.hi .j-stage-name { color: var(--c-paper); }

/* lane grid */
.j-lanes { display: grid; grid-template-columns: 104px repeat(5, 1fr); margin-top: 14px; }
.j-lane-label {
  font-size: 10px; font-weight: 700; letter-spacing: var(--track-label);
  text-transform: uppercase; color: var(--c-muted);
  padding: 10px 14px 10px 0; line-height: 1.45;
}
.j-cell { font-size: 12.5px; line-height: 1.42; padding: 10px 16px 12px 0; }
.j-row-rule { grid-column: 1 / -1; border-top: 1px solid var(--c-rule); }
.j-row-rule.first { border-top: 1px solid var(--c-ink); }
.j-cell .stat { font-weight: 700; color: var(--c-primary); }
.j-cell.empty { color: var(--c-rule); }
.j-cell.hi-col { background: var(--c-tint); padding-left: 10px; padding-right: 12px; margin-right: 2px; }

/* visibility band: spanning cells */
.j-band { font-size: 11px; line-height: 1.4; padding: 8px 16px 9px 10px; }
.j-band .b-label { font-size: 10px; font-weight: 700; letter-spacing: var(--track-label); text-transform: uppercase; display: block; margin-bottom: 2px; }
.j-band.dark { background: var(--c-primary); color: var(--c-paper); margin-right: 2px; }
.j-band.dark .b-label { color: var(--c-paper); opacity: 0.8; }
.j-band.lit { border-top: 1px solid var(--c-ink); }

/* bracket annotations */
.j-brackets { display: grid; grid-template-columns: 104px repeat(5, 1fr); margin-top: 16px; }
.j-bracket { position: relative; padding-top: 10px; margin-right: 8px; }
.j-bracket + .j-bracket { margin-left: 8px; margin-right: 0; }
.j-bracket::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 7px; border-left: 1px solid var(--c-ink); border-right: 1px solid var(--c-ink); border-top: 1px solid var(--c-ink); }
.j-bracket-head { font-size: 10.5px; font-weight: 700; letter-spacing: var(--track-label); text-transform: uppercase; margin-top: 4px; }
.j-bracket-text { font-size: 11.5px; line-height: 1.4; color: var(--c-muted); margin-top: 3px; max-width: 560px; }
```

Prototype-to-system deltas applied during assembly (kept here because they generalize):
- The prototype used `:nth-child(1..5)` + `grid-column` per stage. In the system, emit `class="j-stage first"` / `class="j-stage last"` on the end cells and an explicit `style="grid-column: {i+1}"` on every stage cell (auto-placement with a locked grid-row mis-places cells that follow an explicitly placed one — hit this in prototyping; do not rely on auto-flow).
- The slide-body top padding on journey slides is 22px (system default is 26px): `.slide--journey .slide-body { padding-top: 22px; }`.

### Exact markup structure (what the builder emits inside `.slide-body`)

```html
<div class="journey">
  <div class="j-stages">
    <div class="j-stage first" style="grid-column:2"><div class="j-stage-num">Stage 1</div><div class="j-stage-name">Awareness</div><div class="j-stage-sub">problem sensing</div></div>
    <!-- ... one per stage; the highlighted one adds class "hi" ... -->
    <div class="j-stage last" style="grid-column:6">...</div>
  </div>

  <div class="j-lanes">
    <div class="j-row-rule first"></div>          <!-- ink rule opens the table -->
    <div class="j-lane-label">Buyer actions</div>
    <div class="j-cell">...</div>                  <!-- 5 cells, in stage order -->
    <div class="j-cell hi-col">...</div>           <!-- highlighted stage's cell -->
    <div class="j-cell empty">—</div>              <!-- omitted stage number -->

    <div class="j-row-rule"></div>                 <!-- hairline between lanes -->
    <div class="j-lane-label">Seller visibility</div>
    <div class="j-band dark" style="grid-column: 2 / 5;"><span class="b-label">Dark</span>No calls, no RFIs — ...</div>
    <div class="j-band lit" style="grid-column: 5 / 7;"><span class="b-label">Visible</span>First contact ...</div>

    <div class="j-row-rule"></div>                 <!-- closing rule after last lane -->
  </div>

  <div class="j-brackets">
    <div></div>                                    <!-- gutter spacer -->
    <div class="j-bracket" style="grid-column: 2 / 5;">
      <div class="j-bracket-head">Pre-contact zone</div>
      <div class="j-bracket-text">~70% of the journey ...</div>
    </div>
    <div class="j-bracket" style="grid-column: 5 / 7;">...</div>
  </div>
</div>
<div class="source-line">Source: ...</div>
```

Wrapped in the standard frame: `head_html(slide, deck)` before, `foot_html(deck, page)` after, **no `takeaway_html`**. Grid-column math: stage N occupies track N+1; a span N-M is `grid-column: {N+1} / {M+2}`.

### Integration notes for `render_deck.py` (all applied; the pattern for any new archetype)

1. Add the name to `ARCHETYPES`.
2. `SLIDE_KEYS["journey"] = COMMON_KEYS | {"title", "subtitle", "source", "highlight"}` — deliberately no `takeaway`.
3. Write `build_journey(path, slide, deck, page)` following the `build_comparison` pattern: `require(path, slide, "title")`, `require_body(path, slide)`, then a dedicated line parser for the grammar above (the body is line-oriented; do not run it through `parse_blocks`). Every parse failure goes through `err(path, line_no, msg)` so errors keep the file:line contract.
4. Register in `BUILDERS`.
5. Stage count N != 5: emit `style="grid-template-columns:104px repeat({N},1fr)"` on `.j-stages`, `.j-lanes`, `.j-brackets`.
6. Inline text: run `inline_md()` then replace `==(.+?)==` with `<span class="stat">\1</span>`.
7. The overflow-report script in `master.html` covers any new archetype automatically (it checks `.slide-head`/`.slide-body` clipping generically). With 4 lanes + 2-line title + brackets the prototype has ~20px of slack; the layout check will catch content-driven overflow.
8. Add the block grammar to README.md's archetype table.
9. Acceptance: render the demo deck in both brands and compare the new slide against the prototype render — pixel-close in the default brand (the only sanctioned differences: footer page number and brand-token deltas).

---

## General prescriptions from the diagnosis (whole-system; all now live in doctrine/design-doctrine.md)

1. **Takeaway bar is opt-in, not default.** A slide gets a takeaway bar only when the body is an exhibit whose message is not already the action title. If title and takeaway would say the same thing, omit the bar. Never more than two takeaway bars in any consecutive five slides.
2. **Per-archetype density targets.** Graphic archetypes must fill >=70% of the body zone's height; breathers stay under 40%. The failure mode to kill is the 50%-everywhere deck. If a content slide's body ends above 55% of the zone, either promote the content into an exhibit archetype or merge the slide.
3. **Every deck needs at least one third of its content slides in a graphic archetype.** An all-`content`/`two-col` deck should fail review before anyone sees it. Diagrams encode analysis; bullets report it.
4. **Exhibits scale to own the stage.** The `bar-chart--large` pattern (renderer-decided size-up for sparse exhibits) is the norm for every exhibit type: sparse content renders bigger, never smaller-plus-whitespace.
5. **One local judgment per slide.** Each content-bearing slide should contain exactly one element that breaks its own grid deliberately: a spanning cell, a highlighted column, a bracket annotation, an asymmetric column split. Zero = template smell; two-plus = noise. The accent must attach to that judgment and nothing else.

Companion doctrine: `doctrine/design-doctrine.md`.
