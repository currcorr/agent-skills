# Enterprise-Grade AI Systems — A Knowledge Base

*This is the orientation for a knowledge base on production enterprise AI; each module can be understood on its own.*

This is a comprehensive, video-series-ready treatment of the concepts, mechanics, tools, tradeoffs, and failure modes behind production enterprise AI. It is written for an experienced technologist with a strong systems, CRM, and CPQ background who is not an ML specialist.

---

## How to use this knowledge base

This document is organized as a hierarchical outline. Each numbered section is a module, and each subsection is scoped to become a standalone short video. Every subsection is self-contained, defines its jargon on first use, and states why the topic matters before diving into mechanics.

Every substantive subsection follows the same internal rhythm:

- **Why it matters** — plain language, with an analogy where it helps.
- **How it works** — the key technical mechanics, and how it actually works.
- **The main options** — the tools, frameworks, and vendors, and how they differ.
- **When to use it (and when not to)** — the tradeoffs and decision criteria for when to use versus avoid it.
- **Where it goes wrong** — the pitfalls and failure modes, and how it breaks in the real world.
- **A concrete example** — an enterprise scenario, frequently in a CRM or CPQ context.

### The modules

The knowledge base contains eight numbered modules plus one cross-cutting module. They are: one, LLM Foundations; two, Capability Extension; three, RAG and Retrieval; four, Knowledge Representation; five, Agents and Orchestration; six, Enterprise Operationalization; seven, Implementation and Adoption; and eight, Cutting-Edge Methodologies. The cross-cutting module is Integration with Systems of Record.

Modules one through four are the substrate: how models work and how you feed them knowledge. Modules five through eight are the systems built on that substrate. The Systems-of-Record module consolidates the Systems-of-Record integration theme that is also woven through the retrieval, agents, operationalization, and adoption modules. It is broken out as its own module because it is the connective tissue between AI research and AI that runs your business, and it deserves clean source-separation for the video series.

---

## Reading the maturity labels

Wherever a capability is not yet settled practice, it is tagged with one of four maturity labels.

- **Established** — mainstream, well-understood, low-risk to adopt.
- **Stabilizing** — real production usage exists; patterns are converging but not universal.
- **Emerging** — promising, actively researched, but not yet dependable at enterprise scale.
- **Early-production** — shipping in some enterprises, but with caveats and thin public evidence.

The prompt that commissioned this asks for a hard distinction between shipped, generally-available capabilities and announced or roadmap features, especially for vendors. That distinction is honored throughout. Where public detail is genuinely thin, it is flagged explicitly rather than papered over.

---

## A note on sources and time-sensitivity

Durable concepts, such as transformers, attention, RAG, chunking, knowledge graphs, and agent loops, are stable and are stated with confidence.

Vendor capabilities move fast. These include Salesforce Agentforce, Data Cloud, Revenue Cloud, and Logik.ai; ServiceNow Now Assist, AI Agents, and CPQ; and protocol specs like MCP and A2A. This knowledge base reflects understanding as of an early-2026 knowledge horizon. Before you record vendor-specific claims, such as pricing, GA dates, exact feature availability, and security certifications, verify against the vendor's primary documentation and release notes. Treat anything here labeled roadmap or announced as a pointer to check, not a settled fact.

Where a claim is a matter of contested expert opinion, for example how much reasoning current models really do, or when multi-agent beats single-agent, that is called out rather than presented as consensus.

When verifying, prefer these primary-source anchors: Anthropic, OpenAI, and Google DeepMind model cards and docs; the Attention Is All You Need paper by Vaswani and colleagues from 2017, and its successors; the original RAG paper by Lewis and colleagues from 2020; ReAct by Yao and colleagues from 2022; Chain-of-Thought by Wei and colleagues from 2022; LoRA by Hu and colleagues from 2021; the MCP specification at modelcontextprotocol.io; vendor trust and security portals; and standards bodies such as the NIST AI Risk Management Framework, ISO/IEC 42001, and the EU AI Act text for governance claims.

---

## The three ideas that tie everything together

If a viewer remembers only three things across the whole series, make it these.

First: a language model is a next-token predictor, not a database. Everything in the capability extension, retrieval, and knowledge representation modules, such as tool calling, RAG, and knowledge graphs, exists to compensate for the fact that the model reasons well but knows unreliably. You bolt on retrieval and tools to give it trustworthy, current, permissioned knowledge and the ability to act.

Second: the enterprise value is in the plumbing, not the model. Any competent team can call a model API. The moat and the risk both live in retrieval quality, data governance, evaluation, orchestration, and integration with Systems of Record. The retrieval, agents, operationalization, and Systems-of-Record modules are where projects actually succeed or fail.

Third: the System of Record stays authoritative even when AI becomes the primary interface. The durable enterprise pattern is AI as the orchestration and interaction layer, with the SoR as the system of record. The agent reads live, permissioned data and proposes actions. The SoR, whether that is Salesforce, ServiceNow, an ERP, or a data warehouse, remains the single source of truth, enforces entitlements, and governs writes. Get this boundary wrong and you get either a toy or a liability.

---

## Glossary of the most-used terms

These are defined in full at first use in the modules, and collected here for quick reference.

- **LLM** — Large Language Model. A neural network trained to predict the next token in a sequence.
- **Token** — a sub-word unit of text; the atomic unit models read and write.
- **Embedding** — a numeric vector that represents the meaning of text, or an image, and so on, as a point in high-dimensional space.
- **Context window** — the maximum amount of text, measured in tokens, a model can consider at once.
- **RAG** — Retrieval-Augmented Generation. Fetching relevant documents at query time and putting them in the prompt so the model answers from them.
- **Fine-tuning** — further training a base model on your data to change its behavior or style.
- **Agent** — an LLM placed in a loop where it can call tools, observe results, and decide next steps toward a goal.
- **Tool or function calling** — a model emitting a structured request for the host system to run a function and return the result.
- **MCP** — Model Context Protocol. An open standard for connecting models to tools and data sources.
- **SoR** — System of Record. The authoritative store for a class of business data, for example a CRM for customer and opportunity data.
- **CRM and CPQ** — Customer Relationship Management, and Configure-Price-Quote. Our running enterprise examples.
- **LLMOps** — the operational discipline of deploy, monitor, version, cost, and evaluate for LLM-based systems.
