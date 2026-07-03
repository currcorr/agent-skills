# Module 09 — Integration with Systems of Record (Cross-Cutting)

> **Why this module exists:** This is the connective tissue between "AI research" and "AI that runs your business." It consolidates the Systems-of-Record (SoR) integration theme woven through Modules 3–7 into one place — the durable pattern, the read/write distinction, the semantic layer, the platform-native-vs-composable tradeoff, and a concrete CPQ walkthrough. Running examples: **CRM and CPQ**, on two reference platforms, **Salesforce** and **ServiceNow**.
>
> **Vendor-accuracy caveat (read first):** Vendor capabilities in this space move *fast* and marketing often blurs shipped vs. roadmap. This module was **drafted at an early-2026 horizon and refreshed in a mid-2026 research pass**. Every vendor-specific claim below — GA status, feature names, CPQ specifics — should be **verified against the vendor's current documentation, release notes, and trust portal** before you record it. Where public detail is genuinely thin, it is **flagged explicitly**. Treat "roadmap"/"announced" items as pointers to check, not facts.

**Module map**
09.a The core pattern — AI as interaction layer, SoR as system of record
09.b Read vs. write paths (and why writes demand more)
09.c The semantic layer
09.d Platform-native vs. composable — Salesforce vs. ServiceNow
09.e A concrete CPQ walkthrough

---

## 09.a The core pattern — "AI as orchestration/interaction layer, SoR as system of record"

**(a) What it is / why it matters.**
A **System of Record (SoR)** is the authoritative source of truth for a class of business data: **CRM** (Salesforce) for accounts/contacts/opportunities/quotes; **ITSM/workflow** (ServiceNow) for incidents/changes/cases/orders; ERP for finance/inventory. The durable enterprise-AI pattern is:

> **The AI (agent/copilot) is the orchestration and interaction layer; the SoR remains the system of record.**

The agent becomes the *primary interface* — users increasingly talk to the agent instead of clicking through screens — but the SoR stays **authoritative**: it holds the canonical data, enforces the business rules, owns entitlements, and governs every write. The AI *reads from* and *proposes writes to* the SoR; it does not replace it.

**Analogy.** The SoR is the official ledger and the bank's rulebook; the AI is an extremely capable teller/assistant standing at the counter. The teller can look things up, fill out forms, explain policy, and recommend actions — but the ledger is the truth, and the vault rules govern what actually gets recorded. You'd never let the teller keep their own private, unaudited copy of the ledger.

**(b) Why the SoR stays authoritative even as AI becomes the primary interface.**
1. **Single source of truth.** Business data must be consistent across every consumer (AI, dashboards, humans, downstream systems). An AI-side copy inevitably drifts (Module 3.8). The SoR is where truth is reconciled.
2. **Governance & entitlements.** The SoR already encodes who-can-see/do-what (Salesforce sharing model; ServiceNow ACLs), validation rules, and workflows. Re-implementing these in an AI layer is both wasteful and dangerous — the AI should **inherit and defer to** them (Modules 3.8, 6.3).
3. **Transactional integrity.** SoRs provide transactional *primitives*, referential integrity, and workflow state machines that an LLM cannot. (Note: this is *primitives*, not free atomicity — on Salesforce/ServiceNow, making a multi-object write like "quote + line items" all-or-nothing must be **engineered** with savepoints / composite APIs / `allOrNone` flags; see 09.b.)
4. **Auditability & compliance.** The SoR is where regulated, audited records live (Module 6.6). Authoritative writes must land there, logged.
5. **Durability & ecosystem.** The SoR integrates with the rest of the business; the AI layer is comparatively ephemeral and swappable.
6. **The model is unreliable about facts** (Module 1.9). Grounding in the SoR is what makes AI trustworthy.

**(d) Decision criteria.** Route **authority** to the SoR always. Let the AI own **interaction, reasoning, orchestration, and drafting**. Never let the AI become a shadow system of record for business-critical data. Anchor agent memory of business facts to the SoR (Module 5.5).

