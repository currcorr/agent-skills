# Module 6 — Enterprise Operationalization

*This is the enterprise-operationalization module of a knowledge base on production enterprise AI; it can be understood on its own.*

**Why this module exists:** A working prototype and a production enterprise system are separated by a wide, unglamorous gap: reference architecture, data pipelines, security, governance, and operations, known as LLMOps. This is where most enterprise AI initiatives actually succeed or die. This is the "run it in production, safely, at cost, in compliance" module. It's also where the theme of the system of record as the authoritative backbone becomes concrete infrastructure.

**What this module covers.** There are five parts. First, the reference architecture and the modern AI stack. Second, data pipelines and the data backbone. Third, security, access control, PII, and data governance. Fourth, LLMOps, meaning deployment, monitoring, versioning, cost, latency, caching, and scaling. And fifth, compliance and auditability by vertical.

---

## Reference architecture and the modern AI stack

**Why it matters.**
A reference architecture is the canonical layered picture of how the pieces fit, so teams build consistently and know where each concern lives. The modern AI stack has stabilized enough that most enterprise systems share the same layers, even if vendors differ.

**How it works: the layers, from bottom to top.**
First, the data and knowledge layer. These are the sources of truth: Systems of Record such as CRM, ERP, and ITSM; the data warehouse or lakehouse; and document stores. It also includes AI-specific stores: the vector database, the knowledge graph, and a semantic layer. This is the data backbone.

Second, the data pipeline, or ingestion, layer. This covers ETL and ELT, connectors, chunking and embedding pipelines, and change-data-capture to keep AI stores fresh.

Third, the retrieval and context layer. This holds RAG pipelines, rerankers, graph retrieval, and the context assembly that builds each prompt.

Fourth, the model layer. This includes foundation models, whether by API or self-hosted; embedding models; rerankers; and small or specialized models. It also includes a model gateway or router to abstract and route across them.

Fifth, the orchestration layer. This covers agents, workflows, tool and function calling, MCP servers and clients, planning, and memory.

Sixth, the governance and safety layer, which is cross-cutting. This includes guardrails, access control, PII handling, policy, and audit. It wraps every layer.

Seventh, the observability and operations layer, also cross-cutting. This covers tracing, evaluation, monitoring, cost and latency management, and versioning.

Eighth, the experience layer. This is the UI or interface: chat, copilots embedded in apps, APIs, and system-of-record-native surfaces such as Agentforce in Salesforce and Now Assist in ServiceNow.

**The main options and standards: build versus buy at the layer level.** Enterprises rarely build all layers. The common posture is: buy foundation models by API; buy or adopt platform-native tools for use cases embedded in the system of record; and build or assemble the retrieval, orchestration, and governance middle that encodes your differentiation and controls. The model itself is a commodity; the integration, data, and governance are the moat.

**When to use it, and when not to.** Design so layers are swappable. Use a model gateway so you're not locked to one model. Use MCP so tools are portable. Use a semantic layer so data meaning is centralized. Put governance and observability in place as cross-cutting concerns from the start, not bolted on.

**Where it goes wrong.** Skipping the data backbone and pointing an LLM at raw systems. Having no model-abstraction, which locks you to one vendor. Treating governance and observability as afterthoughts. And accumulating a pile of point solutions with no coherent architecture.

**A concrete example.** Consider one company's stack. At the base sit Salesforce and ServiceNow as the systems of record. These feed a data and knowledge layer of Data Cloud, a warehouse, pgvector, and Neo4j. Above that runs an ingestion layer of change-data-capture and embedding pipelines. That supports a retrieval layer of hybrid RAG plus a reranker. The model layer is a model gateway over two frontier models plus a small router model. Orchestration uses LangGraph agents and MCP servers for the systems of record. Governance adds guardrails, entitlement enforcement, and audit. Observability runs on LangSmith and Datadog. And the experience layer is Agentforce plus an internal copilot.

