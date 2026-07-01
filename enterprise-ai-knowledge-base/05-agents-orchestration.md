# Module 5 — Agents & Orchestration

> **Why this module exists:** Everything so far — prompting, structure, tools, retrieval, structured knowledge — becomes an *agent* when you put the model in a **loop** where it can reason, act, observe, and decide what to do next toward a goal. Agents are where enterprise AI moves from "answers questions" to "does work." They're also where risk, cost, and unpredictability spike. This module covers how agents work, how to architect and orchestrate them, and how to keep them safe and observable. The SoR theme continues: agents are the "interaction/orchestration layer" that reads and (carefully) writes to Systems of Record.

**Module map**
5.1 The agent loop (perception → reasoning → action)
5.2 Single-agent vs. multi-agent architectures
5.3 Orchestration frameworks (LangGraph, CrewAI, …)
5.4 Planning
5.5 State and memory management
5.6 Guardrails
5.7 Human-in-the-loop
5.8 Observability

---

## 5.1 The agent loop (perception → reasoning → action)

**(a) What it is / why it matters.**
An **agent** is an LLM operating in a **loop**: it perceives a situation, reasons about what to do, takes an action (usually a tool call), observes the result, and repeats until the goal is met or it stops. The distinguishing feature vs. a plain LLM call is **autonomy over control flow** — the model decides *what to do next and when it's done*, rather than following a fixed script. This is the generalization of ReAct (Module 2.1).

**Analogy.** A single LLM call is a vending machine: input in, output out. An agent is a junior analyst you give a goal ("prepare the ACME renewal quote"): they look things up, use tools, hit obstacles, adjust, and come back when done — exercising judgment about the steps.

**(b) Mechanics — the loop.**
1. **Perception** — take in the goal, context, conversation, and latest observations (retrieved data, tool results).
2. **Reasoning/decision** — the LLM decides the next action: call a tool, ask the user, or finish. (ReAct-style thought → action.)
3. **Action** — execute a tool call (query SoR, run code, search, write a record) — governed by *your* code (Module 2.3).
4. **Observation** — feed the result back into context.
5. **Loop** until a stopping condition (goal met, max steps, error, human handoff).

**Key design choices.** Stopping criteria (avoid infinite loops — cap iterations/budget), how much autonomy vs. fixed workflow (5.2/5.4), what tools are available (defines the action space), and how errors are handled (retry, replan, escalate).

