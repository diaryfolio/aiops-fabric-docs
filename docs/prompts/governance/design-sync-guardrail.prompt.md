# Design Sync Guardrail Prompt

Use this prompt before making code changes in `aiops-fabric`.

---

You are operating in `aiops-fabric`.

All documentation is owned by `aiops-fabric-docs`. Paths beginning with `docs/`
below are relative to that repository. Keep the sibling docs checkout available;
create or update documentation there and coordinate the two repositories' changes.
Do not add architecture, module READMEs, guides, prompts, or screenshots to the
implementation repository.

Your first responsibility is to keep implementation and architecture design in sync.

The repository owner performs Git staging, commits and pushes manually. Do not stage, commit,
amend commits or push through Git or equivalent tools/APIs. Leave edits unstaged and uncommitted.
Do not infer Git-write permission from an implementation/documentation request or ask to commit/
push as a routine completion step. Paired-commit rules require a coordinated handoff with changed
files, validation and available baseline references; do not create placeholder commits. Pending
manual commits alone do not make synchronized working-tree changes fail design sync.

## Mandatory Workflow

1. Classify the requested change as `minor` or `major` using `docs/prompts/governance/major-change-policy.md`.
2. Update `docs/design/high-level/00-implementation-conformance.md` when routes, runtime edges, state owners, provider maturity, trust boundaries, or verification paths change.
3. If `major`, update relevant docs in `aiops-fabric-docs/docs/design/high-level/`
   as part of the same coordinated change and prepare the owner's manual paired-commit/PR handoff.
4. Provide a `Design Impact Summary` that maps code changes to design sections.
5. Refuse to mark the task complete if major code changes are done without design updates.

## Hard Rules

- Never merge major implementation changes without matching updates to high-level design docs.
- If architecture assumptions changed, update the affected `design_0x.md` files and document rationale.
- If unsure whether a change is major, treat it as major.

## Required Output Block

Return this block at the end of your work:

```text
Design Sync Report
- Change Classification: <minor|major>
- Design Docs Updated: <list>
- Code Areas Updated: <list>
- Architecture Delta: <summary>
- Tests/Evidence: <list>
- Known Production Gaps: <list or none>
- Sync Status: <PASS|FAIL>
```

If `Sync Status` is `FAIL`, include exactly what is missing.

---

Do not bypass these rules.
