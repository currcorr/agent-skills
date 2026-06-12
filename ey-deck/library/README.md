# Template Library

A curated set of real slides that worked, kept as actual .pptx files so
their geometry can be copied exactly — not redrawn from a description.

```
library/
├── INDEX.md          # slide catalog — always start here
├── EXEMPLARS.md      # deck-level flags: qualities to emulate
├── decks/            # source .pptx files (flagged slides AND exemplar decks)
├── anatomy/          # construction specs: how each flagged slide is built
├── exemplars/        # one annotation file per deck-level flag
└── thumbnails/       # one PNG per flagged slide, named <entry-name>.png
```

Two kinds of flag, two mechanisms:

- **Slide flag** → exact geometry worth copying. Captured below.
- **Deck flag** ("I like how this deck uses headlines", "I like this one's
  aesthetic") → a *quality* worth emulating. Geometry copying won't transfer
  it; distillation will. See "Flagging a whole deck".

## Flagging a slide (what the agent does when the user says "I like this one")

Trigger phrases: "save this slide", "add slide N to the library", "I really
like this layout", "keep this one for next time".

1. **Copy the source deck** into `decks/` if it isn't already there. Strip or
   anonymize client-confidential content first if the user asks — note in the
   index entry whether the stored copy is sanitized or original.
2. **Render a thumbnail** of the flagged slide (use the `pptx` skill's
   `thumbnail.py`) into `thumbnails/<entry-name>.png`.
3. **Generate the construction spec** — real consulting slides are built
   freehand from shapes on a near-blank layout, so document HOW this one is
   constructed:

   ```bash
   python ../scripts/slide_anatomy.py decks/<deck>.pptx <slide#> anatomy/<entry-name>.md
   ```

   The script writes a markdown spec (human view) **and a .json fixture**
   (machine view, used by `spec_diff.py` to verify rebuilds). Three things
   to **fill in by looking at the thumbnail and the table together**:
   - **Per-element `mode` in the .json** — `preserve` (geometry verified
     strictly on rebuild) or `flex` (may adapt; verified by invariants).
     This is per element, not a general note — the verifier depends on it.
   - **Token map** (in the .json) — every literal color → the kit role it
     plays (accent, muted, border…), so the slide survives restyling
     through any kit and the verifier can check roles, not hex.
   - **Construction notes** (in the .md) — alignment grid, spacing rhythm,
     visual zones, hierarchy, what to preserve vs. flex and why it works.

   The table is facts; the notes are the craft — both are needed for an
   agent to rebuild it well. Note the routing rule: specs drive
   *compositional* rebuilds; data-driven elements (charts/tables whose
   element count varies with data) are generated parametrically instead —
   see the render step in ../SKILL.md.
4. **Add a row to INDEX.md**: short name, source deck filename, slide
   number, closest pattern from `../references/slide-patterns.md`, kit it was
   built with, one line on *why* it earned the flag (that's the retrieval
   key), and the date.
5. **Propose a pattern upgrade** if the slide embodies a reusable layout that
   `slide-patterns.md` doesn't cover yet — ask the user, and on yes, add the
   pattern with a pointer to this entry as its exemplar.
6. **Commit** — the library only compounds if it's pushed.

## Flagging a whole deck (what the agent does on "I like how this deck does X")

The user's flag names a quality dimension — if it's ambiguous, ask which:
**messaging** (titles, wording, simplicity), **aesthetic** (color use,
type, whitespace, motif), **structure** (flow, section rhythm),
**density** (how much per slide), or **charts**. A deck can be flagged on
several dimensions at once; annotate each.

1. **Store the deck** in `decks/` (same confidentiality handling as slide
   flags).
2. **Distill — this is the step that matters.** Don't record "user likes
   it"; extract the operative, transferable rules with evidence from the
   deck itself:
   - *Messaging:* pull every title, then characterize what works — e.g.
     "verb-led assertions, 8–12 words, the key number in the title, no
     two-line titles" — and quote 3–5 of the best as examples.
   - *Aesthetic:* run `ey-brand-kit/scripts/extract_kit.py` on it, then
     capture what the kit alone can't hold: density of accent use, image
     treatment, the repeated motif, dark/light rhythm. Save or update a kit
     and put the rest in the annotation.
   - *Structure / density / charts:* describe the pattern concretely enough
     that a deck for a different topic could follow it ("one full-bleed
     divider per section, then at most three evidence slides before the
     next breather").
3. **Write the annotation** to `exemplars/<name>.md`:

   ```markdown
   # <name>
   Source: decks/<file>.pptx · Kit: <kit> · Flagged: <date>
   Flagged for: messaging | aesthetic | ...

   ## What to emulate
   <the distilled rules, with quoted/visual evidence from the deck>

   ## When it applies / when it doesn't
   <e.g. "exec audiences; not for working-team detail packs">
   ```

4. **Index it** — add a row to `EXEMPLARS.md`.
5. **Watch for promotion.** An exemplar quality cited on two or three
   engagements isn't a preference anymore — propose folding it into
   `design-rules.md` or the storyline guide as a numbered rule. That's the
   pipeline: flag → exemplar → house style.

**How exemplars get used:** `ey-deck` consults `EXEMPLARS.md` at the
storyline step (messaging/structure exemplars shape titles and flow) and at
the render step (aesthetic exemplars shape treatment, alongside the kit).
Exemplars never override the design rules or the active client kit — they
steer choices *within* them.

## Reusing a flagged slide

When building a new deck, scan INDEX.md for entries matching the slide's
message (the "why" column). To reuse:

- **Same/compatible template:** copy the actual slide from the library deck
  via the `pptx` skill's editing workflow (duplicate slide → replace
  content) — preserves exact geometry.
- **Different template, or building freehand:** rebuild from the entry's
  construction spec in `anatomy/` — recreate the elements at the documented
  positions/sizes, mapping its fills to the active kit's roles per the
  spec's construction notes. This is the path that matters most in practice,
  since slides are normally constructed from shapes on a near-blank layout.
- Either way, re-skin to the active brand kit and re-verify contrast and
  accent scarcity (design rules 8, 15).

## Hygiene

- Names are kebab-case and descriptive: `value-bridge-with-initiative-callouts`,
  not `slide7-v2`.
- Library decks containing unsanitized client material inherit that client's
  confidentiality — flag it in the index and keep this repo private.
- Periodically prune: an entry nobody has reused in a year is probably not as
  good as it felt at the time.
