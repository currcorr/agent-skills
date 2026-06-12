# Template Library

A curated set of real slides that worked, kept as actual .pptx files so
their geometry can be copied exactly — not redrawn from a description.

```
library/
├── INDEX.md          # the catalog — always start here
├── decks/            # source .pptx files containing flagged slides
└── thumbnails/       # one PNG per flagged slide, named <entry-name>.png
```

## Flagging a slide (what the agent does when the user says "I like this one")

Trigger phrases: "save this slide", "add slide N to the library", "I really
like this layout", "keep this one for next time".

1. **Copy the source deck** into `decks/` if it isn't already there. Strip or
   anonymize client-confidential content first if the user asks — note in the
   index entry whether the stored copy is sanitized or original.
2. **Render a thumbnail** of the flagged slide (use the `pptx` skill's
   `thumbnail.py`) into `thumbnails/<entry-name>.png`.
3. **Add a row to INDEX.md**: short name, source deck filename, slide
   number, closest pattern from `../references/slide-patterns.md`, kit it was
   built with, one line on *why* it earned the flag (that's the retrieval
   key), and the date.
4. **Propose a pattern upgrade** if the slide embodies a reusable layout that
   `slide-patterns.md` doesn't cover yet — ask the user, and on yes, add the
   pattern with a pointer to this entry as its exemplar.
5. **Commit** — the library only compounds if it's pushed.

## Reusing a flagged slide

When building a new deck, scan INDEX.md for entries matching the slide's
message (the "why" column). To reuse:

- Copy the actual slide from the library deck via the `pptx` skill's editing
  workflow (duplicate slide → replace content) — this preserves exact
  geometry, which is the whole point of the library.
- Then re-skin to the active brand kit: swap theme colors/fonts per the kit's
  roles, and re-verify contrast and accent scarcity (design rules 8, 15).

## Hygiene

- Names are kebab-case and descriptive: `value-bridge-with-initiative-callouts`,
  not `slide7-v2`.
- Library decks containing unsanitized client material inherit that client's
  confidentiality — flag it in the index and keep this repo private.
- Periodically prune: an entry nobody has reused in a year is probably not as
  good as it felt at the time.
