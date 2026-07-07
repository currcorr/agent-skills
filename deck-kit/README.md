# deck-kit — self-editable consulting deck system

Content and design are separated: you edit a markdown file, one command renders it through a locked layout system in any brand, headless Chrome prints the PDF. The same content file also renders as a second output — a self-contained interactive HTML experience (see below). Stdlib Python only — no pip installs. Feeding this kit to a coding agent? Point it at `AGENTS.md`.

## The 60-second loop

1. Edit a deck's content file in `content/<deck>.md` (plain text — change a bullet, a title, a number). Start from `content/starter-template.md` or copy the full-scale reference `content/demo-ai-sales-transformation.md`.
2. Render (from the kit root):

   ```
   python3 render_deck.py content/<deck>.md --brand default --pdf
   ```

3. Open `out/<deck>--default.pdf`. Done. Drop `--pdf` for HTML only; `--brand stripe` (or any file in `brands/`) restyles the same content completely. PDF needs any Chrome/Chromium installed; without one you get the self-contained HTML and can print to PDF from a browser.

Content errors fail loudly with a `file:line` message and never render a broken slide — fix the line it names and re-run. This copy of the kit ships without the `examples/` renders to keep the repo lean — the reference examples render locally in under a minute: the two shipped decks (`render_deck.py content/<deck>.md --brand default --pdf`) and the interactive experience (`render_experience.py content/demo-ai-sales-transformation.md --brand default`).

## Content format

A deck file is YAML-ish frontmatter (title, client, date, author, confidentiality, optional logo override) followed by one fenced block per slide. Lines between slides starting with `#` are comments.

````
```slide
archetype: content
kicker: Section label
title: Action title stating the takeaway as a full sentence
takeaway: The one-line so-what shown in the bar at the bottom
source: Where the numbers came from
---
- bullet (max ~5 per slide; **bold** and *italic* work)
  - sub-bullet
```
````

Keys go above the `---`, body below it. Fifteen archetypes:

