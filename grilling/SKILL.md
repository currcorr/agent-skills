---
name: grilling
description: Interview the user relentlessly, ONE question at a time each with a recommended answer, to stress-test a plan, design, approach, or storyline they already have. Use when the user wants to pressure-test / challenge / poke holes in existing thinking before building, or uses any 'grill' trigger phrase. NOT for filling gaps in a vague request (use requirements-clarity) and NOT for producing a full sectioned implementation plan (use gepetto).
---

Interview me relentlessly about every aspect of this plan until we reach a
shared understanding. Walk down each branch of the design tree, resolving
dependencies between decisions one-by-one. For each question, provide your
recommended answer.

Ask the questions one at a time, waiting for feedback on each question before
continuing. Asking multiple questions at once is bewildering.

If a question can be answered by exploring the codebase (or the repo, the
brief, prior deliverables), explore it instead of asking.

---

Credit: the grilling technique is from Matt Pocock's "Skills For Real
Engineers" (github.com/mattpocock/skills, MIT). The two moves that make it
work: **one question at a time** (each answer reshapes the next question) and
**a recommended answer with every question** (you react to a proposal instead
of generating from a blank page, which surfaces disagreement you didn't know
you had).

This loop is the interview engine other skills reach for — e.g. `ey-deck`'s
storyline step and `ey-synthesis` use this technique to sharpen a takeaway
before building.
