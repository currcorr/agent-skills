---
title: Deck title goes here
subtitle: One line saying what this deck argues
client: Prepared for Client Name
date: July 2026
author: Author Name
confidentiality: Confidential — draft for discussion
---

# Minimal starter deck. Every block below is a valid, renderable example of
# the grammar. Replace the placeholder text with your content, delete what
# you don't need, and render:
#   python3 render_deck.py content/starter-template.md --brand default --pdf
# Full block grammar for all 15 archetypes: README.md. Design rules for new
# slides: doctrine/design-doctrine.md (run its self-check gate before showing
# anyone). Lines like this one (starting '#') are comments between slides.

```slide
archetype: title
title: Deck title goes here
subtitle: One line saying what this deck argues
```

```slide
archetype: exec-summary
kicker: Executive summary
title: The answer, stated first, as a full sentence
---
- First finding as a bold lead :: one supporting line with the evidence behind it
- Second finding as a bold lead :: one supporting line with the evidence behind it
- The ask of the reader :: what decision or funding this deck is asking for
```

```slide
archetype: section-divider
title: The first section's claim, as a sentence
subtitle: Optional second line of context
```

```slide
archetype: data
kicker: Section label
title: Action title stating what the numbers show
subtitle: Optional axis/context line
source: Where these numbers came from
---
- The winning option :: 60%+ :: highlight
- The losing option :: <20%
```

```slide
archetype: content
kicker: Section label
title: Action title stating the takeaway as a full sentence
source: Where this comes from
---
- First supporting point (max ~5 bullets; **bold** and *italic* work)
- Second supporting point
  - one level of sub-bullet is allowed; deeper nesting means you should draw a diagram instead
- Third supporting point
```

```slide
archetype: closing
title: Decisions we need from this group
contact: Author Name
---
- First decision being asked for :: owner :: when
- Second decision being asked for :: — :: —
```
