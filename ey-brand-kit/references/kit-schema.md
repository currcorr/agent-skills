# Brand Kit Schema

A kit is one JSON file. Every field is optional except `meta.name` — partial
kits are fine and should be filled in as the engagement progresses.

```json
{
  "meta": {
    "name": "client-name",
    "client": "Client Display Name",
    "source": "ClientTemplate.pptx",
    "extracted": "2026-06-12",
    "confidential": true
  },
  "colors": {
    "theme": {
      "dk1": "#000000", "lt1": "#FFFFFF",
      "dk2": "#1A1A24", "lt2": "#F2F2F4",
      "accent1": "#FFE600", "accent2": "#2E2E38",
      "accent3": "#747480", "accent4": "#C4C4CD",
      "accent5": "#35A4E8", "accent6": "#9C82D4",
      "hlink": "#0563C1", "folHlink": "#954F72"
    },
    "roles": {
      "primary": "#2E2E38",
      "accent": "#FFE600",
      "background": "#FFFFFF",
      "backgroundDark": "#2E2E38",
      "text": "#2E2E38",
      "textOnDark": "#FFFFFF",
      "muted": "#747480",
      "border": "#C4C4CD",
      "positive": "#168736",
      "negative": "#B9251C",
      "chart": ["#FFE600", "#2E2E38", "#747480", "#35A4E8", "#9C82D4", "#C4C4CD"]
    }
  },
  "typography": {
    "heading": { "family": "EYInterstate", "fallback": "Arial, Helvetica, sans-serif", "weight": 700 },
    "body":    { "family": "EYInterstate Light", "fallback": "Arial, Helvetica, sans-serif", "weight": 400 },
    "scale": { "title": 40, "h1": 28, "h2": 20, "body": 14, "caption": 10 }
  },
  "logo": {
    "primary": "assets/logo.svg",
    "onDark": "assets/logo-reverse.svg",
    "placement": "bottom-left, 0.4in margin",
    "clearSpace": "1x logo height on all sides"
  },
  "pptx": {
    "templatePath": "templates/ClientTemplate.pptx",
    "slideSize": "16:9",
    "layoutMap": {
      "title":   { "index": 0, "name": "Title Slide" },
      "section": { "index": 2, "name": "Section Header" },
      "content": { "index": 1, "name": "Title and Content" },
      "twoCol":  { "index": 3, "name": "Two Content" },
      "blank":   { "index": 6, "name": "Blank" },
      "closing": { "index": 8, "name": "Thank You" }
    }
  },
  "notes": [
    "Never place body text on the accent yellow.",
    "Charts use the accent palette in listed order."
  ]
}
```

## Field notes

- **`colors.theme`** mirrors the OOXML color scheme verbatim (what
  `extract_kit.py` produces). Don't edit these — they're the source of truth
  from the client file.
- **`colors.roles`** is the semantic layer everything else consumes. Filling
  this in is a judgment call: extraction can't know whether `accent1` is the
  hero color or a leftover default. Confirm with the user against a real
  client slide.
- **`roles.chart`** order matters — series 1 gets the first color. Lead with
  the brand accent, follow with neutrals, keep adjacent colors distinguishable.
- **`typography.scale`** values are points for PPT; sites convert via
  `kit_to_css.py` (1pt ≈ 1.333px).
- **`pptx.layoutMap`** keys are the role names `ey-deck` requests. Indices are
  zero-based positions in the template's layout list (the extractor prints all
  layouts it finds, with names, so you can assign roles).
- **`notes`** is the escape hatch for rules that matter but don't fit the
  schema. Both `ey-deck` and `ey-site` read and obey them.
