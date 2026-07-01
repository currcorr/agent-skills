# Revision Notes — Consolidated Review & Update Punch List

> Output of an adversarial review (4 lenses: depth 1–4, depth 5–9, sourcing/accuracy, NotebookLM-format) plus a per-module web-research pass (Modules 1–9), conducted mid-2026 against the early-2026 draft. Findings are deduped across lenses and ranked by priority tier. Source URLs live in each module agent's detail; the highest-value ones are inlined here.

**Legend:** 🔴 must-fix factual error · 🟠 high-value currency/accuracy · 🟡 depth gap · 🔵 format/NotebookLM · 🟣 sourcing infrastructure

---

## TIER 0 — Critical factual error (fix regardless of scope)

- 🔴 **Logik.ai was acquired by ServiceNow, not Salesforce.** Module 09 states the opposite (§09.d Salesforce bullet, §09.e roadmap flags, takeaways). Reality: **ServiceNow** announced the Logik.ai acquisition **3 Apr 2025**, closed **May 2025**; it's an API-first/composable AI CPQ engine being folded into ServiceNow Sales & Order Management / CRM. Salesforce's CPQ successor is **Revenue Cloud Advanced** (its own build — no Logik.ai). *Fix: remove Logik.ai from the Salesforce section; attribute it to ServiceNow.* Source: ServiceNow newsroom (Apr 3 2025).

---

## TIER 1 — High-value currency / accuracy updates (per module)

### Module 1 — Foundations (light-moderate)
- 🟠 **Context windows:** 1M tokens now standard across frontier models (Claude Opus 4.8 / Sonnet 5 / Fable 5, Gemini); Llama 4 Scout advertises 10M (with recall caveats). Replace "128k–200k common, some 1M+."
- 🟠 **Tokenizer heuristic:** keep "~4 chars/token" but add that it's tokenizer-specific and drifting — Anthropic's tokenizer from Claude Opus 4.7 onward produces **~30% more tokens** for the same text than earlier Claude models. Strengthens "recount when the tokenizer changes."
- 🟠 **Hallucination causes (§1.9):** add the "evaluation incentives reward confident guessing over abstention" thesis (OpenAI "Why Language Models Hallucinate," 2025; Nature 2026) and the mitigation (reward calibrated uncertainty in evals).
- 🟠 **Reasoning ≠ less hallucination:** hedge the reasoning-models bullet — extended thinking can *increase* hallucination on summarization/faithfulness even as it cuts math/logic errors.
- 🟡 **"Lost in the middle":** firm up from "debated in degree" to "repeatedly confirmed on 1M-token models (RULER, LongBench v2, HELMET)."
- 🟠 **Refresh rosters:** embeddings SOTA now Gemini Embedding + Qwen3-Embedding (open); Mamba/SSM (Mamba-3, Jamba, Nemotron-H) moved from "emerging" to production.

### Module 2 — Capability Extension (MCP is the heavy lift)
- 🟠 **MCP governance:** donated to the **Agentic AI Foundation under the Linux Foundation (Dec 9 2025)** — no longer Anthropic-owned; strengthens the anti-lock-in argument.
- 🟠 **MCP spec:** stable rev **2025-11-25**; RC **2026-07-28** (stateless core, Extensions, MCP Apps, Tasks, OAuth/OIDC hardening, 12-month deprecation policy). Adoption now near-universal (OpenAI, Google, Microsoft). Add the **MCP Registry** (preview, Sept 2025).
- 🟠 **MCP security:** cite real incidents — **tool poisoning**, MCPoison (CVE-2025-54136), CurXecute (CVE-2025-54135), **OWASP MCP Top 10**.
- 🟠 **Structured outputs:** Anthropic shipped **native Structured Outputs** (beta Nov 2025) + strict tools; Gemini has `response_json_schema`. Serving-side grammar backends: **XGrammar / llguidance** (flag XGrammar-as-default as moderately verified).
- 🟠 **Fine-tuning:** **OpenAI is winding down self-serve fine-tuning** (new-job creation ends ~Jan 2027) — reinforces "fine-tunes are a liability." Add **RFT/GRPO** (reinforcement fine-tuning; OpenAI o4-mini, Bedrock Nova).
- 🟠 **Eval:** add **Braintrust** and the now-standard **two-tier pattern** (CI framework like DeepEval/RAGAS/promptfoo + observability platform). LLM-as-judge → "mature/standard."

