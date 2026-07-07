# AGENTS.md — read this first

You are working inside **deck-kit**: a consulting-grade deck system with locked craft, swappable brands, and plain-markdown content. Two renderers (stdlib only) share one content grammar: `render_deck.py` renders a markdown content file through a locked HTML/CSS layout in any brand's tokens (headless Chrome prints the PDF), and `render_experience.py` renders the same file as a self-contained interactive HTML experience. Everything the system knows about looking human-designed is written down in `doctrine/` — your job is to follow it, not to rediscover it.

The quality bar, in three lines: this exact system survived four rounds of adversarial design review — a fresh adversary hunting AI tells slide by slide — before it shipped. The gate question is: **"would a partner believe a consulting team made this?"** Everything in `doctrine/` exists because the answer was once "no," and each rule is the specific fix that turned it to "yes."

## Prime directives

1. **Design is COMPOSED from primitives, not picked from layouts.** The rule, verbatim (from the doctrine's composition amendment, `doctrine/design-doctrine.md`): *"A consulting team will need extreme flexibility in slidework — it is always created with shapes, tables, etc., not SmartArt or predefined layouts. That being said you will often reuse a layout as a starting point. The key is don't rely on layouts."* Archetypes are starting points, never cages. When the thinking has a shape no archetype fits, compose the slide from the system's primitives (tint cells, hairlines, chevrons, spanning bands, brackets, tracked labels, ledger rows, callouts). The `workstreams` archetype was composed exactly this way and passed the gate — it is your template for how.
2. **Run the doctrine's self-check gate on every slide BEFORE showing the user.** `doctrine/design-doctrine.md` §5 — ten checks, run against a rendered screenshot (1280x720), never against the HTML in your head. Any failure: iterate, don't ship.
3. **The tells-checklist is the adversary.** `doctrine/ai-tells-checklist.md` lists the failure modes. Assume your own defaults ARE those failure modes — takeaway bars restating titles, equal boxes for unequal things, content floating over a framed void, 2x2s that plot nothing, decorative accents, dishonest bar geometry. The checklist is written from this system's actual caught failures.
4. **Never edit `layout/` casually.** The layout is locked on purpose so every deck stays consistent. Content changes never touch it; only new archetypes and furniture changes do, and those go through the gate.

## The pieces

```
render_deck.py       the deck renderer — parse content, apply brand tokens, emit self-contained HTML, print PDF
render_experience.py the second renderer — same content file, one self-contained interactive HTML document
deckcheck.py         the deterministic craft sweep (doctrine §6 made executable) — run after every render
layout/              master.html (page frame + built-in overflow check) + deck.css (all craft, incl. the locked type scale and spacing tokens)
brands/              one YAML per brand: palette, type stacks, logo, usage rules (default.yaml is the schema reference)
content/             one markdown file per deck (starter-template.md = minimal skeleton; demo-*.md = full 16-slide reference incl. the xp- experience layer)
doctrine/            design-doctrine.md (binding design law + self-check gate + §6 craft layer)
                     ai-tells-checklist.md (the adversarial review rubric)
                     journey-spec.md (the worked example of designing an archetype properly)
                     experience-spec.md (the interactive renderer's binding spec + its gate)
                     style-rip.md (how to extract a client brand)
out/                 render output (created on first run; this copy ships without pre-rendered
                     examples — render the two shipped decks + the experience locally, see README)
```

## How to render

From the kit root:

```
python3 render_deck.py content/demo-ai-sales-transformation.md --brand default --pdf
```

- Output lands in `out/<deck>--<brand>.html` (+ `.pdf` with `--pdf`).
- PDF needs any Chrome/Chromium on the machine (the script auto-finds it on macOS/Linux paths and `$PATH`); without one, the self-contained HTML still renders and the script tells you.
- No dependencies: Python 3 stdlib only. Nothing to install.
- **Verify every render:** the HTML embeds a layout check. `chrome --headless=new --dump-dom out/<deck>.html | grep overflow-report` must say `LAYOUT-OK <N> slides`. `LAYOUT-FAIL` names the slide and the clipped zone — fix the content, re-render.
- **Then run the craft sweep:** `python3 deckcheck.py` — the deterministic half of the gate (type-scale membership, spacing tokens, tracking, caps budget, em-dash ration, numeral face). `DECKCHECK-OK` or it names the violation with `file:line`.
- Content errors fail loudly with `file:line` — the script never renders a broken or placeholder slide.

## The second renderer — the interactive experience

`python3 render_experience.py content/<deck>.md --brand <name>` renders the SAME content file as one self-contained interactive HTML document (`out/experience--<brand>.html`): zero external requests, works from `file://` — sharing it means opening or sending the file, nothing to serve. It imports `render_deck.py`'s parser and brand loader, so the grammar never forks. Optional `xp-` keys in content drive the interactive layer and are ignored by the PDF renderer (adding them never changes the PDF); the demo content file is the worked reference for all of them.

**The interactivity doctrine applies and is binding: `doctrine/experience-spec.md`.** Its law — *don't mistake animation for interactivity* — means every animated thing is a response to a client action or one of ≤5 once-per-session narrative beats, and every interactive stage must answer "what did the client DO here that the PDF couldn't?" Before shipping any experience change, run the spec's §10 gate: the wow-test per stage, the transition-to-listener audit, the anti-tech-demo checks, and the honesty sweep (client inputs never dress up as research; geometry data-true; no-JS document reads complete).

## How to edit content

Deck = frontmatter + one ` ```slide ` fenced block per slide. Keys above a `---` line, body below. `#` lines between blocks are comments. Example:

````
```slide
archetype: data
kicker: The gap
title: Agentic AI pays only when the process is redesigned end to end
source: BCG, 2025
---
- With end-to-end process redesign :: 60%+ :: highlight
- Without process redesign :: <20%
```
````

The full grammar for all 15 archetypes (`title`, `exec-summary`, `agenda`, `section-divider`, `content`, `two-col`, `data`, `kpi`, `framework`, `quote`, `timeline`, `journey`, `workstreams`, `comparison`, `closing`) is the table in `README.md`. The `::` separator is the house delimiter everywhere (value :: label, decision :: owner :: when, `N-M!: Label :: text`). `==text==` marks a stat in journey/workstreams cells. `content/demo-ai-sales-transformation.md` exercises nearly every archetype — copy from it.

Editing content, re-rendering, swapping brands, reordering slides: none of this needs design judgment. Just keep the grammar and re-run.

## How to add a brand

Follow `doctrine/style-rip.md` — extract tokens from the client's shipped website CSS or .pptx theme XML (never eyeball screenshots when tokens exist), map them to the schema in `brands/default.yaml`, compute contrast (4.5:1 for small text — computed, not vibed), write `brands/<client>.yaml` with provenance notes, render a 3-slide sample for approval. `brands/stripe.yaml` is a real extraction — the reference. Never hard-code a client hex in CSS or content.

## How to design a NEW slide (bespoke or new archetype)

This is the one task where you must slow down. The procedure:

1. Read `doctrine/design-doctrine.md` end to end. It is binding.
2. Ask "what structure does THIS thought have?" — sequence, contrast, position, magnitude, convergence — then check the decision procedures in doctrine §2. Only if no archetype fits the shape do you compose.
3. Compose from the existing primitives in `deck.css` (chevron cells, lane grids, spanning bands, brackets, gate lines, stat treatment, ledger rows). Read `doctrine/journey-spec.md` first — it is the worked example of the full loop: diagnosis → rationale → grammar → CSS → markup → integration. The `workstreams` builder in `render_deck.py` shows how composed primitives become a reusable archetype (timeline's axis+gate idiom + journey's lane grid).
4. Prototype in HTML, render, screenshot, and run the doctrine §5 self-check gate (all ten checks), the §6.10 craft gate (200% crops, squint test, `deckcheck.py`, the device-existence question), plus the `doctrine/ai-tells-checklist.md` hunt. Iterate until clean.
5. Only then wire it into the system: `ARCHETYPES` tuple, `SLIDE_KEYS` entry, a `build_*` function whose every parse failure goes through `err(path, line, msg)` (the file:line contract), a `BUILDERS` registration, CSS under a named section comment, and a row in README's archetype table.

## How to extend an existing archetype

Fork the builder, don't fight it. Add optional keys to `SLIDE_KEYS` (never break existing content files — every new key must be optional or fail loudly with a clear message), keep the renderer's honest-geometry habits (spans computed from stated values, e.g. `render_phasebar`'s proportional `span:` weights), and re-render both shipped decks in both brands afterward: `LAYOUT-OK` on all of them is the regression test. If you add a background-color state (a wash, a stripe), check it against every other background state that can hit the same cell — state-style collisions are a caught failure mode (tells-checklist #21, doctrine §3b.6).

## Non-negotiables (summary)

- Paper, ink, hairlines, square corners. No gradients, shadows, icons, emoji, rounded card panels.
- Accent = the tag + at most one meaningful element per slide, and you can say what it means in one sentence.
- Takeaway bars, brackets, and callouts must say something the action title doesn't — or they don't exist.
- Geometry is honest: drawn spans match stated values. Time gets an axis; unequal things never render as equal boxes.
- All type from the locked scale (11/13/16/20/25/31/44/55px + display numerals); spacing from the 4pt-family tokens; two tracking tokens; numerals ≥20px are body-sans bold lining, never the serif face. `deckcheck.py` enforces all of it.
- Test by running: rendered screenshot + `LAYOUT-OK` + `DECKCHECK-OK`, never "it should look fine."
- In the experience: interaction is the meal, animation is seasoning — nothing moves except in response to the client or as the stage's single narrative beat.
