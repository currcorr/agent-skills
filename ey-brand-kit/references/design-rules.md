# Overarching Design Rules

These rules apply to every deliverable — deck or site, any client kit. A kit
changes colors, fonts, and logos; it never changes these rules.

## Hierarchy and message

1. **One message per slide/section.** The action title states the takeaway as
   a full sentence ("Cloud migration cuts run-rate cost 23% by FY28"), not a
   topic label ("Cloud migration costs"). A reader skimming only titles must
   get the whole storyline.
2. **Pyramid order.** Answer first, support after. Exec summary up front;
   detail and methodology in appendix.
3. **Title → evidence → so-what.** Every content slide has all three. If a
   slide has no so-what, cut it or merge it.

## Density and layout

4. **Max ~30 words of body text per slide** outside of tables. If you need
   more, the content belongs in two slides or in the appendix.
5. **Whitespace is not wasted space.** Margins ≥ 0.4in on slides; generous
   padding on sites. Never shrink font size below the kit's `caption` size to
   cram content in.
6. **Align to a grid.** Pick column boundaries once per deck/site and snap
   everything to them. Misaligned edges read as careless.
7. **Consistent furniture.** Page numbers, confidentiality footer
   ("Confidential — for internal use of [Client] only" unless told otherwise),
   and source notes in the same position on every slide.

## Color

8. **The accent is scarce.** Brand accent on ≤ 10% of any slide/screen — key
   numbers, the recommended option, the current section marker. If everything
   is highlighted, nothing is.
9. **Neutrals carry the layout** (backgrounds, borders, body text). Use the
   kit's `muted` and `border` roles, not arbitrary grays.
10. **Semantic colors are reserved.** `positive`/`negative` only for genuinely
    good/bad values, never decoration.

## Charts and data

11. **Chart junk dies.** No 3D, no gradients on bars, no gridline thickets,
    no legend when direct labels fit. Maximize data-ink.
12. **Sort to the message.** Bars sorted by value unless time or a natural
    order applies. Highlight the bar that proves the title; gray the rest.
13. **Every chart names its source and units.** Bottom-left, caption size.
14. **Tables for lookup, charts for comparison.** If the audience will read
    individual values, use a table.

## Accessibility

15. **Contrast ≥ 4.5:1** for body text, ≥ 3:1 for large text. Check the kit's
    text-on-background pairs; EY yellow fails as a text color on white —
    use it as a background block or marker instead.
16. **Don't encode by color alone.** Pair color with position, labels, or
    shape so the deck survives grayscale printing.
17. **Sites:** semantic HTML, keyboard-navigable interactions, visible focus
    states, `prefers-reduced-motion` respected.

## Restyling between clients

18. Build with **role tokens, never literal hex/font values**, so swapping
    the kit restyles the artifact completely. If you catch a hard-coded
    `#FFE600` outside a kit file, fix it.
19. After a kit swap, re-check rules 8 and 15 — a palette change can break
    accent scarcity and contrast even when the layout is untouched.
