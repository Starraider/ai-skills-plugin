# AGENTS.md Authoring Guidance

Last researched: 2026-08-20.

## Purpose and format

`AGENTS.md` is plain Markdown with no required schema or frontmatter. Treat it as a compact README for coding agents: it should contain operational project context that belongs in the agent's working context, rather than user-facing introduction material. The open format recommends a root file and, for monorepos, additional files only where subprojects need different instructions. [AGENTS.md](https://agents.md/)

## Inclusion test

Keep a rule only if omitting it could plausibly lead the agent to make a project-specific mistake. Prefer facts the agent cannot reliably infer from source, conventional configuration, or an existing human-facing document. This is consistent with OpenCode's `/init` guidance—build, lint, and test commands; non-obvious structure; conventions; setup quirks; and operational gotchas—and with Microsoft’s recommendation to focus on non-obvious rules rather than formatter- or linter-enforced conventions. [OpenCode Rules](https://opencode.ai/docs/rules/), [VS Code custom instructions](https://code.visualstudio.com/docs/agent-customization/custom-instructions)

## High-value content

Include a section only when the repository supports it:

- **Project orientation:** short description, major packages or services, and an architecture boundary that file names alone do not make obvious.
- **Commands:** exact setup, focused test, lint, type-check, build, and local validation commands; state where each should run and when it applies.
- **Non-default conventions:** dependency manager, language/runtime version, naming, import, error-handling, or API patterns that tooling does not enforce.
- **Boundaries and hazards:** generated files, migrations, compatibility guarantees, sensitive data handling, prohibited paths, and safe alternatives.
- **Definition of done:** targeted verification, documentation changes when behavior changes, and the review or handoff evidence the project actually requires.

For an instruction that needs judgment, give the reason or a safe path in the same bullet. For example: "Do not edit generated API clients; update the schema and run `pnpm generate` so the client remains reproducible." Codex specifically recommends concise review rules that state the behavior to flag and the safe path or exception. [Codex AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

## Writing and formatting

- Use a descriptive top-level heading and short, stable Markdown headings.
- Write direct, imperative bullets: "Run `pnpm test --filter api` from `packages/api` before changing public handlers." Avoid paragraphs that blend several conditions.
- Put commands in code spans or fenced blocks. Never invent a command; inspect manifests, CI, scripts, or obtain it from a maintainer.
- State conditions and scope: "For changes under `infra/`, run …" is better than an unconditional command that does not apply everywhere.
- Link rather than copy a lengthy style guide, runbook, or API specification. Add a one-line condition saying when to read it.
- Keep the document short and self-contained enough to load on every task. Break genuinely distinct monorepo guidance into nested files when the target supports that behavior.

## Exclude or relocate

- README-style marketing, onboarding, or a full file tree the agent can inspect.
- Vague demands such as "write clean code," "be careful," or a generic model persona.
- Rules enforced deterministically by a formatter, linter, type checker, CI, or branch protection; point to the check when it matters.
- Large copied policies, long examples, repeated instructions from other agent files, and stale historical notes.
- Secrets, access tokens, passwords, private endpoints, or broad instructions to bypass approvals, sandboxes, or review.
- Tool-permission policy. Configure it in the product's native permission controls instead of trying to enforce it through prose.

## Maintenance

Keep `AGENTS.md` versioned with the project. Update it when commands, project topology, generated-code flows, or safety constraints change; delete rules that have become enforceable by automation or redundant with source documentation. After an agent makes a repeatable project-specific error, add the smallest precise rule that prevents that failure and verify it with a representative task.
