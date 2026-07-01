# Module 7 — Implementation & Adoption

> **Why this module exists:** The hardest part of enterprise AI is usually *not* the technology — it's choosing the right problems, justifying the investment, redesigning how people work, governing it, and measuring whether it paid off. This module is the leadership/program view. It's deliberately less about tokens and more about **turning capability into durable business value** — and avoiding the failure patterns that sink most initiatives.

**Module map**
7.1 Use-case selection & ROI framing
7.2 Build-vs-buy at the platform level
7.3 Change management & workflow redesign
7.4 Governance & maturity models
7.5 Common enterprise failure patterns
7.6 Measuring value

---

## 7.1 Use-case selection & ROI framing

**(a) What it is / why it matters.**
Most AI programs fail not because a model underperforms but because they picked the **wrong use case** — too risky, too vague, too low-value, or a poor fit for what LLMs are actually good at. Disciplined selection is the highest-leverage decision in the entire program.

**(b) Mechanics — selection criteria.** Score candidate use cases on:
- **Value** — hard $ (cost reduction, revenue, cycle-time) or strategic value; big enough to matter.
- **Feasibility / AI-fit** — does it play to LLM strengths (language, summarization, extraction, drafting, retrieval-grounded Q&A, classification) rather than weaknesses (exact calc without tools, guaranteed correctness, real-time precision)?
- **Data readiness** — is the grounding data available, clean, accessible, and permissioned (Module 6.2)? *Frequently the real gate.*
- **Risk / stakes** — consequences of error; reversibility; regulatory exposure (Module 6.6). High stakes ≠ avoid, but ≠ start-here.
- **Feedback loop** — can you measure quality and improve (evals, Module 2.6)?
- **Adoption feasibility** — will users actually change behavior (7.3)?

**A useful 2×2:** *Value* vs. *Risk/effort*. Start in **high-value / low-risk** (internal productivity, drafting, retrieval Q&A, deflection). Graduate to high-value/high-risk (autonomous actions on the SoR) once you've built trust, evals, and governance.

**(b′) ROI framing.** Quantify baseline (time/cost/error today), expected improvement, and **full cost** (model/API, infra, build, *ongoing eval + maintenance*, change management). Include the often-forgotten **run costs**: prompt/model spend at scale, human-in-the-loop labor, and maintenance as models/data evolve. Frame ROI as a portfolio (some quick wins to fund/justify the harder bets), not a single moonshot.

**(d) Decision criteria.** Prefer use cases where **AI augments a human** (draft/assist/recommend) over full automation for the first wave — lower risk, faster value, builds trust and training data (Module 5.7). Favor problems with **abundant, accessible, well-governed data**. Kill or defer use cases that require guaranteed correctness without a verification path.

**(e) Pitfalls & failure modes.**
- **Solution in search of a problem** — "we need an AI strategy" → building tech, not solving a problem.
- **Boiling the ocean** — one huge transformational project vs. compounding wins.
- **Ignoring data readiness** — the demo works on cherry-picked data; production data isn't ready.
- **Chasing the flashiest, riskiest use case first** (autonomous agent on financial writes) before the org has evals/governance/trust.
- **No ROI baseline** — can't prove value later (7.6).

**(f) Enterprise example.** A B2B company starts with **support-ticket deflection + rep-assist** (high value, low risk, data ready, measurable) rather than a fully-autonomous quoting agent. The wins fund and de-risk the later, higher-stakes CPQ-agent initiative (Module 09) — by which point they have evals, governance, and organizational trust.

---

## 7.2 Build-vs-buy at the platform level

**(a) What it is / why it matters.**
Enterprises must decide, layer by layer (Module 6.1), what to **build**, **buy**, or **adopt from a platform they already own**. Getting this wrong wastes money (rebuilding commodities) or creates lock-in and gaps (buying where you needed control). The calculus is unusual here because the underlying tech moves so fast that today's custom build is tomorrow's commodity feature.

