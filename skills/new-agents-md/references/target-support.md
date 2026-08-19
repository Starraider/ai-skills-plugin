# Target Support and Verification

Last researched: 2026-08-20. Product behavior changes; recheck the linked primary documentation before making compatibility claims outside this skill.

## Antigravity

Antigravity's native always-on customization is a Rule: global rules live in `~/.gemini/GEMINI.md`, and workspace Rules live under `.agents/rules/`. Rules have activation modes and a 12,000-character limit per file. Antigravity also added support for reading `AGENTS.md` alongside `GEMINI.md`, but its Rule documentation remains the authoritative path for native IDE customization. [Rules](https://antigravity.google/docs/ide-rules/), [changelog](https://antigravity.google/changelog)

- Use a repository-root `AGENTS.md` when the user explicitly needs cross-agent portability or has confirmed Antigravity's loader in their version.
- Prefer `.agents/rules/` for an Antigravity-only rule, but do not create it while fulfilling an `AGENTS.md` request unless separately authorized.
- Verify with a new Antigravity agent conversation in the target workspace and a harmless request to summarize active project guidance. If it is not visible, report that the native Rule path is documented while the requested loader is not verified for that installation.

## Codex

Codex reads global guidance from `$CODEX_HOME/AGENTS.override.md` or `$CODEX_HOME/AGENTS.md` (normally `~/.codex`). At project scope it walks from the project root to the current directory, selecting at most one of `AGENTS.override.md`, `AGENTS.md`, or configured fallback files per directory. More-local instructions appear later and override broader instructions. The default combined project-document limit is 32 KiB. [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

- Use `<repository>/AGENTS.md` for shared repository guidance, or `$CODEX_HOME/AGENTS.md` for private global preferences.
- Use nested files only for a subtree with different instructions. Use `AGENTS.override.md` only for an intentional local override.
- Verify with `codex --ask-for-approval never "Summarize the current instructions."` from the relevant directory. To check an override, add `--cd <subdirectory>` and ask for active instruction sources.

## ChatGPT

The documented `AGENTS.md` behavior is for Codex; its current documentation is hosted in ChatGPT Learn and covers Codex-backed coding work. A general ChatGPT Project, custom GPT, or Workspace Agent should not be represented as automatically loading a local `AGENTS.md` unless the user supplies documentation for that surface. [Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md)

- If the user means ChatGPT Desktop or another Codex-backed coding surface, use the Codex branch and verify in a new coding session.
- Otherwise, create a repository artifact only if requested, label it as portable guidance, and explain that it must be attached, imported, or copied into that ChatGPT surface according to its own configuration workflow.

## Zed

Zed treats `AGENTS.md` as its primary instruction file. A personal file lives at `~/.config/zed/AGENTS.md`; a project file is one of its supported project instruction files, including root or compatible `AGENTS.md`. Project guidance overrides personal guidance when they conflict. Zed’s native Agent loads it; external agents and terminal threads may instead follow their own instruction-file rules. [Zed instructions](https://zed.dev/docs/ai/instructions)

- Use `<project>/AGENTS.md` for shared project guidance or `~/.config/zed/AGENTS.md` for personal Zed guidance.
- Verify in Zed Agent (not merely an external-agent terminal) with an explicit request to summarize project instructions.

## OpenCode

OpenCode loads a project `AGENTS.md` from the current directory upward and a global file at `~/.config/opencode/AGENTS.md`. `AGENTS.md` wins over compatible `CLAUDE.md` in the same discovery category. Its `/init` command can create or improve the project file, and `opencode.json` can load additional instruction files. [OpenCode Rules](https://opencode.ai/docs/rules/)

- Use `<project>/AGENTS.md` for shared rules or `~/.config/opencode/AGENTS.md` for personal preferences.
- Use `opencode.json` only when the user separately wants a maintained set of additional instructions; do not duplicate their contents in `AGENTS.md`.
- Verify with `/init` only if the user wants OpenCode to improve the file; otherwise start a fresh session and ask it to summarize its project rules.

## Qoder

Qoder CLI uses `~/.qoder/AGENTS.md`, project `${project}/AGENTS.md`, and local `${project}/AGENTS.local.md` as memory files. `/init` generates or updates the project file. The default project discovery boundary is `.git`; the name, boundary markers, directory limit, and inclusion behavior are configurable. [Qoder tasks and memory](https://docs.qoder.com/cli/run-tasks), [Qoder loading troubleshooting](https://docs.qoder.com/cli/troubleshoot-loading)

- Use `<project>/AGENTS.md` for shared conventions; use `AGENTS.local.md` only for non-versioned local guidance, and `~/.qoder/AGENTS.md` only for personal preferences.
- Verify in the target project with `/memory` or a fresh session that summarizes project instructions. If it does not load, check the configured filename and `.git` discovery boundary before changing content.

## Orca

Orca coordinates and launches agents; it does not redefine Codex's `AGENTS.md` semantics. Its documentation says it preserves the repository and nested `AGENTS.md` files belonging to Codex and surfaces them for editing. Therefore, the effective location and precedence come from the launched agent, usually Codex. [Orca agent hooks and memory](https://www.onorca.dev/docs/agents/hooks-memory)

- When Orca launches Codex workers, use the Codex branch for a repository `AGENTS.md` and test it with that worker agent.
- Do not claim that Orca itself injects arbitrary root or `.orca/AGENTS.md` files unless the user's installed Orca version documents that behavior.
- Verify in a newly launched worker with a harmless instruction-summary task; Orca's UI showing the file is not proof that the worker loaded it.
