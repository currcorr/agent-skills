---
name: large-program-orchestration
description: "Run a multi-session agent program that is too big for one context — codebase migrations, framework swaps, monorepo-wide refactors, 'change X across every service' work. One parent orchestrator freezes scope into an immutable manifest, decomposes it into risk-ordered waves of file-disjoint work packages, gates every wave with fresh-context verification, and writes zero code itself. Use when a task would span many sessions ('40-session program'), when parallel agents might collide on files, or when irreversible steps (schema, prod data, deletes) need human sign-off machinery."
license: MIT
---

# Large Program Orchestration

The reference pattern for agent programs too big for one session. Source: Ryan
Carson's ~40-session migration (1 parent + 39 children; parent wrote zero
code), captured 2026-07-06. The architecture generalizes to any program where
scope, parallelism, and irreversibility all exceed what a single context can
hold safely.

**Use when** the request sounds like: "migrate X across the codebase",
"replace the ORM / auth / build system everywhere", "this refactor touches
every service", "too big for one context", "run this as a program". **Do not
use** for anything one session can finish — see "Below program scale" at the
end for the smaller loop primitives.

## The four laws

1. **The parent writes zero code.** The orchestrator plans, spawns workers,
   reviews outputs, sequences waves, enforces gates, and escalates to the
   human. It never edits a file itself. The moment the parent starts coding,
   it burns the clean context that makes its judgment trustworthy.
2. **Scope is frozen in one version-controlled manifest.** Every code unit
   gets a verdict and a wave number before execution starts. Workers treat
   the manifest as immutable — no worker re-litigates scope. Anything marked
   UNKNOWN triggers an immediate stop and a human ruling, which is written
   back into the manifest by the parent.
3. **Waves are risk-ordered; work packages within a wave are file-disjoint.**
   Sequence safest → most irreversible. Within a wave, parallel workers get
   explicitly disjoint file sets, stated in every prompt. No two agents touch
   the same file, ever.
4. **A gate stands between every wave.** Dedicated fresh-context sessions
   verify the wave (regression, inventory, backup) before the next wave
   starts. The builder of a wave never grades it. Failed gates spawn scoped
   fix sessions — they do not roll into the next wave.

## Phase 0 — Parallel audits → frozen manifest

Before any change: spawn N parallel audit sessions over **disjoint slices**
of the system (e.g. routes, APIs/crons, DB schema, libraries, scripts/docs —
Carson used 11). Each audit reports what exists, what it depends on, and a
proposed verdict per unit.

The parent synthesizes the audits into **one committed manifest file** that
assigns every code unit:

```
unit                          verdict        wave   notes
src/routes/billing/*          MIGRATE        3      touches payments — gate 3 covers it
src/lib/legacy-auth.ts        DELETE         5      after wave-4 regression proves unused
scripts/nightly-sync.cron     KEEP           -      out of scope, confirmed by owner
src/lib/pdf-render/*          UNKNOWN        ?      owner ruling needed: vendor or rewrite?
```

Rules baked into **every** downstream worker prompt:

- The manifest is the immutable source of truth. Do not re-litigate scope.
- If you hit anything not matching the manifest — a surprise file, an
  undocumented dependency, an UNKNOWN — **stop and report to the parent.
  Never improvise.**

UNKNOWNs go to the human owner; the ruling is written into the manifest
before any worker proceeds on that unit.

## Waves — risk-ordered, file-disjoint

- Order waves safest → most irreversible. Read-only and additive changes
  first; behavior changes next; schema migrations, prod-data mutation, and
  deletions last.
- Decompose each wave into work packages whose **file sets do not overlap**.
  State the exact file boundary in each worker's prompt ("you own
  `src/routes/billing/**` and nothing else").
- Each worker gets one narrow job, its file boundary, the manifest rules,
  and the escalation path. Nothing more.
- Tag every worker's output (branch, commit tag, or report file) so the
  parent can review and the program is auditable and meterable.

## Gates — between every wave

Run gates as **dedicated child sessions with fresh context** — never as a
self-check by the wave's builders (whatever builds never grades).