**Spectrum of "agentic."** From **workflows** (fixed, code-defined sequences with LLM steps — predictable, testable) to **autonomous agents** (model plans its own path — flexible, less predictable). A widely-shared industry view (e.g., Anthropic's "Building Effective Agents") is: **prefer the simplest thing that works** — often a structured workflow, not a fully autonomous agent. Add autonomy only when the task's variability demands it.

**(e) Pitfalls (expanded throughout module).** Runaway loops (cost/latency), **compounding errors** (each step's mistakes propagate — a 95%-reliable step run 10× is ~60% reliable end-to-end), tool misuse, and unpredictability that defeats testing. Autonomy is a cost, not a virtue.

**(f) Enterprise example.** A "renewal prep" agent: perceives the goal + account, reasons it needs the current contract → calls CRM → observes terms → checks open support issues → drafts a renewal summary → asks the rep to confirm before writing anything back. Loop, with a human gate on the write (5.7, Module 09b).

---

## 5.2 Single-agent vs. multi-agent architectures

**(a) What it is / why it matters.**
You can build with **one agent** (one LLM loop with many tools) or **multiple agents** (specialized agents that collaborate — e.g., a planner, researchers, a writer, a critic). Multi-agent is fashionable and sometimes powerful, but it adds coordination cost and failure surface. Choosing correctly is a major architectural decision.

**(b) Mechanics.**
- **Single-agent** — one loop, one context, a toolbox. Simpler, easier to debug/evaluate, cheaper. Scales surprisingly far. Limits: too many tools degrade selection (2.3); very long tasks strain one context.
- **Multi-agent patterns:**
  - **Orchestrator–worker (supervisor)** — a lead agent decomposes the task and delegates to sub-agents, then synthesizes. Common and effective.
  - **Role-based crew** — agents with personas/roles collaborate (researcher, writer, reviewer).
  - **Sequential pipeline** — output of one feeds the next (often better modeled as a *workflow*, 5.3).
  - **Debate/critique** — agents critique each other to improve quality (overlaps with LLM-as-judge, 8.8).
- **Why multi-agent can help:** separation of concerns, parallelism (fan-out research), specialized prompts/tools per role, and larger effective context (each sub-agent has its own window). Anthropic's multi-agent research system and similar report gains on **broad parallelizable search/research** tasks.
- **Why it often hurts:** coordination overhead, error propagation between agents, higher cost/latency (many LLM calls), harder debugging, and **context-passing loss** (agents miscommunicate). A large body of practitioner experience says **most "multi-agent" needs are actually one good agent or a workflow.**

**(d) Decision criteria.**
- **Start single-agent** (or a workflow). Reach for multi-agent when: the task **parallelizes** (independent subtasks — research many sources at once), needs **genuinely distinct specializations/tools**, exceeds one context's practical limit, or benefits from **independent critique**.
- Prefer **orchestrator–worker** over free-for-all agent swarms; constrain communication paths.
- **Maturity:** multi-agent orchestration is **stabilizing** — real wins in specific shapes (parallel research, clear role separation), still immature for tightly-coupled tasks where coordination cost dominates (Module 8.3).

**(e) Pitfalls & failure modes.** Multi-agent as a solution in search of a problem; unbounded agent-to-agent chatter (cost explosion); lost context between agents; no clear termination; debugging a distributed nondeterministic system; diffusion of responsibility (no single place enforces guardrails).

**(f) Enterprise example.** A market-research task fans out five sub-agents (one per competitor) in parallel, each retrieving and summarizing, with an orchestrator synthesizing — a good multi-agent fit. By contrast, the CPQ quote flow (Module 09e) is better as a **single agent + workflow with gated steps**, because the steps are tightly coupled and each needs governance, not parallelism.

---

## 5.3 Orchestration frameworks

**(a) What it is / why it matters.**
Orchestration frameworks manage the agent loop, tool calling, state, multi-step control flow, and (for some) multi-agent coordination — so you don't rebuild that plumbing. Choosing one shapes how you build, test, and operate. They differ mainly in **how much structure/control** they impose vs. how much they abstract away.

**(c) Tools/frameworks and how they differ.**
- **LangGraph** (LangChain ecosystem) — models agents as **graphs/state machines**: nodes = steps, edges = control flow, explicit **state**, support for cycles, checkpoints, human-in-the-loop pauses, and durable execution. Favored for **production** because control flow is explicit and inspectable (vs. "magic" autonomy). Pairs with **LangSmith** for observability/eval.
- **CrewAI** — **role-based multi-agent** framework: define agents (role, goal, backstory), tasks, and processes (sequential/hierarchical). Fast to prototype crews; more opinionated/abstracted.
- **AutoGen (Microsoft)** — conversation-centric multi-agent framework (agents message each other); research-strong, flexible; **AG2** community fork exists.
- **OpenAI Agents SDK / Swarm-lineage** — lightweight agent + handoff primitives from OpenAI.
- **LlamaIndex** — retrieval/RAG-centric, with agent/workflow features; strong when data/RAG is the core.
- **Semantic Kernel (Microsoft)** — enterprise/.NET-friendly orchestration.
- **Cloud/platform-native** — **AWS Bedrock Agents**, **Google Vertex AI Agent Builder / Agentspace**, **Azure AI Agent Service**; and **application-platform-native** agent layers — **Salesforce Agentforce**, **ServiceNow AI Agents** (Module 09d) — which trade openness for deep SoR integration and built-in governance.
- **Model-native "agentic" APIs** — vendors increasingly offer built-in tool-use loops, computer-use, and memory primitives, reducing framework dependence.

**(d) Decision criteria.**
- **Production, need control/observability/durability** → LangGraph (or a cloud-native equivalent) with explicit state and checkpoints.
- **Fast multi-agent prototype** → CrewAI/AutoGen.
- **RAG-heavy** → LlamaIndex.
- **Deep SoR integration + built-in governance** → platform-native (Agentforce / ServiceNow) — see Module 09d for the walled-garden vs. composable tradeoff.
- **General principle:** favor frameworks that make **control flow and state explicit** for anything that touches money, records, or customers. Avoid lock-in where you can (MCP, Module 2.4, helps keep the tool layer portable).
- **Caveat:** this space churns fast; frameworks rise and fall quarterly. Bet on **portable concepts** (loops, state, tools, checkpoints, evals) over any one framework, and keep the model/tool boundaries clean.

**(e) Pitfalls.** Framework lock-in; over-abstracted "magic" that's impossible to debug or evaluate; adopting multi-agent frameworks for single-agent problems; version churn; hiding the security boundary inside framework internals you don't control.

**(f) Enterprise example.** A regulated insurer builds its claims-triage agent on **LangGraph** so every state transition is explicit, checkpointed (resumable/auditable), and can **pause for human approval** before any payout write — then exposes SoR tools via **MCP** so the same governed tools serve other agents.

---

## 5.4 Planning

**(a) What it is / why it matters.**
**Planning** is how an agent decides the *sequence* of steps to reach a goal, rather than reacting one step at a time. Good planning is what lets agents handle complex, multi-step tasks; poor planning is a top cause of agents wandering, looping, or missing steps.

**(b) Mechanics — approaches.**
- **ReAct (implicit planning)** — plan-as-you-go, one step at a time (2.1). Flexible, adaptive; can lose the thread on long tasks.
- **Plan-and-execute** — generate a full plan first, then execute steps (re-planning as needed). More structured; better for known-shaped tasks; the plan is inspectable/approvable.
- **Decomposition** — break the goal into sub-goals/sub-tasks (least-to-most, task trees). Pairs with orchestrator–worker (5.2).
- **Reflection / self-critique** — the agent reviews its own progress/output and revises (Reflexion-style). Improves quality at cost.
- **Tree/graph search over actions** — explore multiple paths (more research-y; expensive).
- **Deterministic scaffolding** — encode the plan as a **workflow** (5.1/5.3) when the steps are known; let the LLM fill the reasoning within fixed structure. Often the most reliable enterprise choice.

**(d) Decision criteria.** Known, repeatable process → **encode the plan as a workflow** (predictable, testable, governable). Variable/open-ended task → let the agent plan (ReAct or plan-and-execute) with strict stopping conditions. Add reflection for quality-critical outputs. **The more autonomy in planning, the more you need evaluation, guardrails, and human gates.**

**(e) Pitfalls & failure modes.** Over-planning trivial tasks; plans that don't adapt when reality diverges (no re-planning); no termination (loops); plans that skip validation/permission steps; the model **confidently planning a wrong approach** and executing it (compounding errors, 5.1).

**(f) Enterprise example.** The CPQ agent (Module 09e) uses a **deterministic plan** — requirements → configure → price → quote — because the process is known and each stage has governance. Within each stage, the LLM reasons freely (e.g., which clarifying questions to ask), but it cannot reorder or skip stages. Structure where it matters, flexibility where it helps.

---

## 5.5 State and memory management

**(a) What it is / why it matters.**
Agents need to **remember** — within a task (working state) and, increasingly, across sessions (persistent memory). But the model itself is **stateless**: each call only knows what's in the context window (Module 1.6). Memory is therefore an **engineered system around the model**, not a model feature. Getting it right is central to coherent, personalized, non-repetitive agents; getting it wrong causes context bloat, forgetting, and cost blowups. (The cutting-edge of *persistent cross-session* memory is Module 8.2.)

**(b) Mechanics — the memory taxonomy.**
- **Short-term / working memory** — the current context window: conversation, recent tool results, scratchpad. Bounded; must be curated.
- **Context management** — because the window is finite, you **summarize/compress** older turns, **trim** irrelevant content, and keep critical facts pinned. "Context engineering" (deciding what's in the window at each step) is now a core skill.
- **Long-term memory** — persisted outside the model and **retrieved when relevant** (this is RAG applied to memory):
  - **Episodic** — past interactions/events ("last quarter we discussed X").
  - **Semantic** — facts/preferences about the user/domain ("this customer requires NET-60 terms").
  - **Procedural** — learned how-to/skills.
- **Storage** — vector store (semantic recall), key-value/profile store (structured facts/preferences), and increasingly the **SoR itself** as durable memory (write agreed facts back to CRM, don't invent a shadow store).
- **State (for workflows/agents)** — explicit state objects (LangGraph), checkpoints for durability/resumption/audit.

**(d) Decision criteria.** Use **working memory + summarization** for single sessions; add **long-term memory** when cross-session continuity/personalization has clear value. **Prefer the SoR as the durable memory of record** for business facts (a customer's terms belong in CRM, not only in an agent's private memory) — this keeps one source of truth and respects entitlements. Use vector memory for softer recall (past conversations).

**(e) Pitfalls & failure modes.**
- **Context bloat** — stuffing all history → cost/latency up, "lost in the middle" (1.5) → quality down.
- **Memory poisoning** — a wrong or injected "fact" persists and corrupts future behavior (a security concern for persistent memory — 8.2).
- **Stale/contradictory memory** — remembered facts conflict with the SoR; the SoR must win.
- **Privacy** — persisting PII in agent memory creates governance/retention obligations (Module 6.3); and cross-user memory leakage is a breach.
- **Shadow source of truth** — an agent memory that diverges from the SoR.

**(f) Enterprise example.** A customer-success agent keeps working memory of the current chat, summarizes long threads to stay within budget, and stores durable facts ("prefers quarterly reviews," "escalation contact = …") **as structured fields on the CRM account** — so the next session (and human reps) see the same truth, entitlements apply, and nothing lives in an ungoverned side-store.

---

## 5.6 Guardrails

**(a) What it is / why it matters.**
**Guardrails** are the controls that keep an agent within safe, correct, compliant bounds — on **inputs** (block malicious/off-topic requests), **outputs** (prevent PII leakage, toxicity, hallucinated commitments), and **actions** (constrain what tools it can call and with what authority). For enterprises, guardrails are the difference between a demo and something you can point at customers, money, and records. **The central principle: the LLM is never the security boundary** (it can be manipulated); guardrails live in deterministic code and policy around it.

**(b) Mechanics — layers.**
- **Input guardrails** — detect/deflect prompt injection (2.1), jailbreaks, off-scope requests, disallowed topics; validate/parse inputs.
- **Output guardrails** — PII/secret detection and redaction, toxicity/safety filters, format/schema validation (2.2), groundedness checks (answer supported by sources — 3.9), and **policy checks** ("never promise a discount," "always include disclosure").
- **Action guardrails (most important for agents):**
  - **Least-privilege tools** — the agent can only call what it needs; **read vs. write separation** (Module 09b).
  - **Permission enforcement in code** — the tool layer checks the *user's* entitlements on every call (3.8); the model can request, but code authorizes.
  - **Confirmation/approval gates** for high-stakes actions (5.7).
  - **Idempotency, transaction limits, rate limits, spend caps** — bound blast radius.
  - **Allow-lists / sandboxing** — for code execution, external calls, MCP servers (2.4).
- **Deterministic + model-based** — combine hard rules (regex/policy engines, schema) with model-based classifiers (a small model flags unsafe content). Defense in depth.

**(c) Tools.** NVIDIA NeMo Guardrails, Guardrails AI, Llama Guard / Prompt Guard, vendor safety filters and moderation endpoints, policy engines (OPA), DLP tools, plus platform-native guardrails in Agentforce/ServiceNow (Module 09d).

**(d) Decision criteria.** Scale guardrails to **stakes and autonomy**: an internal brainstorming bot needs little; an agent that writes quotes or touches customer data needs the full stack, with **writes and high-stakes actions always gated**. Enforce entitlements and destructive-action limits in **code**, not prompts.

**(e) Pitfalls & failure modes.**
- **Trusting the prompt** ("I told it not to…") — bypassed by injection. Enforce in code.
- **Over-blocking** — heavy-handed filters frustrate users and break legitimate flows.
- **Guardrails only on inputs/outputs, not actions** — the dangerous gap for agents.
- **No injection defense in RAG/agents** — retrieved/tool content carries hidden instructions (2.1, 2.4).
- **Confused-deputy** — the agent acts with its own broad privileges on behalf of a manipulated request (propagate user identity; least privilege).

**(f) Enterprise example.** The CPQ agent may *read* the catalog and *draft* a quote freely, but the tool that **writes a quote or applies a discount** enforces: the rep's entitlements, discount limits by role, mandatory approval above a threshold, idempotency keys (no duplicate quotes on retry), and a full audit log — all in code, independent of anything the model "decided" (Module 09b/e).

---

## 5.7 Human-in-the-loop (HITL)

**(a) What it is / why it matters.**
**Human-in-the-loop** inserts human judgment at critical points — approval before consequential actions, review of uncertain outputs, escalation of hard cases. It's the pragmatic bridge between "fully manual" and "fully autonomous," and it's how enterprises deploy agents responsibly *today* for anything high-stakes. It also builds the trust and the training data needed to safely expand autonomy over time.

**(b) Mechanics — patterns.**
- **Approve/reject gates** — agent proposes, human approves before the action commits (the default for writes to SoR, payments, external comms). Requires the framework to **pause and resume** (LangGraph checkpoints, 5.3).
- **Confidence-based escalation** — auto-handle high-confidence cases (use logprobs / eval signals, 1.8/2.6), route low-confidence to humans.
- **Human-on-the-loop (oversight)** — agent acts autonomously but humans monitor and can intervene/override; suited to lower-stakes or reversible actions.
- **Review-and-edit** — agent drafts, human edits and sends (email, quote, summary).
- **Feedback capture** — human decisions become **evaluation and training data** (2.6), improving the system and justifying more autonomy over time.

**(d) Decision criteria — where to put the human.** Gate on **stakes × reversibility × confidence**: high-stakes + irreversible (pricing, contracts, payouts, external customer commitments) → **mandatory approval**; reversible/low-stakes → oversight or autonomous with logging; uncertain → escalate. Design the human step to be **fast and well-contextualized** (show the proposed action + rationale + sources) so it doesn't become a bottleneck.

**(e) Pitfalls & failure modes.**
- **Rubber-stamping** — humans approve without reading (automation bias); mitigate with clear, concise, well-justified proposals and spot-checks.
- **Bottlenecks** — too many gates kill the efficiency you deployed AI for; gate only what matters.
- **No audit trail** of who approved what (compliance gap — Module 6.6).
- **Approval fatigue** leading to gate removal without re-assessing risk.

**(f) Enterprise example.** The renewal agent drafts the quote and shows the rep: proposed line items, price, the discount applied, the policy it cites, and flagged risks. The rep approves with one click (or edits) — *then* the write commits to the SoR. Every approval is logged with user, timestamp, and the exact proposal (Module 09b).

---

## 5.8 Observability

**(a) What it is / why it matters.**
**Observability** is the ability to see what an agent did and why — every prompt, tool call, retrieval, decision, token, dollar, and latency — in development and production. Agents are **nondeterministic, multi-step, and expensive**; without observability you can't debug failures, control cost, catch regressions, prove compliance, or improve the system. It's not optional at enterprise scale. (This is the runtime half of LLMOps — Module 6.5.)

**(b) Mechanics — what to capture.**
- **Tracing** — the full execution trace of a run: each LLM call (prompt, response, tokens, latency, cost, model version), each tool call (inputs, outputs, errors), each retrieval (query, chunks, scores), state transitions, and the final outcome. **Distributed tracing** across multi-agent/multi-step flows (OpenTelemetry-based standards are emerging).
- **Metrics** — latency (per step and end-to-end), token/cost per run, tool success/error rates, retrieval quality signals, task-completion rate, human-intervention rate, guardrail triggers.
- **Evaluation integration** — run online evals (2.6/3.9) on production traffic; sample and score; alert on drift.
- **Logging for audit** — immutable records of actions taken (esp. writes), approvals (5.7), and the data/permissions involved (Module 6.6).
- **Feedback loops** — thumbs up/down, corrections, escalations → eval sets and improvement.

**(c) Tools.** LangSmith, Arize Phoenix, Langfuse, Helicone, Weights & Biases (Weave), Datadog LLM Observability, OpenTelemetry GenAI conventions, plus platform-native monitoring in Agentforce/ServiceNow/cloud agent services.

**(d) Decision criteria.** Instrument **from day one** — retrofitting observability is painful. Prioritize **tracing + cost + audit logging** for any production agent; add online eval and drift detection as usage grows. For regulated/high-stakes agents, treat **audit logging of actions and approvals** as a hard requirement (Module 6.6).

**(e) Pitfalls & failure modes.** No tracing → "the agent did something weird" is unsolvable; no cost tracking → surprise bills (deep loops, verbose contexts); logging sensitive data insecurely (traces contain PII/secrets — govern them, Module 6.3); metrics without evals (you see latency but not *quality* drift); no audit trail for actions (compliance failure).

**(f) Enterprise example.** When a customer disputes a quote the agent generated, ops pulls the full trace: the requirements captured, the catalog queried (with entitlements), the price rule applied, the discount and its approver, the exact model version, and the timestamped write to the SoR — a complete, auditable reconstruction. That same trace pipeline flags a week-long rise in "needs-clarification" outcomes, surfacing a catalog data issue before it becomes a revenue problem.

---

### Module 5 takeaways
- An **agent** is an LLM in a **loop** with autonomy over control flow; prefer the **simplest thing that works** — often a workflow, not full autonomy.
- **Single-agent/workflows** first; go **multi-agent** only for parallelizable or genuinely specialized work (orchestrator–worker over swarms). Multi-agent is **stabilizing**, not a default.
- **Frameworks** (LangGraph for control/production, CrewAI/AutoGen for multi-agent prototypes, LlamaIndex for RAG, platform-native for deep SoR integration) — bet on **portable concepts**, keep the tool layer portable (MCP).
- **Planning:** encode known processes as workflows; let agents plan open-ended tasks with strict stopping conditions.
- **Memory** is engineered around a stateless model; prefer the **SoR as durable memory of record** for business facts.
- **Guardrails:** the LLM is **never** the security boundary; enforce entitlements and action limits in code; gate writes and high-stakes actions.
- **Human-in-the-loop** on stakes × reversibility × confidence; make the human step fast and well-contextualized; capture decisions as training/eval data.
- **Observability** (tracing, cost, audit logging, online eval) is mandatory for production agents — instrument from day one.

*Proceed to `06-enterprise-operationalization.md`.*
