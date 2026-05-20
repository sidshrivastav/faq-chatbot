# qa-reviewer Skill

## Purpose

Perform structured QA review and produce auditable findings across performance, security, code quality, observability, test coverage, and documentation consistency.

## When to Use

Use during Stage 7 after implementation and change management are complete. Do not run on an in-progress branch with open tasks.

## Required Inputs

Read these before starting any review area:

- `specs/001-faq-knowledge-assistant/spec.md`
- `specs/001-faq-knowledge-assistant/plan.md`
- `specs/001-faq-knowledge-assistant/tasks.md`
- `AGENTS.md`
- `backend/`
- `frontend/`
- `docs/harness-traces/`
- `openspec/changes/`

## Review Areas

1. Performance
2. Security
3. Code quality
4. Observability
5. Test coverage
6. Documentation consistency

## Required Outputs

Produce one file per area plus a summary:

| File | Contents |
|---|---|
| `docs/performance.md` | Baseline metrics, bottleneck findings, optimization outcomes |
| `docs/security.md` | Security checklist results, risk ratings, accepted risks |
| `docs/code-review.md` | Code quality findings, pattern violations, maintainability notes |
| `docs/qa-summary.md` | Cross-area rollup, open items, final pass/fail per area |

## Review Method

For each review area:

1. Identify the checklist for that area (see checklists below).
2. Run or recommend commands. Record whether each was run or not.
3. Record each finding with: area, severity, file path or test name, description, evidence.
4. Mark each finding with one status:
   - `AI-found` — identified by AI review, not yet human-confirmed
   - `human-confirmed` — reviewed and confirmed by a human
   - `fixed` — addressed in code before or during this review
   - `accepted-risk` — known issue, accepted for documented reason
   - `follow-up` — deferred to a future change or stage
5. Do not make vague claims. Every finding must cite evidence: file path, line reference, test name, command output, or measured result.
6. Do not claim a test passed unless it was run in this session or explicitly marked as `not-run` with a reason.

---

## Security Checklist

- [ ] All admin-only routes require `require_admin` dependency
- [ ] All authenticated routes require `get_current_user` dependency
- [ ] Unauthenticated requests to protected routes → 401
- [ ] End-user requests to admin routes → 403
- [ ] Users cannot access other users' chat sessions or feedback
- [ ] Input validation: Pydantic schemas reject malformed requests
- [ ] No real secrets committed to code, tests, fixtures, or docs
- [ ] `.env.example` contains no real secret values
- [ ] Dependency vulnerabilities: run `pip-audit` or `safety check` and record results
- [ ] CORS configuration reviewed (origins, credentials, methods)
- [ ] OWASP API Security Top 10 — check applicable items:
  - API1: Broken Object Level Authorization
  - API2: Broken Authentication
  - API3: Broken Object Property Level Authorization
  - API5: Broken Function Level Authorization
  - API8: Security Misconfiguration
- [ ] Prompt injection risks: LLM receives only retrieved FAQ content, not raw user input
- [ ] LLM data leakage: answers must not expose non-FAQ content or system prompts
- [ ] Sensitive data not logged: user IDs, question text, and answer text must not appear in production-level log lines that could be captured in error-reporting tools

---

## Performance Checklist

- [ ] Baseline latency recorded for: chat answer endpoint, FAQ source list, feedback submission
- [ ] P50 / P95 / P99 latency captured or estimated (use `locust`, `hey`, or `ab`)
- [ ] Chat answer endpoint: identify whether bottleneck is retrieval, LLM call, or serialization
- [ ] FAQ source list endpoint: verify list is not unbounded (check for pagination or record-count cap)
- [ ] Feedback endpoint: confirm no synchronous side effects beyond record write
- [ ] Analytics endpoint (if implemented): confirm aggregation does not full-scan unbounded records
- [ ] Any optimization applied: record before/after metric side by side
- [ ] Unoptimized bottlenecks: document with severity and proposed fix

---

## Code Quality Checklist

- [ ] Route handlers are thin: no business logic, only auth dependency → service call → response
- [ ] Business logic lives in `backend/app/services/`
- [ ] Persistence access is isolated in `backend/app/repositories/`
- [ ] Domain enums and state helpers are in `backend/app/domain/`
- [ ] LLM access is isolated behind `backend/app/llm/`
- [ ] Pydantic v2 schemas used for all API request/response types
- [ ] No arbitrary `dict` accepted where a typed schema is possible
- [ ] Cross-field validation uses `model_validator`; domain-state validation stays in services
- [ ] Error messages are safe: no secrets, no stack traces exposed to callers
- [ ] Frontend API calls isolated in `frontend/src/services/`
- [ ] Frontend state: all active, invalid, helpful, unhelpful, loading, empty, and error states conveyed with text, not color alone
- [ ] No significant duplication: three or more identical code blocks should be extracted
- [ ] No unused imports, dead code, or orphaned files
- [ ] Commit history follows `change:<change-id> <summary>` format for Stage 6 changes

---

## Observability Checklist

- [ ] `GET /health` returns 200 with `{"status": "ok"}`
- [ ] Structured logs (not bare `print`) used throughout backend
- [ ] Request logs include: route, method, role or auth status
- [ ] Authorization failures are logged
- [ ] FAQ source lifecycle events logged: create, update, activate, deactivate, archive, delete
- [ ] Chat events logged: question received, retrieval result, LLM boundary called/skipped/failed, answer persisted with state
- [ ] Feedback submission logged with rating (not full comment text)
- [ ] Analytics and unanswered-question requests logged with filters
- [ ] Sensitive content not in logs: no full question/answer text at INFO level, no user tokens
- [ ] Metrics plan documented if no metrics instrumentation exists yet

---

## Test Coverage Checklist

- [ ] Run `pytest --cov=app --cov-report=term-missing` and record coverage percentage
- [ ] Coverage target ≥ 70% on backend `app/`
- [ ] Source management tests: create, list, update, detail, activate, deactivate, archive, delete
- [ ] Grounded chat tests: answered, unsupported, no-active-source, inactive-source exclusion
- [ ] Feedback tests: helpful, unhelpful, reason validation, duplicate feedback
- [ ] Role authorization tests: unauthenticated → 401, end_user on admin routes → 403, admin → 200
- [ ] Frontend tests cover: chat states, feedback states, admin nav, end-user nav
- [ ] No real LLM API called in any automated test
- [ ] All TDD-written tests have a harness trace or task log entry confirming they were written before implementation

---

## Documentation Consistency Checklist

- [ ] `AGENTS.md` reflects the actual implemented structure
- [ ] `specs/001-faq-knowledge-assistant/contracts/openapi.yaml` matches implemented routes and schemas
- [ ] `docs/harness-traces/task-log.md` has an entry for every implemented task
- [ ] OpenSpec change archives exist for every Stage 6 change that was applied
- [ ] `docs/harness-traces/` files do not contain secrets, real tokens, or sensitive user data
- [ ] Setup commands in `AGENTS.md` or quickstart docs match actual working commands

---

## Rules

- Do not make vague claims. Cite file path, test name, command output, or measured result for every finding.
- Do not claim a test passed unless it was run in this session or explicitly marked `not-run` with a reason.
- Do not call real LLM APIs.
- Prefer concrete file paths and command names over general statements.
- Separate `AI-found` issues from `human-confirmed` issues in all output files.
- Do not fix issues outside the review scope without recording the fix as a finding.

## Suggested Commit Message

```text
docs add Stage 7 QA review outputs
```
