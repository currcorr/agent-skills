# Enterprise-Grade AI Systems — Knowledge Base

A comprehensive, video-series-ready treatment of production enterprise AI, written for an experienced technologist (systems / CRM / CPQ background) who is not an ML specialist. Designed for clean source-separation in tools like NotebookLM: each file is a self-contained module; each subsection is scoped to become a standalone short video.

**Start here:** [`00-overview.md`](00-overview.md) — orientation, how to use, maturity-label key, glossary, and the three ideas that tie it all together.

## Modules

| # | Module | File |
|---|--------|------|
| — | Overview & how to use | [`00-overview.md`](00-overview.md) |
| 1 | LLM Foundations | [`01-llm-foundations.md`](01-llm-foundations.md) |
| 2 | Capability Extension | [`02-capability-extension.md`](02-capability-extension.md) |
| 3 | RAG & Retrieval | [`03-rag-retrieval.md`](03-rag-retrieval.md) |
| 4 | Knowledge Representation | [`04-knowledge-representation.md`](04-knowledge-representation.md) |
| 5 | Agents & Orchestration | [`05-agents-orchestration.md`](05-agents-orchestration.md) |
| 6 | Enterprise Operationalization | [`06-enterprise-operationalization.md`](06-enterprise-operationalization.md) |
| 7 | Implementation & Adoption | [`07-implementation-adoption.md`](07-implementation-adoption.md) |
| 8 | Cutting-Edge Methodologies | [`08-cutting-edge.md`](08-cutting-edge.md) |
| — | **Cross-cutting:** Systems of Record Integration | [`09-systems-of-record-integration.md`](09-systems-of-record-integration.md) |
| — | Sources & verification appendix | [`SOURCES.md`](SOURCES.md) |
| — | Review + update punch list | [`REVISION-NOTES.md`](REVISION-NOTES.md) |
| — | **Narration-clean variant** (for NotebookLM / audio & video) | [`narration/`](narration/) |

> **Two variants of every module.** The files above are the **reader-facing** version (rich formatting, tables, cross-links). The [`narration/`](narration/) folder holds a **format-only transformation** of the same content optimized to be read aloud by NotebookLM / text-to-speech (letter-tags and cross-refs removed, tables and symbols converted to prose, each file self-contained). Same facts; different presentation. Use the reader set for skimming/reference; use `narration/` for generating audio overviews or video. Upload only one set to NotebookLM to avoid duplicate weighting.

## Conventions

- **Maturity labels:** *Established*, *Stabilizing*, *Emerging*, *Early-production* (defined in the overview).
- **Shipped vs. roadmap:** vendor capabilities are separated into GA vs. announced/roadmap, and thin public detail is flagged.
- **Knowledge horizon:** the content was drafted at an early-2026 horizon and **refreshed against the web in a mid-2026 research pass** (currency updates applied across all modules; see `REVISION-NOTES.md` for the full change log and the outstanding depth/format follow-ups). Claims flagged ⚠ in the text, and everything in `SOURCES.md`, should still be **re-verified against primary vendor/standards sources before recording** — this space moves fast. Note the critical correction applied: **Logik.ai was acquired by ServiceNow, not Salesforce.**
- **Running enterprise examples:** CRM and CPQ, on Salesforce and ServiceNow as reference platforms.
