---
name: deep-research
description: >
  Produce a deep, multi-source, fact-checked research report with full
  citations. Use when the user asks for "deep research", a research report,
  due diligence, a market/technology/competitor scan, or any question where
  the answer must be verified across independent sources before being acted
  on. NOT for quick lookups or current-chatter scans — use perplexity for a
  fast answer and last30days for what people are saying right now. Works
  with whatever web search/fetch tools the host agent provides; parallelize
  with subagents when the host supports them.
license: MIT
metadata:
  version: "1.0"
---

# Deep Research

Turn a question into a decision-grade report: plan the coverage, collect
from multiple angles, extract claims with provenance, adversarially verify
the load-bearing ones, and synthesize with citations and explicit
confidence. The failure mode this skill exists to prevent is the fluent,
plausible report built on one aggregator article and model memory.

## Phase 0 — Scope

Before searching, pin down:

- **The decision**: what will the user do with the answer? A market-entry
  call needs different evidence than background reading.
- **Key questions**: decompose the ask into 3–7 sub-questions that, answered
  well, answer the whole.
- **Depth and recency**: is this a 1-page brief or a full report? Does the
  answer depend on the last 6 months or the last decade?

If the request is underspecified in a way that changes the research (no
market/geography, no use case, no timeframe), ask 2–3 clarifying questions
first. Otherwise state your assumptions in the report and proceed.

## Phase 1 — Research plan

Build a search matrix: each sub-question crossed with several **angles**, so
one search style's blind spots don't become the report's blind spots:

| Angle | Looking for |
|---|---|
| Primary / official | filings, docs, standards, company pages, papers, data releases |
| Reporting | quality news and trade press |
| Community | practitioner forums, reviews, discussions — what users actually experience |
| Quantitative | statistics, market data, benchmarks — with methodology |
| Contrarian | criticism, failures, lawsuits, negative reviews, "X is wrong/overhyped" |

The contrarian angle is mandatory for every sub-question. If everything you
collect agrees, you searched wrong.

## Phase 2 — Collection

- Run the matrix. If the host agent supports subagents, fan out one per
  sub-question or angle and have each return sources + candidate claims;
  otherwise work through the matrix sequentially.
- Follow aggregators to their **primary sources** and cite the primary, not
  the aggregator. A stat with no traceable origin is an anecdote.
- Log every source as you go: URL, title, publisher, date, type
  (primary/reporting/community), and what it supports. You will not
  remember later.
- Prefer dated material; note the publication date next to every
  time-sensitive fact.

## Phase 3 — Claim extraction

From the collected material, list the **load-bearing claims** — the
statements the report's conclusions actually rest on. For each: the claim,
its source(s), date, and whether it is a measured fact, an estimate, or an
opinion. Everything else is color.

## Phase 4 — Adversarial verification

For each load-bearing claim:

1. **Try to refute it.** Search specifically for contradicting evidence,
   not confirming evidence ("<claim> criticism", "<claim> debunked",
   competing figures).
2. **Independence check.** Two articles citing the same press release are
   one source. Critical claims need 2+ genuinely independent sources.
3. **Verdict**: Confirmed (2+ independent sources, no credible
   contradiction) / Single-source (plausible, unverified) / Contested
   (credible sources disagree — report the disagreement, don't average it)
   / Refuted (drop it, and drop conclusions that relied on it).

Do not skip this phase to save time — it is the difference between this
skill and a long perplexity answer.

## Phase 5 — Synthesis

Write the report per `references/report-template.md`:

- **Answer first**: a direct executive summary answering the original
  question, before any background.
- Findings organized by sub-question, every non-obvious statement carrying
  a numbered citation `[n]`.
- Confidence labels (High / Medium / Low) on each key finding, driven by
  the Phase 4 verdicts.
- A **"Where sources disagree"** section for contested claims.
- A **"Gaps"** section: what couldn't be verified, angles not covered,
  what further research would resolve.
- Full numbered source log (URL, publisher, date, type).

Before delivering, run a completeness check: any sub-question unanswered?
Any angle never searched? Any load-bearing claim still single-source? Fix
or disclose — never silently truncate coverage.

## Downstream

- Findings → `startup-competitors` (competitive framing),
  `management-consulting` (framework analysis), `ey-synthesis` (merge with
  interview evidence), `ey-deck` / `ey-doc` (client deliverable).
- The source log doubles as the provenance record consulting deliverables
  need.
