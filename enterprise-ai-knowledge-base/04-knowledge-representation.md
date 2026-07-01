# Module 4 — Knowledge Representation

> **Why this module exists:** Vector RAG (Module 3) is great at "find me passages about X." It's weak at "how are these entities *related*?" and "answer a question that requires traversing connections." **Structured knowledge** — knowledge graphs, ontologies, semantic layers — encodes *entities and their relationships explicitly*, giving AI systems something precise to reason over. This module also carries the **semantic-layer** thread of the SoR theme (item **c**): how messy enterprise schemas become something an agent can actually reason about.

**Module map**
4.1 Knowledge graphs (nodes, edges, triples)
4.2 Ontologies vs. taxonomies
4.3 Schema design
4.4 Entity resolution
4.5 Graph databases & query languages (Neo4j / Cypher, etc.)
4.6 **The semantic layer** over enterprise data (SoR theme c)
4.7 How structured knowledge integrates with LLMs

---

## 4.1 Knowledge graphs (nodes, edges, triples)

**(a) What it is / why it matters.**
A **knowledge graph (KG)** represents information as **entities (nodes)** connected by **relationships (edges)**, often with **properties** on both. It captures *facts as connections*: `(ACME) —[HAS_OPPORTUNITY]→ (Renewal-2026)`, `(Renewal-2026) —[INCLUDES]→ (Firewall-Bundle)`. Where a document says things in prose and a table says things in rows, a graph says things as an explicit web of relationships you can **traverse and query precisely**. It's how you answer "connect-the-dots" questions and how you give an LLM a source of *structured truth*.

**Analogy.** A vector store is like a pile of well-indexed articles; a knowledge graph is like the org chart + the wiring diagram — it doesn't just have the facts, it has *how they connect*, so you can trace paths ("who reports to whom," "which product depends on which component").

**(b) Mechanics.**
- **Node** — an entity (a customer, product, contract, person, incident).
- **Edge** — a typed, directed relationship (`OWNS`, `DEPENDS_ON`, `RENEWS`).
- **Triple** — the atomic unit in the **RDF** tradition: **(subject, predicate, object)** — `(ACME, hasContract, C-1023)`. A graph is a set of triples.
- **Properties** — attributes on nodes/edges (a contract's `value`, an edge's `since` date). The **Labeled Property Graph (LPG)** model (Neo4j) is built around rich properties; **RDF** is built around triples + formal semantics.
- **Provenance** — good KGs record *where each fact came from* (source, timestamp) — essential for trust and auditability.

**(c) Two traditions.**
- **RDF / W3C stack** — triples, **SPARQL** query language, **OWL/RDFS** for formal ontologies; strong for standards-based, interoperable, reasoning-heavy domains (life sciences, government).
- **Labeled Property Graph (LPG)** — nodes/edges with properties; **Cypher/Gremlin** queries (Neo4j, etc.); more developer-friendly, dominant in enterprise app contexts.

**(d) Decision criteria — when a KG earns its cost.** Use a KG when relationships are first-class (recommendations, dependencies, fraud rings, org/asset hierarchies, supply chains), when you need **multi-hop** reasoning, when you must integrate heterogeneous sources under one model, or when **explainability** matters (a graph path is an auditable explanation). *Avoid* the overhead when your questions are "find similar text" — that's vector RAG.

**(e) Pitfalls.** Building a graph nobody queries (modeling for its own sake); underestimating the **construction and maintenance** cost; noisy graphs from bad extraction/entity resolution (4.4); treating a KG as a substitute for, rather than a complement to, vector search.

**(f) Enterprise example.** A KG links accounts → opportunities → quotes → products → components → known issues. "Which renewing accounts depend on a component with an open critical defect?" is one graph traversal — a question vector RAG can only approximate by luck.

---

## 4.2 Ontologies vs. taxonomies

**(a) What it is / why it matters.**
Both organize concepts, but at different power levels. A **taxonomy** is a **hierarchy** (a tree of categories: Product → Networking → Firewall → FW-9000). An **ontology** is a **richer model of concepts *and* the relationships and rules among them** (a firewall *is-a* security product, *has* throughput, *is compatible with* certain licenses, *cannot* be sold without a support plan). Getting this vocabulary right matters because the ontology is the **shared meaning** an AI agent reasons over — it's the difference between "categories" and "a model of the domain."

