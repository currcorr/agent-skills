# Enterprise-Grade AI Systems — A Knowledge Base

> A comprehensive, video-series-ready treatment of the concepts, mechanics, tools, tradeoffs, and failure modes behind production enterprise AI — written for an experienced technologist (strong systems / CRM / CPQ background) who is not an ML specialist.

---

## How to use this knowledge base

This document is organized as a **hierarchical outline**. Each numbered section is a **module**; each subsection is scoped to become a **standalone short video** — it is self-contained, defines its jargon on first use, and states why the topic matters before diving into mechanics.

Every substantive subsection follows the same internal rhythm:

- **(a) What it is / why it matters** — plain language, with an analogy where it helps.
- **(b) Key technical mechanics** — how it actually works.
- **(c) Tools / frameworks / vendors** — the main options and how they differ.
- **(d) Tradeoffs & decision criteria** — when to use vs. avoid.
- **(e) Pitfalls & failure modes** — how it breaks in the real world.
- **(f) Enterprise example** — a concrete scenario, frequently in a CRM/CPQ context.

### The modules

| # | Module | File |
|---|--------|------|
| 1 | LLM Foundations | `01-llm-foundations.md` |
| 2 | Capability Extension | `02-capability-extension.md` |
| 3 | RAG & Retrieval | `03-rag-retrieval.md` |
| 4 | Knowledge Representation | `04-knowledge-representation.md` |
| 5 | Agents & Orchestration | `05-agents-orchestration.md` |
| 6 | Enterprise Operationalization | `06-enterprise-operationalization.md` |
| 7 | Implementation & Adoption | `07-implementation-adoption.md` |
| 8 | Cutting-Edge Methodologies | `08-cutting-edge.md` |
| — | **Cross-cutting:** Integration with Systems of Record | `09-systems-of-record-integration.md` |

Modules 1–4 are the **substrate** (how models work and how you feed them knowledge). Modules 5–8 are the **systems** built on that substrate. Module 09 consolidates the **Systems-of-Record (SoR) integration theme** that is also woven through Sections 3–7 — it's broken out as its own module because it's the connective tissue between "AI research" and "AI that runs your business," and it deserves clean source-separation for the video series.

---

## Reading the maturity labels

Wherever a capability is not yet settled practice, it is tagged:

- **Established** — mainstream, well-understood, low-risk to adopt.
- **Stabilizing** — real production usage exists; patterns are converging but not universal.
- **Emerging** — promising, actively researched, but not yet dependable at enterprise scale.
- **Early-production** — shipping in some enterprises, but with caveats and thin public evidence.

The prompt that commissioned this asks for a hard distinction between **shipped / generally-available (GA)** capabilities and **announced / roadmap** features — especially for vendors. That distinction is honored throughout, and where public detail is genuinely thin, it is **flagged explicitly** rather than papered over.

---

## A note on sources and time-sensitivity

- **Durable concepts** (transformers, attention, RAG, chunking, knowledge graphs, agent loops) are stable and are stated with confidence.
- **Vendor capabilities** (Salesforce Agentforce / Data Cloud / Revenue Cloud; ServiceNow Now Assist / AI Agents / CPQ / Logik.ai; protocol specs like MCP and A2A) **move fast**. This knowledge base was **drafted at an early-2026 horizon and refreshed against the web in a mid-2026 research pass**. Before you record vendor-specific claims — pricing, GA dates, exact feature availability, security certifications — **verify against the vendor's primary documentation and release notes**. Treat anything here labeled *roadmap* or *announced* as a pointer to check, not a settled fact.
- Where a claim is a matter of **contested expert opinion** (e.g., "how much reasoning do current models really do," "when multi-agent beats single-agent"), that is called out rather than presented as consensus.

**Primary-source anchors to prefer** when verifying: Anthropic / OpenAI / Google DeepMind model cards and docs; the *Attention Is All You Need* paper (Vaswani et al., 2017) and successors; the original RAG paper (Lewis et al., 2020); ReAct (Yao et al., 2022); Chain-of-Thought (Wei et al., 2022); LoRA (Hu et al., 2021); the MCP specification (modelcontextprotocol.io); vendor trust/security portals; and standards bodies (NIST AI RMF, ISO/IEC 42001, EU AI Act text) for governance claims.

---

## The three ideas that tie everything together

If a viewer remembers only three things across the whole series, make it these:

1. **A language model is a next-token predictor, not a database.** Everything in Modules 2–4 (tool calling, RAG, knowledge graphs) exists to compensate for the fact that the model *reasons well but knows unreliably*. You bolt on retrieval and tools to give it trustworthy, current, permissioned knowledge and the ability to act.

2. **The enterprise value is in the plumbing, not the model.** Any competent team can call a model API. The moat and the risk both live in **retrieval quality, data governance, evaluation, orchestration, and integration with Systems of Record.** Modules 3, 5, 6, and 09 are where projects actually succeed or fail.

3. **The System of Record stays authoritative even when AI becomes the primary interface.** The durable enterprise pattern is **"AI as the orchestration/interaction layer, SoR as the system of record."** The agent reads live, permissioned data and *proposes* actions; the SoR (Salesforce, ServiceNow, an ERP, a data warehouse) remains the single source of truth, enforces entitlements, and governs writes. Get this boundary wrong and you get either a toy or a liability.

---

## Glossary of the most-used terms

Defined in full at first use in the modules; collected here for quick reference.

- **LLM** — Large Language Model. A neural network trained to predict the next token in a sequence.
- **Token** — a sub-word unit of text; the atomic unit models read and write.
- **Embedding** — a numeric vector that represents the *meaning* of text (or an image, etc.) as a point in high-dimensional space.
- **Context window** — the maximum amount of text (in tokens) a model can consider at once.
- **RAG** — Retrieval-Augmented Generation. Fetching relevant documents at query time and putting them in the prompt so the model answers from them.
- **Fine-tuning** — further training a base model on your data to change its behavior or style.
- **Agent** — an LLM placed in a loop where it can call tools, observe results, and decide next steps toward a goal.
- **Tool / function calling** — a model emitting a structured request for the host system to run a function and return the result.
- **MCP** — Model Context Protocol. An open standard for connecting models to tools and data sources.
- **SoR** — System of Record. The authoritative store for a class of business data (e.g., CRM for customer/opportunity data).
- **CRM / CPQ** — Customer Relationship Management / Configure-Price-Quote. Our running enterprise examples.
- **LLMOps** — the operational discipline (deploy, monitor, version, cost, evaluate) for LLM-based systems.

---

*Proceed to `01-llm-foundations.md`.*
