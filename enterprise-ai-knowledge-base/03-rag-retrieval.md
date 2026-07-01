# Module 3 — RAG & Retrieval

> **Why this module exists:** Retrieval is where most enterprise AI value — and most enterprise AI failure — actually lives. RAG (Retrieval-Augmented Generation) is the dominant pattern for giving a model current, private, permissioned, citable knowledge without fine-tuning. It's also the single best mitigation for hallucination on factual tasks. This module builds RAG from the ground up, then layers on the advanced techniques and the failure modes, and begins weaving in the **Systems-of-Record (SoR) integration** theme that continues through Module 09.

**Module map**
3.1 The retrieval problem (and what RAG is)
3.2 Chunking strategies
3.3 Embedding models for retrieval
3.4 Vector databases (pgvector, Pinecone, Weaviate, …)
3.5 Semantic vs. hybrid search
3.6 Reranking
3.7 Advanced RAG (query rewriting, multi-hop, contextual retrieval, GraphRAG)
3.8 **SoR integration:** grounding on live SoR data & entitlement-aware retrieval
3.9 Retrieval evaluation and failure modes

---

## 3.1 The retrieval problem (and what RAG is)

**(a) What it is / why it matters.**
Models have three knowledge gaps: they don't know **your private data**, they don't know **anything after their training cutoff**, and they **hallucinate** on specifics (Module 1.9). **RAG** closes all three by **retrieving relevant text at query time and putting it in the prompt**, so the model answers *from provided sources* rather than from memory. It's the difference between "what do you remember?" and "here are the documents — answer from these and cite them."

**Analogy.** Closed-book exam (bare LLM: recall from memory, confident guessing) vs. open-book exam (RAG: look up the relevant page, answer from it, cite it). Open-book is more accurate, updatable, and auditable.

**(b) Mechanics — the classic RAG pipeline** (Lewis et al., 2020, generalized):
1. **Ingest (offline):** collect documents → **chunk** them (3.2) → **embed** each chunk (3.3) → store vectors + text + metadata in a **vector database** (3.4).
2. **Retrieve (online):** embed the user's query → find the **top-k** most similar chunks (semantic search, 3.5) → optionally **rerank** (3.6).
3. **Augment:** insert retrieved chunks into the prompt with instructions ("answer only from this context; cite sources; say you don't know if unsupported").
4. **Generate:** the model produces a grounded, cited answer.