---

## Data pipelines and the data backbone

**Why it matters.**
AI is only as good as the data feeding it. The data backbone is the curated, governed, connected data that grounds every answer and action. The data pipelines are what keep it accurate, fresh, and permissioned. The unglamorous truth is that most enterprise AI failure is data failure, meaning stale, fragmented, mislabeled, or ungoverned data, not model failure.

**How it works.**
Start with ingestion and integration. This means connectors to systems of record, documents, and apps; ETL and ELT into a warehouse or lakehouse; and change data capture, which propagates updates in near-real-time so AI stores don't go stale. That is critical for RAG over volatile data.

Then comes processing for AI. This covers parsing and cleaning, including layout-aware extraction; chunking and embedding pipelines; entity extraction and resolution for the knowledge graph; and metadata plus entitlement tagging at ingest, which is essential for security and governance.

Next is freshness strategy, decided per data type. You can live-query the system of record for volatile or transactional facts. You can use a change-data-capture-synced mirror for data that is frequently read and moderately changing. Or you can batch re-index slow-changing documents. The wrong choice leads to stale answers.

Then there's data quality: validation, deduplication, lineage and provenance tracking so you know where each fact came from, and monitoring for drift.

Finally, zero-copy and federation. Modern platforms, such as Salesforce Data Cloud and cloud lakehouses, increasingly federate or zero-copy data rather than physically duplicating it, which reduces sync burden and residency risk.

**The main options and standards.** For ingestion and ELT, there are Fivetran, Airbyte, and dbt. For streaming and change data capture, Kafka and Debezium. For orchestration, Airflow and Dagster. For the lakehouse, Snowflake, Databricks, and BigQuery. For document parsing, unstructured and Docling. And for platform data backbones, Salesforce Data Cloud, Microsoft Fabric, and Databricks.

**When to use it, and when not to.** Match the freshness mechanism to volatility and stakes. Tag entitlements at ingest, because retrofitting access control is painful and leaky. Track lineage for auditability. And prefer federation and zero-copy to reduce copies, because each copy is a residency, staleness, and security liability.

**Where it goes wrong.** Stale indexes are the classic RAG failure: the source changed but the vectors didn't. Fragmented data with no unified customer view produces inconsistent answers; it needs entity resolution plus a semantic layer. With no entitlement metadata, you can't do access-aware retrieval later. Garbage in, meaning bad extraction from mangled tables or PDFs, leads to bad retrieval. Uncontrolled copies mean data sprawl across vector stores and warehouses, which multiplies breach and compliance surface. And with no lineage, you can't answer "why did the AI say that?" or "where did this come from?", which is an audit gap.

**A concrete example.** A quote agent gives wrong prices intermittently. The root cause: the pricing table synced nightly, but reps changed prices intraday. The fix: switch pricing to a live system-of-record query, so volatile prices are never embedded, and change-data-capture-sync the slower-moving product catalog. This is a data-pipeline decision, not a model change.

---

## Security, access control, PII, and data governance

**Why it matters.**
This is the layer that determines whether enterprise AI is an asset or a liability. AI systems concentrate access to sensitive data and can take actions. So they inherit *and amplify* every security and privacy obligation the enterprise already has, plus new AI-specific threats. Get this wrong and you get data breaches, privacy violations, regulatory penalties, and lost trust. This is frequently the actual blocker to enterprise AI deployment, not capability.

**How it works: the concerns and controls.**
Access control and entitlements are the core. The agent must operate with the requesting user's permissions, not a super-user service account. Enforce entitlements at the authoritative source, meaning system-of-record sharing rules and ACLs, and pre-filter all retrieval by access tags. Propagate identity end-to-end through OAuth or token exchange. The LLM is never the access boundary.

