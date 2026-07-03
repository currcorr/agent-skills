# Sources & Verification Appendix

> Primary and reputable-secondary sources underpinning the factual, vendor, regulatory, and statistical claims in this knowledge base. Compiled during the mid-2026 web-research pass. **Before recording any time-sensitive claim on video, re-verify against these (or newer) primary sources** — vendor products, protocol specs, and regulations move fast. Claims marked ⚠ in the modules are the ones most likely to drift.
>
> **Confidence tiers used below:** *Primary* (vendor doc / standards body / press release / paper) · *Secondary* (reputable trade press / analyst) · *Soft* (blog/aggregator or contested — cite directionally only).

---

## Foundational papers (durable)
- *Attention Is All You Need* — Vaswani et al., 2017 (arXiv:1706.03762). Transformer architecture (Module 1.4–1.5).
- *Retrieval-Augmented Generation…* — Lewis et al., 2020 (arXiv:2005.11401). RAG (Module 3.1).
- *Chain-of-Thought Prompting* — Wei et al., 2022 (arXiv:2201.11903). (Module 2.1)
- *ReAct: Synergizing Reasoning and Acting* — Yao et al., 2022 (arXiv:2210.03629). (Module 2.1, 5.1)
- *LoRA: Low-Rank Adaptation* — Hu et al., 2021 (arXiv:2106.09685). (Module 2.5)
- *Constitutional AI* — Bai et al., 2022 (arXiv:2212.08073). (Module 1.7)
- *Why Language Models Hallucinate* — Kalai, Nachum, Vempala, Zhang, 2025 (OpenAI; published in *Nature*, 2026). (Module 1.9) — *Primary.*
- Long-context degradation: RULER (Hsieh et al., 2024), LongBench v2, HELMET. (Module 1.5–1.6)

## Module 1 — Foundations
- Model lineup & context windows & tokenizer note (Opus 4.7 "~30% more tokens"): Anthropic model docs — `platform.claude.com/docs/en/about-claude/models/overview`. *Primary.*
- Embedding SOTA (Gemini Embedding, Qwen3-Embedding): MTEB leaderboard + vendor blogs. *Secondary; rankings drift — verify.*
- SSMs in production (Mamba-3, Jamba, Nemotron-H): AI21 Jamba announcement; Cartesia/Together Mamba-3. *Secondary.*

## Module 2 — Capability Extension
- **MCP → Linux Foundation / Agentic AI Foundation (Dec 9, 2025):** `linuxfoundation.org` press release; `blog.modelcontextprotocol.io/posts/2025-12-09-...`; Anthropic announcement. *Primary.*
- MCP spec `2025-11-25` (stable) + a release candidate with target date `2026-07-28` (stateless core, MCP Apps, Tasks, OAuth/OIDC): `modelcontextprotocol.io/specification/...`; `blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/`. *⚠ The RC date is slightly in the future relative to this pass — verify it has published before citing as shipped.*
- MCP Registry (preview, Sept 8 2025): `blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/`. *Primary.*
- MCP security (Tool Poisoning; MCPoison CVE-2025-54136; CurXecute CVE-2025-54135; OWASP MCP Top 10): `owasp.org/www-project-mcp-top-10/`. *Primary/Secondary.*
- Anthropic native Structured Outputs (beta, Nov 2025): `platform.claude.com/docs/en/build-with-claude/structured-outputs`. *Primary.*
- OpenAI fine-tuning wind-down (to ~Jan 2027): `developers.openai.com/api/docs/deprecations`. *Primary.*
- RFT / GRPO: OpenAI RFT guide; AWS Bedrock RFT (Nova). *Primary.*
- Eval two-tier pattern, Braintrust: vendor comparison write-ups. *Soft — directional.*
- **Portable task adapters (emerging):** *PorTAL: Portable Task Adapters for LLMs* — Geist, B., Ramp Labs (2026), corporate research blog. Related prior art it builds on: Text-to-LoRA (Charakorn et al., ICML 2025, `openreview.net/forum?id=zWskCdu3QA`), Cross-LoRA (Xia et al., 2025, arXiv:2508.05232), LoRA-X (Farhadzadeh et al., 2025, arXiv:2501.16559), Platonic Representation Hypothesis (Huh et al., 2024, arXiv:2405.07987). *⚠ Soft — single-source, not peer-reviewed, narrow eval (14 MCQ tasks, small Qwen3/Gemma-3 models), self-reported; some cited references appear future-dated/unverifiable. Treat as a direction to watch, verify before relying.*

