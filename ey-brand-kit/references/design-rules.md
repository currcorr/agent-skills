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

Charts follow Tufte. This repo ships a full toolkit — use it rather than
improvising: `orchestrate-tufte-vdqi` routes the request,
`render-tufte-chart` produces the SVG/HTML (its scripts' output drops
directly into `ey-site` pages and converts to images for slides), and
`assess-graphical-excellence` is the QA pass for any chart inherited from a
client or an earlier deck. The rules below are the binding summary; the
toolkit's `references/tufte-principles.md` is the authority when they're not
enough.

11. **Chart junk dies.** No 3D, no gradients on bars, no border boxes, no
    moiré (cross-hatching, dense patterns), no grid darker than the data, no
    legend when direct labels fit. Maximize data-ink; default to white
    background, range-frame axes, endpoint labels.
12. **Sort to the message, honest proportions.** Bars sorted by value unless
    time or a natural order applies; zero baselines for bars; encode 1-D
    quantities with length/position, never area or volume (keep the lie
    factor between 0.95 and 1.05). Highlight the bar that proves the title in
    `accent`; set the rest in `muted`.
13. **Every chart names its source and units.** Bottom-left, caption size.
    Currency over multiple years gets deflated to real terms and labeled so.
14. **Pick the genre for the data shape, not the habit.** ≤ 20 numbers →
    table (rule: tables for lookup, charts for comparison). Many series →
    small multiples with shared scales, never an overplotted spaghetti line.
    Distributions → quartile plots. Chart colors come from the kit's
    `roles.chart` in order, but Tufte wins ties: a one-series chart needs one
    color plus `muted`, not the whole palette.

## Accessibility

15. **Contrast ≥ 4.5:1** for body text, ≥ 3:1 for large text. Check the kit's
    text-on-background pairs; EY yellow fails as a text color on white —
    use it as a background block or marker instead.
16. **Don't encode by color alone.** Pair color with position, labels, or
    shape so the deck survives grayscale printing.
17. **Sites:** semantic HTML, keyboard-navigable interactions, visible focus
    states, `prefers-reduced-motion` respected.

## Avoiding AI design tells

LLM-generated decks and sites converge on a recognizable look that reads as
machine-made to anyone who has seen a few of them. Senior partners and
clients increasingly *have* seen a few of them. These rules exist because
the tells are exactly what a model produces by default — treat the list as a
pre-delivery lint pass, not as taste advice.

20. **No cartoony or decorative icons.** No emoji as bullets or headers, no
    clip-art-style illustrations, no rocket ships/light bulbs/sparkles, no
    icons-in-colored-circles grids. An icon is allowed only when it encodes a
    repeated meaning (e.g. one marker for "decision required" used
    consistently), drawn in a single-weight stroke style, in `muted` or
    `text` — never multicolored.
21. **Square corners by default.** Heavy border-radius on every card, button,
    and image is the single strongest tell. Corporate consulting materials
    are rectilinear: 0 radius unless the client's own template demonstrably
    uses rounding, in which case match the client and record it in the kit's
    `notes`.
22. **No neon, no gradients.** Saturated cyan/magenta/violet palettes,
    purple-to-blue gradient washes, gradient text, and "glassmorphism" blur
    panels are all banned. Color comes from the kit's roles, and rule 8
    already caps the accent at ~10% — a deliverable that looks colorful has
    already failed.
23. **Boxes are not structure.** The default AI layout — a grid of
    equal-sized cards, each with a one-color top border or tinted header —
    substitutes decoration for hierarchy. Build hierarchy with type scale,
    weight, spacing, and alignment on the grid (rule 6). A box earns its
    border only when grouping is the message (e.g. options in a comparison).
    Same for the reflexive `callout`-with-colored-left-border: one per page
    at most, only for the statement that is genuinely the point.
24. **Vary the rhythm.** AI layouts give every section identical weight:
    three columns, then three columns, then three columns, with identical
    padding between every section. Real documents have asymmetry — a dense
    evidence page followed by a single-number page, a full-bleed section
    divider, a wide table, tight spacing next to generous. If three
    consecutive slides/sections share the same layout skeleton, redesign
    one. On sites, the centered stack of headline + subheader + button on a
    gradient is the canonical AI hero — lead left-aligned and asymmetric
    instead.
25. **Kill the AI writing register.** The `humanizer` skill (in this repo)
    is the authority — run its detection patterns over all deck and site
    copy as part of this lint. The patterns that show up most in consulting
    materials: filler vocabulary ("delve", "leverage", "seamless", "robust",
    "holistic", "unlock value"), significance inflation ("underscores",
    "pivotal", "evolving landscape"), negative parallelisms ("it's not just
    X, it's Y"), rule-of-three everywhere, vague attributions ("industry
    experts agree"), em-dash density, boldface sprinkled through prose,
    Title Case On Every Heading, hedging stacks ("could potentially help
    enable"), and generic positive conclusions. One scope limit: apply
    humanizer's *detection* patterns only — its advice to add first-person
    voice and opinions suits essays, not client deliverables. The target
    register is crisp assertions in the client's own vocabulary (see the
    storyline guide), with sentence-case headings. Three more patterns that
    survive into decks: superficial "-ing" tack-ons ("…highlighting the
    importance of"), formulaic "challenges and outlook" boilerplate that
    asserts nothing, and knowledge-cutoff phrasing ("as of this writing,
    details are limited") — a consulting document states what is known and
    sources it.
26. **No untouched defaults, and real type hierarchy.** One font at one
    weight for everything, default-template typography (Inter everywhere),
    or a component library's stock look (the Tailwind/shadcn fingerprint:
    identical spacing, borders, and grays on every element) all read as
    machine output. The kit's heading/body pairing and size scale exist to
    be used: headings visibly heavier and 2x+ body size, weights chosen
    deliberately.
27. **No AI-generated imagery in client deliverables.** Malformed hands,
    garbled embedded text, plastic skin, and impossible lighting are
    instantly recognizable, and even a clean generation reads as filler.
    Use client-supplied assets, licensed photography, or drawn diagrams
    (the repo's diagram skills). If a concept needs illustrating, a labeled
    schematic beats a decorative image every time.
28. **Nothing dead on a site.** Buttons that link to `#`, placeholder
    copy that survived to delivery, fine print nobody wrote, three
    different button styles on one page. Every interactive element does
    something real; one button hierarchy (primary filled, secondary
    outline) sized consistently; every string read by a human before it
    ships.

## Restyling between clients

18. Build with **role tokens, never literal hex/font values**, so swapping
    the kit restyles the artifact completely. If you catch a hard-coded
    `#FFE600` outside a kit file, fix it.
19. After a kit swap, re-check rules 8 and 15 — a palette change can break
    accent scarcity and contrast even when the layout is untouched.
