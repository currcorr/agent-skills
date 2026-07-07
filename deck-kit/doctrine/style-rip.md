# Style rip — extract a client's brand into deck tokens and prove it with a sample render

Any agent with web access (or a copy of the client's .pptx) can run this procedure. Output: a new `brands/<client>.yaml` plus a rendered approval sample.

## When to use

The user needs a deck in a client's look. Trigger phrases: "make it look like [client]", "rip [client]'s style", "new brand for the deck system", or any deck request naming a client with no `brands/<client>.yaml`. Input is a client website URL or a client .pptx template.

## Steps

1. **Check for an existing kit.** `ls brands/` — if `<client>.yaml` exists, use it and stop here.
2. **Extract honestly from the source.**
   - *Website:* fetch the site's shipped CSS (follow `<link rel=stylesheet>` from the homepage; design-system custom properties are the gold source, e.g. Stripe's `--hds-color-*`). Pull: the brand accent, the structural ink/heading color, secondary-text gray, hairline/border gray, any tinted ground, and the `font-family` stacks. Prefer tokens defined in their CSS over colors eyeballed from screenshots.
   - *PPT template:* unzip the .pptx and read `ppt/theme/theme1.xml` — the `<a:clrScheme>` block holds the theme palette, `<a:fontScheme>` the major/minor fonts. Any XML-literate script or manual read works; the mapping is mechanical.
3. **Map to the deck token schema** (`brands/default.yaml` is the reference): `palette.primary` (structure/dividers), `ink` (text), `paper`, `accent` (the scarce brand pop), `muted`, `rule`, `tint`; `type.display/body/mono`; `logo.text`; `rules.accent-usage`. Then the optional dimensions — extract them when the source has them, otherwise leave them unset (the renderer's fallbacks are documented in `default.yaml`):
   - `palette.chart` `1:`..`4:` — the brand's data-viz/series scale if its design system defines one (chart tokens, category colors); series 1 is usually the accent. Don't invent a scale that isn't there.
   - `palette.positive` / `negative` — the brand's success/error tokens (e.g. Stripe's HDS `core-success-600` / `core-error-600`).
   - `palette.accent-2` — a real second brand color, only if the brand genuinely runs a two-color system.
   - `palette.divider-ground` / `divider-ink` — only when the brand's full-bleed sections aren't primary-on-paper (e.g. a dark-mode brand or a tinted section ground).
   - `logo.image` — only if the user supplies the asset file; it gets base64-embedded. Never hotlink a logo off the site.
   - `type.files` — only for licensed font files actually held on disk; note that the rendered HTML then references them by `file://` path and is no longer self-contained.

   Record extraction provenance in `meta.source` and `meta.extraction-notes` — which file, which tokens, what was approximated, which optional dimensions were left to fallbacks. `brands/stripe.yaml` is a real extraction from stripe.com's shipped CSS — the reference for what good provenance notes look like.
4. **Check contrast before writing.** Computed, not vibed: `ink` and `muted` on `paper` must clear 4.5:1; `accent` used for small labels must clear 4.5:1 (darken the accent for text use if the brand's web accent fails — note it). `paper` on `primary` (dividers) must clear 4.5:1 — same check for `divider-ink` on `divider-ground` if set, and `positive`/`negative` on `paper` (they set small delta text).
5. **Write `brands/<client>.yaml`** and render a 3-slide sample for approval: pick a title, one content+takeaway, and one data slide from an existing content file (or a scratch 3-slide file in `content/`), then `python3 render_deck.py <content> --brand <client> --pdf`.
6. **Get the user's sign-off on the sample** before using the brand on a real deck. Adjust tokens per feedback; the layout never changes per client.

## Notes

- **Honest limits — say them out loud in the sample handoff:** proprietary fonts (Söhne, corporate faces) are approximated by self-contained system stacks — name the real face in the yaml comments; `logo.text` is a text placeholder unless the user supplies an asset; a website's marketing gradients do not survive the rip — deck discipline is flat color, and the yaml's `rules` block should say how the accent is rationed (≤10% of any slide).
- Never hard-code a client hex in layout CSS or content — everything goes through the token file, or the brand swap breaks.
- Client templates are confidential: keep extracted kits private, never in anything published.
- The tag, takeaway label, and one highlight per slide take `accent`; dividers take `primary`. If the client's palette makes those collide, pick the darker color for `primary`.
