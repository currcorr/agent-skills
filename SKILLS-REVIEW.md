# Skills repo review — issues + top 15 skills to add

Reviewed 2026-07-02. 68 skills audited (frontmatter validation, file-reference
checks, size/overlap analysis). Recommendations target the workflow this repo
implies: EY-style consulting delivery (decks, sites, synthesis, exhibits) plus
agent tooling and moderate full-stack development, run across Claude Code,
Codex, and Gemini.

---

## Part 1 — Issues in existing skills

### Broken references (real bugs)

1. **skill-judge** — `SKILL.md:397` says "**MANDATORY**: Use exact script in
   `scripts/create-doc.py`", but the skill has no `scripts/` directory at all.
   Any agent following the skill hits a dead end at a step marked mandatory.
   Either add the script or rewrite the step as inline instructions.
2. **orchestrate-tufte-vdqi** — `SKILL.md:27` cites
   `references/tufte-principles.md` "(mirrored into both skills)", but the
   orchestrator itself has no `references/` dir. The file exists in
   `render-tufte-chart/references/`. Point the path at the downstream skill
   explicitly so a reader can actually open it.

### Naming / registration

3. **refero-design-research** — frontmatter `name: refero-design` doesn't match
   the directory name. With the README's symlink install, the folder registers
   under one name and the skill self-identifies as another; invocation and
   cross-references get confused. Align them.
4. **README symlink loop** — `for d in ~/skills/*/; do ln -sfn ...` symlinks
   `tools/` and `releases/` (which have no SKILL.md) into `~/.claude/skills/`,
   creating invalid skill dirs. Filter on the presence of `SKILL.md`.

### Trigger collisions (the biggest systemic problem)

The Tufte toolkit solved routing with `orchestrate-tufte-vdqi`; no other
cluster has a router.