| archetype | body |
|---|---|
| `title` | none — uses frontmatter meta |
| `exec-summary` | 3-4 numbered findings, `Bold lead statement :: supporting line` — answer-first, pyramid-principle |
| `agenda` | bullets, `Item :: optional detail` |
| `section-divider` | none — `title:`, optional `subtitle:`/`label:` (auto "Part N"; use `label: Appendix` for backup sections) |
| `content` | bullets and/or paragraphs |
| `two-col` | two `## Column heading` sections; optional `split: 2-1` for asymmetric column weights (evidence/implication). A heading flag turns a column into an exhibit: `## Heading :: stat-rail` (bullets `value :: one-line claim` render as a ledger of large pulled numbers; a value with no digit is a verbal pull and renders one scale step down) or `## Heading :: steps` (bullets become stacked step cells with arrows; a trailing bold paragraph is the close caption) — flagged columns stretch so both end together |
| `data` | bar bullets `Label :: 60%+ :: highlight` or a markdown table; `dense: true` for appendix exhibits (smaller type, more rows), `label-width: <px>` widens the bar-label column |
| `kpi` | 1-3 stats, `Value :: label [:: highlight]` — big flat numbers, left-aligned; a single stat renders huge. Split mode: exactly one hero stat plus one `Value :: label :: counter` stat, both percentage shares of one whole (must sum to ~100) — renders as ONE proportional device: hero numeral, a split bar drawn to the true proportions, and the counter share as an accent tick-note (geometry carries the quantity, typography carries the rank) |
| `framework` | a 2x2: `x-axis:`/`y-axis:` keys, four `## Quadrant title [:: highlight]` cells (order TL, TR, BL, BR) with 1-2 plain lines each; the highlighted quadrant takes the tint wash. Optional `plot: Quadrant :: label` (today's position, primary marker) and `target: Quadrant :: label` (the destination, accent marker) — trajectory is two plotted positions, never a drawn arrow |
| `quote` | the quote as plain text; `attribution:` key |
| `timeline` | bullets `Label :: timeframe :: description [:: highlight]` (2-6 phases, full-height columns). Axis mode (`axis: W0 :: M18`) draws a proportional phase bar on a time axis instead: each phase adds `:: span: N` (width weight — durations to scale) and optionally `:: exit: deliverable` (one ledger lane row per phase below the band); `gate: 11% :: Week 8 :: callout text` places the accent decision marker on the axis (no `highlight` in axis mode — the gate carries the accent) |
| `journey` | stages + swim lanes + brackets: `stages:` with `N. Name :: sub` lines, `lane: Label` with per-stage `N: text` cells (omitted stages render as honest em-dashes) or spanning `N-M: Label :: text` bands (`N-M!:` = filled dark), 0-3 `bracket: N-M :: Head :: text` annotations, `highlight: N` accents one stage, `==text==` marks a stat. No `takeaway:` by design — brackets carry the message. Spec: `doctrine/journey-spec.md` |
| `workstreams` | parallel streams on a week grid, converging on a decision gate: `weeks: N` sets the columns (4-12); each `stream: Label` takes exactly one `A-B: text` bar spanning weeks A-B (`A-B!:` = the dark converging stream, at most one); `checkpoint: W :: text` hangs a quiet hairline at end of week W; `gate: W :: Head :: text` places the accent gate line + annotation; `==text==` marks a stat. No `takeaway:` by design — the gate annotation carries the message |
| `comparison` | a markdown `\| pipe \| table \|`; optional `highlight-col: N` washes the winner column. A 2-cell row in a ≥3-column table (`\| Net effect \| text \|`) renders as a spanning band row — the second cell spans all data columns |
| `closing` | bullets; `contact:` key. Bullets `decision :: owner :: when` become a DECISION / OWNER / WHEN ledger; `—` or blank renders as an honest empty cell |

## The second output — the interactive experience

The same content file renders as one self-contained interactive HTML document:

```
python3 render_experience.py content/<deck>.md --brand default
```

Output: `out/experience--<brand>.html` — a single file, zero external requests, works from `file://`. Sharing it means opening or sending the file; there is nothing to serve. It reuses `render_deck.py`'s parser and brand tokens, so the PDF and the experience never drift. Optional `xp-` keys in the content file drive the interactive layer (drill panels, the what-if model, the self-plot 2x2, act labels, claim→evidence jumps); the PDF renderer ignores them entirely, so adding them never changes the PDF. The shipped demo content carries the full `xp-` grammar as the worked reference.

The interactivity doctrine applies: **don't mistake animation for interactivity** — every animated thing is either a response to a client action or one of at most a handful of once-per-session narrative beats, and every interactive stage must answer "what did the client DO here that the PDF couldn't?" The full spec (stage grammar, motion tokens, no-JS/print fallback, the gate) is `doctrine/experience-spec.md`.

## The craft check

`python3 deckcheck.py` (from the kit root, after rendering) runs the deterministic half of the craft gate against `layout/deck.css` and every rendered deck in `out/`: type-scale membership, spacing tokens, tracking tokens, caps length and tier budget, em-dash ration, numeral face. It prints a per-slide summary and exits non-zero with `file:line` on any violation; `DECKCHECK-OK` is the pass signal. The judgment half of the gate (structure, density, honesty) stays in `doctrine/design-doctrine.md` §5-§6.

## Adding a brand

Brands are single YAML files in `brands/` — palette (primary / ink / paper / accent / muted / rule / tint), type stacks, logo text, accent-usage rules. Copy `default.yaml` and edit, or point an agent at a client website or PPT template with the style-rip procedure (`doctrine/style-rip.md`) to extract one and render a 3-slide approval sample. `stripe.yaml` is a real extraction from stripe.com's shipped CSS — the proof of the pattern.

Optional token dimensions (every one falls back, so minimal brand files keep working — `default.yaml` documents them in comments): `palette.chart` (series 1..4), `positive`/`negative`, `accent-2`, `divider-ground`/`divider-ink`, `logo.image` (base64-embedded asset), `type.files` (@font-face for licensed faces — output is only self-contained when unset).

## What needs an agent vs what never does

**Never needs an agent:** editing content files, re-rendering, swapping brands, reordering slides, changing frontmatter — the whole daily loop.

**Needs an agent:** new slide archetypes (`layout/deck.css` + builders in `render_deck.py`), style rips for new clients, changes to the furniture (footer, takeaway bar, tag), and anything in `layout/` — the layout is locked on purpose so decks stay consistent. Agents: read `AGENTS.md` first, and `doctrine/design-doctrine.md` before designing anything new.

## Design discipline (why it looks the way it does)

Paper ground, ink type, hairline rules, square corners. No gradients, no shadows, no icons, no emoji. The accent color appears only on the tag, the takeaway label, and at most one highlighted element per slide. Beneath the structure sits a locked craft layer (`doctrine/design-doctrine.md` §6): a fixed type scale (11/13/16/20/25/31/44/55px + display numerals), 4pt-family spacing tokens, two tracking tokens, and numeral rules — all machine-checked by `deckcheck.py`. Action titles are full sentences; a reader skimming only titles gets the storyline. The layout check is built in: every render embeds a script that flags any slide overflowing its 1280x720 frame (`chrome --headless=new --dump-dom out/<deck>.html | grep overflow-report` — look for `LAYOUT-OK`).