## Module 3 — RAG & Retrieval
- Embedding models: Gemini Embedding GA (`developers.googleblog.com`), Cohere Embed v4 (AWS Bedrock docs), Voyage-3.5, Qwen3-Embedding. *Primary/Secondary.*
- Rerankers: Cohere Rerank (`docs.cohere.com/docs/rerank`), Voyage rerank-2.5, Jina v2. *Primary.*
- pgvector 0.8 iterative index scans: `postgresql.org/about/news/pgvector-080-released-2952/`; AWS Aurora write-up. *Primary.*
- LazyGraphRAG: `microsoft.com/en-us/research/blog/lazygraphrag-...`. *Primary.*
- Contextual Retrieval in Bedrock: `aws.amazon.com/blogs/machine-learning/contextual-retrieval-in-anthropic-...`. *Primary.*
- Agentic RAG survey: arXiv:2501.09136. *Primary.*
- "RAG isn't dead / context engineering": multiple 2026 analyses. *Soft — directional.*

## Module 4 — Knowledge Representation
- **GQL = ISO/IEC 39075 (published April 2024):** `neo4j.com/press-releases/gql-standard/`; `aws.amazon.com/blogs/database/gql-...`. *Primary.*
- Neo4j native vector type + in-Cypher GraphRAG + neo4j-graphrag: `neo4j.com/blog/developer/...`; `neo4j.com/docs/neo4j-graphrag-python/`. *Primary.*
- Neptune Analytics + Bedrock GraphRAG GA: `aws.amazon.com/blogs/machine-learning/announcing-general-availability-of-amazon-bedrock-knowledge-bases-graphrag-...`. *Primary.*
- **Kùzu acquired by Apple, repo archived (Oct 2025):** `theregister.com/2025/10/14/kuzudb_abandoned/`; `github.com/kuzudb/kuzu`. *Secondary/Primary.*
- **Open Semantic Interchange (OSI, Sept 2025):** `snowflake.com/en/news/press-releases/...open-semantic-interchange...`. *Primary.*
- Semantic-layer vs text-to-SQL benchmark: `docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026`. *Soft — vendor benchmark, directional.*
- Palantir Ontology/AIP: `palantir.com/docs/foundry/aip/overview`. *Primary.*

## Module 5 — Agents & Orchestration
- LangChain/LangGraph 1.0 (Oct 2025): `langchain.com/blog/langchain-langgraph-1dot0`. *Primary.*
- Microsoft Agent Framework (AutoGen + Semantic Kernel merge): `learn.microsoft.com/en-us/agent-framework/overview/`. *Primary.*
- OpenAI AgentKit (DevDay Oct 2025): `openai.com/index/introducing-agentkit/`. *Primary.*
- Google ADK: `google.github.io/adk-docs/`. *Primary.*
- CrewAI 1.0: `crewai.com/blog/crewai-oss-1-0...`. *Primary.*
- Cloud renames: AWS Bedrock AgentCore GA (`aws.amazon.com/about-aws/whats-new/2025/10/...`); Google Gemini Enterprise Agent Platform (`cloud.google.com/products/gemini-enterprise-agent-platform`); Microsoft Foundry Agent Service (`techcommunity.microsoft.com/...`). *Primary.*
- OpenTelemetry GenAI semantic conventions: `opentelemetry.io/docs/specs/semconv/gen-ai/`. *Primary.*
- Multi-agent debate: Cognition "Don't Build Multi-Agents" (`cognition.com/blog/dont-build-multi-agents`); Anthropic multi-agent research system (`anthropic.com/engineering/multi-agent-research-system`). *Primary.*
- ⚠ Langfuse→ClickHouse acquisition (Jan 2026): secondary sources; verify.

