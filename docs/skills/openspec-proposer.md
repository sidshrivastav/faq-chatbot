# openspec-proposer Skill

## Purpose

Create proposal artifacts for a Stage 6 change before implementation.

## When to Use

Use when the user says:

- Propose change `<change-id>`
- Create OpenSpec proposal for `<change-id>`
- Start Stage 6 change `<change-id>`
- Prepare change case `<change-id>`

## Inputs

- Change ID
- Change type: add feature, modify feature, or remove feature
- Current behavior
- Proposed behavior
- Rationale
- Related completed user story or feature
- Known constraints

## Required Context Reads

Before creating proposal artifacts, read:

- `specs/001-faq-knowledge-assistant/spec.md`
- `specs/001-faq-knowledge-assistant/plan.md`
- `specs/001-faq-knowledge-assistant/tasks.md`
- `docs/architecture.md`
- Relevant backend/frontend files only if needed to understand existing behavior

## Required Output Folder

Create:

```text
openspec/changes/<change-id>/
```

## Required Files

Create exactly these files during propose:

- `proposal.md`
- `spec-diff.md`
- `tasks.md`
- `impact-analysis.md`

Do not create `archive.md` during propose.
Do not implement application code during propose.

## proposal.md Requirements

Include:

- Change ID
- Change type
- Problem statement
- Current behavior
- Proposed behavior
- User impact
- Business/product value
- Acceptance criteria
- Out of scope
- Rollback plan

## spec-diff.md Requirements

Include:

- Existing requirement or behavior
- Modified/new requirement
- New acceptance criteria
- Deprecated or removed behavior, if any
- Compatibility notes

## tasks.md Requirements

Include:

- Test tasks
- Backend tasks
- Frontend tasks if applicable
- Documentation tasks
- Verification commands
- Completion checklist

Use `TC` prefix (Task Change) to distinguish from main task IDs (e.g., `TC01`, `TC02`).

## impact-analysis.md Requirements

Include:

- Backend impact
- Frontend impact
- Data/model impact
- API impact
- Test impact
- Security impact
- Performance impact
- Observability impact
- Rollback impact

## Scope Rules

- Do not implement code.
- Do not modify production files.
- Do not update tests.
- Do not archive the change.
- Keep the proposal scoped to the change ID.
- If the requested change depends on unfinished work, call that out clearly.

## Suggested Commit Message

Suggest:

```text
change:<change-id> document change case
```

## Example: add-feedback-reasons

Input:

```text
change-id: add-feedback-reasons
type: add feature
behavior: add optional structured reason when user marks answer unhelpful
```

Expected output:

```text
openspec/changes/add-feedback-reasons/proposal.md
openspec/changes/add-feedback-reasons/spec-diff.md
openspec/changes/add-feedback-reasons/tasks.md
openspec/changes/add-feedback-reasons/impact-analysis.md
```

## Example: modify-active-source-deletion-policy

Input:

```text
change-id: modify-active-source-deletion-policy
type: modify existing behavior
current behavior: admins can delete active FAQ sources
new behavior: active FAQ sources must be deactivated or archived before deletion
```

Expected output:

```text
openspec/changes/modify-active-source-deletion-policy/proposal.md
openspec/changes/modify-active-source-deletion-policy/spec-diff.md
openspec/changes/modify-active-source-deletion-policy/tasks.md
openspec/changes/modify-active-source-deletion-policy/impact-analysis.md
```
