# openspec-archiver Skill

## Purpose

Create archive evidence for a completed Stage 6 change.

## When to Use

Use when the user says:

- Archive change `<change-id>`
- Complete archive for `<change-id>`
- Finalize OpenSpec change `<change-id>`

## Inputs

- Change ID
- Tests run
- Verification result
- Files changed
- Commit messages used or suggested
- Remaining risks, if any

## Required Context Reads

Before archiving, read:

- `openspec/changes/<change-id>/proposal.md`
- `openspec/changes/<change-id>/spec-diff.md`
- `openspec/changes/<change-id>/tasks.md`
- `openspec/changes/<change-id>/impact-analysis.md`
- `docs/harness-traces/task-log.md`
- Relevant test result notes if available

## Preconditions

Before archive, verify:

- `proposal.md` exists
- `spec-diff.md` exists
- `tasks.md` exists
- `impact-analysis.md` exists
- Implementation has been applied or clearly documented
- Verification commands were run or failures are explicitly documented

If preconditions are missing, stop and report what is missing.

## Required Output

Create:

```text
openspec/changes/<change-id>/archive.md
```

## archive.md Requirements

Include:

- Date archived
- Change ID
- Change type
- Summary of implemented behavior
- Proposal completed: yes/no
- Spec diff completed: yes/no
- Tasks completed: yes/no
- Impact analysis completed: yes/no
- Tests run
- Verification result
- Files changed
- Commit messages used or suggested
- Remaining risks
- Rollback note
- Final status

## Scope Rules

- Do not implement code.
- Do not change the proposal after archive unless explicitly asked.
- Do not archive unverified changes unless verification gap is clearly documented.
- Keep archive scoped to one change ID.

## Suggested Commit Message

Suggest:

```text
change:<change-id> archive completed change
```
