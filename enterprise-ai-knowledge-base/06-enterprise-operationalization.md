# Module 6 — Enterprise Operationalization

> **Why this module exists:** A working prototype and a production enterprise system are separated by a wide, unglamorous gap: reference architecture, data pipelines, security, governance, and operations (LLMOps). This is where most enterprise AI initiatives actually succeed or die. This module is the "run it in production, safely, at cost, in compliance" module — and it's where the SoR-as-authoritative-backbone theme becomes concrete infrastructure.

**Module map**
6.1 Reference architecture & the modern AI stack
6.2 Data pipelines & the data backbone
6.3 Security, access control, PII & data governance
6.4 (folded into 6.3/6.5) — see cross-references
6.5 LLMOps: deployment, monitoring, versioning, cost, latency, caching, scaling
6.6 Compliance & auditability by vertical

---

## 6.1 Reference architecture & the modern AI stack

**(a) What it is / why it matters.**
A **reference architecture** is the canonical layered picture of how the pieces fit — so teams build consistently and know where each concern lives. The "modern AI stack" has stabilized enough that most enterprise systems share the same layers, even if vendors differ.

**(b) The layers (bottom to top).**
1. **Data & knowledge layer** — the sources of truth: **Systems of Record** (CRM, ERP, ITSM), data warehouse/lakehouse, document stores; plus AI-specific stores: **vector DB** (Module 3.4), **knowledge graph** (Module 4), and a **semantic layer** (Module 4.6). This is the **data backbone** (6.2).
2. **Data pipeline / ingestion layer** — ETL/ELT, connectors, chunking/embedding pipelines, change-data-capture to keep AI stores fresh (6.2).
3. **Retrieval & context layer** — RAG pipelines, rerankers, graph retrieval, the **context assembly** that builds each prompt (Modules 3–4).
4. **Model layer** — foundation models (API and/or self-hosted), embedding models, rerankers, small/specialized models; a **model gateway/router** (6.5, Module 8.7) to abstract and route across them.
5. **Orchestration layer** — agents, workflows, tool/function calling, **MCP** servers/clients, planning, memory (Modules 2, 5).
6. **Governance & safety layer (cross-cutting)** — guardrails, access control, PII handling, policy, audit (6.3, 6.6, Module 5.6). Wraps every layer.
7. **Observability & Ops layer (cross-cutting)** — tracing, eval, monitoring, cost/latency management, versioning (6.5, Module 5.8).
8. **Experience layer** — the UI/interface: chat, copilots embedded in apps, APIs, and **SoR-native surfaces** (Agentforce in Salesforce, Now Assist in ServiceNow).

**(c) Build vs. buy at the layer level (previews Module 7.2).** Enterprises rarely build all layers. Common posture: buy foundation models (API), buy or adopt platform-native for SoR-embedded use cases, build/assemble the retrieval + orchestration + governance "middle" that encodes your differentiation and controls. The **model itself is a commodity; the integration, data, and governance are the moat.**