### Module 3 — RAG & Retrieval (rosters a generation behind)
- 🟠 **Embeddings:** Gemini Embedding (`gemini-embedding-001`, GA Feb 2026), **Cohere Embed v4** (multimodal, 128K ctx, Matryoshka+int8/binary), Voyage-3.5/-lite, **Qwen3-Embedding** (open SOTA), Jina v4. Add multimodality + long-context as selection axes.
- 🟠 **Rerankers:** Cohere **Rerank 4.0**, Voyage **rerank-2.5**, Jina Reranker v2, bge-reranker-v2-m3 (top options cluster within a few nDCG points).
- 🟠 **pgvector 0.8** iterative index scans fix filtered-ANN under-fetching (directly strengthens the "filtering correctness" + "pgvector as default" theses); pgvectorscale StreamingDiskANN + SBQ.
- 🟠 **LazyGraphRAG** (Microsoft, open-source) removes GraphRAG's indexing cost (~0.1% of full) — answers the module's own GraphRAG con.
- 🟠 **Agentic/Adaptive RAG** now mainstream best-practice; add "**context engineering**" framing and the "RAG isn't dead vs long-context" consensus (retrieval far cheaper/auditable).
- 🟡 **Contextual retrieval** → "Established" (built into Amazon Bedrock Knowledge Bases).

### Module 4 — Knowledge Representation (frontier → productized)
- 🟠 **GQL** is a **published ISO standard (ISO/IEC 39075, Apr 2024)** — not "being standardized"; Cypher now conforms. Update takeaways.
- 🟠 **Kùzu acquired by Apple, repo archived (Oct 2025)** — add a vendor-durability note.
- 🟠 **Neo4j native vector data type + in-Cypher GraphRAG + neo4j-graphrag lib** are GA; **Amazon Neptune Analytics + Bedrock GraphRAG** GA.
- 🟠 **Open Semantic Interchange (OSI)** — vendor-neutral semantic standard (Snowflake/Salesforce/dbt/Cube, Sept 2025) aimed at BI+agents; benchmark-backed semantic-layer-beats-text-to-SQL. Elevate Palantir Ontology as the leading ontology-for-agents exemplar.
- 🟡 **GraphRAG and LLM-assisted entity resolution** → downgrade "emerging" to "productized/maturing."

### Module 5 — Agents & Orchestration (framework list materially stale)
- 🟠 **LangGraph/LangChain 1.0** (GA Oct 2025); prebuilt ReAct agent now in `langchain.agents`.
- 🟠 **Microsoft Agent Framework** (GA early 2026) = **AutoGen + Semantic Kernel merged**; both predecessors now maintenance-only. (Replaces the "AG2 fork" note.)
- 🟠 **OpenAI AgentKit** (Agent Builder, ChatKit, Connector Registry, Evals) on the Agents SDK (Oct 2025). Add **Google ADK** and **Pydantic AI 1.0** to the framework list; **CrewAI 1.0 + Flows/AMP**.
- 🟠 **Cloud renames/GA:** AWS **Bedrock AgentCore** (GA), Google **Gemini Enterprise Agent Platform** (Vertex+Agentspace merged), Azure **Foundry Agent Service** ("Microsoft Foundry").
- 🟠 **OTel GenAI/agent semantic conventions** matured (agent + MCP tool-call spans); observability tools now OTel-native (Langfuse→ClickHouse, flag to verify).
- 🟡 Cite the **Cognition ("Don't Build Multi-Agents") vs Anthropic** debate as the named source of the single-vs-multi stance; add "context engineering"; note 2026 convergence on orchestrator-of-isolated-workers. Add **A2A** alongside MCP in the portability caveat.

