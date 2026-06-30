# Cartha QA Test Writing Roadmap

**Current Status:** 2 tests written  
**Phase 1 Target:** +5-8 tests (weeks 1-3)  
**Total Needed:** 20-25 tests

---

## 📊 Current vs. Needed

```
CURRENTLY WRITTEN:
  ✅ payment_result_cancel_test.dart (Widget)
  ✅ 201_party_join_invalid_code_dead_end.yaml (Maestro)

PHASE 1 NEEDED (Next 3 weeks):
  ⏳ test_plan_route_gated_shows_signin_modal (Integration)
  ⏳ test_meet_create_route_gated_shows_signin_modal (Integration)
  ⏳ test_invalid_route_shows_404_page (Integration)
  ⏳ test_group_invalid_code_shows_error_modal (Widget)
  ⏳ test_room_invalid_id_shows_error (Integration)
  ⏳ test_moment_invalid_id_shows_error (Integration)
  ⏳ test_clip_invalid_id_shows_error (Integration)
  ⏳ test_invalid_deep_links_maestro (Maestro)

PHASE 2 NEEDED (Weeks 4-5):
  ⏳ test_invalid_bible_book_shows_error (Widget)
  ⏳ test_invalid_watch_category_defaults_safely (Widget)
  ⏳ test_invalid_community_event_handled (Widget)
  ⏳ test_deep_link_valid_while_logged_out (Integration)
  ⏳ test_deep_link_after_session_expiry (Integration)
  ⏳ test_deep_link_invalid_code_maestro (Maestro)

PHASE 3 NEEDED (Week 6+):
  ⏳ test_rooms_browse_page_loads (Widget)
  ⏳ test_rooms_filtering_and_sorting (Widget)
  ⏳ test_rooms_join_from_browse (Maestro)
  ⏳ test_empty_state_messages (Widget)
  ⏳ test_empty_state_rooms (Widget)
  ⏳ test_empty_state_moments (Widget)
  ⏳ test_double_submit_prevention (Widget)
  ⏳ test_rapid_navigation_no_crash (Integration)
  ⏳ test_back_button_from_dead_ends (Maestro)
```

---

## 📅 Phase 1 Timeline (Next 3 Weeks)

### Week 1: Auth Gating + Invalid Routes

**Mon-Tue: Auth Gating Tests** (2 tests)
```
1. test_plan_route_gated_shows_signin_modal
   - Type: Integration test
   - Time: 1 day
   - Location: integration_test/auth/plan_route_gated_test.dart
   
2. test_meet_create_route_gated_shows_signin_modal
   - Type: Integration test
   - Time: 1 day
   - Location: integration_test/auth/meet_create_gated_test.dart
```

**Wed: Invalid Route 404 Handling** (1 test)
```
3. test_invalid_route_shows_404_page
   - Type: Integration test
   - Time: 1 day
   - Location: integration_test/routing/invalid_route_404_test.dart
```

**Thu-Fri: Review + Fixes**
```
- Test other developers' code
- Fix failures
- Document patterns
```

---

### Week 2: Resource Validation (Groups, Rooms, Moments, Clips)

**Mon-Tue: Group + Room Validation** (2 tests)
```
4. test_group_invalid_code_shows_error_modal
   - Type: Widget test
   - Time: 1 day
   - Location: test/groups/invalid_code_error_test.dart

5. test_room_invalid_id_shows_error
   - Type: Integration test
   - Time: 1 day
   - Location: integration_test/meet/invalid_room_test.dart
```

**Wed: Moments + Clips Validation** (2 tests)
```
6. test_moment_invalid_id_shows_error
   - Type: Integration test
   - Time: 1 day
   - Location: integration_test/moments/invalid_moment_test.dart

7. test_clip_invalid_id_shows_error
   - Type: Integration test
   - Time: 1 day
   - Location: integration_test/watch/invalid_clip_test.dart
```

**Thu-Fri: Maestro End-to-End**
```
8. test_invalid_deep_links_maestro
   - Type: Maestro flow
   - Time: 1 day
   - Location: test-cases/maestro/300_invalid_deep_links.yaml
```

---

### Week 3: Validation + Polish

**Mon-Tue: All tests passing locally**
```
- Run all 8 tests
- Fix failures
- Verify coverage reports
```

**Wed-Thu: Copy to upstream**
```
- Copy test files to cartha.ai.mobile/test/
- Create PR with evidence
- Get Zack's review
```

**Fri: Merge + celebrate Phase 1 complete**

---

## 🎯 Breakdown by Test Type

### Widget Tests (5 needed in Phase 1)
```
1. test_group_invalid_code_shows_error_modal
2. (Phase 2) test_invalid_bible_book_shows_error
3. (Phase 2) test_invalid_watch_category_defaults_safely
4. (Phase 2) test_invalid_community_event_handled
5. (Phase 3) test_rooms_browse_page_loads
```

**Why Widget?** 
- Fast execution (seconds)
- High isolation
- Easy to debug
- Good for: error states, UI rendering, unit logic

---

### Integration Tests (5 needed in Phase 1)
```
1. test_plan_route_gated_shows_signin_modal
2. test_meet_create_route_gated_shows_signin_modal
3. test_invalid_route_shows_404_page
4. test_room_invalid_id_shows_error
5. test_moment_invalid_id_shows_error
6. test_clip_invalid_id_shows_error
7. test_deep_link_valid_while_logged_out (Phase 2)
8. test_deep_link_after_session_expiry (Phase 2)
```

**Why Integration?**
- Test with API mocks
- Cross-feature validation
- Realistic routing scenarios
- Good for: auth gating, resource validation, deep-links