**(b) Mechanics — the spectrum.**
- **Buy/consume** the commoditizing layers: **foundation models** (via API/cloud), embeddings, vector DBs, observability, guardrail libraries. Building these rarely makes sense.
- **Adopt platform-native** where the use case lives inside a SoR you already run: **Salesforce Agentforce**, **ServiceNow AI Agents**, Microsoft Copilot, cloud agent services. Pros: deep integration, inherited security/governance, fast time-to-value. Cons: lock-in, walled-garden limits, cost, less flexibility across a **multi-SoR** estate (Module 09d).
- **Build/assemble** the **differentiating middle**: your retrieval quality, your semantic layer/knowledge, your orchestration and guardrails, your evals — the parts that encode competitive advantage and control. This is usually *assembly of bought components*, not from-scratch.
- **Model choice within "buy"** — API vs. open/self-hosted (residency/control/cost — Module 6.5).

**(d) Decision criteria.** Buy commodities; adopt platform-native for **single-platform, SoR-embedded** workflows where speed and built-in governance win; build/assemble where **differentiation, control, cross-platform reach, or vendor-neutrality** matter. Key questions: Is this a **commodity** or a **differentiator**? Does it need to span **multiple SoRs**? What's the **lock-in and switching cost**? Can we **evaluate and govern** a bought solution to our standard? Preserve optionality with abstractions (model gateway, MCP, semantic layer — Module 6.1).

**(e) Pitfalls & failure modes.**
- **Building commodities** (a homegrown vector DB, a bespoke model) — sunk cost, quickly outdated.
- **Over-buying into one platform** then hitting its ceiling or lock-in across a fragmented estate.
- **Ignoring total cost/lock-in** of platform-native licensing at scale.
- **Reinventing governance** the platform already provides — or conversely, assuming a composable stack "inherits" governance it doesn't.
- **Framework/tool churn** (Module 5.3) turning a "build" into perpetual rework.

**(f) Enterprise example.** A firm running both Salesforce and ServiceNow adopts **Agentforce** for CRM-native selling assist and **Now Assist/AI Agents** for service workflows (platform-native, fast, governed) — but builds a **composable orchestration layer with MCP** for cross-platform journeys that must read from *both* SoRs plus an ERP, because no single platform owns the whole process. Walled-garden where it's self-contained; vendor-neutral where the estate is fragmented (Module 09d).

---

## 7.3 Change management & workflow redesign

**(a) What it is / why it matters.**
Technology adoption is a **people** problem. The largest AI ROI comes not from bolting a copilot onto an unchanged process, but from **redesigning the workflow** around what AI now makes cheap — and bringing people along. Ignore this and you get expensive shelfware with 5% adoption.

**(b) Mechanics.**
- **Workflow redesign** — don't pave the cow path. Ask "if drafting/summarizing/retrieval/triage is now near-free, how *should* this process work?" Redesign roles and hand-offs (AI drafts, human reviews and decides — Module 5.7).
- **Trust-building** — start with **augmentation** (human stays in control), show reliability with citations/explainability, and let evidence, not mandate, drive adoption.
- **Training & enablement** — teach people to prompt, to verify AI output (not blindly trust — automation bias), and *when not to* use it.
- **Incentives & metrics** — align individual incentives with adoption; measure and celebrate wins; make the AI-assisted path the easy default (embed in existing tools/SoR surfaces, not a separate app).
- **Feedback channels** — users report failures; those become eval cases (Module 2.6) and improvements — a virtuous loop that also builds ownership.
- **Job/role impact** — address fears honestly; frame as augmentation and reskilling; be transparent about changes.

**(d) Decision criteria.** Embed AI **where work already happens** (inside CRM/ITSM, not a bolt-on chatbot) to minimize behavior change. Sequence: augmentation → trust → workflow redesign → expanded autonomy. Invest in enablement proportional to the behavior change required.

**(e) Pitfalls & failure modes.**
- **"Build it and they will come"** — no adoption plan; tool ignored.
- **Paving the cow path** — automating a broken process instead of redesigning it.
- **Over-trust / automation bias** — users rubber-stamp wrong outputs (Module 5.7); or **under-trust** after an early visible failure poisons the well.
- **Separate-app friction** — forcing users out of their SoR into a standalone tool.
- **Ignoring the human impact** — resistance, fear, quiet non-adoption.

**(f) Enterprise example.** Instead of a standalone quoting chatbot, the CPQ assistant lives **inside the CRM** where reps already work; it drafts quotes for rep review, cites the pricing rules it used, and gets better as reps correct it. Adoption climbs because it fits the existing workflow and visibly saves time — and the redesigned process (AI drafts, rep approves, SoR records) is faster *and* better-governed than before.