Next, PII and sensitive data handling. Practice minimization: only send the model what's needed. Use redaction, tokenization, and masking to strip or pseudonymize PII before it hits the model or logs where feasible, using DLP tooling. Respect data residency and sovereignty: keep regulated data in-region, and choose model hosting accordingly, whether an in-region API, a VPC, or self-hosted open models. Govern retention: control how long prompts, outputs, and traces, which contain PII, are kept, and honor deletion and right-to-erasure. And guard against training-data leakage: ensure your data isn't used to train third-party models, using enterprise API terms and no-train guarantees, and watch for fine-tuning baking PII into weights.

Then, AI-specific threats, mapped to the OWASP Top 10 for LLM Applications, 2025 edition. These include prompt injection, both direct and indirect via retrieved or tool content; sensitive information disclosure; supply chain; data and model poisoning; improper output handling; excessive agency, meaning agents with too-broad permissions; system prompt leakage, which is new; vector and embedding weaknesses, also new and relevant to RAG; misinformation; and unbounded consumption, which broadens the old "model denial of service" to include denial-of-wallet. Reference also NIST-AI-600-1, the GenAI Profile, and the OWASP MCP Top 10.

There's also the governance program. This means data classification, model and vendor risk assessment, an AI acceptable-use policy, an AI governance board, model cards and documentation, and an inventory of AI systems, which is increasingly a regulatory requirement.

And finally, secrets and supply chain: protect the API keys and credentials the agent uses, and vet third-party models, tools, and MCP servers.

**The main options and standards.** For identity and access management, there are enterprise tools such as Okta and Entra. For DLP, Microsoft Purview and others. For PII detection, Presidio. There are also secrets managers, policy engines such as OPA, and guardrail libraries. On standards: the NIST AI RMF plus the GenAI Profile, NIST-AI-600-1; ISO/IEC 42001 for AI management systems, now a live procurement requirement; the OWASP Top 10 for LLM Applications, 2025, plus the OWASP MCP Top 10; SOC 2; plus sector rules.

**When to use it, and when not to.** Classify data and match controls to sensitivity. For regulated or PII-heavy workloads, consider in-VPC or self-hosted models and strict redaction. Enforce least privilege and user-scoped entitlements always. Treat writes and cross-customer data as highest-risk. And bake governance into the architecture, not a review at the end.

**Where it goes wrong.** Service-account god-mode is the archetypal breach: the agent sees everything, so users see everything they shouldn't. Entitlement bypass in RAG happens when you index without access tags. PII in logs and traces turns observability data into a breach vector. Indirect prompt injection can exfiltrate data via a tool. Shadow AI is employees pasting sensitive data into unsanctioned consumer tools. And assuming the vendor handles it leads to shared-responsibility gaps.

**A concrete example.** A support agent is architected so every system-of-record query runs as the authenticated agent or user, through ServiceNow ACLs and Salesforce sharing rules. Retrieved knowledge chunks are pre-filtered by access tags. PII is redacted from traces. The deployment uses an in-region model endpoint with a no-train contract. And a write to a case requires the user's entitlement plus an audit entry. The security review passes because the AI inherits, rather than bypasses, existing controls.

---

## LLMOps: deployment, monitoring, versioning, cost, latency, caching, scaling

**Why it matters.**
LLMOps is the operational discipline for running LLM systems in production. It's the AI-specific extension of DevOps and MLOps. It's what keeps the system reliable, affordable, fast, and improvable *after* launch. Because LLM systems are nondeterministic, prompt-and-data-dependent, and usage-priced, they need ops practices that classic software doesn't.

**How it works: the pillars.**
Start with deployment and environments. There are several model-access options. A hosted API is fastest and least ops, but data leaves your boundary unless you use an enterprise tier. Cloud-managed options such as Bedrock, Vertex, and Azure stay in-cloud and give more control. Self-hosted open models give maximum control and residency but the most ops, since they need GPU serving via vLLM, TGI, or TensorRT-LLM. You'll also want CI/CD for prompts, tools, and agents, along with staged rollouts, canaries, and feature flags for models and prompts.