**(b′) Why RAG beats fine-tuning for knowledge (recap of 1.7/2.5):** updatable in real time (change the data, not the model), permissionable per-user (filter what's retrieved — 3.8), citable/auditable, cheaper, and it doesn't bake stale facts into weights.

**(d) Decision criteria.** Use RAG whenever the answer depends on data that is **private, changing, large, or must be cited/permissioned** — i.e., nearly all enterprise knowledge work. Skip RAG when the task is pure reasoning/transformation over text already in the prompt.

**On "is RAG dead?" (the long-context debate).** Million-token windows and agents did *not* replace retrieval. For large, changing, permissioned, citable corpora, retrieval remains far cheaper and more auditable than context-stuffing (widely cited as roughly an order of magnitude cheaper, with better latency and traceability). The mid-2026 mental-model shift is toward **"context engineering"**: retrieval is one tool — chosen, often via adaptive routing (3.7), alongside long context, tools, and memory — for assembling the right context per query.

**(e) Pitfalls (previewing 3.9).** "RAG" is easy to demo and hard to make reliable. Most failures are **retrieval** failures (wrong/missing chunks), not generation failures — you can't reason well over the wrong context. Garbage retrieved → garbage answered, but *confidently*.

**(f) Enterprise example.** "What's our return policy for enterprise hardware?" A bare model invents a plausible policy. A RAG system retrieves the actual policy document section and answers from it with a citation — and returns "I couldn't find that" if nothing relevant exists.

---

## 3.2 Chunking strategies

**(a) What it is / why it matters.**
Documents are too big to embed or retrieve whole, so you split them into **chunks**. Chunking quality **caps** the quality of everything downstream: chunk too big and retrieval is imprecise and dilutes attention; too small and you sever the context needed to understand a passage. It's the most under-appreciated lever in RAG.

**(b) Mechanics — strategies, weakest to strongest for most cases.**
- **Fixed-size** (e.g., 500 tokens) with **overlap** (e.g., 10–20%) — simple baseline; overlap avoids cutting mid-idea. Blind to structure.
- **Recursive/character splitting** — split on a hierarchy of separators (paragraphs → sentences → words) to respect natural boundaries. Common default.
- **Structure-aware** — split on document structure (markdown headings, HTML sections, PDF layout, code functions, table rows). Much better because chunks align to semantic units.
- **Semantic chunking** — detect topic shifts (via embedding similarity between sentences) and split there. Better coherence; more compute.
- **Sentence-window / small-to-big** — retrieve on small precise chunks but *feed the model a larger surrounding window* for context. Strong pattern.
- **Parent-document / hierarchical retrieval** — index small child chunks, return the parent section. Balances precision and context.
- **Contextual chunking** (see 3.7, "contextual retrieval") — prepend a short LLM-generated summary of the chunk's place in the document before embedding, so isolated chunks stay interpretable.

**Metadata is part of chunking.** Store with each chunk: source doc, section, date, author, **access-control tags/entitlements** (critical for 3.8), and any structured fields you'll filter on.

**(c) Tools.** LangChain/LlamaIndex splitters, `unstructured` (layout-aware parsing of PDFs/Office docs), Docling, vendor ingestion pipelines.

**(d) Decision criteria.** Match chunking to document type: structured docs → structure-aware; dense prose → semantic/recursive; contracts/policies → section-aware with generous overlap so clauses aren't severed; tables → row- or record-oriented. **A defensible default to deviate from:** start with **recursive splitting at ~300–500 tokens with ~15% overlap** for prose, then measure and adjust — go **smaller** (~150–250) when you need precise pinpoint retrieval and will use small-to-big/parent-document expansion, **larger** (~800–1,000) for narrative documents where continuity matters. **Tune against your embedding model's sweet spot and measure via retrieval eval (3.9).** There is no universal chunk size — but "recursive, ~400 tokens, ~15% overlap" is a sane starting point.

**(e) Pitfalls & failure modes.**
- **Severed context** — a clause split from its heading ("Section 7.2… the party may terminate…" without knowing which party/contract).
- **Mixing topics** in one chunk → muddy embeddings → poor retrieval.
- **Losing tables/layout** — naïve text extraction destroys tabular meaning; use layout-aware parsers.
- **No metadata** — you can't filter by recency or entitlement later; a governance dead-end.
- **One-size chunking** across heterogeneous corpora.

**(f) Enterprise example.** For master service agreements, the team chunks by clause/section, prepends the contract title + section heading to each chunk (contextual), and tags each with the owning account and its access group — so retrieval is precise *and* entitlement-filterable (3.8).

---

## 3.3 Embedding models for retrieval

**(a) What it is / why it matters.**
The embedding model (Module 1.3) decides what "similar" means for your corpus. Its quality directly determines whether the *right* chunks are retrievable at all. Choosing and evaluating it is a first-class decision, not a default.

**(b) Mechanics & selection axes.**
- **Retrieval quality on your domain** — measure with your own eval set (3.9); public leaderboards (e.g., MTEB) are a starting point, not an answer.
- **Dimensionality** — higher dims can capture more but cost more storage/latency; **Matryoshka** embeddings let you truncate dimensions for a tunable tradeoff.
- **Max input length** — must accommodate your chunk size (3.2).
- **Multilingual** needs.
- **Multimodality & long context (newer axis)** — several current models (Cohere Embed v4, Jina v4, Gemini) embed text *and* images/PDF pages into one space (useful for charts/tables/scans), and very long context (Embed v4 ≈128K tokens) relaxes the chunk-size ceiling.
- **Query vs. document asymmetry** — some models use different encodings for queries vs. passages (or instruction prefixes like "query: …"/"passage: …"); use them correctly.
- **Domain adaptation** — general embeddings can miss jargon (medical, legal, telecom, product SKUs); domain-tuned or fine-tuned embeddings help.
- **Hosting/residency** — API vs. self-hosted (open models like `bge`, `e5`, `nomic`, `gte`, Qwen3-Embedding) for data-residency/compliance (Module 6.3).

**(c) Vendors (mid-2026).** **Google Gemini Embedding (`gemini-embedding-001`)** and open-weight **Qwen3-Embedding** lead MTEB; **Cohere Embed v4** (multimodal, ~128K context, Matryoshka + int8/binary compression) and **Voyage-3.5 / -lite** (domain variants) are strong; OpenAI `text-embedding-3-large` is still solid but no longer benchmark-leading; open: Qwen3, Jina v4 (multimodal), BGE, E5, GTE, Nomic. The open-vs-proprietary gap has largely closed. ⚠ *MTEB rankings drift monthly — verify.*

**(d) Decision criteria.** Pick 2–3 candidates, run *your* retrieval eval, and choose on quality-per-cost. Prefer a model you can afford to **re-run over the whole corpus** when you upgrade. If data can't leave your boundary, choose a strong open model you can self-host.

**(e) Pitfalls.** Query/document embedded with different models (breaks geometry — 1.3); ignoring instruction prefixes the model expects; assuming biggest = best; forgetting that **changing the model means re-indexing everything**.

**(f) Enterprise example.** A pharma company finds a general embedding model conflates drug names; a domain-tuned biomedical embedding model lifts retrieval hit-rate on their eval set from 71% → 89%, and they self-host it to keep documents on-prem.

---

## 3.4 Vector databases

**(a) What it is / why it matters.**
A **vector database** stores embeddings and finds the nearest ones to a query vector fast, at scale — **Approximate Nearest Neighbor (ANN)** search. It's the retrieval engine of RAG. The market ranges from "a Postgres extension" to dedicated distributed systems; the right choice depends on scale, existing stack, and filtering needs.

**(b) Mechanics.**
- **Why "approximate"?** Exact nearest-neighbor means comparing the query to *every* stored vector — linear per query, which is far too slow at millions of vectors. **ANN (Approximate Nearest Neighbor)** pre-builds an index — a navigable "map" of the vector space — that you traverse greedily to find *almost* the closest vectors while touching only a tiny fraction of them, trading occasional misses for 100–1000× speed.
- **ANN indexes** trade a little recall for big speed: **HNSW** (a *hierarchical navigable small-world graph* — think layered shortcuts, coarse-to-fine, that you hop across to home in on neighbors; low-latency, memory-heavy — most common), **IVF/IVF-PQ** (cluster the space, then search only the nearest clusters, with product **quantization** to compress vectors for memory savings), **DiskANN** (SSD-backed graph for huge corpora that won't fit in RAM).
- **Metadata filtering** — restrict search by fields (date, source, **entitlement tags** — 3.8). *How* filtering interacts with the ANN index (pre-filter vs. post-filter) affects correctness and speed; entitlement filtering must be **pre-filter / correct**, never best-effort. (Filtered-ANN "under-fetching" was a classic failure; **pgvector 0.8's iterative index scans** specifically address it.)
- **Quantization** (scalar/product/binary) shrinks vectors for cost; trades some recall.
- **Hybrid support** — many stores now index both dense vectors and sparse/keyword (BM25) for hybrid search (3.5).

**(c) Tools/vendors and how they differ.**
- **pgvector (Postgres extension)** — vectors *inside* your existing Postgres. Huge advantage: **co-locate with your relational data**, transactional consistency, familiar ops, join vectors to business tables, reuse row-level security. A pragmatic default for many enterprises up to large scale; may need tuning/partitioning at very high scale. (**pgvector 0.8** added iterative index scans + faster HNSW build/query; **pgvectorscale** adds StreamingDiskANN + Statistical Binary Quantization for compressed, disk-backed scale.)
- **Pinecone** — fully managed, serverless, scales easily, strong metadata filtering; SaaS (data leaves your VPC unless using private networking tiers); usage-based cost.
- **Weaviate** — open-source or managed; built-in hybrid search, modules, GraphQL; self-hostable for residency.
- **Qdrant** — open-source, performant, strong filtering; self-host or managed.
- **Milvus / Zilliz** — built for very large scale, multiple index types.
- **Elasticsearch/OpenSearch** — mature keyword + added vector; great when you already run it and want hybrid.
- **Cloud-native** — Azure AI Search, Vertex AI Vector Search, MongoDB Atlas Vector Search, Redis. Convenience + integration with existing platform.

**(d) Decision criteria.**
- **Already on Postgres / need transactional consistency & joins to business data / moderate scale** → **pgvector** (often the pragmatic winner; fewer moving parts).
- **Massive scale, want zero ops, SaaS acceptable** → Pinecone/Zilliz.
- **Data residency / must self-host / want built-in hybrid** → Weaviate/Qdrant/Milvus.
- **Already run Elastic/OpenSearch** → use its vector support for hybrid.
- Decisive factors: scale, latency SLA, **filtering correctness (entitlements!)**, hybrid support, hosting/residency, and ops burden.

**(e) Pitfalls & failure modes.**
- **Recall vs. speed** misconfigured — over-aggressive ANN/quantization silently drops relevant results.
- **Filtering that's post-hoc** — entitlement filters applied after ANN can miss or leak; ensure correct pre-filtering (security-critical, 3.8).
- **Stale index** — source data changes but vectors don't; need re-index/CDC pipelines (Module 6.2).
- **Over-engineering** — spinning up a distributed vector cluster when pgvector would do, adding ops cost and a sync problem.
- **Metadata as an afterthought** — you can't filter/permission what you didn't store.

**(f) Enterprise example.** A company already running managed Postgres for its CRM-adjacent data uses **pgvector**: chunks live in the same database as the accounts they belong to, entitlement tags are enforced with Postgres **row-level security**, and retrieval joins vectors to live account rows — one system, one security model, transactional consistency (a preview of 3.8 and Module 09).

---

## 3.5 Semantic vs. hybrid search

**(a) What it is / why it matters.**
**Semantic (dense) search** matches by *meaning* (embeddings). **Keyword (sparse/lexical) search** (e.g., **BM25**) matches by *exact terms*. Each fails where the other shines. **Hybrid search** combines them and is, in practice, the strongest general default for enterprise retrieval.

**(b) Mechanics.**
- **Semantic** — great for paraphrase, synonyms, concepts ("end my plan" ≈ "cancel subscription"). Weak on exact identifiers.
- **Keyword/BM25** — great for **exact tokens**: product SKUs, error codes, part numbers, names, acronyms, legal citations — precisely where embeddings blur ("SKU-4471-B" must match exactly).
- **Hybrid** — run both, then **fuse** the two result lists. The standard method is **Reciprocal Rank Fusion (RRF)**: it scores each result by the **reciprocal of its rank position** in each list — `1 / (k + rank)`, summed across lists (k is a small constant) — and re-sorts by that sum. The key insight: RRF uses only **rank positions, not raw scores**, which is exactly why it sidesteps the problem that BM25 scores and cosine similarities live on **incomparable scales**. (Weighted score-blending is the alternative but requires normalizing those scales first.) Captures both meaning and exact matches.

**(d) Decision criteria.** Corpora full of **identifiers, codes, names, jargon** (enterprise reality — SKUs, incident IDs, config codes) → **hybrid**. Pure conceptual prose → semantic may suffice. Because enterprise data is riddled with exact identifiers, **default to hybrid** unless you've measured that semantic-only is enough.

**(e) Pitfalls.** Semantic-only missing exact SKU/code matches (a classic CPQ failure); keyword-only missing paraphrased questions; naïve score fusion (raw cosine vs. BM25 scores aren't comparable — use RRF or normalize).

**(f) Enterprise example.** A user asks "pricing for the enterprise firewall bundle SKU FW-9000." Semantic search finds firewall/bundle concepts; keyword search nails "FW-9000"; hybrid returns the exact product page *and* related bundles. Semantic-only would risk returning the wrong SKU's price — dangerous in CPQ (Module 09e).

---

## 3.6 Reranking

**(a) What it is / why it matters.**
Initial retrieval optimizes for **speed at scale** (ANN over millions of chunks), so it's approximate. A **reranker** takes the top ~20–100 candidates and **re-scores them for true relevance** with a heavier, more accurate model, keeping only the best few for the prompt. It's one of the highest-ROI additions to a RAG pipeline: better precision, fewer tokens, less "lost in the middle" (1.5).

**(b) Mechanics.**
- **Two-stage retrieval, and *why* it's two stages:** a **bi-encoder** embeds the query and each document **separately**, so document vectors can be **pre-computed once at index time and cached** — fast and scalable, but the model never sees query and document together. A **cross-encoder** feeds **query + document as one input** and scores their *interaction* — far more accurate, but it **can't be pre-computed** (it needs the query), so every query-document pair is a fresh model call. That caching asymmetry is the whole reason for the design: use the cheap cacheable bi-encoder to retrieve a candidate set over millions of chunks, then spend the expensive cross-encoder only on the ~20–100 survivors.
- **LLM rerankers** — prompt an LLM to score/order passages (more powerful, more expensive; overlaps with LLM-as-judge, 8.8).
- Output: a tightly relevant, ordered short list (e.g., top 3–5) placed in the prompt, best-first.

**(c) Tools/vendors (mid-2026).** **Cohere Rerank 4.0** (fast/pro) and 3.5 (multilingual, handles JSON/semi-structured, 4096-token); **Voyage rerank-2.5 / -lite** (with code/finance/legal variants); **Jina Reranker v2** (open, multilingual/multimodal); open **bge-reranker-v2-m3**; newer entrants (e.g., Zerank); Elastic/Vertex rerankers and vendor-native rerank in RAG platforms. On typical English RAG the top options cluster within a few nDCG points — pick on latency, cost, language, and your eval.

**(d) Decision criteria.** Add reranking when retrieval recall is decent but precision is poor (right docs are *somewhere* in the top 50 but not the top 5), when you must **minimize context tokens** for cost/latency, or when "lost in the middle" is hurting answers. Nearly always worth testing.

**(e) Pitfalls.** Added latency/cost per query (budget for it); reranking can't fix bad *recall* (if the right chunk isn't in the candidate set, reranking can't rescue it — fix chunking/embeddings/hybrid first); over-trimming to top-1 can drop needed context.

**(f) Enterprise example.** A support RAG bot retrieves 50 candidate KB passages via hybrid search, reranks to the 4 most relevant, and feeds those to the model — cutting prompt tokens ~80% while *raising* answer accuracy, because the model now sees only on-point context.

---

## 3.7 Advanced RAG

> Beyond "chunk-embed-retrieve," these techniques handle hard queries, multi-step questions, and structured knowledge. Maturity varies — labeled per technique.

**Query rewriting / transformation (Established → Stabilizing).**
The user's raw question is often a poor search query (ambiguous, pronoun-laden, multi-part). An LLM rewrites/expands it before retrieval:
- **Query expansion** — add synonyms/related terms.
- **Decomposition** — split a compound question into sub-queries, retrieve each.
- **HyDE (Hypothetical Document Embeddings)** — generate a hypothetical *answer*, embed *that*, and retrieve — often matches real documents better than the terse question.
- **Conversational rewriting** — resolve "what about the enterprise tier?" into a standalone query using chat history.
*Pitfall:* rewriting can drift from intent; keep the original as a fallback.

**Multi-hop retrieval (Stabilizing → mainstream via agentic RAG).**
Some questions need chained lookups ("Which of our accounts renewing this quarter use the discontinued module?" = find renewals → find module usage → intersect). The system retrieves, reasons, retrieves again — an **agentic RAG** loop (Module 8.6): the model decides what to fetch next. As of 2026 this is a mainstream best-practice frame, not fringe. More powerful, more latency/cost, harder to evaluate.

**Adaptive RAG (Stabilizing).** A classifier routes each query to the *cheapest sufficient* pipeline — trivial questions answered directly, moderate ones via single-shot RAG, hard ones via multi-hop/agentic retrieval. Increasingly the default way to balance cost and quality.

**Contextual retrieval (Established; popularized by Anthropic, 2024).**
Before embedding each chunk, prepend a short, LLM-generated description of the chunk's context within its document (e.g., "This is from ACME's 2025 MSA, Section 7, on termination…"). This fixes the "severed context" problem (3.2) and materially improves retrieval accuracy (Anthropic reported ~35% fewer retrieval failures, more with hybrid + rerank). Now offered as a built-in feature in managed RAG platforms (e.g., Amazon Bedrock Knowledge Bases).

**GraphRAG (Stabilizing; cost barrier now largely solved).**
Instead of (or alongside) vector search over text, build a **knowledge graph** (Module 4) from the corpus and retrieve over *entities and relationships*. *How it answers a "global" question (the mechanic that makes it different):* Microsoft's **GraphRAG** extracts entities/relations from the whole corpus, runs **community detection** to cluster related entities into groups, and **pre-generates a summary of each community**. A global question like "what themes span all our incident reports?" is then answered by **map-reducing over those community summaries** — aggregating across the entire corpus — whereas vector RAG can only fetch the top-k *local* passages and literally never sees the whole picture. Also strong for multi-hop reasoning over structured relationships.
*Tradeoffs:* classic GraphRAG's up-front graph construction is expensive and can be noisy (entity-resolution errors — Module 4.5). But **LazyGraphRAG** (Microsoft, open-source) defers summarization to query time using cheap noun-phrase co-occurrence, cutting indexing cost to roughly that of vector RAG (~0.1% of full GraphRAG) while keeping strong global-question quality — largely removing the adoption blocker. Usually combined with vector RAG (**hybrid GraphRAG**, routed by query type) rather than replacing it. Deep integration is covered in Module 4 and its evolution in Module 8.6.

**Other patterns worth naming.** **Self-RAG / corrective RAG (CRAG)** — the model critiques retrieved context and re-retrieves or abstains if it's insufficient (reduces answering from irrelevant context). **Fusion retrieval** — multiple query variants + result fusion.

**(d) Decision criteria.** Add complexity only when basic RAG's eval (3.9) shows a specific gap: ambiguous queries → rewriting; compound questions → decomposition/multi-hop; isolated-chunk failures → contextual retrieval; global/relational questions → GraphRAG. Each addition costs latency, money, and evaluability — earn it.

**(f) Enterprise example.** A revenue-ops analyst asks, "Across all at-risk enterprise accounts, what common product gaps are driving churn?" Vector RAG returns scattered passages; **GraphRAG** over an account-product-issue graph surfaces the recurring relationships and summarizes the theme — a global question basic RAG can't answer well.

---

## 3.8 SoR integration — grounding on live SoR data & entitlement-aware retrieval

> **Cross-cutting theme (a & b, read paths).** This is where RAG meets the enterprise's authoritative data. Full treatment — write paths, the semantic layer, platform-native vs. composable, and the CPQ walkthrough — is in **Module 09**. Here we establish the *retrieval* side.

**(a) The core pattern.**
Enterprise knowledge doesn't live only in documents; it lives in **Systems of Record (SoR)** — CRM (Salesforce), ITSM/workflow (ServiceNow), ERP, data warehouses. The durable architecture is **"AI as the interaction/orchestration layer, the SoR as the system of record."** For retrieval, that means the agent grounds its answers in **live SoR data**, not a stale copy, and treats the SoR (not the model) as the source of truth.

**(b) Two grounding modes.**
- **Structured retrieval (query the SoR directly)** — for authoritative, current, transactional facts (an opportunity's amount, a quote's status, an incident's priority), the agent uses **tool calls** (2.3) / an MCP server (2.4) to *query the SoR API live* — often better than embedding this data, because it must be **exact and current**. Example: `crm.get_opportunity(id)` returns the real, up-to-the-second record.
- **Unstructured retrieval (vector/hybrid RAG)** — for knowledge articles, notes, attachments, past cases, contracts, the classic RAG pipeline (3.1–3.7) applies, indexing SoR-attached content.
- **Real systems combine both**: retrieve the structured record *and* related unstructured context, then reason.

**(b′) Entitlement- and row-level-security-aware retrieval — the non-negotiable.**
The agent must see **only what the requesting user is permitted to see.** An AI layer that bypasses SoR permissions is a data-exfiltration incident waiting to happen (a rep querying accounts they don't own; a customer seeing another customer's data). Mechanisms:
- **Propagate the user's identity** end-to-end (not a service account with god-mode). The retrieval layer acts *as the user*.
- **Enforce entitlements at the source** where possible — call the SoR API with the user's context so the SoR's own sharing rules/ACLs apply (Salesforce sharing model; ServiceNow ACLs). This is the safest: the authoritative system decides.
- For **vector stores**, tag every chunk with access-control metadata at ingest (3.2) and **pre-filter** retrieval by the user's entitlements (3.4). This must be **correct-by-construction**, never best-effort — a post-hoc filter that occasionally leaks is a breach.
- **Re-check at generation/action time** — permissions can change; high-stakes reads/writes re-validate.
- **Never let the LLM be the access-control boundary.** The model can be prompt-injected; authorization lives in code/the SoR (Modules 5.6, 6.3, 09b).

**(d) Decision criteria.** Query the SoR **live** for anything that must be exact/current/transactional; use **vector RAG** for unstructured knowledge; always enforce entitlements at the authoritative source and pre-filter vector retrieval by access tags.

**(e) Pitfalls & failure modes.**
- **Stale mirror** — copying SoR data into a vector store and answering from a day-old snapshot (wrong prices, closed deals shown as open). Prefer live queries for volatile facts; use change-data-capture to keep mirrors fresh (Module 6.2).
- **Entitlement bypass** — the RAG index ignores sharing rules → users see forbidden records. The #1 enterprise RAG security failure.
- **Embedding volatile transactional data** — amounts/statuses change constantly; embedding them guarantees staleness.
- **Confusing "retrieved" with "authoritative"** — retrieved text can be an old draft; tie answers to the SoR's current record and cite it.

**(f) Enterprise example.** A sales rep asks the assistant, "What's the status of the ACME renewal and are there open support issues?" The agent (acting as the rep) calls Salesforce for the opportunity/quote (live, entitlement-filtered by sharing rules) and ServiceNow for open incidents (filtered by ACLs), plus vector-retrieves the account's recent call notes tagged to accounts the rep can access — then answers with citations, showing nothing the rep isn't allowed to see. (The *write* path — updating that renewal — is Module 09b.)

---

## 3.9 Retrieval evaluation and failure modes

**(a) What it is / why it matters.**
Most RAG failures are **retrieval** failures, and most teams can't see them because they only look at final answers. **Retrieval eval** decomposes the pipeline so you know *where* it breaks — retrieval vs. generation — and can fix the right thing. This is the applied version of Module 2.6, specialized to RAG.

**(b) Mechanics — what to measure.**
- **Retrieval metrics** (need labeled query→relevant-chunk sets):
  - **Recall@k / Hit rate** — is the right chunk in the top k? (If not, generation is doomed.)
  - **Precision@k / MRR / nDCG** — how highly ranked and how clean are the results?
  - **Context precision/recall** (RAG frameworks) — fraction of retrieved context that's relevant, and fraction of needed info retrieved.
- **Generation-given-context metrics:**
  - **Faithfulness / groundedness** — is every claim supported by the retrieved context? (Detects hallucination-despite-retrieval.)
  - **Answer relevance** — does it address the question?
  - **Citation accuracy** — do citations point to text that actually supports the claim?
- **End-to-end** — task success, correctness vs. gold answers, human/LLM-judge scores.
- **The RAG "triad" (TruLens framing):** context relevance → groundedness → answer relevance. If all three are high, the system is working; each one localizes a different failure.

**(c) Tools.** RAGAS, TruLens, DeepEval, promptfoo, Arize Phoenix, LangSmith, vendor eval suites. Build a **golden set** of real queries with known-relevant sources and expected answers; grow it from production failures.

**(d) Decision criteria — the diagnostic flow.**
1. Low **recall@k**? → fix chunking (3.2), embeddings (3.3), add hybrid (3.5), or query rewriting (3.7).
2. Good recall but low **precision**/high tokens? → add **reranking** (3.6).
3. Good context but **unfaithful** answers? → fix the prompt ("answer only from context," cite), lower temperature, or the model isn't following context (consider stronger model / Self-RAG).
4. Everything good offline but **users unhappy**? → your golden set isn't representative; expand it from real traffic.

**(e) Failure modes — the field guide.**
- **Missing content** — the answer isn't in the corpus at all → system must say "I don't know," not fabricate.
- **Retrieval miss** — it's in the corpus but not retrieved (bad chunking/embeddings/no hybrid).
- **Lost in the middle** (1.5) — retrieved but buried/ignored → rerank, trim, reorder best-first.
- **Ignored context** — model answers from parametric memory despite good context → prompt/model issue.
- **Unfaithful synthesis** — model blends context with invented details → groundedness eval + citations.
- **Wrong chunk, right topic** — retrieved a related-but-incorrect passage (e.g., wrong SKU's price) → hybrid + reranking + metadata filters.
- **Entitlement leak** (3.8) — retrieved data the user shouldn't see → a *security* failure, caught by access-control tests, not quality metrics.
- **Stale data** — mirror out of sync with SoR → CDC/live queries.
- **Conflicting sources** — corpus contains contradictory versions → dedupe, prefer authoritative source, surface conflict.

**(f) Enterprise example.** A CPQ RAG assistant gives a wrong discount answer. Eval reveals recall@10 is fine (the right policy chunk *is* retrieved) but groundedness is low — the model is merging two discount tiers. Fix: reranking to surface the single relevant tier first + a prompt that forces per-claim citation. Separately, an access-control test catches that the index would have returned another region's pricing to an unauthorized rep — fixed by pre-filtering on entitlement tags (3.8).

---

### Module 3 takeaways
- **RAG** = retrieve relevant text at query time and answer from it — the primary fix for private/current/citable knowledge and hallucination.
- **Chunking** caps everything downstream; be structure- and metadata-aware.
- **Embeddings + vector DB** are the engine; **pgvector** is a pragmatic default (co-located, transactional, RLS-friendly), with Pinecone/Weaviate/Qdrant/etc. for scale or residency.
- **Hybrid search** (semantic + keyword) is the enterprise default because your data is full of exact identifiers; **reranking** is high-ROI precision.
- **Advanced RAG** (query rewriting, multi-hop, contextual retrieval, GraphRAG) earns its complexity only against a measured gap.
- **SoR integration:** ground on **live** SoR data for volatile facts, RAG for unstructured knowledge, and make retrieval **entitlement-aware at the authoritative source** — never let the LLM be the access boundary.
- **Evaluate retrieval separately** from generation; most failures are retrieval failures, and entitlement leaks are security failures your quality metrics won't catch.

*Proceed to `04-knowledge-representation.md`.*
