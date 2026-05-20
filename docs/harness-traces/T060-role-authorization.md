# Harness Trace: T060 Role-Based Authorization

## Task
T060 [US5] Harness trace task: write failing role-based authorization API tests in `backend/tests/api/test_role_authorization.py`

## Phase / User Story
Phase 7 — User Story 5: Enforce Admin and End-User Roles (P3)

## Brainstorm
1. Write tests that hit every admin route as end user → expect 403
2. Write tests for unauthenticated access → expect 401
3. Write tests for `GET /me` as admin and end user → expect 200 with role in response (fails before /me exists)
4. Write tests for invalid role header → expect 403

Selected approach: comprehensive test file covering all four scenarios; fails on /me before T063 is implemented.

## Selected Approach
Single focused test file. Tests are grouped by scenario: unauthenticated, end-user-forbidden, admin-allowed, end-user-allowed. /me tests provide the failing anchor for T063.

## Plan
- File: `backend/tests/api/test_role_authorization.py`
- Implementation follows in T063 (`/me`) and T064/T065 (frontend)
- Verification: `pytest tests/api/test_role_authorization.py`

## Test Plan
1. Unauthenticated → 401 on admin routes, /me, and chat
2. End user → 403 on all /admin/* routes
3. Admin → 200 on /admin/faq-sources and /me
4. End user → 200 on /me and /chat/questions
5. Invalid role header → 403

## Failing Test Evidence
Before T063:
```
FAILED test_unauthenticated_cannot_access_me – assert 404 == 401
FAILED test_admin_can_access_me_endpoint – assert 404 == 200
FAILED test_end_user_can_access_me_endpoint – assert 404 == 200
```
Failure reason: `/me` route not registered; returns 404.

## Implementation Summary
T063 created `backend/app/api/me.py` with `GET /me` and `CurrentUserResponse` schema in `backend/app/schemas/me.py`. Registered `me_router` in `create_app()` in `main.py`.

## Verification Commands
```bash
cd backend
pytest tests/api/test_role_authorization.py -v --no-cov
# 18 passed
pytest tests/api/ -q --no-cov
# 32 passed
```

## Final Result
All 18 role-authorization tests pass. All 32 backend API tests pass. No regressions.

## AI Mistake or Risk Found
None — auth dependencies were already applied to all admin routes from T028.

## Human Correction or Judgment
None.

## Files Changed
- `backend/tests/api/test_role_authorization.py` (new — T060)
- `backend/app/api/me.py` (new — T063)
- `backend/app/schemas/me.py` (new — T063)
- `backend/app/main.py` (updated — T063)

## Suggested Commit Message
`Add role-based authorization tests and /me endpoint (T060–T065)`
