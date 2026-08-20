# new-hook

Create a narrowly scoped event hook for one supported developer environment—or establish that a hook is the wrong mechanism and select the right alternative.

## What this skill solves

It turns a loosely stated request such as “block unsafe commands” or “set up every new worktree” into a documented event contract, a native implementation, and a real verification path. It avoids a common trap: treating a prompt instruction, a permission setting, a CI job, or a scheduled automation as an agent lifecycle hook.

## Use when

- Creating, revising, or debugging an event-driven hook for Antigravity, Codex, Zed, OpenCode, Qoder, or Orca.
- Deciding whether a requested behavior should be a hook, Skill, permission policy, plugin/app/MCP integration, task, CI check, or automation.
- Assessing a ChatGPT request that is described as a hook and needs a supported alternative.

Do not use this skill for a generic event bus, an OpenAI API webhook receiver, or a Git hook unless the request is specifically about the target client’s agent/worktree integration.

## Expected outputs

- A clear yes/no hook decision and rationale.
- A target-native configuration and only the necessary handler source, when a hook is appropriate and authorized.
- Exact scope, reload/trust steps, representative and negative smoke tests.
- A supported replacement design when the target lacks the needed hook semantics.

## Context requirements

Provide the target product, desired trigger, outcome, scope (project or user), and whether the behavior may block, edit files, run commands, use the network, or make an external write. The skill asks only when a missing detail would change the implementation or risk.

## Installation

This directory is an Agent Skill inside the repository’s portable plugin. Keep the complete `new-hook/` directory together.

| Client | Project installation | User installation |
| --- | --- | --- |
| Antigravity | `.agents/skills/new-hook/` | `~/.gemini/config/skills/new-hook/` |
| Codex | `.agents/skills/new-hook/` | `~/.agents/skills/new-hook/` |
| Zed | `.agents/skills/new-hook/` | `~/.agents/skills/new-hook/` |
| OpenCode | `.opencode/skills/new-hook/` or `.agents/skills/new-hook/` | `~/.config/opencode/skills/new-hook/` |
| Qoder | `.qoder/skills/new-hook/` | `~/.qoder/skills/new-hook/` |
| Orca | Install as a compatible Agent Skill for the launched agent | Install in that agent’s global Skills location |
| ChatGPT Desktop App | Upload the complete skill through Plugins → Skills in the desktop app | Install through the desktop app Skills UI |

The hook itself is configured separately in the selected product; see [target hook formats and research](references/target-hook-formats.md).

## Example prompts

- “In Codex, block a Bash command that contains `rm -rf` outside `./tmp`; keep it project-local and explain how to test both paths.”
- “Should we use an OpenCode hook to force every agent to write a changelog? If so, create it; otherwise recommend the right mechanism.”
- “Set up Qoder to run Prettier after the agent edits TypeScript files, without blocking the edit.”
- “Make a Zed hook that copies `.env` into each newly created worktree.”
- “Create a ChatGPT hook after every response that posts to Slack.”

## Validation

Validate this skill’s portable structure from the repository root:

```bash
skills/new-skill/scripts/validate-skill.sh skills/new-hook \
  --clients codex,antigravity,opencode,qoder
```

Then follow the target’s loading and behavioral test in [target hook formats and research](references/target-hook-formats.md). Test a no-op or allowed path as well as the condition that triggers the hook.

## Sources

Research was verified on 2026-08-19 against the primary documentation linked in [target hook formats and research](references/target-hook-formats.md). The products do not expose interchangeable hook models: ChatGPT does not document a comparable local lifecycle hook, Zed’s documented hook is worktree-task specific, and Orca either reuses underlying agent hooks or runs a worktree setup command.

## Related skills

- [`new-skill`](../new-skill/README.md) to author reusable instructions instead of deterministic event code.
- [`agent-plugin-builder`](../agent-plugin-builder/README.md) to package a portable Skill and supported client components.

## License

Licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
