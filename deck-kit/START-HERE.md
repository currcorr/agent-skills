# START HERE — for the agent evaluating this kit

You (Codex, Cursor, or any coding agent) have been handed this kit by its owner with two asks:
**(1) evaluate it, (2) figure out how to plug it into your tooling as his deck-production system.**

## The mission, stated plainly
The owner is a strategy consultant. He wants to produce **consulting-grade slide decks from criteria he gives you** — audience, argument, key points — **usually themed to a specific client's brand**. Raw LLM deck output reads as AI-generated to design-literate audiences; this kit exists to fix that. It encodes design judgment (a doctrine, a tells-checklist, a deterministic checker) that survived six adversarial design-review rounds. **Your job is to operate inside it, not to redesign it.**

## The intended workflow (what "plugged in" looks like)
1. Owner gives you deck criteria (+ the client).
2. **Client theme:** if no brand file exists for that client in `brands/`, run `doctrine/style-rip.md` against the client's website or PPT template → write `brands/<client>.yaml`. Render a 3-slide sample for approval before the full deck.
3. **Compose the content** as a `content/<deck>.md` file (the block grammar — see README). Choose archetypes per the doctrine's decision procedures; when no archetype fits the thought's structure, COMPOSE from the primitives (the doctrine's composition rule — archetypes are starting points, never cages).
4. **Render:** `python3 render_deck.py content/<deck>.md --brand <client> --pdf`. Then `python3 deckcheck.py` must pass.
5. **Self-gate before showing the owner:** run the doctrine's self-check on every slide + the tells-checklist as an adversary. The bar: would a partner believe a consulting team made this?
6. Iterate on his feedback by editing the content file (his edits) or the composition (yours). The interactive variant: `render_experience.py` (same content file).

## What to evaluate (his ask #1)
- Does the kit run clean in your environment? (stdlib Python + any Chrome for PDF; zero other deps.)
- Where does it fit your workflow: as a skill/rules file you load? a repo you operate in? Recommend the integration.
- Gaps you notice — missing archetypes, grammar limits, doctrine ambiguities. REPORT them to the owner; do not unilaterally restructure. Extending an archetype or adding a brand is in-bounds; changing the doctrine, tokens, or checker thresholds is his call.

## Hard rules (from the doctrine — non-negotiable)
- Facts in decks trace to sources the owner provides; never fabricate numbers.
- No gradients, shadows, rounded-everything, emoji, or template-smell (the tells-checklist enumerates 23+).
- deckcheck must pass before anything is shown.
- The design system is locked; brands are swappable; content is the owner's editing surface.
