# Cartha Live-Site QA Findings

**Report Date:** [TBD — will be updated when exploratory QA completes]

**Scope:** cartha.com live-site exploration — groups mode, navigation, auth flows, negative space, edge cases.

**Model:** Claude Opus (delegated subagent with deep reasoning for edge-case discovery)

---

## Executive Summary

[TBD — synthesized overview of key findings, severities, patterns]

---

## Findings by Category

### Groups Mode

[Findings related to joining groups, viewing messages, group interactions, leaving groups]

#### Finding: [Title]

**Severity:** Blocker / High / Medium / Low

**URL/Flow:**
- Start: [cartha.com/groups or specific group URL]
- Steps: [1. Click X, 2. Do Y, 3. See Z]

**Evidence:**
- Screenshot: `findings/screenshots/groups_[name].png`
- Error message: [if applicable]
- API response: [if applicable]

**Root Cause Hypothesis:**
[What do you think is broken?]

**Recommendation:**
[How to fix / investigate further]

**Status:** Open / In-Progress / Resolved

---

### Navigation (Left Rail)

[Findings related to Watch, Bible, Moments, Messages, Community sections]

#### Finding: [Title]

---

### Auth Flows

[Findings related to sign-in, OAuth cancel, invalid credentials, expired session, gated deep-links]

#### Finding: [Title]

---

### Negative Space & Dead-Ends

[Findings related to empty states, 404s, network drop mid-call, permission denials, back-button traps]

#### Finding: [Title]

---

### Edge Cases

[Findings related to double-submit, rapid navigation, stale tokens, deep-link to gated content while logged out]

#### Finding: [Title]

---

## Summary Table

| Category | Severity | Count | Status |
|----------|----------|-------|--------|
| Groups | | | |
| Navigation | | | |
| Auth | | | |
| Negative Space | | | |
| Edge Cases | | | |
| **Total** | | | |

---

## Recommendations

### High-Priority Fixes

[List of blockers/high-severity findings that should be fixed first]

### Medium-Priority Improvements

[Enhancements and medium-severity issues]

### Test Coverage Gaps

[Which of these findings should have tests written?]

---

## Next Steps

- [ ] Triage findings with product/engineering team
- [ ] Assign to sprint
- [ ] Add test cases to cartha-qa repo for each finding
- [ ] Iterate live-site QA in future sprints

---

## Appendix: Evidence Files

```
findings/
├── screenshots/
│   ├── groups_join_success.png
│   ├── groups_empty_messages.png
│   ├── auth_sign_in_invalid.png
│   ├── deep_link_404.png
│   └── [more screenshots]
├── logs/
│   ├── network_trace_[name].json
│   ├── error_log_[name].txt
│   └── [more logs]
└── report.md (this file)
```