Next, versioning of everything. Not just code, but prompts, tools and schemas, models and their versions, embeddings and index, eval sets, and agent graphs are all versioned and traceable. Pin model versions, because a silent provider update can change behavior. And manage model deprecation and migration with re-evaluation.

Then, monitoring and online eval. Track latency, cost, error and tool-failure rates, quality and drift via online evals, guardrail triggers, and user feedback, with alerting on regressions.

Cost management is the big one. First, right-size the model: don't use a frontier model where a small or cheap one passes eval; route or cascade instead. Second, use prompt caching: cache stable prompt prefixes, meaning the system prompt, tools, and retrieved context, to cut cost and latency dramatically on repeated calls, which leverages the KV-cache. The mechanics differ by provider. Anthropic uses explicit cache breakpoints, with a write surcharge of roughly 1.25 times for the 5-minute TTL or roughly 2 times for the 1-hour TTL, and cached reads at roughly 0.1 times. OpenAI caches automatically with no write surcharge, and cached input is heavily discounted, up to roughly 90% on current models. Google Gemini offers implicit, or default, caching plus explicit context caching. All of them discount cached input dramatically. Third, semantic or response caching returns cached answers for semantically-equivalent queries. There's a correctness caveat here: a too-loose similarity threshold can return a wrong answer for a subtly different query. So use tight thresholds plus scope keys, and never semantic-cache personalized or entitlement-sensitive results. Fourth, practice token discipline: trim context, rerank, and summarize history. And fifth, use batching, plus budgets and quotas per app or agent, to prevent runaway loops.

Then there's latency management. Stream responses for perceived speed. Use smaller and faster models for interactive steps. Run parallel tool calls. Cache. And minimize agent loop depth. Interactive UX targets and async or batch jobs have very different budgets.

Then, scaling, which is the enterprise-hard part, not just "autoscale." Provider rate limits are per-key or per-org and do *not* autoscale, so bursts hit a hard ceiling. Handle it with request queuing plus backpressure, using a token-bucket, at the gateway, not with naïve retries, which amplify the overload. Multi-region and multi-provider failover has a subtle trap: a fallback model is not a drop-in. It may not support the same tool-call schema or JSON mode, and it may not behave the same way. So the fallback path must be separately evaluated, not assumed equivalent. Load-balance across regions and providers via the gateway, and autoscale self-hosted serving.

Finally, reliability. Use retries with backoff, timeouts, fallback models that have been re-evaluated, circuit breakers, and idempotency for actions.

**The main options and standards.** For model gateways and proxies, there are LiteLLM, supporting more than 140 providers; Portkey, whose core is now open-source; cloud gateways; Kong AI; and TrueFoundry. Note that these now also govern MCP and agent tool traffic, not just model calls, applying the same access control, guardrails, PII redaction, and audit. That's an architectural convergence with the governance layer. For serving, vLLM is the de-facto open engine, usually fronted by a gateway, alongside TGI and TensorRT-LLM. For observability and eval, there are LangSmith, Langfuse, Arize, Braintrust, and Datadog LLM Obs. For experiment and prompt management, PromptLayer and W&B. For CI on evals, promptfoo and DeepEval. And there's native prompt caching in the Anthropic, OpenAI, and Google APIs.

**When to use it, and when not to.** Introduce a model gateway early, for abstraction, routing, cost tracking, and fallback. Cache aggressively where inputs repeat. Right-size models via eval. Version and pin everything. Set budgets and alerts before, not after, the surprise bill. And choose hosting by residency and control needs.

