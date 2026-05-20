# Retrospective: AI Application Engineer Assessment

## Context

This project built a Configurable FAQ Knowledge Assistant using a harness-driven Codex workflow instead of pure freeform AI chat. The implementation was anchored in `AGENTS.md`, Spec Kit-style artifacts under `specs/001-faq-knowledge-assistant/`, design docs under `docs/design/`, custom skills under `docs/skills/`, harness traces under `docs/harness-traces/`, OpenSpec changes under `openspec/changes/`, and Stage 7 QA outputs in `docs/performance.md`, `docs/security.md`, `docs/code-review.md`, and `docs/qa-summary.md`.

The key product constraint was not "build a chatbot"; it was "build a grounded FAQ assistant." That distinction shaped almost every good decision in the workflow: retrieval before generation, fake LLMs in tests, role checks on backend routes, and clear unsupported/no-active-source states.

## 1. Process

```text
AI helped most in Stages 6 and 7. Stage 6 change management made the required changes reviewable before coding through proposals, spec diffs, tasks, and impact analysis. Stage 7 gave me a structured overview of the application before submission, so I could manually verify performance, security, code quality, and observability findings.

Stage 4 also helped because custom skills reduced repeated prompting and made Codex work incrementally through test-writer and task-runner. Stages 1–3 were fast because AI turned the assignment into requirements, design, plan, and tasks quickly.

The stages that slowed me down were also Stages 1–4 at first. I tried to generate too much in one go and did not review each artifact deeply enough under time pressure. That created gaps in understanding. The biggest lesson was that AI speed is useful, but only if I pause between stages to review and correct the output.
```

## 2. Harness & Skills

```text
I used Codex as my primary implementation tool and Claude as a secondary planning/review tool. My usual workflow is to understand the requirement first, inspect the code, prepare a focused prompt with context and business rules, use planning to shape the approach, then implement incrementally and review the output.

For this assessment, I formalized that into a harness using Spec Kit, AGENTS.md, custom skills, TDD, OpenSpec change management, and QA review. Spec Kit helped turn the assignment into a spec, plan, and modular tasks, although it created more tasks than I would normally want to review under time pressure.

The custom skills reduced repeated prompting. test-writer handled test planning, task-runner handled incremental task execution, OpenSpec skills handled propose/apply/archive, and qa-reviewer handled systematic QA.

The implement phase gave me the most value because it let Codex complete scoped tasks quickly. The Stage 6 ceremony sometimes felt redundant for small changes, but it was useful for proving controlled change management.

```
## 3. AI Collaboration

```text
One “AI saved the day” moment was frontend debugging. I mostly work on backend, but when no frontend developer was available, I used Claude to reason through a tricky frontend issue and validate the data flow. It helped me work outside my strongest area without blindly applying a fix.

One “AI led me astray” moment was from an API contract issue on a previous project. A merge conflict corrupted the API contract, and the team kept asking an LLM to fix the resulting bug. The LLM added code around the symptoms, but the real issue was the corrupted spec. I found the contract problem, fixed it, and reversed unnecessary AI-generated code.

That taught me to treat AI like a junior developer: useful, but not unsupervised. I review the prompt, review the code, verify against the source of truth, and treat AI suggestions as hypotheses until tests, specs, or code confirm them.

```
## 4. Reflection

```text
If I did this again, I would not let AI process such a large requirement in one go. I would split the assignment into smaller requirement slices and run each slice through specify, design, plan, tasks, implementation, verification, and review before moving to the next one. I would also add a stronger review gate before implementation.

This workflow can scale to a team because specs, tasks, change records, and QA docs become development memory. They help the team understand what was built, why it was built, and how later changes connect to the original intent.

The next thing I would automate is a pre-implementation review gate and traceability checker. Before coding, it should verify that the task is clear, testable, scoped, and connected to the spec. After coding, it should verify links between requirements, tasks, tests, code, harness traces, and change records.
