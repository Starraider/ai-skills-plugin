---
name: new-skill
description: Use when creating, improving, validating, or packaging an Agent Skill. Covers standards-compliant SKILL.md authoring, bundled and standalone documentation, progressive disclosure, scripts, templates, and evaluation.
license: CC-BY-4.0
---

# New Skill

Create predictable skills: the same sound process on every run, with outputs adapted to the task.

## 1. Establish the contract

Read the mandatory [Agent Skills specification](references/specification.md) for every creation or material revision. The current specification is authoritative; client conventions and repository preferences may extend it but never contradict it.

Extract known requirements from the conversation, real task evidence, and repository before asking questions. Resolve the outcome, trigger boundary, near misses, inputs, outputs, side effects, target clients, dependencies, and objective success checks. Preserve the user's chosen tools, scope, and authorization boundaries.

For a revision, preserve the existing name unless the user requests a migration. Read every applicable repository instruction file before editing.

Completion: a testable contract exists, the normative specification has been checked, and only materially ambiguous choices remain open.

## 2. Select the compatibility profile

Read [client compatibility](references/client-compatibility.md) whenever a target client is named. Default to the portable Agent Skills core and add client extensions only when they provide required behavior.

Keep automatic discovery unless the user explicitly requests manual-only invocation or a target environment requires another policy. Invocation policy does not authorize side effects: require permission at the actual mutation boundary. Keep client configuration outside `SKILL.md` when that client expects it elsewhere.

Completion: every selected client has a discovery path, valid metadata, and no contradictory extension.

## 3. Design the information hierarchy

Read the [authoring guide](references/authoring-guide.md). Choose one precise capability boundary. Put common ordered steps in `SKILL.md`; give each consequential step a checkable completion criterion. Move branch-specific details behind direct context pointers.

Assume the agent is capable: retain only non-obvious knowledge, real constraints, useful defaults, and instructions that change behavior. Match specificity to fragility. Use `scripts/` for repeated deterministic work, `references/` for on-demand knowledge, and `templates/` or `assets/` for files copied into outputs. Give every Skill its own detailed `README.md`. An owning Agent Plugin README retains plugin-wide guidance and a concise linked summary of each Skill; it does not duplicate detailed Skill documentation. Do not create empty support directories.

Completion: every file has one responsibility and every support file is directly discoverable from `SKILL.md`.

## 4. Implement safely

Use the [scaffolder](scripts/scaffold-skill.sh), [SKILL template](templates/SKILL.md.template), [README template](templates/README.md.template), or [eval template](templates/evals.json.template) as a starting point. Resolve symlinks and edit the source directory, never a client-managed installed copy or cache. State required permissions, dependencies, destructive effects, and external writes. Prefer non-interactive, self-contained scripts with `--help`, actionable errors, structured output, and pinned dependencies where practical.

Completion: the skill can be followed from a clean session without hidden assumptions.

## 5. Validate and evaluate

Run:

```bash
scripts/validate-skill.sh path/to/skill --strict-portable
skills-ref validate path/to/skill
```

Use the current `skills-ref` validator when available, then follow [evaluation and iteration](references/evaluation.md). Test representative, edge-case, and near-miss prompts. Compare against a no-skill or previous-version baseline when the environment supports isolated runs.

Completion: structural checks pass, links resolve, target clients can discover the skill, and evidence supports the claimed improvement.

## 6. Package and close out

For standalone distribution, read [repository and distribution guidance](references/repository-distribution.md) and use the [packager](scripts/package-skill.py) when a `.skill` archive is needed. Prune duplication, stale material, no-op instructions, and unsupported claims. Update owning documentation and report validation plus any intentional exceptions.

Completion: source, documentation, package contents, and release metadata agree.