### Module 6 — Enterprise Operationalization (regulatory precision)
- 🟠 **EU AI Act "Digital Omnibus"** (provisional agreement 7 May 2026): high-risk deadlines deferred — **Annex III → 2 Dec 2027**, **Annex I → 2 Aug 2028**. Replace vague "2025–2027."
- 🟠 **GPAI** obligations apply since **2 Aug 2025**; enforcement powers **2 Aug 2026**; Art. 50 transparency 2 Aug 2026; GPAI Code of Practice.
- 🟠 Name the specifics: **NIST-AI-600-1 GenAI Profile** (12 risks); **ISO/IEC 42001** now a real procurement requirement (Anthropic, Microsoft, Snowflake, ServiceNow, Salesforce, SAP certified); **OWASP LLM Top 10 2025** (add System Prompt Leakage, Vector/Embedding Weaknesses; "Unbounded Consumption" incl. denial-of-wallet).
- 🟠 Sector authorities: **CFPB Circulars 2022-03/2023-03** (adverse action, black-box no defense); **NAIC Model Bulletin** (Dec 2023, ~24+ states); **HHS Jan 2025 HIPAA Security Rule NPRM** (flag: proposed).
- 🟠 **Prompt caching** concrete mechanics/pricing (Anthropic breakpoints 1.25×/2× write, 0.1× read; OpenAI auto ~90% off; Gemini implicit+explicit). Gateways (LiteLLM/Portkey) now **govern MCP/agent tool traffic**, not just model calls.

### Module 7 — Implementation & Adoption (add sourced stats)
- 🟠 **MIT "GenAI Divide" (2025):** 95% of enterprise GenAI pilots show **no measurable P&L return** (flag: measures no-ROI, small sample). Root cause = integration/"learning gap."
- 🟠 **Buy vs build:** MIT — vendor/partnership deployments succeed **~67%** vs internal builds **~⅓**.
- 🟠 **Gartner (2025):** **>40% of agentic AI projects canceled by end-2027**; "**agent washing**." Add as a failure pattern.
- 🟠 **McKinsey (2025):** only **39%** report enterprise EBIT impact, most <5% — the "scaling gap."
- 🟠 **BCG (2025):** ~**70%** of AI value = people/process, ~10% algorithms (flag: reused heuristic). **Deloitte (2025):** only **21%** have mature agentic-AI governance.
- 🟠 Named cautionary cases: **Klarna** (reversed full-AI support), **McDonald's/Taco Bell** (drive-thru pullbacks).

### Module 8 — Cutting-Edge (most out of date; relabel maturities)
- 🟠 **Agent-to-agent (§8.5): emerging → stabilizing.** A2A donated to Linux Foundation (Jun 23 2025), **v1.0 + signed Agent Cards**, **AP2 payments**, GA in Copilot Studio/Foundry & Bedrock AgentCore, **150+ orgs**; MCP/A2A/ACP governance converging under LF. Soften "expect fragmentation."
- 🟠 **Reasoning (§8.1):** `reasoning_effort`/thinking-budget controls now standard → "early-production, approaching standard." Name DeepSeek R1 as the open watershed.
- 🟠 **Memory (§8.2): → stabilizing** — model-native memory now default in consumer assistants (verify product specifics); governed-enterprise version remains the differentiator.
- 🟠 **Computer-use (§8.4): → early-production (embedded).** Operator folded into ChatGPT Agent; Project Mariner into Gemini/Chrome; OSWorld scores rising (flag exact %).
- 🟠 **SLM/routing (§8.7): → early-production.** GPT-5 native auto-router, OpenRouter Auto Router; 40–85% reported bill cuts.
- 🟠 **GraphRAG (§8.6):** cost blocker largely solved (LazyGraphRAG-class).
- 🟠 **Eval (§8.8):** automated red-teaming → **stabilizing** (PyRIT, garak, Inspect, DeepTeam + commercial platforms; CI-gated); simulation eval productized.
- 🟠 **Agent governance (§8.9):** name forming standards — **IETF AIMS/WIMSE, OAuth 2.1, SPIFFE/SPIRE**, MCP-mandated OAuth 2.1; AIAP vendor category (Aembit, Stytch, WorkOS) — but keep the honest caveat (93% of agent projects still use unscoped API keys). Update the radar table accordingly.

