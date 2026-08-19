# Authoring guide

Use this guide while designing or revising a skill. The objective is predictability: repeated runs should follow the same sound process even when their outputs differ.

## Capture intent before drafting

Ground the skill in real expertise. Mine the current conversation, successful task executions, existing files, runbooks, schemas, incident history, review comments, and user corrections before asking questions. Generic model knowledge alone usually produces no-op advice. Resolve:

- the capability and its exclusions
- realistic trigger and near-miss requests
- required inputs and context
- expected outputs and formats
- permissions, side effects, and destructive operations
- dependencies and supported clients
- objective checks and human judgment criteria

Ask only questions whose answers materially change the skill. For an existing skill, inspect its execution problems and preserve its name unless a deliberate migration is requested.

## Choose invocation deliberately

A model-invoked skill spends context on its description so an agent can discover it. A user-invoked skill spends human attention because the user must remember and call it.

Keep the required portable `description` and automatic discovery by default. Use explicit-only invocation only when the user requests it or a documented target-client requirement calls for it. Timing-sensitive or side-effectful work still needs authorization immediately before the mutation; hiding a skill from automatic discovery is not a permission boundary. Invocation controls are client extensions, not a portable guarantee; see [client compatibility](client-compatibility.md).

Write a model-facing description that:

- front-loads the capability and the user's intent
- names each distinct trigger branch once
- distinguishes near misses and adjacent skills
- avoids implementation detail, marketing language, and restating the name
- remains under the portable 1024-character limit

## Bound the skill

One skill should own one coherent capability. Split by invocation when a branch has its own independently recognizable intent. Split by sequence only when later steps repeatedly pull the agent into ending an earlier, irreducibly fuzzy step too soon.

Do not split merely to make files small. Every new model-invoked skill adds routing cost; every explicit-only skill adds something the user must remember.

Preserve user intent and scope. A skill must not replace the user's chosen product, expand the assignment, modify unrelated configuration, or imply permission for additional external actions. Do not generalize one example, correction, or preference into a universal rule without supporting evidence.

## Build the information hierarchy

Rank content by when it is needed:

1. Ordered steps common to every run belong in `SKILL.md`.
2. Compact rules needed during those steps may remain beside them.
3. Branch-specific details, long examples, syntax tables, and troubleshooting belong in directly linked references.

Keep a concept's rule, caveat, and example together. Never hide required content behind a reference index that points to another file; link the required file directly from `SKILL.md`.

Give consequential steps a completion criterion. Strong criteria are checkable and demanding, such as “every changed schema has a reversible migration and a passing rollback test,” rather than “review the migrations.”

Use a familiar leading word when it compresses a repeated behavioral idea. The word must change behavior; vague reminders such as “be thorough” are usually no-ops.

Match specificity to fragility. Describe outcomes and decision criteria when several approaches are sound; prescribe exact steps or scripts when ordering, safety, or reproducibility is genuinely fragile. Prefer one useful default with a narrow escape hatch over an undifferentiated menu of tools.

## Choose support files

Create support files only when they remove repeated work or conditional detail:

- `references/`: focused on-demand knowledge, ideally one branch or topic per file
- `scripts/`: deterministic or repetitive operations the model should not reinvent
- `templates/`: starter files copied or filled during output creation
- `assets/`: static media, schemas, or data consumed as-is
- `evals/`: test prompts and objective expectations for maintainers

Scripts should be non-interactive, self-contained or explicit about dependencies, safe on repeated runs, and clear about inputs, outputs, and exit codes. Include `--help`, actionable errors, and structured output when another tool will consume it. Never embed secrets.

Add a support file because evidence shows it helps: repeated improvised logic belongs in a tested script; a strict output shape belongs in a template; conditional domain knowledge belongs in a focused reference. Do not create placeholders or directories in anticipation of hypothetical needs.

## Write SKILL.md

Use imperative instructions and explain non-obvious reasons. Prefer a short workflow over a manual. Include:

- required portable frontmatter
- the outcome
- ordered decisions or actions
- checkable completion criteria
- safety and permission boundaries
- direct pointers to conditional resources
- exact validation commands

Keep all “when to use” routing information in the description unless a client requires additional routing fields. Do not repeat the README's human-facing overview in the runtime body.

Use the smallest effective instruction pattern. Concrete gotchas are valuable when they correct a likely false assumption. Use checklists for dependent multi-step work, validation loops when output can be checked and repaired, and plan-validate-execute for consequential batch or destructive operations. Do not add these patterns mechanically to every skill.

## Document the human-facing surface

Every Skill includes a detailed README that answers, near the top:

- What problem does this solve?
- When should it be used?
- What does it produce?
- What context does it require?
- How is it installed and validated?

Include at least three realistic example prompts, supported-client notes, related skills or an explicit “none,” and honest licensing information. Keep runtime behavior canonical in `SKILL.md`; the README explains and links rather than duplicating it.

For a Skill bundled inside an Agent Plugin, keep this detailed documentation in the Skill directory. The plugin root README keeps only plugin-wide setup, validation, licensing, and a concise table of Skills with one-line descriptions that link to their detailed READMEs. Do not duplicate detailed usage material at both levels.

## Prune before evaluation

Run four passes:

1. **Duplication:** keep each meaning in one authoritative place.
2. **Relevance:** remove stale or out-of-scope branches.
3. **No-op:** delete instructions that do not change default model behavior.
4. **Sprawl:** disclose conditional material and shorten oversized examples.

Then evaluate. A skill that is merely valid but has not demonstrated better behavior is unfinished when the task permits testing.

## Revise from evidence

Generalize from all observed runs rather than inserting phrases tailored to one failure. Read execution traces and final artifacts: repeated improvised scripts belong in `scripts/`; skipped pointers need stronger wording; consistently ignored rules may need a sharper criterion or deterministic check; unused instructions should be removed.

Stop iterating when users approve the outputs, feedback is empty, or further changes do not improve held-out performance.