## Module 6 — Enterprise Operationalization
- **EU AI Act Digital Omnibus (provisional 7 May 2026; high-risk deferred to Dec 2027 / Aug 2028):** `gibsondunn.com/eu-ai-act-omnibus-...`; `artificialintelligenceact.eu/implementation-timeline/`. *Secondary/Primary — provisional, verify adoption.*
- EU AI Act GPAI obligations (since 2 Aug 2025; enforcement 2 Aug 2026): `digital-strategy.ec.europa.eu`; `artificialintelligenceact.eu/enforcement-of-chapter-v-...`. *Primary.*
- NIST-AI-600-1 GenAI Profile (July 2024): `nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf`. *Primary.*
- ISO/IEC 42001 adoption: `iso.org/standard/42001`; vendor trust portals. *Primary/Secondary.*
- OWASP Top 10 for LLM Applications 2025: `genai.owasp.org/llm-top-10/`. *Primary.*
- CFPB Circulars 2022-03 / 2023-03 (adverse action + AI): `consumerfinance.gov/compliance/circulars/...`. *Primary.*
- NAIC Model Bulletin on AI (Dec 2023; ~24+ states): `content.naic.org/insurance-topics/artificial-intelligence`. *Primary/Secondary.*
- HHS Jan 2025 HIPAA Security Rule NPRM: `hipaajournal.com/when-ai-technology-and-hipaa-collide/`. *Secondary — proposed rule, verify final status.*
- Prompt caching mechanics: Anthropic (`platform.claude.com/docs/en/build-with-claude/prompt-caching`); OpenAI (`openai.com/index/api-prompt-caching/`); Google (`ai.google.dev/gemini-api/docs/caching`). *Primary.*
- Gateways (LiteLLM `github.com/BerriAI/litellm`; Portkey). *Primary.*

## Module 7 — Implementation & Adoption
- **MIT "GenAI Divide: State of AI in Business 2025"** (95% no-ROI; buy ~67% vs build ~⅓): MIT NANDA report PDF (`mlq.ai/media/...State_of_AI_in_Business_2025_Report.pdf`); Fortune coverage. *Primary/Secondary; ⚠ "95%" measures no-ROI on a modest sample — cite carefully.*
- **Gartner (Jun 2025):** >40% agentic AI projects canceled by 2027; "agent washing": `gartner.com/en/newsroom/press-releases/2025-06-25-...`. *Primary.*
- **McKinsey State of AI 2025** (39% EBIT impact / scaling gap): `mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai`. *Primary.*
- **BCG (Sep 2025)** (10/20/70 value split; 5% "future-built"): `bcg.com/publications/2025/are-you-generating-value-from-ai-the-widening-gap`. *Primary; ⚠ 10/20/70 is a reused heuristic.*
- **Deloitte State of AI in the Enterprise 2026** (21% mature agentic governance): `deloitte.com/us/en/...state-of-ai-in-the-enterprise.html`. *Primary.*
- Cases: Klarna (`fortune.com/2025/05/09/klarna-ai-humans-...`); Taco Bell (`inc.com/...taco-bell...`); McDonald's (`qsr.pro/...mcdonalds-ai-drive-thru-failed`). *Secondary.*
- ⚠ "~3× hub-and-spoke" stat: consultancy blogs, no clear primary — directional only.