**(b) Mechanics.**
- **Taxonomy** — parent/child classification; "is-a" and "part-of" hierarchies. Simple, powerful for navigation/faceting.
- **Ontology** — **classes**, **properties/relationships** (with domains and ranges), **constraints/axioms**, and sometimes **inference rules** (if X is-a Y and Y has property P, X has P). Defines *what can exist and how it can relate*. Expressed in OWL/RDFS (RDF world) or as a schema/metamodel (LPG world).
- **Controlled vocabulary / thesaurus** — sits between: agreed terms + synonyms/relations (SKOS).
- **Schema vs. instances** — the ontology is the **template** (Customer, Order, "places"); the graph holds the **instances** (ACME places Order-42).

**(c) Tools.** Protégé (OWL editing), SKOS for vocabularies; in LPG land the ontology is often a documented schema + constraints; enterprise catalogs/data-modeling tools; increasingly, LLMs assist in *drafting* ontologies from documents.

**(d) Decision criteria.** A **taxonomy** suffices for classification/navigation. Invest in an **ontology** when you need shared semantics across systems, machine reasoning/validation, or an agent that must understand *rules* ("a quote can't include incompatible products"). Start minimal — a lightweight ontology you maintain beats an elaborate one you don't.

**(e) Pitfalls.** **Over-engineering** (academic ontologies that never ship); **analysis paralysis**; ontologies that drift from reality because no one owns them; conflating a taxonomy with an ontology and then being surprised it can't express rules.

**(f) Enterprise example.** A CPQ domain ontology defines Product, Bundle, Feature, Constraint, PriceRule, and relationships like `REQUIRES`, `INCOMPATIBLE_WITH`, `UPSELLS_TO`. An agent uses it to reason that a proposed configuration violates a `REQUIRES` constraint *before* it ever generates a quote (Module 09e).

---

## 4.3 Schema design

**(a) What it is / why it matters.**
**Schema design** is deciding *what* your nodes, edges, and properties are — the model of your domain. Good schema makes queries simple and answers correct; bad schema makes everything downstream painful. For AI, the schema is also what the agent "reads" to know how to query — so clarity is a functional requirement, not just hygiene.

**(b) Mechanics & principles.**
- **Model relationships as edges, not foreign keys buried in properties** — the point of a graph is traversable connections.
- **Nouns = nodes, verbs = edges** as a first cut; promote a relationship to a node when it has its own attributes/relationships (a "Purchase" with date, amount, and links to Product and Rep is often better as a node — "reification").
- **Naming conventions** — consistent, human-readable labels; edges named as verbs/relationships (`WORKS_FOR`, not `rel1`). LLMs generate better queries against clear names.
- **Granularity** — too coarse loses queryability; too fine explodes complexity.
- **Provenance & temporality** — timestamp facts; model change over time when it matters (contracts, prices, org changes).
- **Align to source SoR** — where the graph mirrors CRM/ERP entities, mirror their identity and keys so you can join back (Module 09).

**(d) Decision criteria.** Design for the **questions you must answer** (query-driven modeling), not for theoretical completeness. Iterate: start with the top 10 questions, model just enough, expand as needed.

