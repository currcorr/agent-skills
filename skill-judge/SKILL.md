---
name: skill-judge
description: Evaluate Agent Skill design quality against official specifications and best practices. Use when reviewing, auditing, or improving SKILL.md files and skill packages. Provides multi-dimensional scoring and actionable improvement suggestions.
---

# Skill Judge

Evaluate Agent Skills against official specifications and patterns derived from 17+ official examples.

---

## Core Philosophy

> **Good Skill = Expert-only Knowledge − What Claude Already Knows**

A Skill is NOT a tutorial — it is a **knowledge externalization mechanism**. Its value is its **knowledge delta**: the gap between what it provides and what the model already knows. When a Skill explains "what is PDF" or "how to write a for-loop", it wastes tokens compressing knowledge Claude already has.

When evaluating, categorize each section of the target Skill:

| Type | Definition | Treatment |
|------|------------|-----------|
| **Expert** | Claude genuinely doesn't know this | Must keep — this is the Skill's value |
| **Activation** | Claude knows but may not think of | Keep if brief — serves as reminder |
| **Redundant** | Claude definitely knows this | Should delete — wastes tokens |

**Read before your first evaluation**: [`references/core-philosophy.md`](references/core-philosophy.md) — the full philosophy (Skill as hot-swappable knowledge, Tool vs Skill distinction, the knowledge-delta formula). Skip if you have already internalized it this session.

---

## Evaluation Dimensions (120 points total)

| Dimension | Max | Focus |
|-----------|-----|-------|
| D1: Knowledge Delta | 20 | Does the Skill add genuine expert knowledge? **THE core dimension** |
| D2: Mindset + Appropriate Procedures | 15 | Thinking patterns + domain-specific procedures Claude wouldn't know |
| D3: Anti-Pattern Quality | 15 | Specific NEVER lists with non-obvious WHY |
| D4: Specification Compliance | 15 | Valid frontmatter; description answers WHAT + WHEN + KEYWORDS |
| D5: Progressive Disclosure | 15 | Three-layer loading; explicit loading triggers; "Do NOT Load" guidance |
| D6: Freedom Calibration | 15 | Specificity matches task fragility (creative=high freedom, fragile=low) |
| D7: Pattern Recognition | 10 | Follows one of 5 official patterns: Mindset, Navigation, Philosophy, Process, Tool |
| D8: Practical Usability | 15 | Decision trees, working examples, error handling, edge cases |

**MANDATORY before scoring — read BOTH rubric files completely** (they contain the score bands, red/green flags, and worked good/bad examples for every dimension; never assign scores from the table above alone):

- [`references/rubrics-knowledge-and-content.md`](references/rubrics-knowledge-and-content.md) — full rubrics for D1–D3 (knowledge delta, mindset/procedures, anti-patterns)
- [`references/rubrics-structure-and-usability.md`](references/rubrics-structure-and-usability.md) — full rubrics for D4–D8 (spec compliance, progressive disclosure, freedom calibration, pattern recognition, usability)

---

## NEVER Do When Evaluating

- **NEVER** give high scores just because it "looks professional" or is well-formatted
- **NEVER** ignore token waste — every redundant paragraph should result in deduction
- **NEVER** let length impress you — a 43-line Skill can outperform a 500-line Skill
- **NEVER** skip mentally testing the decision trees — do they actually lead to correct choices?
- **NEVER** forgive explaining basics with "but it provides helpful context"
- **NEVER** overlook missing anti-patterns — if there's no NEVER list, that's a significant gap
- **NEVER** assume all procedures are valuable — distinguish domain-specific from generic
- **NEVER** undervalue the description field — poor description = skill never gets used
- **NEVER** put "when to use" info only in the body — Agent only sees description before loading

---

## Evaluation Protocol

### Step 1: First Pass — Knowledge Delta Scan

Read SKILL.md completely and for each section ask:
> "Does Claude already know this?"

Mark each section as:
- **[E] Expert**: Claude genuinely doesn't know this — value-add
- **[A] Activation**: Claude knows but brief reminder is useful — acceptable
- **[R] Redundant**: Claude definitely knows this — should be deleted

