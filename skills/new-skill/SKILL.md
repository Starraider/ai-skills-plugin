---
name: new-skill
description: Use when creating, consolidating, improving, validating, or packaging an agent skill for Claude Code, Codex, Cursor, Antigravity, OpenCode, or Qoder. Covers portable SKILL.md authoring, bundled and standalone documentation, progressive disclosure, scripts, templates, and evaluation.
---

# New Skill

Create predictable skills: the same sound process on every run, with outputs adapted to the task.

## 1. Establish the contract

Extract known requirements from the conversation and repository before asking questions. Resolve the outcome, trigger boundary, inputs, outputs, side effects, target clients, dependencies, and objective success checks.

For a revision, preserve the existing name unless the user requests a migration. Read every applicable repository instruction file before editing.

Completion: a testable contract exists, and only materially ambiguous choices remain open.

## 2. Select the compatibility profile

Read [client compatibility](references/client-compatibility.md) whenever a target client is named. Default to the portable Agent Skills core: `name` and `description`, Markdown instructions, and optional `license`, `compatibility`, `metadata`, `scripts/`, `references/`, and `assets/`.

Add client extensions only when they provide required behavior. Keep client configuration outside `SKILL.md` when that client expects it elsewhere.

Completion: every selected client has a discovery path, valid metadata, and no contradictory extension.

## 3. Design the information hierarchy

Read the [authoring guide](references/authoring-guide.md). Choose one precise capability boundary. Put common ordered steps in `SKILL.md`; give each consequential step a checkable completion criterion. Move branch-specific details behind direct context pointers.

Use `scripts/` for repeated deterministic work, `references/` for on-demand knowledge, and `templates/` for files copied into outputs. Give a standalone Skill its own `README.md`; document a bundled Skill in the owning Agent Plugin's root README unless it needs an independent human surface. Do not create empty support directories.

Completion: every file has one responsibility and every support file is directly discoverable from `SKILL.md`.

## 4. Implement safely

Use the [scaffolder](scripts/scaffold-skill.sh), [SKILL template](templates/SKILL.md.template), [README template](templates/README.md.template), or [eval template](templates/evals.json.template) as a starting point. Resolve symlinks and edit the source directory, never a client-managed installed copy or cache. State required permissions, dependencies, destructive effects, and external writes. Prefer non-interactive, self-contained scripts with `--help`, actionable errors, structured output, and pinned dependencies where practical.

Completion: the skill can be followed from a clean session without hidden assumptions.

## 5. Validate and evaluate

Run:

```bash
scripts/validate-skill.sh path/to/skill --clients claude,codex,cursor,antigravity,opencode,qoder
```

For a Skill documented by its containing Agent Plugin, add `--documentation-profile bundled`. Then follow [evaluation and iteration](references/evaluation.md). Test representative, edge-case, and near-miss prompts. Compare against a no-skill or previous-version baseline when the environment supports isolated runs.

Completion: structural checks pass, links resolve, target clients can discover the skill, and evidence supports the claimed improvement.

## 6. Package and close out

For standalone distribution, read [repository and distribution guidance](references/repository-distribution.md) and use the [packager](scripts/package-skill.py) when a `.skill` archive is needed. Prune duplication, stale material, no-op instructions, and unsupported claims. Update owning documentation and report validation plus any intentional exceptions.

Completion: source, documentation, package contents, and release metadata agree.