### Module 9 — Systems of Record (beyond the Logik.ai fix)
- 🟠 **Agentforce 3 / Atlas Reasoning Engine 3.0** (Summer '26): **Multi-Agent Orchestration GA**, native **MCP + A2A** (strengthens the hybrid/composable narrative).
- 🟠 **Agentforce pricing:** flex credits (~$0.10/action) or ~$2/conversation (org-level). **ARR ~$800M, ~29k deals (Q4 FY26)** — attribute to Salesforce, note marketing-defined.
- 🟠 **Salesforce CPQ End-of-Sale 27 Mar 2025** → Revenue Cloud Advanced. **Einstein Trust Layer** adds zero-data-retention. Data Cloud (now under **Data 360**) zero-copy confirmed — drop "verify."
- 🟠 **ServiceNow:** AI Agents GA via **Yokohama (Mar 2025)**, extended **Zurich (Q4 2025)**; **AI Agent Fabric** ships with **A2A + MCP**; **SOM/CPQ/Telecom OM** are GA/documented — narrow the "thin" flag to *fully autonomous agentic CPQ* only (that caveat still holds).

---

## TIER 2 — Depth gaps (explain the mechanics, don't just name them)

- 🟡 **Explain, don't name-drop** (recurring across Modules 1–4): constrained decoding (token masking), Reciprocal Rank Fusion (combines ranks not scores), ANN/HNSW (navigable graph vs brute force), RLHF/DPO/Constitutional AI (one sentence of mechanism each), contrastive embedding training, GraphRAG communities→summaries→map-reduce, bi- vs cross-encoder caching asymmetry, FFN + residual connections.
- 🟡 **Worked examples** for the two most decision-critical, currently-thinnest sections: **evaluation (§2.6)** — a sample eval row + LLM-judge rubric + set-size guidance; **chunking (§3.2)** — a concrete default (e.g., ~300–500 tokens, ~15% overlap for prose) to deviate from.
- 🟡 **Write-path mechanics (§09.b/e) — biggest depth hole:** multi-object atomicity (Salesforce Composite/savepoints/allOrNone; sagas), idempotency-key derivation (deterministic from business intent, reused across retries), rollback taxonomy (reversible/compensating/irreversible), and OBO token-exchange (RFC 8693 — intersection of agent scope ∩ user rights; token lifetime for long tasks; how an unattended agent has an identity at all). **Also correct the "SoRs give you ACID for free" claim** — atomicity across a multi-object quote write must be engineered on Salesforce/ServiceNow.
- 🟡 **Salesforce vs ServiceNow — make it substantive** (§09.d): record-of-truth SoR vs workflow-state SoR, and what that implies for where approvals/audit/CPQ natively live. Distinguish Data Cloud (data-unification backbone) from a governed metric/semantic layer; develop CSDM as ServiceNow's canonical-model answer.
- 🟡 **CPQ pricing depth** (§09.e Stage 3): price waterfall (list→volume→contracted→promo→net), price rules vs discount schedules, approval matrix (discount % × deal size × product), margin-impact surfacing.
- 🟡 **Memory mechanics (§5.5):** write/salience policy, conflict resolution (SoR-wins by re-fetch), retrieval trigger (tool-invoked vs always-on).
- 🟡 **Entitlement-aware RAG hard case** (§09.b/§3.8): static ingest-time tags can't represent dynamic/criteria-based sharing (Salesforce sharing is *computed*) → options: post-retrieval re-check as the user, tag+resync (staleness risk), or route record-level facts through live structured reads.
- 🟡 **Caveat two over-confident heuristics:** the "0.95^10 ≈ 60%" compounding-error math (assumes independence; verification/HITL break it) and logprob-based confidence routing (often unavailable/poorly calibrated; prefer judge/self-consistency/groundedness).

---

## TIER 3 — Format normalization for NotebookLM (needs a pass before upload)

- 🔵 **Kill the `(a)/(b)/(c)/(d)/(e)/(f)` letter scaffolding** (60+ subsections) → plain spoken sub-heads ("Why it matters," "How it works," "A common pitfall"). Remove `(b′)`, `(c/d)` merged/prime variants.
- 🔵 **Strip/prose-ify inline cross-refs** (~289 total "Module X.Y" / "(1.5)" refs) — they narrate as gibberish and dangle when a file is uploaded alone. Replace with prose bridges ("as covered in the retrieval module").
- 🔵 **Convert the 3 load-bearing tables to prose** (Module 8 radar; §09.d platform tradeoff; drop the redundant §09.e boundary table).
- 🔵 **Fix special glyphs / inline code:** `→` chains, `O(n²)`, `king − man + woman ≈ queen`, `≥`/`×`, inline Cypher/JSON — spell out or move code to fenced blocks preceded by a prose gloss.
- 🔵 **Structural consistency:** delete the phantom **§6.4** placeholder (renumber); normalize **"09" vs "9"** and `09.b`/`9.2` subsection scheme; remove the **"(Pass 2)"** artifact and filename-based "Proceed to" lines; make heading levels consistent (promote §3.7's techniques and §09.e's stages to real subsections).
- 🔵 **Self-containment:** add a 2–3 sentence standalone summary at the top of each subsection + a per-file "this is one module of a series; understandable on its own" context line.
- 🔵 **Reduce cross-file redundancy:** give each mantra one canonical home ("LLM is never the boundary," "fine-tune for behavior/retrieve for knowledge," the CPQ walkthrough) and soften restatements.
- 🔵 **Recommended approach:** produce a **narration-clean variant** for NotebookLM while keeping the current reader-facing version (best of both).

---

## TIER 4 — Sourcing infrastructure (prompt explicitly required primary sources)

- 🟣 **Per-claim verify flags** on from-memory factual claims — vendor, regulatory, protocol-origin, superlative, and numeric-heuristic — because subsections get extracted as standalone videos and a README caveat doesn't travel with them.
- 🟣 **Add a Sources appendix** (one file, or per-module references) with real links: papers (arXiv/DOI), specs (MCP, A2A, ISO/IEC 39075 & 42001), vendor docs (Agentforce/Data Cloud/Revenue Cloud; ServiceNow AI Agents/CPQ/Logik.ai), regulatory primaries (EUR-Lex AI Act, Fed SR 11-7, NIST-AI-600-1, OWASP LLM Top 10 2025, CFPB Circulars, NAIC).
- 🟣 **Label illustrative numbers as hypothetical** (the ~60% cost cuts, 71%→89% retrieval, 40% error reduction, "market leader" for Neo4j) so viewers don't take them as measured results.

---

## Suggested sequencing

1. **Tier 0 + Tier 1** (factual correctness + currency) — the credibility-critical edits; ~1 focused rewrite of §2.4 (MCP) and §5.3 (frameworks), regulatory refresh of §6.6, roster refresh in §3/§8, and the Module 9 vendor updates.
2. **Tier 4** (verify flags + sources appendix) — pairs naturally with Tier 1 since you're already touching each claim.
3. **Tier 2** (depth) — the write-path mechanics, worked examples, and Salesforce-vs-ServiceNow substance are the highest-value additions.
4. **Tier 3** (format) — best done last, ideally as a generated narration-clean variant so the reader version stays intact.

*All source URLs are preserved in the individual research-agent outputs.*