---

## 7.4 Governance & maturity models

**(a) What it is / why it matters.**
**AI governance** is the organizational system — policies, roles, review processes, standards — that ensures AI is built and used responsibly, safely, and in compliance. **Maturity models** describe the stages orgs move through, giving a roadmap and a way to assess where you are. Together they turn ad-hoc experimentation into a scalable, trustworthy capability.

**(b) Mechanics.**
- **Governance components:** an **AI governance body** (cross-functional: legal, security, data, business, ethics); an **acceptable-use policy**; a **use-case intake & risk-tiering** process (proportionate controls by risk — Module 6.6); **standards** for eval, security, data handling, human oversight; an **AI system inventory**; vendor/model risk assessment; incident response for AI failures; and alignment to frameworks (**NIST AI RMF**, **ISO/IEC 42001**, EU AI Act obligations).
- **Operating model:** ranges from **centralized** (a central AI team/platform — control, consistency, but can bottleneck) to **federated / hub-and-spoke** (central platform + standards, business units build on top — scales, common at maturity) to **decentralized** (fast, risky, inconsistent). Most mature orgs land on **hub-and-spoke**: a central platform/CoE provides paved-road tooling, guardrails, and governance; teams innovate within it.
- **Maturity stages (typical):** (1) **Experimentation** (scattered pilots, shadow AI) → (2) **Foundational** (first production use cases, basic governance, a platform emerging) → (3) **Operational/Scaling** (repeatable delivery, evals, hub-and-spoke, reuse) → (4) **Transformational** (AI reshapes core processes, agents in workflows, strong governance and measurement embedded).

**(d) Decision criteria.** Stand up **lightweight governance early** (risk-tiering + basic standards) — enough to be safe without smothering experimentation; mature toward **hub-and-spoke** with a paved road (shared platform, guardrails, evals) as use cases multiply. Match control intensity to **risk tier**, not a blanket policy.

**(e) Pitfalls & failure modes.**
- **No governance** — shadow AI, data leakage, inconsistent risky deployments.
- **Governance so heavy it kills innovation** — every use case a 6-month review; teams route around it.
- **Governance without enablement** — rules but no paved road, so teams can't comply easily.
- **Perpetual pilots** — never crossing from experimentation to production (the "pilot purgatory" failure — 7.5).
- **No central learning** — every team re-solves retrieval/eval/guardrails from scratch.

**(f) Enterprise example.** A company forms an AI governance board, adopts risk-tiering (Tier 1: internal drafting — light; Tier 3: customer-facing writes to SoR — full evals, HITL, audit), and stands up a central platform team providing a paved road (approved models via gateway, shared RAG/guardrail/eval tooling, MCP connectors to Salesforce/ServiceNow). Business units ship fast **on** that road — hub-and-spoke maturity.

---

## 7.5 Common enterprise failure patterns

**(a) What it is / why it matters.**
Enterprise AI failures rhyme. Naming the patterns lets teams recognize and avoid them. (This section is a checklist the video series can turn into a memorable "how not to" episode.)

**(b) The pattern catalog.**
- **Pilot purgatory / "death by POC"** — endless demos that never reach production because there's no path through security, governance, integration, and evals. *Fix: pick production-viable use cases and build the operational path from day one.*
- **Solution in search of a problem** — tech-first, not value-first (7.1).
- **Data-readiness denial** — the demo works; production data is fragmented, stale, or ungoverned (Modules 6.2, 6.3). *The most common silent killer.*
- **Fine-tuning to inject knowledge** — stale, hallucination-prone; should have used RAG (Modules 1.7, 2.5).
- **No evaluation** — can't tell if it's good, can't catch regressions, can't improve (Module 2.6). *Flying blind.*
- **Hallucination reaching users** — no grounding/verification on factual/high-stakes outputs (Module 1.9).
- **Entitlement/security bypass** — service-account god-mode; RAG ignoring sharing rules (Modules 3.8, 6.3). *A breach, and a deployment blocker.*
- **Cost blowups** — frontier model everywhere, deep agent loops, no caching/budgets (Module 6.5).
- **Over-automation too soon** — autonomous high-stakes actions before trust/guardrails/evals exist (Module 5.7).
- **Adoption failure** — great tech, no change management; shelfware (7.3).
- **Multi-agent over-engineering** — complexity where one agent/workflow would do (Module 5.2).
- **Framework churn / lock-in** — betting the architecture on a fast-moving framework (Module 5.3) or a single platform across a multi-SoR estate (Module 09d).
- **Governance extremes** — none (chaos) or too much (paralysis) (7.4).
- **Ignoring maintenance** — treating AI as build-once; models/data drift, prompts rot, fine-tunes go stale.

