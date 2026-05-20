# task-runner Skill

## Purpose

The `task-runner` skill executes one task ID or a task range from `specs/001-faq-knowledge-assistant/tasks.md` while keeping scope tight, preserving the required harness workflow, and stopping after the requested work is complete.

## When to Use

Use this skill when the user says:

- `Implement T001`
- `Implement T001-T008`
- `Continue with T009-T020`
- `Run next task`
- `Complete Phase 1 setup`
- `Complete the next task range`

## Inputs

Provide:

- Task ID, for example `T001`
- Task range, for example `T001-T008`
- Optional phase name
- Optional stop condition
- Optional verification command override

## Input Parsing Rules

- If the input is a single task ID, implement only that task.
- If the input is a range, implement tasks sequentially in ascending order.
- Do not skip tasks inside the requested range unless the task is already complete.
- Before starting each task, locate the exact task description in `specs/001-faq-knowledge-assistant/tasks.md`.
- If a task cannot be found, stop and report the issue.
- If the requested range crosses phase boundaries, warn the user and ask for confirmation unless explicitly told to continue.
- Stop after the requested task or range is complete.
- Do not continue to the next unrequested task.

## Required Context Reads

Before executing any task, read:

- `AGENTS.md`
- `docs/skills/test-writer.md`
- `specs/001-faq-knowledge-assistant/tasks.md`
- Related sections of `specs/001-faq-knowledge-assistant/spec.md`
- Related sections of `specs/001-faq-knowledge-assistant/plan.md`
- `docs/architecture.md` when architecture or module boundaries are relevant
- `specs/001-faq-knowledge-assistant/contracts/openapi.yaml` when implementing or testing API behavior

## Execution Workflow

For every task:

1. Identify Task
   - Extract task ID, title, phase, story label, estimate, and test scenario.
   - Identify dependencies listed in the task file.
   - Confirm whether the task is setup, test, implementation, frontend, backend, documentation, or polish.
2. Scope Guard
   - List what is included.
   - List what is explicitly excluded.
   - Do not implement unrelated future tasks.
   - Do not create speculative features.
3. Brainstorm
   - Identify 2-3 possible approaches.
   - Identify likely risks.
   - Select the simplest approach that satisfies the task.
4. Plan
   - List files to create or modify.
   - List tests or verification commands.
   - List expected result.
5. Test or Verification Plan
   - Use `docs/skills/test-writer.md` for test-related tasks.
   - If this is a test task, write failing tests only.
   - If this is an implementation task, first review or run the related failing tests.
   - If this is a setup or documentation task, use the verification command listed in the task instead of inventing unnecessary tests.
6. Implement
   - Implement only the minimum code or docs required for the current task.
   - Keep business logic outside FastAPI route handlers.
   - Preserve grounded-answer rules.
   - Do not call real LLM APIs in automated tests.
   - Mock external services.
7. Verify
   - Run the task-specific verification command.
   - If verification fails, fix only issues related to the current task.
   - Record command and result.
8. Trace
   - Add a short entry to `docs/harness-traces/task-log.md` for every task.
   - For representative harness tasks, create a detailed trace file:
     - `T022`: `docs/harness-traces/T022-faq-source-activation.md`
     - `T032`: `docs/harness-traces/T032-grounded-chat-mocked-llm.md`
     - `T060`: `docs/harness-traces/T060-role-authorization.md`
9. Summary
   - Summarize completed task ID.
   - List files changed.
   - List verification commands run.
   - List result.
   - Suggest a concise commit message.
   - Stop unless the user requested a range.

## Representative Harness Trace Format

For `T022`, `T032`, and `T060`, the detailed trace must include:

```text
# Harness Trace: <TASK-ID> <TASK-TITLE>

## Task
## Phase / User Story
## Brainstorm
## Selected Approach
## Plan
## Test Plan
## Failing Test Evidence
## Implementation Summary
## Verification Commands
## Final Result
## AI Mistake or Risk Found
## Human Correction or Judgment
## Files Changed
## Suggested Commit Message
```

## Range Execution Rules

When executing a range such as `T001-T008`:

- Execute tasks one by one.
- Complete verification for each task before starting the next.
- Add trace-log entry for each task.
- Stop the range if a task fails verification.
- Do not silently continue after failure.
- At the end, provide a range summary with:
  - completed tasks
  - skipped tasks, if any
  - failed task, if any
  - verification commands
  - files changed
  - suggested commit message

## Safety and Quality Rules

- Never call real LLM APIs in tests.
- Never commit secrets.
- Do not log sensitive question/answer content unnecessarily.
- Preserve role-based access rules.
- Preserve grounded-answer rules.
- Admin routes must require admin role.
- End-user routes must reject admin-only actions.
- Unsupported questions must not generate fabricated answers.
- If no relevant FAQ source exists, return safe fallback and record unanswered question.
- Keep imports consistent with backend package path: `from app.*` when running inside `backend/`.

## Example Invocation: Single Task

User says:

```text
Implement T001
```

Expected behavior:

- Locate `T001` in `tasks.md`.
- Implement only backend skeleton files.
- Run `python -m compileall backend/app`.
- Write `docs/harness-traces/T001-backend-skeleton.md` or add a task-log entry.
- Stop and suggest a commit message.

## Example Invocation: Task Range

User says:

```text
Implement T001-T008
```

Expected behavior:

- Execute `T001`, then `T002`, then `T003`, through `T008`.
- Verify each task before continuing.
- Stop if any task fails.
- Summarize the range.
- Do not start `T009`.

## Example Invocation: Harness Trace Task

User says:

```text
Implement T032
```

Expected behavior:

- Create detailed trace at `docs/harness-traces/T032-grounded-chat-mocked-llm.md`.
- Write failing service tests for deterministic retrieval and mocked LLM boundary.
- Verify tests fail for the expected missing-implementation reason.
- Do not implement `retrieval_service` or `answer_service` unless the requested task includes implementation.
