# Test Execution Tracking

Templates for tracking test runs, results, and requirement coverage.

---

## Test Run Report Template

```markdown
# Test Run: [Release Version]

**Date:** 2024-01-15
**Build:** v2.5.0-rc1
**Tester:** [Name]
**Environment:** Staging

## Summary
- Total Test Cases: 150
- Executed: 145
- Passed: 130
- Failed: 10
- Blocked: 5
- Not Run: 5
- Pass Rate: 90%

## Test Cases by Priority

| Priority | Total | Pass | Fail | Blocked |
|----------|-------|------|------|---------|
| P0 (Critical) | 25 | 23 | 2 | 0 |
| P1 (High) | 50 | 45 | 3 | 2 |
| P2 (Medium) | 50 | 45 | 3 | 2 |
| P3 (Low) | 25 | 17 | 2 | 1 |

## Critical Failures
- TC-045: Payment processing fails
  - Bug: BUG-234
  - Status: Open

## Blocked Tests
- TC-112: Dashboard widget (API endpoint down)

## Risks
- 2 critical bugs blocking release
- Payment integration needs attention

## Next Steps
- Retest after BUG-234 fix
- Complete remaining 5 test cases
- Run full regression before sign-off
```

---

## Coverage Tracking

```markdown
## Coverage Matrix

| Feature | Requirements | Test Cases | Status | Gaps |
|---------|--------------|------------|--------|------|
| Login | 8 | 12 | Complete | None |
| Checkout | 15 | 10 | Partial | Payment errors |
| Dashboard | 12 | 15 | Complete | None |
```

---

For regression-specific execution reports (suite-level summaries, go/no-go
recommendations), see [regression_testing.md](regression_testing.md).