**(d) Decision criteria.** Design so layers are **swappable** (model gateway so you're not locked to one model; MCP so tools are portable; semantic layer so data meaning is centralized). Put **governance and observability as cross-cutting** from the start, not bolted on.

**(e) Pitfalls.** Skipping the data backbone and pointing an LLM at raw systems; no model-abstraction (locked to one vendor); governance/observability as afterthoughts; a pile of point solutions with no coherent architecture.

**(f) Enterprise example.** A company's stack: Salesforce + ServiceNow (SoR) → Data Cloud + warehouse + pgvector + Neo4j (data/knowledge) → CDC + embedding pipelines (ingestion) → hybrid RAG + reranker (retrieval) → model gateway over two frontier models + a small router model (models) → LangGraph agents + MCP servers for SoR (orchestration) → guardrails + entitlement enforcement + audit (governance) → LangSmith/Datadog (observability) → Agentforce + an internal copilot (experience).

---

## 6.2 Data pipelines & the data backbone

**(a) What it is / why it matters.**
AI is only as good as the data feeding it. The **data backbone** is the curated, governed, connected data that grounds every answer and action; **data pipelines** are what keep it accurate, fresh, and permissioned. The unglamorous truth: **most enterprise AI failure is data failure** — stale, fragmented, mislabeled, or ungoverned data — not model failure.

**(b) Mechanics.**
- **Ingestion & integration** — connectors to SoRs, docs, and apps; **ETL/ELT** into a warehouse/lakehouse; **CDC (change data capture)** to propagate updates in near-real-time so AI stores don't go stale (critical for RAG over volatile data — Module 3.8).
- **Processing for AI** — parsing/cleaning (layout-aware extraction), **chunking + embedding pipelines** (Module 3.2/3.3), entity extraction/resolution for the KG (Module 4.4), metadata + **entitlement tagging** at ingest (essential for 6.3).
- **Freshness strategy** — decide per data type: **live query** the SoR (volatile/transactional facts), **CDC-synced mirror** (frequently-read, moderately-changing), or **batch re-index** (slow-changing docs). Wrong choice → stale answers.
- **Data quality** — validation, deduplication, lineage/provenance tracking (where did this fact come from?), and monitoring for drift.
- **Zero-copy / federation** — modern platforms (e.g., Salesforce Data Cloud, cloud lakehouses) increasingly **federate or zero-copy** data rather than physically duplicating it, reducing sync burden and residency risk.

**(c) Tools.** Ingestion/ELT (Fivetran, Airbyte, dbt), streaming/CDC (Kafka, Debezium), orchestration (Airflow, Dagster), lakehouse (Snowflake, Databricks, BigQuery), document parsing (`unstructured`, Docling), and platform data backbones (**Salesforce Data Cloud**, Microsoft Fabric, Databricks) — Module 09d.

**(d) Decision criteria.** Match freshness mechanism to volatility and stakes; **tag entitlements at ingest** (retrofitting access control is painful and leaky); track **lineage** for auditability; prefer **federation/zero-copy** to reduce copies (each copy is a residency + staleness + security liability).

**(e) Pitfalls & failure modes.**
- **Stale indexes** — the classic RAG failure; source changed, vectors didn't (Module 3.8).
- **Fragmented data / no unified customer view** — inconsistent answers; needs entity resolution + semantic layer (Module 4).
- **No entitlement metadata** — can't do access-aware retrieval later (6.3).
- **Garbage in** — bad extraction (mangled tables/PDFs) → bad retrieval.
- **Uncontrolled copies** — data sprawl across vector stores/warehouses multiplies breach and compliance surface.
- **No lineage** — can't answer "why did the AI say that?" or "where did this come from?" (audit gap).

**(f) Enterprise example.** A quote agent gives wrong prices intermittently. Root cause: the pricing table synced nightly, but reps changed prices intraday. Fix: switch pricing to a **live SoR query** (never embed volatile prices) and CDC-sync the slower-moving product catalog — a data-pipeline decision, not a model change.

---

## 6.3 Security, access control, PII & data governance

**(a) What it is / why it matters.**
This is the layer that determines whether enterprise AI is an asset or a liability. AI systems concentrate access to sensitive data and can take actions — so they inherit *and amplify* every security and privacy obligation the enterprise already has, plus new AI-specific threats. Get this wrong and you get data breaches, privacy violations, regulatory penalties, and lost trust. **This is frequently the actual blocker to enterprise AI deployment** — not capability.

**(b) Mechanics — the concerns and controls.**
- **Access control & entitlements (the core).** The agent must operate with the **requesting user's** permissions, not a super-user service account. Enforce entitlements **at the authoritative source** (SoR sharing rules / ACLs) and **pre-filter** all retrieval by access tags (Module 3.8). Propagate identity end-to-end (OAuth/token exchange). **The LLM is never the access boundary** (Module 5.6).
- **PII / sensitive data handling.**
  - **Minimization** — only send the model what's needed.
  - **Redaction/tokenization/masking** — strip or pseudonymize PII before it hits the model or logs where feasible (DLP tooling).
  - **Data residency & sovereignty** — keep regulated data in-region; choose model hosting accordingly (in-region API, VPC, or self-hosted open models).
  - **Retention** — govern how long prompts/outputs/traces (which contain PII) are kept; honor deletion/right-to-erasure.
  - **Training-data leakage** — ensure your data isn't used to train third-party models (enterprise API terms / no-train guarantees); watch fine-tuning baking PII into weights (Module 2.5).
- **AI-specific threats.** Mapped to the **OWASP Top 10 for LLM Applications (2025 edition)**: prompt injection (direct and **indirect** via retrieved/tool content — Modules 2.1, 2.4, 5.6), **sensitive information disclosure**, **supply chain**, **data/model poisoning**, **improper output handling**, **excessive agency** (agents with too-broad permissions), **system prompt leakage** (new), **vector & embedding weaknesses** (new — relevant to RAG), **misinformation**, and **unbounded consumption** (broadens the old "model DoS" to include denial-of-wallet). Reference also **NIST-AI-600-1** (GenAI Profile) and the **OWASP MCP Top 10** (Module 2.4).
- **Governance program.** Data classification, model/vendor risk assessment, an **AI acceptable-use policy**, an **AI governance board**, model cards/documentation, and an inventory of AI systems (increasingly a regulatory requirement — 6.6).
- **Secrets & supply chain.** Protect API keys/credentials the agent uses; vet third-party models/tools/MCP servers.

**(c) Tools/standards.** Enterprise IAM (Okta, Entra), DLP (Microsoft Purview, others), PII detection (Presidio), secrets managers, policy engines (OPA), guardrail libraries (Module 5.6); standards: **NIST AI RMF + GenAI Profile (NIST-AI-600-1)**, **ISO/IEC 42001** (AI management systems — now a live procurement requirement), **OWASP Top 10 for LLM Applications (2025)** + **OWASP MCP Top 10**, SOC 2, plus sector rules (6.6).

**(d) Decision criteria.** Classify data and match controls to sensitivity; for regulated/PII-heavy workloads consider **in-VPC or self-hosted** models and strict redaction; enforce **least privilege** and **user-scoped entitlements** always; treat **writes and cross-customer data** as highest-risk. Bake governance into the architecture (6.1), not a review at the end.

**(e) Pitfalls & failure modes.**
- **Service-account god-mode** — the agent sees everything, so users see everything they shouldn't. The archetypal breach.
- **Entitlement bypass in RAG** (Module 3.8) — indexing without access tags.
- **PII in logs/traces** — observability data becomes a breach vector (Module 5.8).
- **Indirect prompt injection** exfiltrating data via a tool.
- **Shadow AI** — employees pasting sensitive data into unsanctioned consumer tools.
- **Assuming the vendor handles it** — shared-responsibility gaps.

**(f) Enterprise example.** A support agent is architected so every SoR query runs **as the authenticated agent/user** through ServiceNow ACLs and Salesforce sharing rules; retrieved knowledge chunks are pre-filtered by access tags; PII is redacted from traces; the deployment uses an in-region model endpoint with a no-train contract; and a write to a case requires the user's entitlement plus an audit entry. Security review passes because the AI **inherits, not bypasses**, existing controls.

---

## 6.5 LLMOps: deployment, monitoring, versioning, cost, latency, caching, scaling

**(a) What it is / why it matters.**
**LLMOps** is the operational discipline for running LLM systems in production — the AI-specific extension of DevOps/MLOps. It's what keeps the system reliable, affordable, fast, and improvable *after* launch. Because LLM systems are nondeterministic, prompt-and-data-dependent, and usage-priced, they need ops practices that classic software doesn't.

**(b) Mechanics — the pillars.**
- **Deployment & environments.** Model access options: **hosted API** (fastest, least ops, data leaves boundary unless enterprise tier), **cloud-managed** (Bedrock/Vertex/Azure — in-cloud, more control), **self-hosted open models** (max control/residency, most ops — needs GPU serving via vLLM/TGI/TensorRT-LLM). CI/CD for prompts, tools, and agents; staged rollouts, canaries, and **feature flags** for models/prompts.
- **Versioning (of everything).** Not just code — **prompts, tools/schemas, models (and versions), embeddings/index, eval sets, and agent graphs** are all versioned and traceable. Pin model versions (a silent provider update can change behavior); manage model **deprecation/migration** with re-evaluation.
- **Monitoring & online eval** (Module 5.8) — latency, cost, error/tool-failure rates, quality/drift via online evals, guardrail triggers, user feedback; alerting on regressions.
- **Cost management** — the big one:
  - **Right-size the model** — don't use a frontier model where a small/cheap one passes eval; **route/cascade** (Module 8.7).
  - **Prompt caching** — cache stable prompt prefixes (system prompt, tools, retrieved context) to cut cost/latency dramatically on repeated calls (leverages KV-cache — Module 1.5). Mechanics differ by provider: **Anthropic** uses explicit cache breakpoints (write surcharge ~1.25× for 5-min / ~2× for 1-hr TTL, cached reads ~0.1×); **OpenAI** caches automatically with no write surcharge (cached input heavily discounted — up to ~90% on current models); **Google Gemini** offers implicit (default) + explicit context caching. All discount cached input dramatically.
  - **Semantic/response caching** — return cached answers for semantically-equivalent queries. *Correctness caveat: a too-loose similarity threshold can return a wrong answer for a subtly different query — use tight thresholds + scope keys, and never semantic-cache personalized or entitlement-sensitive results.*
  - **Token discipline** — trim context, rerank (Module 3.6), summarize history (Module 5.5).
  - **Batching**, and **budgets/quotas** per app/agent to prevent runaway loops (Module 5.1).
- **Latency management** — streaming responses (perceived speed), smaller/faster models for interactive steps, parallel tool calls, caching, and minimizing agent loop depth. Interactive UX targets vs. async/batch jobs have very different budgets.
- **Scaling — the enterprise-hard parts (not just "autoscale").** Provider **rate limits are per-key/per-org and do *not* autoscale**, so bursts hit a hard ceiling: handle it with **request queuing + backpressure (token-bucket) at the gateway**, not naïve retries (which amplify the overload). Multi-region/multi-provider failover has a subtle trap: a **fallback model is not a drop-in** — it may not support the same tool-call schema, JSON mode, or exhibit the same behavior, so the fallback path must be **separately evaluated** (Module 2.6), not assumed equivalent. Load-balance across regions/providers via the **gateway**; autoscale self-hosted serving.
- **Reliability** — retries with backoff, timeouts, fallback models (re-eval'd), circuit breakers, idempotency for actions (Module 5.6/09b).

**(c) Tools.** Model gateways/proxies (LiteLLM — 140+ providers; Portkey, now open-source core; cloud gateways; Kong AI; TrueFoundry) — note these now also **govern MCP/agent tool traffic**, not just model calls, applying the same access control, guardrails, PII redaction, and audit (an architectural convergence with the governance layer, 6.3). Serving (**vLLM** as the de-facto open engine, usually fronted by a gateway; TGI, TensorRT-LLM). Observability/eval (LangSmith, Langfuse, Arize, Braintrust, Datadog LLM Obs — Module 5.8), experiment/prompt management (PromptLayer, W&B), CI for evals (promptfoo, DeepEval). Native prompt caching in Anthropic/OpenAI/Google APIs.

**(d) Decision criteria.** Introduce a **model gateway** early (abstraction, routing, cost tracking, fallback). Cache aggressively where inputs repeat. Right-size models via eval (Module 2.6). Version and pin everything. Set **budgets and alerts** before, not after, the surprise bill. Choose hosting by residency/control needs (6.3).

**(e) Pitfalls & failure modes.**
- **Surprise cost** — deep agent loops, verbose contexts, using a frontier model everywhere; no budgets/caching.
- **Silent model drift** — provider updates a model version; behavior changes; no version pin, no regression eval.
- **No online eval** — quality degrades invisibly as data/queries shift.
- **Latency blowups** — long chains, huge contexts, no streaming.
- **Vendor lock-in / single point of failure** — no gateway, no fallback; provider outage takes you down.
- **Un-versioned prompts** — "someone changed the prompt and quality dropped, and we can't tell what changed."

**(f) Enterprise example.** A support copilot cuts cost ~60% by (1) routing simple FAQ deflections to a small model and only escalating hard cases to a frontier model (Module 8.7), (2) prompt-caching the large static system prompt + policy docs, and (3) capping agent loop depth. A model gateway tracks per-team spend, pins versions, and fails over to a secondary provider during an outage — all monitored with online eval that flags a quality dip the day a provider silently updated a model.

---

## 6.6 Compliance & auditability by vertical

**(a) What it is / why it matters.**
Regulated industries can't deploy AI on capability alone — they must satisfy **compliance** (legal/regulatory obligations) and **auditability** (the ability to prove, after the fact, what the system did, why, and under whose authority). This is often the gating factor for high-value use cases and it varies sharply by vertical. Auditability isn't a feature you add later — it's an architecture choice (logging, lineage, versioning, approvals baked in).

**(b) Mechanics — what auditability requires.**
- **Immutable audit logs** of actions (esp. writes), decisions, the data and permissions used, model/prompt versions, and **human approvals** (Modules 5.7/5.8).
- **Data lineage/provenance** (Module 6.2) — trace every answer to its sources.
- **Explainability** — cited sources (RAG), graph paths (Module 4), and recorded reasoning where required.
- **Model & system documentation** — model cards, risk assessments, DPIAs, an AI system inventory.
- **Reproducibility** — versioned prompts/models/data so a past decision can be reconstructed.
- **Access & retention controls** aligned to regulation (6.3).

**(c) The regulatory landscape (verify current specifics — this moves fast).**
- **Cross-cutting:** **EU AI Act** (risk-tiered obligations). ⚠ *Time-sensitive, verify:* **GPAI (general-purpose AI model) obligations apply since 2 Aug 2025** (technical docs, copyright policy, training-content summary), with Commission enforcement powers and Article 50 transparency duties from **2 Aug 2026**; a voluntary **GPAI Code of Practice** is the main compliance vehicle. The **"Digital Omnibus"** (provisional political agreement 7 May 2026, pending formal adoption) **deferred high-risk deadlines**: Annex III standalone systems (hiring, credit, biometrics…) to **2 Dec 2027** (from Aug 2026), and Annex I product-embedded systems to **2 Aug 2028** (from Aug 2027). Also: **NIST AI RMF** and its **Generative AI Profile (NIST-AI-600-1, July 2024, 12 GenAI-specific risks)**; **ISO/IEC 42001** (now a real procurement/vendor-selection requirement — Anthropic, Microsoft, Snowflake, ServiceNow, Salesforce, SAP among the certified); **GDPR/CCPA** (automated-decision and erasure rights).
- **Financial services** — model risk management (**SR 11-7**), fair-lending/**ECOA (Regulation B)** adverse-action rules per **CFPB Circulars 2022-03 and 2023-03** (specific, accurate reasons required *even for AI/"black-box" models* — inability to explain your own model is no defense), **FINRA/SEC** recordkeeping and supervision, AML/KYC. Heavy emphasis on explainability, audit trails, and human oversight — often confining the LLM to *assisting/drafting* rather than making the decision.
- **Healthcare** — **HIPAA** (PHI protection, BAAs; the **HHS Jan 2025 Security Rule NPRM**, if finalized, would explicitly require AI tools in risk analysis and bind them to minimum-necessary — verify final status), FDA considerations for clinical decision tools; consumer AI tools are **not** HIPAA-compliant for unredacted PHI without a BAA.
- **Insurance** — state regulation; the **NAIC Model Bulletin on Use of AI Systems by Insurers** (adopted Dec 2023; ~24+ states adopted by 2025) requires a written AI governance program, with stricter regimes in Colorado and New York (Circular Letter 2024-7).
- **Legal** — confidentiality/privilege, and duty-of-competence concerns (the notorious fabricated-citation sanctions — Module 1.9).
- **Public sector** — transparency, records laws, procurement rules.
- **Telecom/CPQ/commercial** — pricing/discount governance, contract accuracy, SOX for financially-material processes, consumer-protection rules.

**(c′) Regulation → concrete AI control (the mapping that makes this actionable).** A regulation isn't a checkbox; each forces a *specific* design choice:
- **ECOA/Reg B adverse action** doesn't just want "explainability" — it needs **specific, accurate reason codes** for a denial, which black-box LLMs can't reliably produce. Net effect: the LLM is usually **barred from making the decision** and confined to drafting/explanation, with a transparent model making the actual call.
- **SR 11-7 (model risk management)** implies a *program*: independent **model validation**, **challenger models**, ongoing performance **monitoring**, and documented lineage — not a one-time sign-off.
- **HIPAA** forces PHI **minimization + redaction**, a **BAA** with any model provider, and (per the 2025 NPRM) inclusion of AI tools in the **risk analysis**; consumer AI without a BAA is out.
- **EU AI Act high-risk** forces **human oversight**, technical documentation, logging, and transparency for in-scope systems.
The pattern: for the highest-stakes regulated decisions, regulation often **forbids the LLM from being the decision-maker** (adverse action, clinical decisions) and confines it to assisting — design for that up front.

**(d) Decision criteria.** Let the vertical's requirements drive architecture: high-stakes regulated decisions → **mandatory human-in-the-loop**, full audit logging, explainability (citations/paths), in-region/private model hosting, and conservative autonomy. Classify each use case by risk tier and apply proportionate controls. Engage compliance/legal **early** (Module 7.4 governance).

**(e) Pitfalls & failure modes.**
- **No audit trail** for AI actions/approvals — fails audit, blocks deployment.
- **Unexplainable decisions** in domains that legally require explanation (lending adverse action).
- **Treating compliance as a final gate** rather than an architecture input — expensive rework.
- **PII/PHI in prompts, logs, or training** — direct violation.
- **Assuming a global system fits all jurisdictions** — residency and rules differ.
- **Autonomy exceeding what regulation allows** — e.g., fully automated consequential decisions where human oversight is required.

**(f) Enterprise example.** A bank's collections-assistant proposes actions but a human makes every consequential decision; each recommendation logs the data used, the model/prompt version, cited policy, and the approver; adverse outcomes carry an explainable rationale; PHI/PII is redacted from traces; and the model runs in a private in-region endpoint. When examiners audit, ops reconstructs any decision end-to-end. In the CPQ context (Module 09), the analog is SOX-aligned logging of every price/discount/quote write with approver and rationale.

---

### Module 6 takeaways
- The **modern AI stack** is layered (data/knowledge → pipelines → retrieval → models → orchestration → experience) with **governance and observability cross-cutting**; design layers to be **swappable**.
- The **data backbone** (fresh, connected, entitlement-tagged, lineage-tracked) is where most AI success/failure actually lives; match freshness mechanism to volatility; prefer federation/zero-copy.
- **Security/governance** is often the real deployment blocker: user-scoped entitlements enforced at the source, PII minimization/redaction/residency, defense against injection and excessive agency, and a governance program (NIST AI RMF, ISO 42001, OWASP LLM Top 10). The LLM is **never** the access boundary.
- **LLMOps** keeps it reliable and affordable: version everything, monitor + online-eval, and control cost/latency via **right-sizing, routing/cascades, prompt/semantic caching, token discipline, gateways, and fallbacks**.
- **Compliance/auditability** is vertical-specific and an **architecture input**: immutable audit logs, lineage, explainability, human-in-the-loop, and reproducibility — not a final gate.

*Proceed to `07-implementation-adoption.md`.*