**(d) Decision criteria.** Run new initiatives against this checklist as a pre-mortem. Most fixes trace back to earlier modules: value-first selection, data readiness, evals, grounding, entitlements, cost control, human-in-the-loop, and change management.

**(f) Enterprise example.** A retailer's "AI concierge" stalls in pilot purgatory: impressive demo, but no entitlement model, no evals, and data spread across three systems. Reset: narrow to one high-value flow, build the data backbone + entitlement-aware retrieval + eval harness first, ship an augmentation-mode version, then expand. The technology barely changed; the *approach* did.

---

## 7.6 Measuring value

**(a) What it is / why it matters.**
If you can't measure value, you can't sustain investment, prioritize, or improve. Measurement closes the loop from Module 7.1's ROI framing — and it's a common blind spot (teams ship and never quantify impact, then struggle to justify the next phase).

**(b) Mechanics — the metric layers.**
- **System/quality metrics** (Modules 2.6, 5.8) — accuracy, groundedness, task-completion, guardrail triggers, human-intervention rate. *Necessary but not sufficient — these aren't business value.*
- **Operational metrics** — latency, cost per task, throughput, deflection/automation rate.
- **Business outcome metrics** (the point) — cycle-time reduction (e.g., quote turnaround), cost savings (support cost per ticket), revenue impact (conversion, upsell, win rate), quality/error reduction, CSAT/NPS, employee productivity and satisfaction.
- **Adoption metrics** — active users, usage depth, retention (a great tool nobody uses has no value — 7.3).
- **Attribution** — baseline before, measure after; where possible use **controlled comparisons (A/B, holdouts)** to isolate AI's contribution from confounds.
- **Leading vs. lagging** — adoption and quality are leading indicators; business outcomes lag; track both.

**(d) Decision criteria.** Define **success metrics and a baseline before building** (7.1). Tie system metrics to a business outcome (don't optimize a proxy — Module 2.6). Use holdouts/A-B where feasible for credible attribution. Report a **balanced scorecard** (quality + ops + business + adoption), not a single vanity number.

**(e) Pitfalls & failure modes.**
- **No baseline** — impact unprovable.
- **Vanity metrics** — "queries served" without outcomes.
- **Proxy optimization** — great offline scores, no business impact.
- **Ignoring adoption** — value assumed, not realized.
- **Over-attribution** — crediting AI for gains driven by other changes (no holdout).
- **Only measuring cost savings** — missing revenue/quality/experience value (or vice versa).

**(f) Enterprise example.** For the CPQ assistant, the team baselines quote turnaround (avg 2 days), quote error rate, and win rate. Post-launch, an A/B holdout shows turnaround down to 4 hours, quote errors down 40%, and a modest win-rate lift on faster quotes — plus 80% rep adoption. That balanced, attributable scorecard justifies expanding from augmentation toward more autonomous quoting (with the governance from Modules 5–6 and 09).

---

### Module 7 takeaways
- **Select use cases** on value × feasibility × data-readiness × risk × measurability; start **high-value/low-risk augmentation**, graduate to higher-stakes autonomy.
- **Build vs. buy:** buy commodities, adopt platform-native for SoR-embedded single-platform work, build/assemble the differentiating middle; preserve optionality (gateway, MCP, semantic layer).
- **Change management/workflow redesign** is where the big ROI is: embed AI where work happens, augment before automating, redesign the process, build trust with evidence.
- **Governance + maturity:** lightweight-early → hub-and-spoke paved road; risk-tiered, proportionate control; avoid both chaos and paralysis.
- Know the **failure patterns** (pilot purgatory, data-readiness denial, no evals, entitlement bypass, cost blowups, over-automation, adoption failure) and pre-mortem against them.
- **Measure value** with a baseline and a balanced scorecard (quality + ops + business + adoption), attributed via holdouts where possible.

*Proceed to `08-cutting-edge.md`.*