**Where it goes wrong.** Surprise cost comes from deep agent loops, verbose contexts, and using a frontier model everywhere, with no budgets or caching. Silent model drift happens when a provider updates a model version, behavior changes, and there's no version pin and no regression eval. With no online eval, quality degrades invisibly as data and queries shift. Latency blowups come from long chains, huge contexts, and no streaming. Vendor lock-in and single points of failure arise with no gateway and no fallback, so a provider outage takes you down. And un-versioned prompts leave you saying "someone changed the prompt and quality dropped, and we can't tell what changed."

**A concrete example.** A support copilot cuts cost by roughly 60% in three ways. First, it routes simple FAQ deflections to a small model and only escalates hard cases to a frontier model. Second, it prompt-caches the large static system prompt plus policy docs. Third, it caps agent loop depth. A model gateway tracks per-team spend, pins versions, and fails over to a secondary provider during an outage. All of this is monitored with online eval that flagged a quality dip the day a provider silently updated a model.

---

## Compliance and auditability by vertical

**Why it matters.**
Regulated industries can't deploy AI on capability alone. They must satisfy compliance, meaning legal and regulatory obligations, and auditability, meaning the ability to prove, after the fact, what the system did, why, and under whose authority. This is often the gating factor for high-value use cases, and it varies sharply by vertical. Auditability isn't a feature you add later. It's an architecture choice, with logging, lineage, versioning, and approvals baked in.

**How it works: what auditability requires.**
You need immutable audit logs of actions, especially writes, along with decisions, the data and permissions used, the model and prompt versions, and human approvals. You need data lineage and provenance, so you can trace every answer to its sources. You need explainability, meaning cited sources from RAG, graph paths, and recorded reasoning where required. You need model and system documentation: model cards, risk assessments, DPIAs, and an AI system inventory. You need reproducibility, meaning versioned prompts, models, and data so a past decision can be reconstructed. And you need access and retention controls aligned to regulation.

**The regulatory landscape.** Verify current specifics, because this moves fast.

Start with cross-cutting rules. There's the EU AI Act, with its risk-tiered obligations. The next part is time-sensitive, so verify it carefully. The GPAI, or general-purpose AI model, obligations apply since the 2nd of August 2025. These cover technical docs, copyright policy, and a training-content summary. Commission enforcement powers and the Article 50 transparency duties apply from the 2nd of August 2026. A voluntary GPAI Code of Practice is the main compliance vehicle. The Digital Omnibus, which reached provisional political agreement on the 7th of May 2026 and is pending formal adoption, deferred the high-risk deadlines. Under it, Annex III standalone systems, covering hiring, credit, and biometrics, move to the 2nd of December 2027, from the earlier August 2026. And Annex I product-embedded systems move to the 2nd of August 2028, from the earlier August 2027. Also cross-cutting: the NIST AI RMF and its Generative AI Profile, NIST-AI-600-1, from July 2024, covering 12 GenAI-specific risks. Then ISO/IEC 42001, now a real procurement and vendor-selection requirement, with Anthropic, Microsoft, Snowflake, ServiceNow, Salesforce, and SAP among the certified. And GDPR and CCPA, covering automated-decision and erasure rights.

Next, financial services. This involves model risk management under SR 11-7. It involves fair-lending and adverse-action rules under ECOA, meaning Regulation B, per CFPB Circulars 2022-03 and 2023-03, which require specific, accurate reasons even for AI or "black-box" models; inability to explain your own model is no defense. It involves FINRA and SEC recordkeeping and supervision, plus AML and KYC. There's heavy emphasis on explainability, audit trails, and human oversight, often confining the LLM to assisting or drafting rather than making the decision.

Then healthcare. This centers on HIPAA, covering PHI protection and BAAs. The HHS January 2025 Security Rule NPRM, if finalized, would explicitly require AI tools in risk analysis and bind them to minimum-necessary; verify the final status. There are also FDA considerations for clinical decision tools. And consumer AI tools are *not* HIPAA-compliant for unredacted PHI without a BAA.

