# openspec-applier Skill

## Purpose

Apply a proposed Stage 6 change using TDD while keeping implementation scoped to the change ID.

## When to Use

Use when the user says:

- Apply change `<change-id>`
- Implement proposed change `<change-id>`
- Apply OpenSpec change `<change-id>`

## Inputs

- Change ID
- Optional verification commands
- Optional implementation constraints

## Required Context Reads

Before applying a change, read:

- `openspec/changes/<change-id>/proposal.md`
- `openspec/changes/<change-id>/spec-diff.md`
- `openspec/changes/<change-id>/tasks.md`
- `openspec/changes/<change-id>/impact-analysis.md`
- `AGENTS.md`
- `docs/skills/test-writer.md`
- Relevant spec/plan/task files
- Relevant backend/frontend files

## Preconditions

Before implementation, verify:

- `proposal.md` exists
- `spec-diff.md` exists
- `tasks.md` exists
- `impact-analysis.md` exists

If any are missing, stop and ask to run `openspec-proposer` first.

## Apply Workflow

For the change:

1. **Review Proposal**
   - Summarize proposed behavior.
   - Identify affected files.
   - Identify risks.

2. **Test Plan**
   - Use `docs/skills/test-writer.md`.
   - Identify backend tests.
   - Identify frontend tests if applicable.
   - Identify regression tests.

3. **Tests First**
   - Write or update failing tests first.
   - Verify they fail for expected reasons where practical.

4. **Implement**
   - Implement the minimum scoped code.
   - Do not implement unrelated features.
   - Keep business logic outside FastAPI route handlers.
   - Preserve role-based access.
   - Preserve grounded-answer behavior.
   - Do not call real LLM APIs in automated tests.

5. **Verify**
   - Run relevant backend tests.
   - Run relevant frontend tests if touched.
   - Run build if frontend changed.
   - Record commands and results.

6. **Trace**
   - Update `docs/harness-traces/task-log.md` with a Stage 6 apply note.
   - Include change ID, tests run, result, files changed, and risks.

## Scope Rules

- Do not create proposal artifacts here; they must already exist.
- Do not archive here unless user explicitly asks.
- Do not modify unrelated Stage 5 tasks.
- Do not combine multiple changes.
- Keep all implementation traceable to the change ID.

## Suggested Commit Messages

Suggest:

```text
change:<change-id> add tests
change:<change-id> implement behavior
```

## Example: add-feedback-reasons

Apply behavior:

- Feedback payload supports optional reason when rating is unhelpful.
- Reason is validated.
- Helpful feedback still works without reason.
- Existing feedback behavior remains compatible.

## Example: modify-active-source-deletion-policy

Apply behavior:

- Deleting active FAQ source is rejected.
- Error uses shared error shape.
- Deleting inactive/archived/draft source still works if previously allowed.
- Admin-only route protection remains intact.
