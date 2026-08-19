# Authoring guide

Use this guide while designing or revising a skill. The objective is predictability: repeated runs should follow the same sound process even when their outputs differ.

## Capture intent before drafting

Mine the current conversation, existing files, successful demonstrations, and user corrections before asking questions. Resolve:

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

Use model invocation when intent can be recognized safely and the skill should be selected automatically. Use explicit invocation for timing-sensitive or side-effectful work. Invocation controls are client extensions, not a portable guarantee; see [client compatibility](client-compatibility.md).

Write a model-facing description that:

- front-loads the capability and the user's intent
- names each distinct trigger branch once
- distinguishes near misses and adjacent skills
- avoids implementation detail, marketing language, and restating the name
- remains under the portable 1024-character limit

## Bound the skill

One skill should own one coherent capability. Split by invocation when a branch has its own independently recognizable intent. Split by sequence only when later steps repeatedly pull the agent into ending an earlier, irreducibly fuzzy step too soon.

Do not split merely to make files small. Every new model-invoked skill adds routing cost; every explicit-only skill adds something the user must remember.

## Build the information hierarchy

Rank content by when it is needed:

1. Ordered steps common to every run belong in `SKILL.md`.
2. Compact rules needed during those steps may remain beside them.
3. Branch-specific details, long examples, syntax tables, and troubleshooting belong in directly linked references.

Keep a concept's rule, caveat, and example together. Never hide required content behind a reference index that points to another file; link the required file directly from `SKILL.md`.

Give consequential steps a completion criterion. Strong criteria are checkable and demanding, such as “every changed schema has a reversible migration and a passing rollback test,” rather than “review the migrations.”

Use a familiar leading word when it compresses a repeated behavioral idea. The word must change behavior; vague reminders such as “be thorough” are usually no-ops.

## Choose support files

Create support files only when they remove repeated work or conditional detail:

- `references/`: focused on-demand knowledge, ideally one branch or topic per file
- `scripts/`: deterministic or repetitive operations the model should not reinvent
- `templates/`: starter files copied or filled during output creation
- `assets/`: static media, schemas, or data consumed as-is
- `evals/`: test prompts and objective expectations for maintainers

Scripts should be non-interactive, self-contained or explicit about dependencies, safe on repeated runs, and clear about inputs, outputs, and exit codes. Include `--help`, actionable errors, and structured output when another tool will consume it. Never embed secrets.

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

## Document the human-facing surface

A standalone Skill includes a README that answers, near the top:

- What problem does this solve?
- When should it be used?
- What does it produce?
- What context does it require?
- How is it installed and validated?

Include at least three realistic example prompts, supported-client notes, related skills or an explicit “none,” and honest licensing information. Keep runtime behavior canonical in `SKILL.md`; the README explains and links rather than duplicating it.

For a Skill bundled inside an Agent Plugin, put this information in the plugin root README and list the Skill's purpose and trigger boundary there. Add a Skill-local README only when the Skill is also consumed independently or needs substantially different human documentation. Do not duplicate the same usage material at both levels.

## Prune before evaluation

Run four passes:

1. **Duplication:** keep each meaning in one authoritative place.
2. **Relevance:** remove stale or out-of-scope branches.
3. **No-op:** delete instructions that do not change default model behavior.
4. **Sprawl:** disclose conditional material and shorten oversized examples.

Then evaluate. A skill that is merely valid but has not demonstrated better behavior is unfinished when the task permits testing.

## Revise from evidence

Generalize from failures rather than inserting phrases tailored to one prompt. Read execution traces when available: repeated improvised scripts belong in `scripts/`; skipped pointers need stronger wording; consistently ignored rules may need a sharper criterion or deterministic check.

Stop iterating when users approve the outputs, feedback is empty, or further changes do not improve held-out performance.
