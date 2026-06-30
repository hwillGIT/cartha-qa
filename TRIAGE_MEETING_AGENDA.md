# Cartha QA Triage Meeting — Bug Confirmation & Prioritization

**Date:** 2026-06-30  
**Participants:** Zack Seyun Kim (Product Owner), Hubert Williams (QA Lead)  
**Purpose:** Confirm bugs found by Opus, validate against intended design, prioritize fixes  
**Deliverable:** Confirmed bug list + priority ranking for Phase 1 test implementation

---

## Pre-Meeting Summary

Opus conducted comprehensive exploratory testing of cartha.com and **confirmed 8 bugs** (5 CRITICAL, 3 MEDIUM). All findings are documented in `docs/OPUS_EXPLORATORY_FINDINGS.md` with reproduction steps and evidence.

**We need to confirm:**
1. Which bugs are actual bugs vs. intended design
2. Which bugs are high-priority (Phase 1 fixes)
3. Which bugs can be deferred (Phase 2-3)
4. Any additional context on root causes

---

## Bug List for Triage

### 🔴 CRITICAL (5 Bugs)

#### BUG-003: `/plan` Route Gating Failure
- **What:** User navigates to `/plan` while logged out → redirects to external marketing page
- **Expected:** Should show signin modal within app
- **Evidence:** Route navigation test confirmed
- **Question for Zack:** Is this intended? Should it redirect or show signin modal?
- **Recommendation:** CRITICAL — blocks feature access, needs fix before Phase 1 tests
- **Fix Effort:** LOW (authentication middleware)

#### BUG-009: `/meet/create` Route Gating Failure
- **What:** User navigates to `/meet/create` while logged out → shows homepage instead of signin modal
- **Expected:** Should show signin modal (per spec)
- **Evidence:** Route navigation test confirmed
- **Question for Zack:** Same as BUG-003 — intended redirect or signin modal?
- **Recommendation:** CRITICAL — blocks feature access
- **Fix Effort:** LOW (authentication middleware)

#### BUG-001: Groups Invalid Code — Silent Fallback
- **What:** User tries to join group with invalid code → no error modal, silently returns to home
- **Expected:** Show "Group code not found" error modal (per spec)
- **Evidence:** Invalid code navigation → silent fallback with no feedback
- **Question for Zack:** Should we show error modal or let user discover wrong code?
- **Recommendation:** CRITICAL — users get zero feedback, breaks UX
- **Fix Effort:** MEDIUM (error modal + API error handling)

#### BUG-010: Watch — Invalid Clip ID Silent Fallback
- **What:** User navigates to `/watch/clips/INVALIDID` → no error modal, silently returns to feed
- **Expected:** Show "Clip not found" error modal (per spec)
- **Evidence:** Invalid clip ID navigation → silent fallback
- **Question for Zack:** Should we show error or just return to feed?
- **Recommendation:** CRITICAL — users get no feedback when link is broken
- **Fix Effort:** MEDIUM (error modal + validation)

#### BUG-006: Meet — Invalid Room ID Silent Return
- **What:** User navigates to `/meet/room/INVALIDID` → silently returns to Meet home with no error
- **Expected:** Show "Room not found" error modal (per spec)
- **Evidence:** Invalid room ID navigation → silent return to home
- **Question for Zack:** Should we show error or allow silent fallback?
- **Recommendation:** CRITICAL — users get no feedback when room doesn't exist
- **Fix Effort:** MEDIUM (error modal + validation)

---

### 🟡 MEDIUM (3 Bugs)

#### BUG-002: Invalid Routes — Redirect to Marketing Site
- **What:** User navigates to invalid route like `/invalid-page` → redirects to `og.cartha.com`
- **Expected:** Show in-app 404 page (per spec)
- **Evidence:** Invalid route navigation → external redirect
- **Question for Zack:** Is the external redirect intentional or should we have in-app 404?
- **Recommendation:** MEDIUM — UX issue (takes user out of app), but not feature-blocking
- **Fix Effort:** LOW (add catch-all 404 route)

#### BUG-008: Moments — Invalid ID Shows Generic Page
- **What:** User navigates to `/moments/INVALIDID` → shows generic "invited you" page, no validation
- **Expected:** Show "Moment not found" error or moment detail if valid
- **Evidence:** Invalid moment ID shows placeholder page
- **Question for Zack:** Should invalid moments show error or generic page?
- **Recommendation:** MEDIUM — confusing UX but doesn't completely block feature
- **Fix Effort:** MEDIUM (validation + error modal)

#### BUG-004: Bible — Invalid Book ID Silent Default
- **What:** User navigates to `/bible/invalidbook/1` → shows Bible home with loading spinner, no error
- **Expected:** Show error modal or valid message like "Book not found, showing Genesis"
- **Evidence:** Invalid book slug → silent fallback to home
- **Question for Zack:** Should we show error or default to Genesis with message?
- **Recommendation:** MEDIUM — confusing but Bible feature still works (just wrong book)
- **Fix Effort:** MEDIUM (validation + message)

---

### ✓ WORKING (3+ Features)

#### Working: Watch Navigation & Pagination
- Categories filter correctly
- Video feed loads properly
- Pagination works (ArrowDown, scroll)
- **Status:** ✓ No action needed

#### Working: Community/Groups Discovery
- Community page displays events and groups
- Tabs navigate correctly (For You, Calendar, Groups)
- Member counts display
- **Status:** ✓ No action needed

---

## Triage Questions for Zack

### Authentication & Gating (BUG-003, BUG-009)