- **Regression gate**: browser-driven or test-suite E2E on a fresh isolated
  environment (Carson: fresh isolated DB branch) after key waves.
- **Pre-destructive gate**: before any prod-data or schema step — backup
  inventory audit plus a fresh point-in-time snapshot.
- **Inventory-then-execute**: destructive steps must first produce the exact
  inventory (file list, row counts) for human approval, then execute **only
  that list**, then re-verify, with a git tag restore point. Proposed
  inventories, never vague intent.
- **Failed gate** → parent spawns a scoped fix session against the specific
  failure. The next wave does not start until the gate passes.

## Escalation and human sign-off

The human owner is in the loop at exactly these points — no more, no less:

- Every UNKNOWN ruling (scope decisions).
- Every merge to main, prod data change, and schema migration.
- Every irreversible go/no-go, approved against a concrete inventory.

Workers escalate to the parent; only the parent escalates to the human. The
parent absorbs every surprise into the plan/manifest so the program's state
lives in one place.

## Final wave — campsite cleanup

Before closing, dedicated sessions update the repo's agent context to match
the new reality: AGENTS.md / CLAUDE.md, repo skills, and the agent knowledge
base. A migrated codebase with stale agent docs re-breaks on the next
session.

## Worked mini-example — "move 3 services off REST client v1"

Small enough to see whole, big enough to need the machinery:

1. **Phase 0** (3 parallel audits: `services/a`, `services/b`,
   `shared/clients`) → manifest: 14 call sites MIGRATE, 2 helpers DELETE
   (wave 3), 1 cron marked UNKNOWN (does anything still consume its output?).
   Owner rules: cron is dead, mark DELETE wave 3. Manifest committed.
2. **Wave 1** (safe, parallel ×2): worker A migrates `services/a/**`, worker
   B migrates `services/b/**` — disjoint file sets, additive changes behind
   the existing interface. Both report; parent reviews diffs.
3. **Gate 1** (fresh session): runs both services' integration suites on an
   isolated branch. One flaky contract test fails → parent spawns a scoped
   fix session for that one test. Gate re-run passes.
4. **Wave 2** (single worker): flips `shared/clients` default to v2 —
   behavior change, so it runs alone after the gate proved the callers.
5. **Gate 2** (fresh session): E2E on staging + human approves merge to main.
6. **Wave 3** (destructive): worker produces the exact delete inventory
   (2 helpers, 1 cron, 312 lines). Human approves the list. Worker deletes
   exactly that, tags a restore point, re-runs the suite.
7. **Cleanup**: a session updates AGENTS.md ("HTTP goes through client v2")
   and the service READMEs. Program closed.

Parent sessions used: 1. Code written by parent: none.

## Below program scale — the loop ladder

Most work does not need a program. Route by scale (taxonomy from the Claude
Code team's loops guide, claude.com/blog/getting-started-with-loops):

| Scale | Primitive | Fit |
|---|---|---|
| One prompt, self-judged done | **Turn-based loop** | short one-off tasks; encode end-to-end self-verification in a skill so it checks before handing back |
| Explicit completion criteria | **Goal-based loop** (`/goal`) | "iterate until tests pass / score ≥ N / max K attempts" — deterministic criteria work best |
| Recurring on an interval | **Time-based loop** (`/loop` local, `/schedule` cloud) | morning summaries, babysitting a PR through CI |
| Continuous stream, no human | **Proactive loop** (auto mode + workflows) | bug triage, dependency upgrades; small models for routine, big model for judgment |
| Too big for one context, parallel + irreversible steps | **This skill** | migrations, monorepo-wide changes, multi-day programs |

Two rules carry across every rung, from the same source plus the
fresh-context-verifier argument (sysls, captured 2026-07-03):

- **Whatever builds never grades.** Same-context self-review polishes the
  existing trajectory; a fresh-context verifier with an explicit rubric
  catches drift and normalized mistakes. That is why gates here are
  dedicated sessions.
- **Define stop conditions before you start.** "Good enough" thresholds,
  improvement deltas, and attempt caps — loops without them are slop
  factories or cost furnaces. When output falls short, fix the system (a
  skill, the manifest, cleaner docs), not the one instance.
