# Craft Rules — Anti-Tells

Guidance against the visual clichés that mark a page as AI-generated. These
patterns aren't wrong individually; they're tells because generators reach for
them *by default*, producing pages that look templated rather than designed.
This document is part of the design-system contract: builders must not ship
them, reviewers must flag them, and the proposal site consuming this system
inherits every rule.

Each rule is checkable. "Instead" always points at a token or pattern this
system already provides.

## The banned list

### 1. Accent-stripe boxes (`border-left: 4px solid <accent>`)
The single most recognizable tell: a callout/card with one edge highlighted.
**Never** use a colored stripe on any side of a box — left-border callouts,
top-border cards, bottom-border "active" cards.
**Instead:** signal emphasis with the layered-surface system
(`--color-bg-layer-1`, semantic `*-subtle-bg` tokens for callouts), spacing,
or type weight. Featured/pricing emphasis uses a full hairline border
(`2px var(--color-text-heading)`, all four sides) plus a badge — see the
pricing card. The one sanctioned exception: the tabs component's *sliding
underline indicator*, which is an animated control affordance, not a static
highlight.

### 2. Icon soup
An icon in front of every heading, list item, and feature blurb; sparkles ✨,
rockets 🚀, lightning bolts; emoji anywhere in UI copy or headings.
**Instead:** icons only where they carry meaning a scanner needs (check/dash
in comparison tables, directional arrows on links, semantic status glyphs).
A feature list with strong typography needs no icons at all. All icons are
inline SVG on `currentColor` from one coherent hand-rolled set — never emoji,
never a second icon library.

### 3. The AI gradient
Indigo→fuchsia/purple→pink gradients; gradient text; gradient buttons;
gradient borders. Adobe's language is flat, confident color.
**Instead:** gradients exist in exactly two sanctioned places — media
*placeholders* (standing in for real imagery, blue/gray tones) and the dark
hero's slow ambient backdrop drift. Never on text, buttons, borders, or as a
section background in the light theme. Real imagery replaces placeholder
gradients in the final site.

### 4. Symmetric icon-title-blurb feature grids
Three perfectly equal columns, each with icon on top, four-word title, and
two lines of filler ("Seamlessly integrate…"). The layout isn't banned —
the *autopilot* version is.
**Instead:** vary the rhythm: a 2/3 + 1/3 split, a horizontal card row, a
stat row, or an asymmetric editorial layout. When a card grid is genuinely
right, cards must carry real, differentiated content (see rule 8) and no
per-card icon unless it disambiguates.

### 5. Center-everything
Every section centered: centered heading, centered paragraph, centered
button, repeated down the page.
**Instead:** Adobe's default is **left-aligned** editorial composition inside
generous whitespace (see design-rules.md hero patterns). Centered treatment
is reserved for the campaign hero and CTA band — at most one centered moment
per few sections.

### 6. Decoration inflation
Drop shadows on everything, glassmorphism/backdrop-blur cards, floating
blob shapes, dotted/grid pattern backgrounds, badges and pills scattered as
decoration.
**Instead:** elevation is *earned* — `--shadow-card` for interactive cards,
`--shadow-elevated` for overlays, nothing else casts a shadow. Flat hairline
borders (`--color-border`) are the default separator. One "New" badge with a
red dot is an accent; five badges is noise.

### 7. Radius and accent-word autopilot
Maximum roundness on every element, and an accent-colored word in every
heading.
**Instead:** the radius scale is semantic — pills are for CTAs only
(`--radius-pill`), cards/media take `--radius-xl`, small controls `--radius-s`
to `--radius-m`. The red single-word headline emphasis exists but is rationed
exactly like all red: at most one instance per page, in the hero.

### 8. Filler copy and fake proof
"Unlock the power of…", "Elevate your workflow", "Seamlessly…", five-star
testimonial cards with stock names, walls of checkmarked bullet lists,
round-number stats invented to fill a counter ("10,000+ customers").
**Instead:** copy states something specific and checkable; stats come from
the actual proposal's data (the demo placeholders model this: "40% faster
delivery" tied to a named phase). If a section's content isn't real yet,
keep the honest placeholder register — never invent social proof.

### 9. Uniform scroll-reveal on everything
Every element on the page fading up on scroll at the same speed, forever.
**Instead:** entrance choreography follows motion.md §3 — grouped reveals
with stagger, *once per element*, and plenty of elements that simply don't
animate. If everything moves, nothing reads as considered.

### 10. Dark-mode-by-inversion
A dark theme produced by flipping every color, yielding pure-black cards,
neon accents, and gray-on-gray text.
**Instead:** use the dark-set ramp tokens (they're Spectrum's own dark
values, not inversions) and the surface-layer system; permanently-dark
surfaces (footer) use the `*-on-dark` tokens in both themes.

## Review checklist (add to every design-review pass)

- [ ] No box anywhere has a single highlighted edge (grep: `border-left`,
      `border-top` with color tokens on card/callout classes)
- [ ] No emoji in markup; every SVG icon earns its place (meaning, not decor)
- [ ] No gradient outside media placeholders + dark-hero ambient backdrop
- [ ] No section is a symmetric icon-title-blurb grid with interchangeable copy
- [ ] Centered composition appears at most once per 3–4 sections
- [ ] Shadows only on interactive cards and overlays
- [ ] Pills = CTAs only; red = ≤1–2 elements per viewport (incl. accent words)
- [ ] No filler superlatives, fake testimonials, or invented stats
- [ ] Some visible elements do not scroll-animate
- [ ] Dark theme uses dark-set tokens, not inverted light values
