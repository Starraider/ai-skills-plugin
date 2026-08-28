# new-workflow

`new-workflow` decides whether a repeatable workflow is useful and creates the smallest documented representation for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, Orca, Cursor, GitHub Copilot / VS Code, Windsurf, Kiro, or Google Agents CLI.

## What this skill solves

“Workflow” means different things in different products. This skill prevents incompatible output by distinguishing native workflows, prompt commands, Skills, Workspace Agents, tasks, schedules, and multi-agent orchestration. It also rejects a workflow when a one-off prompt, a Skill, a hook, a permission policy, or CI better fits the problem.

## Use when

- Turning a recurring process—such as triaging issues, preparing releases, reviewing pull requests, scaffolding features, or producing a report—into a safe, reusable procedure.
- Choosing between an explicit workflow, Skill, slash command, agent, hook, scheduled automation, or CI job for one supported product.
- Creating, revising, or debugging a target-native workflow and its discovery/trigger behavior.

Do not use it merely to automate an untested one-off request or to evade approval and permission controls.

## Expected outputs

- A yes/no workflow decision with the appropriate alternative when it is not suitable.
- One target-native file, UI-builder brief, or documented configuration path.
- Ordered workflow instructions with inputs, approvals, stop conditions, output, and verification.
- Discovery/reload and low-risk smoke-test steps.

## Context requirements

Provide the target product, the recurring outcome, how it starts, desired inputs/output, project or personal scope, and whether it may edit files, run commands, access tools/network, or make external writes. The skill asks only when a missing target, outcome, or trigger would change the result.

## Installation

This is a portable Agent Skill. Keep its complete directory together when installing it.

| Client | Project installation | User installation |
| --- | --- | --- |
| Antigravity | `.agents/skills/new-workflow/` | `~/.gemini/config/skills/new-workflow/` |
| Codex | `.agents/skills/new-workflow/` | `~/.agents/skills/new-workflow/` |
| Zed | `.agents/skills/new-workflow/` | `~/.agents/skills/new-workflow/` |
| OpenCode | `.opencode/skills/new-workflow/` or `.agents/skills/new-workflow/` | `~/.config/opencode/skills/new-workflow/` |
| Qoder | `.qoder/skills/new-workflow/` | `~/.qoder/skills/new-workflow/` |
| Orca | Install as a compatible Agent Skill for the launched agent | Install in that agent's global Skills location |
| ChatGPT Desktop App | Upload through Plugins → Skills in the desktop app | Install through the desktop app Skills UI |
| Cursor | `.agents/skills/new-workflow/` | `~/.agents/skills/new-workflow/` |
| GitHub Copilot / VS Code | `.agents/skills/new-workflow/` | `~/.agents/skills/new-workflow/` |
| Windsurf | `.agents/skills/new-workflow/` | `~/.agents/skills/new-workflow/` |
| Kiro | `.agents/skills/new-workflow/` | `~/.agents/skills/new-workflow/` |
| Google Agents CLI (Gemini CLI) | `.agents/skills/new-workflow/` | `~/.agents/skills/new-workflow/` |

## Example prompts

- “Create an **Antigravity** workspace workflow named `release-check` that verifies the changelog and test suite, then prepares a release checklist. It must not publish or deploy.”
- “Should our **Codex** team create a workflow for daily support triage? We have ChatGPT Workspace Agents available, need read-only Slack and Drive access, and want a manager to approve every ticket draft.”
- “Make an **OpenCode** project command `/review-api` that accepts a path, reviews it against our API guidelines, and returns a severity-ranked Markdown report without changing files.”
- “In **Zed**, create an explicit `/deploy-preview` procedure that requests approval before it runs any command or external write.”
- “Build a **Qoder** Dynamic workflow for three agents to investigate a flaky test, compare evidence, and stop for a maintainer before any code is changed.”
- “Set up an **Orca** recurring workflow to inspect open pull requests every weekday, but draft the automation first and do not enable it.”
- “Create a **Cursor** project command workflow `/refactor-module` in `.cursor/commands/` that inspects dependencies, plans changes, and requires approval before writing files.”
- “Add a **GitHub Copilot** agentic prompt workflow `/generate-pr-description` in `.github/prompts/` with `agent: agent` and codebase search tools.”
- “Create a **Windsurf** workflow `/scaffold-api-endpoint` in `.windsurf/workflows/` that creates schema, route, and test files sequentially.”
- “Define a **Kiro** manual steering workflow `/security-audit` in `.kiro/steering/` with `inclusion: manual` that reviews code against OWASP guidelines.”
- “Scaffold a **Google Agents CLI** ADK workflow `daily-log-analyzer` that fetches Cloud Run logs, summarizes error clusters, and deploys to Cloud Run with human approval gates.”

## Validation

From the repository root, validate the portable structure:

```bash
skills/new-skill/scripts/validate-skill.sh skills/new-workflow \
  --clients codex,antigravity,opencode,qoder,cursor,copilot,windsurf,kiro,google-agents-cli
python3 skills/new-plugin/scripts/validate_agent_plugin.py . --strict
```

Then complete the selected product’s discovery and low-risk execution check in [target workflow formats and research](references/target-workflow-formats.md). The included eval cases cover representative workflows, unsuitable-workflow decisions, and safety boundaries.

## Sources

The target formats were researched on 2026-08-20 against primary documentation: [Antigravity Workflows](https://antigravity.google/docs/ide/workflows?app=antigravity-ide), [ChatGPT Workspace Agents](https://help.openai.com/en/articles/20001143/), [ChatGPT Scheduled Tasks](https://help.openai.com/en/articles/10291617-tasks-inchatgpt), [Skills in ChatGPT](https://help.openai.com/en/articles/20001066), [Zed Skills](https://zed.dev/docs/ai/skills), [OpenCode Commands](https://opencode.ai/docs/commands/), [Qoder Commands](https://docs.qoder.com/cli/commands), [Qoder Working Modes](https://docs.qoder.com/cli/working-modes), [Orca CLI overview](https://www.onorca.dev/docs/cli/overview), [Cursor Custom Commands](https://www.cursor.com/chat/commands), [Cursor Agent Skills](https://cursor.com/docs/skills), [GitHub Copilot Prompt Files](https://code.visualstudio.com/docs/copilot/copilot-customization#_prompt-files), [Windsurf Workflows](https://docs.windsurf.com/windsurf/customization), [Kiro Steering](https://kiro.dev/docs/steering/), [Kiro Custom Agents](https://kiro.dev/docs/agents/custom-agents), [google-agents-cli](https://github.com/google/agents-cli), [ADK documentation](https://google.github.io/adk-docs/), and [Gemini CLI Custom Commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md).

## Related skills

- [`new-skill`](../new-skill/README.md) for reusable, context-dependent agent instructions.
- [`new-agent`](../new-agent/README.md) for a long-lived specialist with a tool boundary.
- [`new-hook`](../new-hook/README.md) for deterministic lifecycle reactions rather than an ordered workflow.
- [`new-slash-command`](../new-slash-command/README.md) for compact, manually invoked prompt shortcuts.

## License

Licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
