---
name: qa-test-planner
description: Generate comprehensive test plans, manual test cases, regression test suites, and bug reports for QA engineers. Includes Figma MCP integration for design validation.
metadata:
  trigger: explicit
---

# QA Test Planner

A comprehensive skill for QA engineers to create test plans, generate manual test cases, build regression test suites, validate designs against Figma, and document bugs effectively.

> **Activation:** This skill is triggered only when explicitly called by name (e.g., `/qa-test-planner`, `qa-test-planner`, or `use the skill qa-test-planner`).

---

## Quick Start

| Say | Example |
|-----|---------|
| Create a test plan | "Create a test plan for the user authentication feature" |
| Generate test cases | "Generate manual test cases for the checkout flow" |
| Build regression suite | "Build a regression test suite for the payment module" |
| Validate against Figma | "Compare the login page against the Figma design at [URL]" |
| Create bug report | "Create a bug report for the form validation issue" |

---

## Quick Reference

| Task | What You Get | Time |
|------|--------------|------|
| Test Plan | Strategy, scope, schedule, risks | 10-15 min |
| Test Cases | Step-by-step instructions, expected results | 5-10 min each |
| Regression Suite | Smoke tests, critical paths, execution order | 15-20 min |
| Figma Validation | Design-implementation comparison, discrepancy list | 10-15 min |
| Bug Report | Reproducible steps, environment, evidence | 5 min |

---

## How It Works

Every request follows a three-step workflow:

1. **ANALYZE** — Parse the feature/requirement, identify the test types needed, determine scope and priorities.
2. **GENERATE** — Create structured deliverables from the templates in `references/`, apply best practices, include edge cases and variations.
3. **VALIDATE** — Check completeness, verify traceability, ensure every step is actionable.

Before generating a deliverable, read the matching reference file (see [Reference Files](#reference-files)) and follow its template exactly.

---

## Commands

### Interactive Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `./scripts/generate_test_cases.sh` | Create test cases interactively | Step-by-step prompts |
| `./scripts/create_bug_report.sh` | Generate bug reports | Guided input collection |

### Natural Language

| Request | Output |
|---------|--------|
| "Create test plan for {feature}" | Complete test plan document |
| "Generate {N} test cases for {feature}" | Numbered test cases with steps |
| "Build smoke test suite" | Critical path tests |
| "Compare with Figma at {URL}" | Visual validation checklist |
| "Document bug: {description}" | Structured bug report |

---

## Core Deliverables

1. **Test Plans** — Scope/objectives, approach and strategy, environment requirements, entry/exit criteria, risk assessment, timeline and milestones.
2. **Manual Test Cases** — Step-by-step instructions, expected vs actual results, preconditions and setup, test data requirements, priority and severity.
3. **Regression Suites** — Smoke tests (15-30 min), full regression (2-4 hours), targeted regression (30-60 min), execution order and dependencies.
4. **Figma Validation** — Component-by-component comparison, spacing and typography checks, color and visual consistency, interactive state validation.
5. **Bug Reports** — Clear reproduction steps, environment details, evidence (screenshots, logs), severity and priority.

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Vague test steps | Can't reproduce | Specific actions + expected results |
| Missing preconditions | Tests fail unexpectedly | Document all setup requirements |
| No test data | Tester blocked | Provide sample data or generation |
| Generic bug titles | Hard to track | Specific: "[Feature] issue when [action]" |
| Skip edge cases | Miss critical bugs | Include boundary values, nulls |

---

## Verification Checklist

**Test Plan:**
- [ ] Scope clearly defined (in/out)
- [ ] Entry/exit criteria specified
- [ ] Risks identified with mitigations
- [ ] Timeline realistic

**Test Cases:**
- [ ] Each step has expected result
- [ ] Preconditions documented
- [ ] Test data available
- [ ] Priority assigned

**Bug Reports:**
- [ ] Reproducible steps
- [ ] Environment documented
- [ ] Screenshots/evidence attached
- [ ] Severity/priority set

---

## Reference Files

Read the relevant file before generating each deliverable — do not invent formats from scratch.

| File | Read when... |
|------|--------------|
| [test_plan_template.md](references/test_plan_template.md) | Creating a test plan — full document structure with scope, strategy, entry/exit criteria, and risk assessment. |
| [test_case_templates.md](references/test_case_templates.md) | Writing test cases — standard/minimal formats, per-type templates (functional, UI, integration, regression, security, performance), test types overview, naming conventions, and priority definitions. |
| [bug_report_templates.md](references/bug_report_templates.md) | Documenting a bug — standard/quick/UI/performance/security/crash templates, severity definitions, priority-vs-severity matrix, and title best practices. |
| [regression_testing.md](references/regression_testing.md) | Building or executing a regression suite — suite types and durations, critical-path selection, prioritization, execution order, and pass/fail criteria. |
| [figma_validation.md](references/figma_validation.md) | Validating implementation against Figma via MCP — full workflow, what to validate per element, example MCP queries, and discrepancy documentation. |
| [test_execution_tracking.md](references/test_execution_tracking.md) | Reporting on a test run — test run report template and requirements coverage matrix. |
| [qa_process.md](references/qa_process.md) | Planning end-to-end QA work — four-phase workflow checklists (planning, design, execution, reporting) and DO/DON'T best practices. |
| [worked_examples.md](references/worked_examples.md) | Unsure of the expected detail level — complete filled-in example test cases (login flow, responsive UI). |

---

**"Testing shows the presence, not the absence of bugs." - Edsger Dijkstra**

**"Quality is not an act, it is a habit." - Aristotle**