**(e) Pitfalls.** Building an AI-side data store that becomes an unreconciled second source of truth; bypassing SoR entitlements/validation "for speed"; treating retrieved/remembered data as authoritative rather than re-checking the SoR for volatile facts.

**(f) Enterprise example.** A rep asks the agent to "bump the ACME renewal to $220k and add premium support." The agent drafts the change and explains the pricing impact — but the *authoritative* update, the validation (is that discount allowed?), the entitlement check (can this rep do this?), and the audit record all happen **in the CRM SoR**, on approval (Module 09b).

---

## 09.b Read vs. write paths (and why writes demand more) — theme (b)

**(a) What it is / why it matters.**
The single most important architectural distinction in SoR integration is **read vs. write**. Reads inform; writes *change reality*. They deserve very different governance. Conflating them is a top cause of both under-powered (read-only, low-value) and dangerously over-powered (unguarded writes) deployments.

**(b) The read path — grounding & retrieval on live SoR data.**
- **Live structured reads** — query the SoR API for current, exact facts (opportunity amount, quote status, contract terms). Prefer **live queries** over embedded copies for volatile data (Module 3.8). Use tool calls / MCP (Modules 2.3–2.4).
- **Unstructured reads** — vector/hybrid RAG over SoR-attached knowledge (KB articles, notes, attachments, past cases) — Module 3.
- **Entitlement- and row-level-security-aware retrieval (non-negotiable).** The agent must see **only what the requesting user is permitted to see.** Enforce at the authoritative source: query **as the user**, so Salesforce sharing rules / ServiceNow ACLs apply; pre-filter vector retrieval by access tags; propagate identity end-to-end; re-check at action time. **The LLM is never the access boundary** (Modules 3.8, 5.6, 6.3). Reads are lower-risk than writes but an entitlement leak on read is still a breach.
- **The hard case — dynamic sharing vs. static tags (name it, don't wave at it).** For *structured* reads, "query as the user" is clean. For *unstructured* vector RAG it's genuinely hard: a chunk was embedded and tagged at ingest time, but Salesforce sharing is **computed** (role hierarchy, criteria-based rules, manual shares) and can **change after ingest** — so a static ingest-time access tag can be *wrong* (stale → leak) and cannot represent a criteria-based rule at all. Three viable patterns, in rough order of safety: **(1) post-retrieval re-check** — after vector search, verify each candidate record's accessibility *as the user* against the live SoR before returning it (safest, adds a round-trip); **(2) tag + periodic re-sync** — cache access tags and re-index on sharing changes / CDC (faster, but a staleness window = leak risk); **(3) scope RAG to coarse-grained/public knowledge** and route all record-level facts through live *structured* reads (simplest and safe, but less powerful). Choosing among these is a real architectural fork the SoR audience must make explicitly.

**(b′) The write path — and why it demands far stronger governance.**
A write (create/update an opportunity, apply a discount, generate a quote, modify a contract) **changes the system of record** and can have financial, legal, and customer consequences. Writes require, at minimum:
- **Stronger entitlement checks** — enforced in code/SoR, not the prompt; scoped to what *this user* may write (Module 8.9 agent identity/scoping).
- **Transactional integrity** — writes must be atomic and respect the SoR's validation rules and workflow states (all-or-nothing; no half-applied quotes). *How, concretely:* a business write like a quote is inherently **multi-object** (quote header + N line items + discounts + document), and a single REST call is **not** automatically atomic. You must use a **composite/transactional API** (e.g., Salesforce **Composite** / `sObject Tree` / a server-side Apex transaction with `Database.Savepoint`; ServiceNow's transaction + rollback semantics) *or* implement a **saga** — a sequence of steps each paired with an explicit **compensating action** — so a failure at step 3 unwinds steps 1–2. Don't simulate transactions in the agent loop.
- **Idempotency** — retries (from timeouts or agent re-planning) must not create duplicates. *How:* derive an **idempotency key deterministically from the business intent** (e.g., `opportunityId + hash(config)`), generate it **once before the first attempt**, and reuse the *same* key across every retry — never let the LLM regenerate arguments (and thus a new key) on retry. The SoR (or a dedup layer) rejects a second write with a key it has seen.
- **Rollback / reversibility — a taxonomy** (pick the right kind per action): **(1) reversible** — undo a draft (delete the draft quote); **(2) compensating** — the action can't be deleted but can be neutralized (void a submitted quote and reissue a corrected version; the saga step above); **(3) irreversible** — once a quote is *sent to the customer* it may be legally binding, so there is no rollback — the remedy is a **new versioned quote**, not an undo. Design high-stakes writes assuming category 2 or 3, and gate them accordingly.
- **Human-in-the-loop for high-stakes writes** — pricing, quotes, discounts, contracts, anything customer-facing or financially material: the agent **proposes**, a human **approves**, *then* it commits (Module 5.7). The write commits only after approval.
- **Delegated identity for the write (OBO)** — the agent should act with a token that is the **intersection of (its own scoped permissions ∩ the user's rights)** — an OAuth on-behalf-of / token-exchange pattern (RFC 8693), so it can never exceed the acting user. For **long-running** tasks, re-mint/refresh short-lived credentials rather than holding a broad token; for **unattended** low-value writes with no user in the loop, the agent uses its *own* scoped identity (capped below any single rep) plus a designated accountable principal — not "acting as a rep" who isn't present (Module 8.9).
- **Audit logging** — immutable record of the write, the data/authority used, the approver, and the rationale (Modules 5.8, 6.6).
- **Blast-radius limits** — value caps, rate limits, spend caps, kill switches (Modules 5.6, 8.9).

**(d) Decision criteria.** Separate read tools from write tools explicitly. Gate writes on **stakes × reversibility × confidence** (Module 5.7). Low-stakes reversible writes (log a call note) can be more autonomous; high-stakes writes (pricing, contracts) are approval-gated by default. Everything transactional goes through the SoR's own APIs to inherit integrity and validation.

**(e) Pitfalls & failure modes.**
- **Unguarded writes** — an injected instruction (Module 2.1) triggers an unauthorized/destructive write. Enforce authz + confirmation in code.
- **Duplicate writes** — no idempotency; a retried agent step creates two quotes.
- **Partial writes** — non-atomic multi-step writes leave the SoR inconsistent.
- **Silent high-stakes autonomy** — an agent applying discounts or changing contract terms without approval or audit. A governance and possibly compliance failure.
- **Bypassing validation** — writing via a back door that skips the SoR's business rules.

**(f) Enterprise example.** The agent freely **reads** ACME's opportunities and quotes (entitlement-filtered, live). To **write** a new quote with a 15% discount, it: checks the rep's discount authority (code), assembles an atomic quote via the SoR's transactional API with an idempotency key, presents it for **human approval** because the discount exceeds the auto-threshold, and — only on approval — commits it, logging the approver, the rule applied, and the rationale. A retry after a timeout produces no duplicate. (Full flow in 09.e.)

---

## 09.c The semantic layer — theme (c)

**(a) What it is / why it matters.**
Enterprise SoR schemas are **messy** — cryptic field names (`opp_amt_c`), custom objects, duplicated data across systems, tribal-knowledge encodings. An agent can't reliably reason over raw schemas (and letting it do raw text-to-SQL/SOQL is brittle and unsafe — Module 4.6/4.7). The **semantic layer** maps that mess into clean, governed **business concepts, metrics, relationships, and entitlements** the agent *can* reason over. It's the translation layer between "how data is stored" and "how the business (and the agent) thinks." (Full treatment: Module 4.6.)

**(b) Mechanics in the SoR context.**
- Canonical entities (Customer, Opportunity, Quote, Product) mapped to underlying SoR objects/fields, resolving duplicates across systems (entity resolution, Module 4.4).
- Governed metric definitions (ARR, win rate, open pipeline) so the agent computes them the way the business does.
- Pre-defined relationships/joins so the agent traverses rather than guesses.
- **Entitlements defined once** and inherited by the agent (ties to 09.b, Module 6.3).
- Often realized as a knowledge graph/ontology (Module 4) and/or a metrics layer, and increasingly by **platform-native data backbones**.

**(c) Platform realizations.**
- **Salesforce Data Cloud** — Salesforce's data backbone: unifies/harmonizes customer data (across Salesforce and external sources, with zero-copy/federation options) into a governed model that **grounds Agentforce**. Functions as the semantic/grounding layer for the CRM SoR. *(Verify current capabilities/naming.)*
- **ServiceNow** — modeling on the Now Platform (CMDB, Common Service Data Model, workflow data) plus its data-integration/"data fabric"-style capabilities provide the structured backbone its AI reasons over. *(Public detail on a formal "semantic layer for AI" is thinner here — flag and verify.)*
- **Independent/composable** — dbt Semantic Layer, Cube, a knowledge graph (Neo4j), or Palantir-style ontology sitting **across** multiple SoRs — the right choice for a multi-SoR estate (09.d).

**(d) Decision criteria.** Invest in a semantic layer whenever agents must reason over enterprise data reliably — it's often the highest-leverage step for trustworthy SoR-grounded AI. Use the **platform-native** layer for single-platform work; build a **cross-SoR** semantic layer/graph when the estate is fragmented.

**(e) Pitfalls.** Letting the agent do raw text-to-query over cryptic schemas (brittle, wrong-metric, insecure); a semantic layer that drifts from the SoR; inconsistent metric definitions between BI and AI; no ownership. (Module 4.6.)

**(f) Enterprise example.** Asked "what's ACME's open pipeline and ARR at risk this quarter?", the agent queries **governed concepts** in the semantic layer (mapped to Data Cloud's harmonized model), returning numbers consistent with the CFO's dashboard and filtered to what the rep may see — instead of guessing at `opp_amt_c` with hand-written SOQL.

---

## 09.d Platform-native vs. composable — Salesforce vs. ServiceNow — theme (d)

**(a) What it is / why it matters.**
A defining enterprise decision: use the **AI embedded in the SoR platform you already own** (deep integration, inherited governance, fast — but a walled garden) versus an **external, composable orchestration layer** that calls into multiple SoRs (vendor-neutral, flexible — but you build more and inherit less). The right answer depends on whether your process lives inside **one** platform or spans a **fragmented, multi-SoR** estate.

**(b) The two reference models.**

### Salesforce — the "walled-garden-with-deep-integration" model (CRM-centric)
- **SoR:** the **CRM** (accounts, contacts, opportunities, quotes, cases).
- **Native agent layer:** **Agentforce** — Salesforce's platform-native agents, built to act inside the CRM, with the **Atlas Reasoning Engine**, low-code agent building, and a library of actions/topics. As of Summer '26 it runs on **Atlas Reasoning Engine 3.0** with **Multi-Agent Orchestration GA** and native **MCP + A2A** support — meaning the walled garden now speaks the open interop standards (strengthening the hybrid story below). Pricing is org-level: **Flex Credits (~$0.10/action)** or **~$2 per conversation**. Salesforce has reported Agentforce ARR ~$800M / ~29,000 deals as of Q4 FY26 (vendor-defined figures — treat as directional). ⚠ *Verify version/GA and pricing against Salesforce release notes.*
- **Data backbone / grounding:** **Data Cloud** (now marketed within **"Data 360"**) — unifies and harmonizes data via zero-copy/federation over Apache Iceberg to ground agents (09.c). *(Confirmed GA capability.)*
- **Governance:** the **Einstein Trust Layer** (data masking, dynamic grounding, prompt defense, toxicity scoring, audit trail, and a **zero-data-retention** contractual guarantee with model providers) plus the CRM's mature **sharing model** for entitlements — agents inherit these. This is the walled garden's biggest advantage: **governance and entitlements come largely for free** and are battle-tested.
- **CPQ direction:** legacy **Salesforce CPQ** (SteelBrick lineage) reached **End-of-Sale on 27 Mar 2025** (existing customers keep using/renewing; no new sales); new deployments go to **Revenue Cloud Advanced** (native, API-first, covering CPQ + billing across quote-to-cash — a Salesforce build). *(Fully agent-driven CPQ specifics remain partly roadmap — see 09.e.)*
- **Character:** deep, opinionated, CRM-first integration. Fast time-to-value and strong governance **inside** the Salesforce world; less natural once a process must span non-Salesforce systems.

### ServiceNow — the "process-and-workflow-centric" model
- **SoR/platform:** the **Now Platform** — a **workflow and process** system of record spanning IT, HR, customer service, and increasingly front-office (its strength is orchestrating *work* across the enterprise, with the CMDB and workflow engine at the core).
- **AI layer:** **Now Assist** (generative assistance) and **ServiceNow AI Agents / AI Agent Orchestrator** — a native **agentic** layer designed to execute and orchestrate work across ServiceNow workflows. GA'd via the **Yokohama** release (Mar 2025, AI Agent Orchestrator as the "control tower") and extended in **Zurich** (Q4 2025), which added **AI Agent Fabric** — a platform layer that ships the **Agent2Agent (A2A) protocol** and **MCP** support for cross-vendor agent interop (reinforcing the hybrid story below). *(Now Assist Pro Plus tiers were replaced by Foundation/Advanced/Prime tiers in Apr 2026.)*
- **CPQ / order-to-cash:** ServiceNow ships GA products — **Sales and Order Management**, **Order Management**, **Telecom Order Management**, and a dedicated **CPQ** — covering catalog→CPQ→order capture/orchestration/fulfillment across lead-to-cash, with a telecom extension. Its AI-CPQ engine is **Logik.ai**, which **ServiceNow acquired** (announced 3 Apr 2025, closed May 2025) — a composable, API-first AI CPQ now being folded into its CRM / Sales & Order Management. This is strong where CPQ is one stage of an end-to-end fulfillment **workflow**. *(The products are GA and documented; only fully autonomous, agent-driven end-to-end CPQ remains thin/maturing — see 09.e.)*
- **Governance:** platform **ACLs**, workflow controls, and its process/audit backbone; agents operate within these.
- **Character:** process-first, cross-domain **workflow** orchestration. Excels when the value is in **connecting steps across systems and departments** (order-to-cash, service fulfillment), less CRM-of-record-centric than Salesforce.

**The substantive difference (not just different feature names): record-of-truth SoR vs. workflow-state SoR — and why it changes how you build the agent.**
- **Salesforce is a *record* SoR:** the source of truth is the **object model** (Account, Opportunity, Quote). An agent "write" is a **record mutation**; atomicity, approvals, and audit are things you *assemble* around the objects (Approval Processes + Flow + savepoints). CPQ lives as a **revenue object model** (Revenue Cloud Advanced). So the agent's job is *populate and mutate the right records, correctly and atomically.*
- **ServiceNow is a *workflow/process* SoR:** the source of truth is the **state of work** moving through a process (a case/order advancing through stages). An agent "write" is often **advancing a workflow state**, and the platform *already* provides the approval engine, Flow Designer, and process audit natively — so HITL and auditability are frequently **built into the process**, not bolted on. CPQ sits as **one node in an order-to-cash workflow graph** (quote → order → fulfillment/provisioning).
- **Implication for design:** in Salesforce you engineer transactional record integrity and wire up approval processes; in ServiceNow you model the process and let its native state machine/approvals carry much of the governance. This is exactly why **telecom order-to-cash favors ServiceNow's model** (the value is orchestrating many fulfillment steps) while **CRM-of-record selling favors Salesforce's** (the value is the authoritative customer/quote record). Match the platform to whether your problem is "get the record right" or "drive the process."

**(c) The broader tradeoff — deep single-platform integration vs. vendor-neutral flexibility.**

| Dimension | Platform-native (Agentforce / ServiceNow AI Agents) | Composable / external orchestration |
|---|---|---|
| Integration depth | Deep, native to that SoR | You build the integrations (MCP helps) |
| Governance/entitlements | Largely inherited, battle-tested | You must implement and prove |
| Time-to-value | Fast (inside the platform) | Slower (assembly) |
| Multi-SoR reach | Weak (walled garden) | Strong (that's the point) |
| Flexibility / model choice | Constrained to the platform's | Full (any model, any framework) |
| Lock-in | High | Lower |
| Cost model | Platform licensing (can be steep at scale) | Component/usage + build/run |
| Best when… | Process lives inside one platform | Process spans a fragmented estate |

**Reality for most large enterprises:** a **hybrid**. Adopt platform-native agents for **self-contained, single-platform** workflows (Agentforce for CRM-native selling assist; ServiceNow AI Agents for service/fulfillment workflows) *and* build a **composable orchestration layer (with MCP, Module 2.4, and a cross-SoR semantic layer/graph, 09.c)** for **cross-platform journeys** that must read/write across Salesforce + ServiceNow + ERP. Walled-garden where self-contained; vendor-neutral where fragmented (Module 7.2).

**(d) Decision criteria.** Map the *process*: if it lives inside one SoR and that SoR has a capable native agent layer, prefer native (speed + governance). If it spans multiple SoRs, or you need model/framework freedom or to avoid lock-in, build composable — but budget for the governance and entitlement work the platform would otherwise have given you.

**(e) Pitfalls.** Over-committing to one walled garden across a multi-SoR estate (hitting its boundary); building composable and **under-investing in governance** you assumed you'd "inherit"; underestimating platform-native **licensing cost** at scale; betting on **roadmap** features as if GA (verify!); framework/platform churn (Module 5.3).

**(f) Enterprise example.** A telecom uses **ServiceNow** for order-to-cash/provisioning workflows (native AI Agents orchestrate the fulfillment steps) and **Salesforce** for the CRM/selling motion (Agentforce assists reps). For a quote-to-provision journey that starts in CRM and completes in ServiceNow, it runs a **composable orchestration layer** over MCP servers wrapping both — with a cross-SoR semantic layer so "the customer," "the order," and "the product" mean the same thing in both systems. Each SoR stays authoritative for its own domain (09.a).

---

## 09.e A concrete CPQ walkthrough — theme (e)

> **CPQ = Configure, Price, Quote:** the process of configuring a valid product/service bundle, pricing it (with discounts/approvals), and generating a formal quote. It's a perfect stress test for SoR-integrated agents because it moves from open-ended conversation to **high-stakes, financially-material writes** — and the SoR boundary and governance shift at each step.
>
> **Detail caveat:** the *agentic-CPQ* specifics of both Salesforce (Revenue Cloud Advanced direction) and ServiceNow (Logik.ai / CPQ within order-to-cash) are **partly roadmap and unevenly documented publicly**. The walkthrough below is the **durable pattern** — where the SoR boundary sits and what governance applies at each step — with vendor specifics flagged as *established* vs. *roadmap/thin* where relevant. Verify vendor capabilities before recording.

**The agent moves through four stages. At each, note the SoR boundary and the governance.**

### Stage 1 — Requirements gathering
- **What the agent does:** converses with the rep/customer to elicit needs (use case, scale, constraints, budget, timeline). Open-ended language work — the agent's sweet spot.
- **SoR boundary:** mostly **outside** the SoR — this is interaction/reasoning. The agent **reads** context from the CRM SoR (account, past purchases, entitlements, contract terms) to ground its questions — **entitlement-filtered** (09.b): it sees only what the rep may see. It may write lightweight, reversible notes (captured requirements) back to the opportunity.
- **Governance:** read entitlements enforced at the SoR; low-stakes note writes are fine with light control; PII minimization in the conversation (Module 6.3).
- **Pitfall:** hallucinating product capabilities or prior-purchase facts — must ground in the SoR/semantic layer, not memory (Modules 1.9, 09.c).

### Stage 2 — Configuration
- **What the agent does:** translates requirements into a **valid** product/service configuration — selecting products, bundles, options — respecting **compatibility and dependency rules** (`REQUIRES`, `INCOMPATIBLE_WITH` — Module 4.2/4.7).
- **SoR boundary:** the boundary **starts to matter**. The authoritative catalog, configuration rules, and validity constraints live in the **CPQ engine / product SoR** (Salesforce Revenue Cloud Advanced; ServiceNow product catalog + CPQ, with Logik.ai as its AI-CPQ engine). The agent should **call the configuration engine to validate** — not invent a configuration in free text. The engine (or the ontology/semantic layer) is the authority on what's a *valid* config; the LLM proposes, the engine validates.
- **Governance:** configuration validity is enforced by the **CPQ rules engine**, not the LLM. A reasoning model (Module 8.1) can help with complex multi-constraint configs, but the engine is the source of truth. Reads are entitlement-filtered.
- **Established vs. roadmap:** deterministic rule-based configuration engines are **established**; **agent-driven** configuration that reasons over the catalog and calls the engine is **emerging/roadmap** at both vendors — verify.
- **Pitfall:** letting the LLM assert a configuration is valid without engine verification → invalid quotes. Always validate against the engine/ontology.

### Stage 3 — Pricing
- **What the agent does:** assembles the pricing *inputs* and **explains the result**, but does **not** compute the number. Concretely, pricing engines run a **price waterfall**: **list price → volume/tier discount → contracted/negotiated price → promotions → net price**, governed by **price rules** and **discount schedules**. The agent's job is to (1) pass structured inputs (products, quantities, term, region/currency, customer entitlements) to the engine, (2) surface the resulting waterfall **and the margin impact**, and (3) map any requested discount against the **approval matrix**.
- **SoR boundary:** **firmly inside** the SoR / pricing engine. Pricing is **exact, financially material, and rule-governed** — it must come from the **authoritative pricing engine / SoR**, via live query (never a stale embedded copy — Module 3.8; never LLM arithmetic — Module 1.2). The LLM **explains** the price; the **engine computes** it.
- **Governance (tightening sharply):** the **approval matrix** is typically keyed to **discount depth × deal size × product family** and the rep's role/limits (enforced in code/SoR, not the prompt). Requests inside the rep's authority auto-price; anything beyond a threshold triggers an **approval workflow** (deal desk / finance) — the natural **human-in-the-loop** entry point for non-standard pricing (Modules 5.7, 09b). All pricing inputs and the resulting waterfall are auditable.
- **Pitfall:** LLM computing or "estimating" price, or applying an unauthorized discount. Price is computed by the engine; the waterfall and margin are surfaced, not invented; discounts are authorization-gated in code against the approval matrix.

### Stage 4 — Quote generation (the high-stakes write)
- **What the agent does:** assembles the formal quote (line items, prices, terms, validity, documents) and **writes it to the SoR**, potentially routing for approval and to the customer.
- **SoR boundary:** **fully inside** the SoR — this is the authoritative **write** that creates a real, legally/financially meaningful record. It goes through the SoR's **transactional API** (atomic, validation-respecting), with an **idempotency key** (no duplicate quotes on retry), and lands as an audited record.
- **Governance (maximum):** **human approval before commit** for high-stakes quotes (pricing, discounts, contract terms) — the agent **proposes**, a human **approves**, then it writes (Module 5.7). Full **audit log**: who/what/when, the discount and its approver, the rules applied, the rationale (Modules 5.8, 6.6 — SOX-relevant). Blast-radius limits (value caps) and, for any autonomous low-value quoting, **agent identity + scoped permissions + kill switch** (Module 8.9).
- **Pitfall:** committing a quote without approval/audit; non-atomic writes; duplicates on retry; bypassing SoR validation. These are the failures that make CPQ agents a liability rather than an asset.

**Where the SoR boundary sits — summary.**

| Stage | Primary locus | Authoritative source | Governance intensity |
|---|---|---|---|
| 1. Requirements | AI interaction layer (reads from SoR) | CRM SoR (context) | Low (read entitlements; light note writes) |
| 2. Configuration | AI proposes → **engine validates** | CPQ/product SoR + rules/ontology | Medium (validity enforced by engine) |
| 3. Pricing | **Pricing engine / SoR** (AI explains) | Pricing engine / SoR | High (discount authority, approvals) |
| 4. Quote generation | **SoR write** (AI drafts) | CRM/CPQ SoR (transactional) | Maximum (HITL approval, audit, idempotency) |

**The through-line:** the process moves from **AI-owned interaction** (Stage 1) to **SoR-owned authority** (Stage 4). Autonomy is *highest* where stakes are lowest (asking questions) and *lowest* where stakes are highest (writing a priced, discounted quote). Governance ratchets up in lockstep. This is the entire SoR-integration philosophy in one workflow.

**Established vs. roadmap / thin-detail flags for the video series.**
- **Established:** CRM/CPQ as SoR; deterministic configuration and pricing engines; approval workflows; transactional/audited quote writes; entitlement models (Salesforce sharing, ServiceNow ACLs); Data Cloud as grounding backbone; Agentforce (Atlas 3.0, Multi-Agent Orchestration GA) and ServiceNow AI Agents (Yokohama/Zurich, AI Agent Fabric) as native agent layers, both now speaking MCP/A2A; ServiceNow's Sales & Order Management / CPQ / Telecom Order Management products; **Logik.ai as ServiceNow's acquired AI-CPQ engine** (closed May 2025).
- **Emerging / roadmap / verify:** fully agent-driven CPQ (an agent reasoning end-to-end through configure→price→quote with engine calls and HITL gating) at both vendors; the exact division of labor between LLM and CPQ engine in shipping products; Logik.ai's depth of integration into ServiceNow's agentic CPQ.
- **Public detail is thin** on the precise, GA agentic-CPQ feature sets at both vendors — **verify against current release notes and documentation** before making concrete capability claims on video.

**(f) Enterprise example (end-to-end).** A rep tells the agent, "ACME wants to expand — 500 seats of the enterprise tier plus premium support, and they're asking for aggressive pricing." The agent: (1) **reads** ACME's history and entitlements from the CRM (filtered to the rep), asks clarifying questions; (2) proposes a configuration and **validates it against the CPQ engine** (catching that the enterprise tier *requires* premium support — the ontology rule, Module 4.7); (3) gets the **exact price from the pricing engine**, notes the requested 18% discount exceeds the rep's 10% authority; (4) drafts the quote, and because the discount needs sign-off, **routes it to the deal desk for approval** — showing the config, price, discount, cited rules, and margin impact. On approval, it writes the quote to the SoR via the transactional API (idempotent, audited, with the approver recorded). A retry after a network blip creates **no** duplicate. The rep got a fast, correct, governed quote; the SoR stayed authoritative; every consequential step was checked and logged.

---

### Module 09 takeaways
- **Core pattern:** AI is the **interaction/orchestration** layer; the **SoR stays authoritative** — for truth, governance, transactions, and audit — even as AI becomes the primary interface.
- **Read vs. write:** reads must be **entitlement-aware at the source** (the LLM is never the access boundary); **writes** demand stronger authz, **transactional integrity, idempotency, rollback, and human-in-the-loop** — especially for pricing, quotes, and contracts.
- **Semantic layer** turns messy SoR schemas into governed business concepts an agent can reason over (Data Cloud for Salesforce; Now Platform modeling for ServiceNow; a cross-SoR graph for fragmented estates).
- **Platform-native vs. composable:** Salesforce = walled-garden-with-deep-integration (CRM SoR, Agentforce/Atlas 3.0, Data Cloud/Data 360, Trust Layer, **Revenue Cloud Advanced** as the CPQ successor); ServiceNow = process/workflow-centric (Now Platform, Now Assist/AI Agents, Sales & Order Management + CPQ, with **Logik.ai** as its acquired AI-CPQ engine). Both now support MCP/A2A. Native for single-platform speed + inherited governance; composable for multi-SoR flexibility; most enterprises go **hybrid**. **Verify GA vs. roadmap.**
- **CPQ walkthrough:** autonomy is highest where stakes are lowest (requirements) and lowest where stakes are highest (quote write); the SoR boundary and governance ratchet up stage by stage. **Agentic-CPQ specifics are partly roadmap and thinly documented — flag and verify.**

*End of knowledge base. Return to `00-overview.md` for the module index.*