---

### Maestro Flows (2 needed in Phase 1)
```
1. 300_invalid_deep_links.yaml
   - Tests: /groups/INVALID, /moments/INVALID, /watch/clips/INVALID
   - Records: Video + screenshots
   - Validates: Error modals, recovery paths

2. (Phase 2) 301_deep_link_robustness.yaml
   - Tests: Valid deep-links while logged out, after auth, stale tokens
   - Records: Video + screenshots
```

**Why Maestro?**
- End-to-end user journeys
- Records video evidence
- Good for: navigation, deep-links, state transitions
- Slower but highest confidence

---

## 💾 File Organization

```
cartha-qa/
├── test/                                  # Widget tests
│   ├── groups/
│   │   └── invalid_code_error_test.dart (NEW)
│   ├── watch/
│   │   └── invalid_category_test.dart (Phase 2)
│   ├── bible/
│   │   └── invalid_book_test.dart (Phase 2)
│   └── community/
│       └── invalid_event_test.dart (Phase 2)
│
├── integration_test/                      # Integration tests
│   ├── auth/
│   │   ├── plan_route_gated_test.dart (NEW)
│   │   └── meet_create_gated_test.dart (NEW)
│   ├── routing/
│   │   └── invalid_route_404_test.dart (NEW)
│   ├── meet/
│   │   └── invalid_room_test.dart (NEW)
│   ├── moments/
│   │   └── invalid_moment_test.dart (NEW)
│   ├── watch/
│   │   └── invalid_clip_test.dart (NEW)
│   └── deep_links/
│       ├── valid_logged_out_test.dart (Phase 2)
│       └── stale_token_test.dart (Phase 2)
│
└── test-cases/maestro/                    # Maestro flows
    ├── 201_party_join_invalid_code_dead_end.yaml (DONE)
    ├── 300_invalid_deep_links.yaml (NEW)
    ├── 301_deep_link_robustness.yaml (Phase 2)
    └── 302_auth_gating_flows.yaml (Phase 2)
```

---

## 📋 Test Writing Checklist

For each test, ensure:

- [ ] **Clear test name** — describes what's being tested
- [ ] **Setup** — mock API, navigate to route
- [ ] **Action** — trigger the broken flow
- [ ] **Assertion** — verify error/correct behavior
- [ ] **Cleanup** — reset state for next test
- [ ] **Comments** — explain why this test matters
- [ ] **Reproducible** — can run locally: `flutter test`
- [ ] **Documented** — link to broken flow in TEST_STRATEGY.md
- [ ] **Evidence** — screenshot/video (for Maestro)

---

## 🚀 How to Assign Tests

### Option 1: Delegate to Sonnet (Coding Model)
```bash
delegate_task(
  goal="Write test_plan_route_gated_shows_signin_modal (integration test)",
  context="<TEST_STRATEGY.md details>"
)
```

### Option 2: Batch Assign (Parallel Writing)
```bash
delegate_task(
  tasks=[
    {goal: "Write test_plan_route_gated..."},
    {goal: "Write test_meet_create_route_gated..."},
    {goal: "Write test_invalid_route_404..."},
    {goal: "Write test_group_invalid_code..."},
  ]
)
```

### Option 3: Manual (You write them)
1. Review TEST_STRATEGY.md patterns
2. Copy template for test type
3. Implement assertions
4. Run locally: `flutter test`
5. Push to cartha-qa
6. Copy to upstream (cartha.ai.mobile) for PR

---

## ✅ Success Criteria

### Phase 1 Complete
- [ ] 8 tests written + passing
- [ ] All 3 HIGH-severity flows covered
- [ ] GitHub Actions shows green ✅
- [ ] Ready to copy to upstream
- [ ] Documentation updated

### Phase 2 Complete
- [ ] All MEDIUM-severity flows covered
- [ ] Deep-link robustness verified
- [ ] Parameter validation complete

### Phase 3 Complete
- [ ] Edge cases handled
- [ ] Empty states tested
- [ ] 20+ total tests in repo

---

## 🎓 Key Learning

**Why we started with 2 tests:**
- Proved patterns work (payment cancel ✅, deep-link invalid ✅)
- Established conventions (Widget + Maestro patterns)
- Built confidence before scaling

**Why we need 20+ tests:**
- 11 broken flows identified by comprehensive analysis (Opus)
- Each broken flow = 1-2 tests minimum
- Edge cases + verification = additional tests
- Total coverage = 20-25 tests across 3 phases

**Timeline Estimate:**
- Phase 1 (critical): 2-3 weeks (5-8 tests)
- Phase 2 (high): 1-2 weeks (4-6 tests)
- Phase 3 (nice): 1 week (6-8 tests)
- Total: 6-8 weeks for 20-25 tests

---

## 📞 Next Steps

1. **Review this roadmap** with Zack
   - Does Phase 1 order make sense?
   - Any tests missing?
   - Any priorities changing?

2. **Assign test writing**
   - Delegate to Sonnet (coding model), or
   - Manual writing, or
   - Batch parallel assignment

3. **Track progress**
   - GitHub issues for each test
   - Kanban board (in-progress, done, blocked)
   - Daily standup

4. **Validate as you go**
   - Run `flutter test` after each
   - Verify CI passes (GitHub Actions)
   - Copy to upstream weekly

---

**Status:** Roadmap complete, ready to assign tests.

**Current:** 2 tests ✅  
**Phase 1 Target:** +5-8 tests ⏳  
**Phase 2 Target:** +4-6 tests ⏳  
**Phase 3 Target:** +6-8 tests ⏳  
**Total:** 20-25 tests