1. **Should gated routes redirect or show signin modal?**
   - `/plan` and `/meet/create` currently redirect to marketing site / homepage
   - Spec says: show signin modal
   - Is this intended behavior or a bug?

2. **If they should show signin modal, should they:**
   - (a) Show modal within the app (inline)
   - (b) Navigate to `/signin` page with redirect URL
   - (c) Stay on same route and show overlay?

### Error Handling (BUG-001, BUG-010, BUG-006, BUG-008, BUG-004)

3. **Should invalid resource deep-links show error modals?**
   - Currently: Silent fallback to home/parent
   - Spec says: Show error modal "Resource not found"
   - User experience: Zero feedback why link didn't work
   - Is this intended or bug?

4. **Which is the priority for error handling?**
   - BUG-001 (Groups) — users actively trying to join, need feedback
   - BUB-010 (Watch) — users receiving shared links, need feedback
   - BUG-006 (Meet) — users receiving room links, need feedback
   - BUG-008 (Moments) — less critical?
   - BUG-004 (Bible) — least critical?

### Invalid Routes (BUG-002)

5. **For invalid routes like `/invalid-page`:**
   - Currently: Redirects to `og.cartha.com`
   - Spec says: Show in-app 404 page
   - Should we keep redirect (maybe for SEO reasons?) or fix to in-app 404?

---

## Proposed Phase 1 Test Plan

**Based on Opus findings, recommend Phase 1 focus (after triage):**

### Phase 1: Critical Auth & Error Handling (8 Tests)

1. ✅ `/plan` route gating (if bug confirmed) → test signin modal
2. ✅ `/meet/create` route gating (if bug confirmed) → test signin modal
3. ✅ Invalid group code → test error modal appears
4. ✅ Invalid clip ID → test error modal appears
5. ✅ Invalid room ID → test error modal appears
6. ✅ Invalid moments ID (if critical) → test error modal
7. ✅ Invalid Bible book (if critical) → test error message
8. ✅ Invalid route `/invalid-page` (if critical) → test 404 page

### Phase 2: Extended Error Handling & Validation (6 Tests)
- Parameter validation for all features
- Deep-link robustness (special characters, missing params)
- Permission denial handling
- Network error handling

### Phase 3: Edge Cases & Performance (8+ Tests)
- Rapid navigation between features
- Pagination stress (scroll to end of long lists)
- Special character handling (XSS prevention)
- Session expiry handling

---

## Next Steps

**During/After Triage Meeting:**

1. ✅ **Confirm** which bugs are actual bugs (not intended design)
2. ✅ **Prioritize** which Phase 1 (blockers), Phase 2 (important), Phase 3 (nice-to-have)
3. ✅ **Discuss** root causes and fix effort
4. ✅ **Decide** which bugs will be fixed vs. accepted
5. ✅ **Update** DEFECTS_AND_REQUIREMENTS.md with Zack's decisions

**After Triage:**

1. Assign confirmed bugs to Phase 1 test plan
2. Delegate test writing to Sonnet (parallel, 7 tests)
3. Write tests for confirmed bugs
4. Validate tests pass when bugs are fixed
5. Copy tests to cartha.ai.mobile upstream

---

## Summary Table for Meeting

| BUG-ID | Type | Title | Severity | Opus Status | Zack Decision | Phase 1? |
|--------|------|-------|----------|-------------|---------------|---------|
| BUG-003 | Auth | /plan route gating | 🔴 CRITICAL | ✓ CONFIRMED | ? TBD | ? |
| BUG-009 | Auth | /meet/create gating | 🔴 CRITICAL | ✓ CONFIRMED | ? TBD | ? |
| BUG-001 | Error | Groups invalid code | 🔴 CRITICAL | ✓ CONFIRMED | ? TBD | ? |
| BUB-010 | Error | Watch invalid clip | 🔴 CRITICAL | ✓ CONFIRMED | ? TBD | ? |
| BUG-006 | Error | Meet invalid room | 🔴 CRITICAL | ✓ CONFIRMED | ? TBD | ? |
| BUG-002 | Routing | Invalid route redirect | 🟡 MEDIUM | ✓ CONFIRMED | ? TBD | ? |
| BUG-008 | Error | Moments generic page | 🟡 MEDIUM | ✓ CONFIRMED | ? TBD | ? |
| BUG-004 | Error | Bible silent default | 🟡 MEDIUM | ✓ CONFIRMED | ? TBD | ? |

---

## Meeting Notes (To Be Filled In)

### Bugs Confirmed as Real Issues
- [ ] BUG-003 (yes / no / defer)
- [ ] BUG-009 (yes / no / defer)
- [ ] BUG-001 (yes / no / defer)
- [ ] BUB-010 (yes / no / defer)
- [ ] BUG-006 (yes / no / defer)
- [ ] BUG-002 (yes / no / defer)
- [ ] BUG-008 (yes / no / defer)
- [ ] BUG-004 (yes / no / defer)

### Phase 1 Priority (Blocking)
- [ ]
- [ ]
- [ ]
- [ ]

### Phase 2 Priority (Important but Not Blocking)
- [ ]
- [ ]
- [ ]
- [ ]

### Deferred / Lower Priority
- [ ]
- [ ]
- [ ]

### Additional Context / Root Causes
```
[Notes from Zack on technical background]
```

### Decisions Made
```
[Summary of outcomes]
```

---

**Document Status:** Ready for Triage Meeting  
**Next Step:** Schedule sync with Zack to discuss findings  
**Timeline:** After meeting → update DEFECTS_AND_REQUIREMENTS.md → write Phase 1 tests
