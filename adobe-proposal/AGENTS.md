# AGENTS.md — building with this design system

Instructions for ANY coding agent (Cursor, Claude Code, Copilot, etc.)
building a real proposal website from this Adobe-styled design system.
Read this file completely before writing any page. (Cursor users: the rule
in `.cursor/rules/design-system.mdc` is always applied and points here;
`CLAUDE.md` is a pointer here too.)

## The one rule that matters most: placeholders are not content

Everything in this package that demonstrates the system uses **sample
content**, and all of it is machine-marked:

| Marker | Meaning | Your obligation |
|---|---|---|
| `data-placeholder="media"` | Gradient block standing in for real imagery | Replace with a real licensed image/screenshot before shipping |
| `data-placeholder="photo"` | Photo-section slot holding the tagged placeholder SVG | Replace with real licensed photography (`<img class="adb-photosec__img" src="…" alt="…">`) |
| `data-placeholder="media-optional"` | Generic illustrative visual (e.g. the hero architecture SVG) | Replace, or keep only if it genuinely depicts the proposal's subject |
| `data-sample-content="northbeam-demo"` on `<body>` | The whole document is a demo | Never copy this attribute to a real page |
| The brand "Northbeam", all its stats, quotes, and copy | Fictional | Replace every instance with the real proposal's content — never invent stats or testimonials (see `design-system/craft-rules.md` rule 8) |

**Gate before declaring any page done:**

```bash
python3 tools/check_placeholders.py path/to/your-page.html
```

Exit 1 = not shippable; the report lists every remaining placeholder with
line numbers. Run it, fix, re-run — a page is not finished while it fails.
If you cannot run Python, grep for `data-placeholder`, `Northbeam`, and
`data-sample-content` yourself — zero hits required.
Do not delete or weaken the markers to make the check pass; replace the
content they mark. When you copy a component out of `components/*.html` or
`landing.html`, the markers come with it — that is intentional: they follow
the placeholder until you replace it.

The gallery (`design-system/index.html`) and the fragments
(`design-system/components/*.html`) are specimen documents — they are
SUPPOSED to contain placeholders. Never run the gate against them, never
"fix" them to pass it, and never ship them as pages.

## Build rules (read the full docs before designing)

1. `kit/tokens.css` is the contract — only `var(--token)` values in any CSS
   you write. No literal hex, ms, or cubic-bezier. Missing token → add it to
   the kit, don't inline.
2. `research/design-rules.md` — layout, typography, red rationing (§2), and
   photography treatment (§3b).
3. `design-system/motion.md` — every motion decision is already made; follow
   it exactly (no ease-in, no layout-property animation, focus never
   animates, reduced-motion always handled).
4. `design-system/craft-rules.md` — ten banned patterns with a review
   checklist. Run the checklist on every page you produce.
5. Landing-page composition reference: `design-system/landing.html` shows
   the intended section rhythm (nav → hero → stats → cards → timeline →
   photo moment → dark section → CTA band → footer).

## Quick facts

- Fonts: Source Sans 3 / Source Code Pro (Adobe Clean substitutes). For
  production, self-host woff2 and keep the token names.
- Red `#EB1000` = brand accent (≤1–2 per viewport); `#F03823` = semantic
  negative only. Never swap them.
- Dark mode: automatic via `prefers-color-scheme` + explicit
  `data-theme="light"|"dark"` on `<html>`. Test both.
- Rebuild the component gallery after editing fragments:
  `cd design-system && python3 build_gallery.py`.
- This system is Adobe-*styled*, not Adobe-branded: no Adobe logo, name, or
  identity anywhere in output.
