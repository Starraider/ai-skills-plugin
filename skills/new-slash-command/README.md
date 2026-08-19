# new-slash-command

Create a safe, manually invoked shortcut for a supported AI coding product—or choose a better documented mechanism when a slash command is not appropriate or not supported.

## What this skill solves

It turns a request such as “make `/review-pr`” into the right, documented artifact for the selected product: a native command where one exists, or an explicit Skill, Workflow, or Orca Quick Command where it does not. It also prevents command-shaped requests from being misimplemented as an unsafe automation, persistent rule, or poorly scoped agent.

## Use when

- Creating, revising, or debugging a reusable manually invoked command for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca.
- Deciding whether a repeated task should be a slash command, Skill, Workflow, agent, hook, rule, or automation.

Do not use it to build a generic command-line interface, an OpenAI API function/tool, an IDE keybinding, or a Git hook unless the request specifically concerns one of the supported agent products.

## Expected outputs

- A clear mechanism decision, including an explicit “not a slash command” result when appropriate.
- One target-native definition or a ready-to-paste UI builder brief, with scope and invocation syntax.
- Discovery/reload instructions and a low-risk happy-path plus safety-boundary verification plan.

## Context requirements

Provide the target product, intended outcome, project or personal scope, arguments, and whether execution may edit files, run commands, use the network, or make external writes. Existing command/skill/workflow configuration is useful for collision checks and conventions. The skill asks only when missing context changes the mechanism or risk.

## Installation

This is a portable Agent Skill. Keep its complete directory together when installing it.

| Client | Project installation | User installation |
| --- | --- | --- |
| Antigravity | `.agents/skills/new-slash-command/` | `~/.gemini/config/skills/new-slash-command/` |
| Codex | `.agents/skills/new-slash-command/` | `~/.agents/skills/new-slash-command/` |
| Zed | `.agents/skills/new-slash-command/` | `~/.agents/skills/new-slash-command/` |
| OpenCode | `.opencode/skills/new-slash-command/` or `.agents/skills/new-slash-command/` | `~/.config/opencode/skills/new-slash-command/` |
| Qoder | `.qoder/skills/new-slash-command/` | `~/.qoder/skills/new-slash-command/` |
| Orca | Install as a compatible Agent Skill for the launched agent | Install in that agent’s global Skills location |
| ChatGPT | Upload through Plugins → Skills | Install through the Skills UI |

## Example prompts

- “Create `/review-api` in OpenCode for this project. It should review the current diff for API breaking changes, accept an optional focus area, and never edit files.”
- “I want `/deploy-preview` in Codex. Decide whether that is possible and create the safest supported alternative with an explicit approval before deployment.”
- “Create a global Qoder command that drafts conventional commit messages from the staged diff. Tell me how to reload and smoke-test it.”
- “Can Orca create `/run-e2e`? If not, set up the appropriate project-scoped replacement without executing the test suite.”

## Validation

From the plugin root, validate the portable structure:

```bash
skills/new-skill/scripts/validate-skill.sh skills/new-slash-command \
  --clients codex,antigravity,opencode,qoder
python3 skills/agent-plugin-builder/scripts/validate_agent_plugin.py . --strict
```

Then use the target-specific discovery and behavioral checks in [target command formats and research](references/target-command-formats.md). Test a low-risk invocation and an invalid, missing, or approval-required input.

Research was verified on 2026-08-19 against the primary documentation linked in the reference. Literal custom `/…` commands are not interchangeable: Codex explicitly selects Skills with `$`, ChatGPT with `@`, and Orca documents Quick Commands rather than an agent slash-command definition.

## Related skills

- [`new-skill`](../new-skill/README.md) for reusable instructions that need supporting scripts or richer context.
- [`new-workflow`](../new-workflow/README.md) for scheduled, multi-step, or multi-agent work.
- [`new-agent`](../new-agent/README.md) for a long-lived specialist with its own tools and boundary.
- [`new-hook`](../new-hook/README.md) for lifecycle-event behavior.

## License

No standalone license is declared for this skill directory. Before external distribution, apply the license required by the containing repository.