Then insurance, which is state-regulated. The NAIC Model Bulletin on Use of AI Systems by Insurers was adopted in December 2023 and had been adopted by roughly 24 or more states by 2025. It requires a written AI governance program, with stricter regimes in Colorado and New York, the latter under Circular Letter 2024-7.

Then legal. This raises confidentiality and privilege concerns, plus duty-of-competence concerns, including the notorious fabricated-citation sanctions.

Then the public sector: transparency, records laws, and procurement rules.

And finally telecom, CPQ, and commercial: pricing and discount governance, contract accuracy, SOX for financially-material processes, and consumer-protection rules.

**From regulation to concrete AI control: the mapping that makes this actionable.** A regulation isn't a checkbox; each one forces a *specific* design choice.

Take ECOA and Regulation B adverse action. It doesn't just want "explainability." It needs specific, accurate reason codes for a denial, which black-box LLMs can't reliably produce. The net effect is that the LLM is usually barred from making the decision and confined to drafting and explanation, with a transparent model making the actual call.

Take SR 11-7, model risk management. It implies a *program*: independent model validation, challenger models, ongoing performance monitoring, and documented lineage, not a one-time sign-off.

Take HIPAA. It forces PHI minimization and redaction, a BAA with any model provider, and, per the 2025 NPRM, inclusion of AI tools in the risk analysis; consumer AI without a BAA is out.

Take EU AI Act high-risk. It forces human oversight, technical documentation, logging, and transparency for in-scope systems.

The pattern is that, for the highest-stakes regulated decisions, regulation often forbids the LLM from being the decision-maker, as with adverse action and clinical decisions, and confines it to assisting. Design for that up front.

**When to use it, and when not to.** Let the vertical's requirements drive architecture. High-stakes regulated decisions call for mandatory human-in-the-loop, full audit logging, explainability through citations and paths, in-region or private model hosting, and conservative autonomy. Classify each use case by risk tier and apply proportionate controls. And engage compliance and legal early.

**Where it goes wrong.** No audit trail for AI actions and approvals fails the audit and blocks deployment. Unexplainable decisions fail in domains that legally require explanation, such as lending adverse action. Treating compliance as a final gate, rather than an architecture input, leads to expensive rework. PII or PHI in prompts, logs, or training is a direct violation. Assuming a global system fits all jurisdictions ignores that residency and rules differ. And autonomy exceeding what regulation allows, such as fully automated consequential decisions where human oversight is required, is a violation.

**A concrete example.** A bank's collections-assistant proposes actions, but a human makes every consequential decision. Each recommendation logs the data used, the model and prompt version, the cited policy, and the approver. Adverse outcomes carry an explainable rationale. PHI and PII are redacted from traces. And the model runs in a private in-region endpoint. When examiners audit, ops can reconstruct any decision end-to-end. In the CPQ context, the analog is SOX-aligned logging of every price, discount, and quote write, with approver and rationale.

---

### Module 6 takeaways
- The modern AI stack is layered, running from data and knowledge, to pipelines, to retrieval, to models, to orchestration, to experience, with governance and observability cross-cutting. Design the layers to be swappable.
- The data backbone, meaning fresh, connected, entitlement-tagged, and lineage-tracked data, is where most AI success and failure actually lives. Match the freshness mechanism to volatility, and prefer federation and zero-copy.
- Security and governance is often the real deployment blocker. It calls for user-scoped entitlements enforced at the source; PII minimization, redaction, and residency; defense against injection and excessive agency; and a governance program built on the NIST AI RMF, ISO 42001, and the OWASP LLM Top 10. The LLM is never the access boundary.
- LLMOps keeps it reliable and affordable. Version everything, monitor and online-eval, and control cost and latency through right-sizing, routing and cascades, prompt and semantic caching, token discipline, gateways, and fallbacks.
- Compliance and auditability is vertical-specific and an architecture input. It calls for immutable audit logs, lineage, explainability, human-in-the-loop, and reproducibility, not a final gate.
