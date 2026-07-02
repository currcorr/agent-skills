# QA Process Workflow & Best Practices

End-to-end QA phase checklists and do/don't guidance for test case writing,
bug reporting, and regression testing.

---

## QA Process Workflow

### Phase 1: Planning
- [ ] Review requirements and designs
- [ ] Create test plan
- [ ] Identify test scenarios
- [ ] Estimate effort and timeline
- [ ] Set up test environment

### Phase 2: Test Design
- [ ] Write test cases
- [ ] Review test cases with team
- [ ] Prepare test data
- [ ] Build regression suite
- [ ] Get Figma design access

### Phase 3: Execution
- [ ] Execute test cases
- [ ] Log bugs with clear steps
- [ ] Validate against Figma (UI tests)
- [ ] Track test progress
- [ ] Communicate blockers

### Phase 4: Reporting
- [ ] Compile test results
- [ ] Analyze coverage
- [ ] Document risks
- [ ] Provide go/no-go recommendation
- [ ] Archive test artifacts

---

## Best Practices

### Test Case Writing

**DO:**
- Be specific and unambiguous
- Include expected results for each step
- Test one thing per test case
- Use consistent naming conventions
- Keep test cases maintainable

**DON'T:**
- Assume knowledge
- Make test cases too long
- Skip preconditions
- Forget edge cases
- Leave expected results vague

### Bug Reporting

**DO:**
- Provide clear reproduction steps
- Include screenshots/videos
- Specify exact environment details
- Describe impact on users
- Link to Figma for UI bugs

**DON'T:**
- Report without reproduction steps
- Use vague descriptions
- Skip environment details
- Forget to assign priority
- Duplicate existing bugs

### Regression Testing

**DO:**
- Automate repetitive tests when possible
- Maintain regression suite regularly
- Prioritize critical paths
- Run smoke tests frequently
- Update suite after each release

**DON'T:**
- Skip regression before releases
- Let suite become outdated
- Test everything every time
- Ignore failed regression tests
