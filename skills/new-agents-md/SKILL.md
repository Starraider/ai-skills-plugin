---
name: new-agents-md
description: Use when the user wants to create, replace, or improve an AGENTS.md instruction file for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca. Establish the target product and scope, inspect the repository for evidence, create concise project-specific guidance, and give target-appropriate discovery checks. Do not use for skills, native rules, custom agents, or generic prompts unless an AGENTS.md is explicitly needed.
---

# New AGENTS.md

## Outcome

Create a concise, factual `AGENTS.md` that gives the selected coding-agent surface the project context it cannot reliably infer: exact commands, non-obvious conventions, boundaries, and verification expectations. Produce a target-appropriate location and discovery check; do not claim that every listed product loads the file the same way.

## Workflow

1. Establish the instruction-file contract.

   Identify the target product and surface, project versus personal scope, intended directories, and whether the user wants a new file or an update. Inspect the repository before drafting: existing instruction files, README and contribution guidance, package/build manifests, CI configuration, scripts, formatter/linter configuration, and the affected subtree.

   If the target is ChatGPT, distinguish a Codex-backed coding surface from a general ChatGPT Project, custom GPT, or Workspace Agent. If it is not a Codex-backed coding surface, explain that a local `AGENTS.md` has no documented automatic loader and offer a reusable repository file rather than claiming it will be applied automatically. If the target or scope is materially ambiguous, ask one concise question before writing.

   Completion: every proposed instruction is backed by repository evidence or an explicit user requirement, and the target's native discovery behavior is known.

2. Select the target-specific location and precedence rules.

   Read [target support and verification](references/target-support.md) and use only the selected product branch. For a shared repository file, use root `AGENTS.md` only when the selected products document or can intentionally consume it; document any product that needs a native Rule or another configuration file instead.

   Do not add YAML frontmatter, client-specific directives, symlinks, or companion configuration files to a portable `AGENTS.md` unless the user explicitly asks for them. A normal `AGENTS.md` is plain Markdown.

   Completion: the output location, inheritance behavior, and validation steps match the selected product; unsupported discovery is clearly labelled.

3. Extract high-value guidance and omit the rest.

   Apply the inclusion test in [authoring guidance](references/authoring-guidance.md): keep a statement only when omitting it would plausibly cause an agent mistake. Prefer exact, project-tested commands and non-obvious constraints over generic advice. Preserve existing project terminology and link to long-lived source documents instead of copying them.

   Include only sections supported by the inspected project. Common high-value sections are project orientation, setup and verification commands, affected-subtree architecture, conventions not enforced by tooling, generated-file or migration boundaries, security or data-handling constraints, and the definition of done. Use the [portable template](templates/AGENTS.md) as a starting structure, then delete every inapplicable heading and placeholder.

   Do not include secrets, credentials, internal URLs that are not meant for all repository readers, invented commands, generic model personas, duplicated README prose, style rules already enforced by formatters or CI, broad tool permissions, or instructions that contradict user, system, or product safety controls. Phrase rules as short imperative statements; state the reason or safe alternative only for non-obvious or high-risk constraints.

   Completion: every rule is specific, actionable, and traceable to evidence or an explicit user decision; the file has no placeholders or generic filler.

4. Write or update the file without losing local knowledge.

   For a new project file, create `AGENTS.md` at the chosen root. For an existing file, preserve accurate project-specific guidance and revise only the requested or demonstrably stale content. Use short Markdown headings and bullets, put commands in code spans or fenced blocks, and make conditional commands explicit about their scope.

   In a monorepo, keep shared instructions at the repository root and add a nested `AGENTS.md` only when a subtree has genuinely different commands, constraints, or ownership. Do not create nested files merely to restate the root.

   Completion: the file is plain, readable Markdown, contains no unverified command, and matches the requested scope.

5. Verify content and discovery.

   Check that the file is non-empty, has no unfinished placeholders, and names only commands that exist in the repository or were explicitly supplied by the user. Run relevant existing verification commands only when their safety and prerequisites are established. Then perform the target-specific discovery check from [target support and verification](references/target-support.md), preferably with a harmless prompt such as “Summarize the active project instructions.”

   Completion: content checks pass and the chosen product is confirmed to load the file, or the exact discovery limitation is reported with no unsupported claim.

## Safety

- Treat `AGENTS.md` as versioned team guidance. Never put API keys, tokens, passwords, private personal preferences, or production access instructions in a project file.
- Do not weaken sandboxing, approvals, browser restrictions, or tool permissions through prose. Configure permissions in the target's native controls only when the user explicitly requests that separate change.
- Do not overwrite an existing `AGENTS.md`, `AGENTS.local.md`, `AGENTS.override.md`, native Rule, or configuration file without the user's authorization.
- Do not present `AGENTS.md` as a custom agent, a Skill, an execution policy, or a substitute for automated checks.

## Resources

- [Target support, locations, precedence, and discovery checks](references/target-support.md)
- [Evidence-based content and writing guidance](references/authoring-guidance.md)
- [Portable AGENTS.md template](templates/AGENTS.md)