## Module 8 — Cutting-Edge
- Reasoning-effort controls: `developers.openai.com/api/docs/guides/reasoning`; GPT-5 launch. DeepSeek R1 (Jan 2025, MIT). *Primary/Secondary.*
- Model-native memory (ChatGPT/Claude/Gemini): ⚠ product names/dates from secondary blogs — verify against vendor release notes.
- Computer-use: Operator→ChatGPT Agent; Project Mariner→Gemini/Chrome; OSWorld benchmark. ⚠ exact scores benchmark-dependent, verify.
- **A2A → Linux Foundation (June 2025); v1.0; AP2; 150+ orgs; cloud GA:** `linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project...`; A2A one-year PR. *Primary; some milestone figures via secondary — verify.*
- Model routing: OpenRouter Auto Router (`openrouter.ai/docs/...`); RouteLLM. *Primary/Secondary.*
- Red-teaming tools: PyRIT, garak, Inspect, DeepTeam + commercial platforms. *Primary/Secondary.*
- Agent identity standards: IETF drafts (AIMS/WIMSE — `ietf.org/archive/id/draft-klrc-aiagent-auth-00.html`), OAuth 2.1, SPIFFE/SPIRE; Microsoft Entra agentic-identity perspective. AIAP vendors (Aembit, Stytch, WorkOS). *Primary/Secondary; "93% unscoped keys" is soft — directional.*

## Module 9 — Systems of Record
- **Logik.ai acquired by ServiceNow (announced 3 Apr 2025, closed May 2025):** `newsroom.servicenow.com/press-releases/details/2025/ServiceNow-to-boost-CRM-offering-with-acquisition-of-Logik-ais-...`. *Primary — corrects the draft's Salesforce attribution.*
- Agentforce 3 / Atlas Reasoning Engine 3.0 / Multi-Agent Orchestration GA + MCP/A2A: `salesforce.com/agentforce/what-is-a-reasoning-engine/atlas/`; Summer '26 coverage. *Primary/Secondary; ⚠ verify version/GA.*
- Agentforce pricing (flex credits / per-conversation): `salesforce.com/news/press-releases/2025/05/15/agentforce-flexible-pricing-news/`; `salesforce.com/agentforce/pricing/`. *Primary; ⚠ verify.*
- Agentforce ARR (~$800M / ~29k deals, Q4 FY26): Salesforce earnings PRs. *Primary; vendor-defined — directional.*
- Salesforce CPQ End-of-Sale (27 Mar 2025) → Revenue Cloud Advanced: `salesforceben.com/salesforce-confirms-the-future-of-cpq/`. *Secondary.*
- Data Cloud / Data 360 zero-copy: `salesforce.com/data/connectivity/zero-copy/`. *Primary.*
- Einstein Trust Layer (zero-data-retention): `salesforce.com/.../trusted-ai/`. *Primary.*
- ServiceNow AI Agents — Yokohama (Mar 2025) / Zurich (Q4 2025), AI Agent Fabric (A2A/MCP): `servicenow.com/docs/r/yokohama/...`; `cio.com/article/...servicenow-zurich-release...`; `servicenow.com/platform/action-fabric.html`. *Primary/Secondary.*
- ServiceNow CPQ / Sales & Order Management / Telecom Order Management: `servicenow.com/products/cpq.html`, `.../sales-management.html`, `.../telecom-order-management.html`. *Primary.*

---

### Record-time verification checklist (highest-risk claims)
Re-verify these against primary sources immediately before recording — they are the most likely to be wrong-on-video if the world moved:
1. Logik.ai = **ServiceNow** (not Salesforce). ✅ corrected; still confirm.
2. Agentforce version/GA/pricing; ServiceNow AI Agents release names & tiers.
3. EU AI Act effective dates (GPAI + Digital Omnibus deferrals — provisional).
4. MCP spec revision & governance; A2A milestone figures.
5. Embedding/reranker/model-name rosters (MTEB drifts monthly).
6. Any illustrative metric in an "enterprise example" (the ~60% cost cuts, 71%→89% retrieval, 40% error reduction) — these are **hypothetical**, not measured results.