**(e) Pitfalls.** Modeling everything as properties (kills traversal); inconsistent naming (breaks both humans and LLM query-generation); no identity strategy (leads to duplicate entities — 4.4); ignoring time (can't answer "what was true then?"); a schema that no query ever uses.

**(f) Enterprise example.** A team initially stores a rep's ID as a property on Account. Later they need "all deals two reps collaborated on" — impossible cleanly. Refactoring to `(Rep)-[:WORKS_ON]->(Opportunity)<-[:WORKS_ON]-(Rep)` makes the traversal trivial.

---

## 4.4 Entity resolution

**(a) What it is / why it matters.**
**Entity resolution (ER)** — a.k.a. deduplication, record linkage, identity resolution — is determining when different records refer to the **same real-world entity** ("ACME Corp," "Acme Corporation," "ACME Inc." → one company). It's the make-or-break step for any KG or unified data layer: without it, the graph is full of duplicate nodes and the "connections" are fragmented and wrong. It's also one of the hardest, messiest problems in enterprise data.

**(b) Mechanics.**
- **Blocking** — cheaply group plausibly-matching records to avoid comparing everything to everything (O(n²) is infeasible at scale).
- **Matching** — compare candidate pairs via deterministic rules (exact IDs, normalized names), probabilistic scoring (Fellegi–Sunter), fuzzy string similarity, or ML classifiers; increasingly **embeddings/LLMs** for semantic matching of tricky cases.
- **Clustering/merging** — group matched records into a single canonical entity with a **golden record** and links to sources (survivorship rules decide which value wins).
- **Identity management** — maintain stable canonical IDs and mappings so downstream joins are consistent.

**(c) Tools.** Master Data Management (MDM) suites (Informatica, Reltio, Tamr, Quantexa); open frameworks (Zingg — incl. on Databricks/Spark, Dedupe, Splink); cloud (AWS Entity Resolution); graph-native ER; **LLM/transformer-based ER** for hard/edge cases (now *maturing* — benchmarked and appearing in platforms; still needs guardrails against wrong merges).

**(d) Decision criteria.** Invest heavily in ER when data comes from **many sources** (multiple CRMs post-acquisition, CRM + ERP + support), when duplicates cause real harm (double-counting revenue, split customer views), or when the KG's value depends on correct linkage. Match strictness to cost of error: **false merges** (two real customers merged) are usually worse than **false splits** (one customer left as two) — tune accordingly, and keep humans in the loop for uncertain merges.

**(e) Pitfalls & failure modes.**
- **Over-merging** — collapsing two distinct entities (two "John Smith"s, a parent and subsidiary) — corrupts data and can leak entitlements (one customer sees another's data). Dangerous.
- **Under-merging** — fragmented view, double counting.
- **No canonical ID strategy** — resolution results that can't be reused.
- **Ignoring provenance** — can't audit or unwind a bad merge.
- **Static rules on drifting data** — ER needs ongoing maintenance.

**(f) Enterprise example.** After acquiring a competitor, a company has ACME in three CRMs with different spellings and IDs. ER produces one canonical ACME node linked to all three source records; now "total ACME pipeline across both businesses" is answerable — and crucially, entitlement rules apply to the *unified* customer correctly, without accidentally merging ACME with a similarly-named unrelated firm.

---

## 4.5 Graph databases & query languages

**(a) What it is / why it matters.**
A **graph database** stores and queries nodes/edges natively, making multi-hop traversals fast and expressive — the operational home of a knowledge graph. Relational databases *can* model relationships (via joins), but deep/variable-length traversals ("all components transitively required by this product") become painful join-heavy queries; graph DBs make them natural.

**(b) Mechanics & the landscape.**
- **Labeled Property Graph (LPG):**
  - **Neo4j** — the most widely-used enterprise graph database; **Cypher** query language; mature tooling. Now ships a **native VECTOR data type + filterable vector indexes**, **in-Cypher GraphRAG/AI procedures**, and an official **neo4j-graphrag** Python library — GA product features, not experiments.
  - Others: **Amazon Neptune** (LPG + RDF) and **Neptune Analytics** (in-memory, native vector search in openCypher; powers Amazon **Bedrock Knowledge Bases GraphRAG**, GA 2025), **TigerGraph**, **Memgraph**, **ArangoDB** (multi-model), **JanusGraph**. The space is **consolidating** — e.g., embedded graph DB **Kùzu** was acquired by Apple and its open-source repo archived (Oct 2025), with maintenance passing to community forks; weigh vendor/project durability.
- **RDF/triple stores:** GraphDB, Stardog, Blazegraph, Neptune — **SPARQL** queries, OWL reasoning.
- **Query languages:**
  - **Cypher** — pattern-matching syntax that *draws the graph in ASCII*: `MATCH (a:Account)-[:HAS_OPPORTUNITY]->(o:Opportunity) WHERE o.stage='Renewal' RETURN a,o`. Intuitive; now standardized as **GQL (ISO/IEC 39075, published April 2024)** — the first new ISO database query language since SQL (1987); Cypher conforms to most mandatory GQL features.
  - **SPARQL** — triple-pattern queries over RDF; powerful, more verbose.
  - **Gremlin** — imperative traversal (Apache TinkerPop), cross-vendor.

**(c) How they differ / decision criteria.**
- **LPG (Neo4j/Cypher)** — best for most enterprise app graphs: developer-friendly, great tooling, good LLM support for text-to-Cypher. Choose when relationships + properties dominate and you want productivity.
- **RDF/SPARQL** — choose for standards-based interoperability, formal ontologies/reasoning, linked-data/regulatory contexts.
- **Multi-model (Neptune/ArangoDB)** — when you want graph alongside document/relational in one store.
- Also weigh: scale, managed vs. self-hosted, vector-index support (for graph+vector hybrid), and existing skills.

**(e) Pitfalls & failure modes.**
- **Choosing a graph DB when relational + a few joins would do** — added ops complexity for no benefit.
- **Unbounded traversals** — `MATCH` with no depth limit can explode; bound path lengths.
- **Text-to-Cypher/SPARQL errors** — LLMs generate invalid or unsafe queries; validate, sandbox, and constrain (read-only, row limits) — see 4.7.
- **Sync drift** — the graph mirrors SoR data that changed; needs a refresh pipeline (Module 6.2).

**(f) Enterprise example.** A support-ops team runs Neo4j linking incidents → affected products → customers → contracts. Cypher answers "which enterprise-contract customers are affected by the current P1 defect?" in one traversal — feeding a proactive-outreach agent.

---

## 4.6 The semantic layer over enterprise data — SoR theme (c)

> **Cross-cutting theme (c).** This is the concept that makes structured enterprise data *usable by an agent* and recurs in Module 09.

**(a) What it is / why it matters.**
Enterprise data is **messy**: cryptic table/column names (`acct_x2`, `opp_amt_c`), duplicated across systems, encoded in ways only tribal knowledge decodes, spread over CRM/ERP/warehouse. A **semantic layer** is a **business-meaning abstraction on top of raw schemas** — it maps the mess to clean, governed concepts ("Customer," "Annual Recurring Revenue," "Open Pipeline") with defined relationships, metrics, and access rules. It's the translation layer between *how data is stored* and *how the business (and an agent) thinks*.

**Analogy.** The raw database is a warehouse of unlabeled boxes with part-number codes. The semantic layer is the *catalog* that says "box 4471-B = enterprise firewall, ships with these licenses, owned by the networking BU." An agent reasons over the catalog, not the box codes.

**(b) Mechanics.**
- **Concept/entity definitions** — canonical business objects mapped to underlying tables/fields (often the KG/ontology, 4.1–4.2).
- **Metric definitions** — governed, single-definition calculations ("ARR," "win rate") so everyone (and the agent) computes them the same way.
- **Relationships & joins** — pre-defined so consumers don't re-derive them.
- **Access/governance** — entitlements defined at the semantic layer, inherited by consumers (ties to 3.8, 6.3).
- **Two flavors converging:** (1) **BI/metrics semantic layers** (dbt Semantic Layer, Cube, LookML, AtScale) — governed metrics for analytics; (2) **knowledge-graph/ontology semantic layers** — entities + relationships for reasoning. For agents, the semantic layer is what turns "text-to-SQL against a cryptic schema" (fragile) into "query well-defined business concepts" (robust) — a shift now **benchmark-backed** (2026 dbt benchmarks show semantic-layer querying materially beating raw text-to-SQL on modeled projects, because the LLM picks a governed metric by name and the engine generates the query deterministically; treat exact percentages as directional).
- **Standardization (new):** the **Open Semantic Interchange (OSI)** — a vendor-neutral open spec (Snowflake, Salesforce, dbt Labs, Cube, RelationalAI, ThoughtSpot, Atlan; announced Sept 2025) — aims to make semantic definitions portable across BI tools *and* agents, directly targeting the "semantic layer for AI/agents" need. dbt's MetricFlow is now Apache-2.0 and aligned to it.

**(c) Tools.** dbt Semantic Layer, Cube, AtScale, LookML (Looker); **Palantir Foundry/AIP**, whose Ontology has become a leading real-world instance of the ontology-as-agent-reasoning-backbone pattern (strong commercial traction); graph/ontology platforms; and **platform-native semantic layers** — notably **Salesforce Data Cloud / Data 360** (unifies/maps customer data into a governed model — a data-unification backbone; you may still layer governed metrics on top) and modeling within **ServiceNow's** platform, e.g. the CMDB / Common Service Data Model (CSDM) as its canonical model (Module 09d).

**(d) Decision criteria.** Build/adopt a semantic layer when multiple consumers (BI, apps, agents) need **consistent definitions**, when schemas are too messy for direct LLM querying, or when governance/entitlements must be centralized. It's often the highest-leverage investment for making agents reliable over enterprise data — and it's reusable beyond AI.

**(e) Pitfalls.** Letting an agent do **raw text-to-SQL over a cryptic schema** (brittle, wrong-metric risk, security holes) instead of querying a governed layer; a semantic layer that drifts from the sources; defining metrics inconsistently across BI and AI (two "revenue" numbers); no ownership.

**(f) Enterprise example.** Without a semantic layer, an agent asked for "ARR at risk this quarter" writes SQL guessing at `opp_amt_c` and renewal flags — sometimes wrong. With a semantic layer, it queries the governed `ARR` metric filtered by the defined `AtRisk` and `CurrentQuarter` concepts — consistent with the CFO's dashboard, and access-controlled. This is the backbone of trustworthy SoR-grounded agents (Module 09).

---

## 4.7 How structured knowledge integrates with LLMs

**(a) What it is / why it matters.**
The payoff: **combining LLMs (fluent reasoning) with structured knowledge (precise, connected truth).** LLMs supply language understanding and reasoning; graphs/semantic layers supply exact, relational, up-to-date, explainable facts. Together they cover each other's weaknesses — this is the frontier of trustworthy enterprise AI (and the heart of GraphRAG, Module 8.6).

**(b) Mechanics — the main integration patterns.**
1. **Text-to-query (LLM → graph/DB).** The LLM translates a natural-language question into **Cypher/SPARQL/SQL** (against the semantic layer), executes it, and explains the result. *Guardrails required:* validate the generated query, run **read-only** with row/timeout limits, constrain to the known schema, and never expose raw destructive access. Provide the schema/ontology in the prompt so the model queries real fields (clear naming from 4.3 pays off here).
2. **Graph-as-retriever (GraphRAG, Module 3.7 / 8.6).** Retrieve relevant subgraphs/paths (not just text passages) as context; enables multi-hop and global questions. Often **hybrid**: vector search finds entry-point entities, graph traversal expands relationships, both feed the prompt.
3. **KG-augmented grounding & verification.** Use the graph to **fact-check** or **constrain** LLM output (does the proposed configuration satisfy the ontology's `REQUIRES`/`INCOMPATIBLE_WITH` rules?). The graph is an authoritative check on the model's fluency.
4. **LLM-assisted graph construction.** Use LLMs to *extract* entities/relations from documents to *build/extend* the graph — accelerates KG creation but needs entity-resolution (4.4) and human review to control noise. *Now production-common* (e.g., Microsoft GraphRAG 1.0 and **LazyGraphRAG**, which defers LLM cost to query time — Module 3.7), no longer merely emerging.
5. **Ontology as agent reasoning scaffold.** The agent uses the ontology to understand valid actions/relationships before acting (Module 5 planning; Module 09e CPQ constraints).

**(d) Decision criteria.** Reach for structured integration when questions are **relational/multi-hop**, when **precision and explainability** are required (a graph path is an audit trail), or when the model must respect **domain rules/constraints**. Combine with vector RAG rather than replacing it — text and structure answer different question types.

**(e) Pitfalls & failure modes.**
- **Text-to-query injection/errors** — untrusted input coaxes a harmful query, or the LLM emits invalid/expensive queries. Sandbox, validate, least-privilege, read-only, limits.
- **Schema hallucination** — the model queries fields that don't exist; supply and constrain to the real schema/semantic layer.
- **Noisy auto-built graphs** — extraction + weak ER produce wrong "facts" that now look authoritative. Review and track provenance.
- **Complexity/cost** — graph infrastructure + maintenance is real; don't adopt without relational/multi-hop need.
- **Two sources of truth** — graph and SoR disagree; anchor the graph to the SoR and keep it synced (Module 6.2).

**(f) Enterprise example.** A deal-desk agent, asked "can we bundle FW-9000 with the basic support tier for ACME?", (1) queries the semantic layer for ACME's entitlements and current products (text-to-query, entitlement-filtered), (2) checks the product ontology's `REQUIRES` rule — FW-9000 requires premium support — and (3) tells the rep the bundle is invalid and proposes the compliant alternative, citing the rule. Fluent reasoning + structured truth = a correct, explainable, governed answer — exactly the pattern Module 09 operationalizes for CPQ.

---

### Module 4 takeaways
- **Knowledge graphs** encode entities + relationships explicitly, enabling precise, multi-hop, explainable answers vector RAG can't give.
- **Taxonomy** = hierarchy; **ontology** = a model of concepts, relationships, and rules the agent can reason over. Start minimal.
- **Schema design** is query-driven; model relationships as edges; name things clearly (LLMs read your schema).
- **Entity resolution** (dedup/linkage) is make-or-break and dangerous when wrong — false merges can leak entitlements.
- **Graph DBs** (Neo4j/Cypher, RDF/SPARQL, GQL emerging) are the operational home; guard LLM-generated queries.
- **The semantic layer** turns messy schemas into governed business concepts an agent can reason over — often the highest-leverage investment for reliable SoR-grounded AI (theme c).
- **LLM + structured knowledge** = fluent reasoning + precise, connected, explainable truth: text-to-query, GraphRAG, verification/constraint-checking, and LLM-assisted construction — combined with, not instead of, vector RAG.

*Proceed to `05-agents-orchestration.md` (Pass 2).*