Calculate rough ratio: E:A:R
- Good Skill: >70% Expert, <20% Activation, <10% Redundant
- Mediocre Skill: 40-70% Expert, high Activation
- Bad Skill: <40% Expert, high Redundant

### Step 2: Structure Analysis

```
[ ] Check frontmatter validity
[ ] Count total lines in SKILL.md
[ ] List all reference files and their sizes
[ ] Identify which pattern the Skill follows
[ ] Check for loading triggers (if references exist)
```

### Step 3: Score Each Dimension

For each of the 8 dimensions (using the rubric files loaded above):
1. Find specific evidence (quote relevant lines)
2. Assign score with one-line justification
3. Note specific improvements if score < max

### Step 4: Calculate Total & Grade

```
Total = D1 + D2 + D3 + D4 + D5 + D6 + D7 + D8
Max = 120 points
```

**Grade Scale** (percentage-based):
| Grade | Percentage | Meaning |
|-------|------------|---------|
| A | 90%+ (108+) | Excellent — production-ready expert Skill |
| B | 80-89% (96-107) | Good — minor improvements needed |
| C | 70-79% (84-95) | Adequate — clear improvement path |
| D | 60-69% (72-83) | Below Average — significant issues |
| F | <60% (<72) | Poor — needs fundamental redesign |

### Step 5: Generate Report

Write the evaluation as a markdown document containing, in order: a summary block (total score out of 120 with percentage, letter grade, identified pattern, E:A:R knowledge ratio, one-sentence verdict), a dimension score table (all 8 dimensions with score, max, and notes), critical must-fix issues, the top 3 improvements ranked by impact, and detailed analysis for every dimension scoring below 80% (what's missing, specific examples from the Skill, concrete suggestions).

**MANDATORY**: Read [`references/output-template.md`](references/output-template.md) and follow its exact structure when producing the report — do not invent an alternative layout.

---

## Common Failure Patterns

Nine recurring failure modes, each with symptom, root cause, and fix: The Tutorial, The Dump, The Orphan References, The Checkbox Procedure, The Vague Warning, The Invisible Skill, The Wrong Location, The Over-Engineered, The Freedom Mismatch.

**Read when diagnosing a low-scoring Skill or writing improvement suggestions**: [`references/failure-patterns.md`](references/failure-patterns.md) — full symptom/root-cause/fix breakdown for all nine patterns.

---

## Quick Reference Checklist

**Read for a fast pre-scoring sanity pass** (optional if you have already applied the full rubrics): [`references/evaluation-checklist.md`](references/evaluation-checklist.md) — one-box-per-criterion checklist covering knowledge delta, mindset, anti-patterns, specification, structure, freedom, and usability.

---

## The Meta-Question

When evaluating any Skill, always return to this fundamental question:

> **"Would an expert in this domain, looking at this Skill, say:**
> **'Yes, this captures knowledge that took me years to learn'?"**

If the answer is yes → the Skill has genuine value.
If the answer is no → it's compressing what Claude already knows.

The best Skills are **compressed expert brains** — they take a designer's 10 years of aesthetic accumulation and compress it into 43 lines, or a document expert's operational experience into a 200-line decision tree.

What gets compressed must be things Claude doesn't have. Otherwise, it's garbage compression.

---

## Self-Evaluation Note

This Skill (skill-judge) should itself pass evaluation:

- **Knowledge Delta**: Provides specific evaluation criteria Claude wouldn't generate on its own
- **Mindset**: Shapes how to think about Skill quality, not just checklist items
- **Anti-Patterns**: "NEVER Do When Evaluating" section with specific don'ts
- **Specification**: Valid frontmatter with comprehensive description
- **Progressive Disclosure**: Lean SKILL.md with rubrics and templates in references/, loaded via mandatory triggers
- **Freedom**: Medium freedom appropriate for evaluation task
- **Pattern**: Follows Tool pattern with decision frameworks
- **Usability**: Clear protocol, report template, quick reference

Evaluate this Skill against itself as a calibration exercise.