5. **Slides: 4-way collision.** "Make me a presentation" plausibly triggers
   `pptx` ("any time a .pptx is involved"), `ey-deck` ("whenever the user asks
   for a deck, slides, presentation"), `marp-slide` ("use when users request
   slide creation, presentations"), and `frontend-slides` ("when the user
   wants to build a presentation"). Which one fires is model roulette. Fix:
   a deck router skill (see recommendation #15) and/or narrowing marp-slide
   and frontend-slides to explicit-mention-only triggers.
6. **UI design: refero-design-research vs frontend-design.** Refero claims
   "Primary/default skill for UI design … frontend/CSS styling, design
   systems, components"; frontend-design claims "when the user asks to build
   web components, pages, applications". Near-total overlap. Decide which is
   the default and make the other explicitly secondary in its description.
7. **Diagrams: draw-io / excalidraw / mermaid-diagrams / c4-architecture** all
   trigger on "architecture diagram". Excalidraw's description in particular
   claims generic "diagrams/flowcharts". Scope each to its file format or add
   routing guidance.
8. **perplexity** triggers on bare "search", "find", "look up" — broad enough
   to hijack requests that `last30days`, `startup-competitors`, or plain web
   search should handle, and its description references Context7, which isn't
   guaranteed to be installed on every machine this repo syncs to.

### Hygiene

9. **Oversized SKILL.md files** (>500-line guideline, loaded into context on
   trigger): `qa-test-planner` (757), `skill-judge` (752), 
   `database-schema-designer` (687), `design-system-starter` (603),
   `docx` (590), `senior-pm` (575), `refero-design-research` (538). The repo
   already contains the cure (`agent-md-refactor` / progressive disclosure —
   move detail into `references/`); apply it to itself.
10. **Nonstandard frontmatter keys** that skill loaders ignore or choke on:
    `last30days` (`install`, `security-review`, `security-status`, `source`,
    `tags`), `qa-test-planner` (`trigger`), `theorist` (`author`, `date`),
    `refero-design-research` (`compatibility`). Move metadata under
    `metadata:` or into the body.
11. **theorist** claims it "Activates EVERY session and stays active" — a
    description can't make that happen (descriptions are advisory to the
    model); if always-on behavior is wanted it needs a SessionStart hook, not
    a skill description. As written it just adds trigger noise.
12. **Machine-dependent skills undercut the "tool-agnostic" claim**:
    `web-to-markdown` (local `web2md` CLI), `codex`/`gemini` (external CLIs),
    `perplexity` (API access). Fine to keep, but each should state its
    dependency and a graceful fallback in the description so remote/web
    sessions don't trigger them and fail.
13. **financial-analyst** description is capability-list prose with no "Use
    when…" trigger language — weakest description in the repo relative to how
    useful the skill is for this workflow.
14. **grill-me vs grilling** — two skills for one loop. Intentional
    (trigger vs engine), but grill-me's body should be near-empty and defer;
    verify it doesn't duplicate instructions that will drift.

---

## Part 2 — Top 15 skills to add

Profile assumed (from the repo itself): consultant at EY doing hands-on
deliverable production — decks, client sites, qualitative synthesis, Excel
evidence — who also builds agent tooling and ships occasional software. The
repo is strong on **producing and QA-ing deliverables** and on **skill
meta-tooling**. The gaps are **upstream of delivery** (selling work, gathering
inputs), **quantitative work** (building models, analyzing raw data), and
**recurring engagement operations**.

Ranked by expected payoff. "Custom" = spec and build with `skill-creator`;
"Import" = vet and adopt an existing published skill.

### Tier 1 — fills a hole you hit weekly

1. **rfp-proposal-response** (custom) — Parse an RFP/tender → requirements +
   compliance matrix → win themes → proposal skeleton rendered through
   `ey-deck` and the active brand kit, SOW/engagement-letter draft included
   (scope, phases, fees, assumptions, exclusions). The repo covers delivering
   work end-to-end but nothing covers *winning* it — the single biggest
   upstream gap.
2. **financial-model-builder** (custom) — Build and audit Excel models:
   business cases, scenario/sensitivity analysis, driver trees, tie-out and
   formula-QA passes. `excel-to-evidence` *consumes* models and
   `financial-analyst` reasons about finance, but nothing *constructs or
   audits* a workbook. Sits on `xlsx` for mechanics.
3. **deep-research** (custom) — Multi-source, verified, fully cited research
   reports: fan out searches, fetch primary sources, adversarially check
   claims, synthesize with a citations section. `perplexity` and `last30days`
   are quick lookups; due-diligence and market-entry questions need the heavy
   version. Feeds `startup-competitors` and `management-consulting`.
4. **ey-doc** (custom) — Long-form Word/PDF client reports styled from
   `ey-brand-kit`, completing the kit-driven trio (deck / site / **document**).
   Same invariant: nothing outside `kits/` hard-codes a color or font. Sits on
   `docx`/`pdf` for mechanics, `ey-synthesis` for content.
5. **client-scrub** (custom) — Anonymize/sanitize deliverables: strip client
   names, figures, logos, and identifying details before reuse as templates,
   sharing as quals, or pasting into external AI tools. A Big-4 compliance
   reality the repo currently ignores, and it makes every other skill's output
   reusable.

### Tier 2 — completes existing pipelines

6. **interview-kit** (custom) — Stakeholder interview discussion guides,
   hypothesis-linked question banks, and note-capture templates whose output
   feeds `ey-synthesis` directly. Synthesis quality is capped by input
   quality; this closes the loop upstream.
7. **workshop-designer** (custom) — Design workshops: agendas, timeboxes,
   exercises, pre-reads, facilitation scripts, capture templates → outputs
   flow into `ey-synthesis` and `ey-site` (workshop sites already exist
   downstream).
8. **engagement-status** (custom) — The recurring PMO chore: weekly status
   report, RAID log, action tracker, decision log — updated incrementally from
   `meeting-minutes` output rather than rebuilt each Friday. Highest
   *frequency* payoff of anything on this list.
9. **data-eda** (custom) — Exploratory analysis of raw CSV/parquet/database
   extracts: profiling, outliers, joins, reconciliation, cleaning — the messy
   step *before* `excel-to-evidence` and `render-tufte-chart` can run. Python
   stdlib + pandas.
10. **survey-analysis** (custom) — Quantitative companion to `ey-synthesis`
    (which is qual-only): crosstabs, significance testing, NPS/Likert
    handling, verbatim coding, chart-ready outputs via the Tufte skills.

### Tier 3 — high leverage, lower frequency

11. **executive-one-pager** (custom) — Distill any deliverable into a
    Minto/pyramid-principle one-page summary (the "read this in the elevator"
    artifact). Deck storylining exists in `ey-deck`; this generalizes it to
    memos, emails, and covers.
12. **quals-library** (custom) — Capture finished engagements as reusable,
    scrubbed case studies/credentials with metadata (sector, offering,
    outcomes); `rfp-proposal-response` queries it. Compounds in value with
    every engagement — start it early.
13. **systematic-debugging** (import — obra/superpowers, MIT) — Disciplined
    root-cause methodology (reproduce → isolate → hypothesize → verify). The
    repo has `bug-hunt` for *finding* bugs but no methodology for *fixing*
    them; this is the most battle-tested community skill in that niche.
14. **canvas-design** (import — anthropics/skills) — Designed visual
    one-pagers/posters as standalone artifacts. Pairs with
    `executive-one-pager` for leave-behinds and workshop walls; vet and
    restyle via `ey-brand-kit` tokens.
15. **deck-orchestrator** (custom) — Router for the slide-skill cluster
    (`ey-deck` vs `pptx` vs `marp-slide` vs `frontend-slides` +
    `theme-factory`), mirroring what `orchestrate-tufte-vdqi` does for charts.
    Doubles as the fix for issue #5 above — one skill that decides by output
    format, audience, and whether a client kit is active.

### Deliberately not recommended

- More dev-stack skills (Docker/Terraform/deploy): no signal in the repo that
  infra is a bottleneck.
- A memory/continuity skill: `session-handoff` + `theorist` already cover it;
  fix theorist's activation model instead (issue #11).
- More writing skills: `writing-clearly-and-concisely` + `humanizer` +
  `ux-copy` + `doc-coauthoring` is already a complete stack.
