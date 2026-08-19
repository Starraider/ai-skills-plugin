# new-workflow

`new-workflow` decides whether a repeatable workflow is useful and creates the smallest documented representation for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca.

## What this skill solves

“Workflow” means different things in different products. This skill prevents incompatible output by distinguishing native workflows, prompt commands, Skills, Workspace Agents, tasks, schedules, and multi-agent orchestration. It also rejects a workflow when a one-off prompt, a Skill, a hook, a permission policy, or CI better fits the problem.

## Use when

- Turning a recurring process—such as triaging issues, preparing releases, reviewing pull requests, or producing a report—into a safe, reusable procedure.
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

Keep the complete `new-workflow/` directory together. In this repository it is available at `skills/new-workflow/`; see the repository’s [installation guidance](../../README.md#install-in-supported-ides-and-agents) for client-specific installation.

## Example prompts

- “Create an **Antigravity** workspace workflow named `release-check` that verifies the changelog and test suite, then prepares a release checklist. It must not publish or deploy.”
- “Should our **Codex** team create a workflow for daily support triage? We have ChatGPT Workspace Agents available, need read-only Slack and Drive access, and want a manager to approve every ticket draft.”
- “Make an **OpenCode** project command `/review-api` that accepts a path, reviews it against our API guidelines, and returns a severity-ranked Markdown report without changing files.”
- “In **Zed**, create an explicit `/deploy-preview` procedure that requests approval before it runs any command or external write.”
- “Build a **Qoder** Dynamic workflow for three agents to investigate a flaky test, compare evidence, and stop for a maintainer before any code is changed.”
- “Set up an **Orca** recurring workflow to inspect open pull requests every weekday, but draft the automation first and do not enable it.”

## Validation

Validate the portable skill structure from the repository root:

```bash
skills/new-skill/scripts/validate-skill.sh skills/new-workflow \
  --clients codex,antigravity,opencode,qoder
```

Then complete the selected product’s discovery and low-risk execution check in [target workflow formats and research](references/target-workflow-formats.md). The included eval cases cover a representative workflow, an unsuitable-workflow decision, and a safety boundary.

## Sources

The target formats were researched on 2026-08-19 against primary documentation: [Antigravity Workflows](https://antigravity.google/docs/ide/workflows?app=antigravity-ide), [ChatGPT Workspace Agents](https://help.openai.com/en/articles/20001143/), [ChatGPT Scheduled Tasks](https://help.openai.com/en/articles/10291617-tasks-inchatgpt), [Zed Skills](https://zed.dev/docs/ai/skills), [OpenCode Commands](https://opencode.ai/docs/commands/), [Qoder Commands](https://docs.qoder.com/cli/commands), [Qoder Working Modes](https://docs.qoder.com/cli/working-modes), and [Orca CLI overview](https://www.onorca.dev/docs/cli/overview). Codex uses the Workspace Agents plugin for eligible workspaces; otherwise its documented reusable-procedure primitive is an Agent Skill.

## Related skills

- [`new-skill`](../new-skill/README.md) for reusable, context-dependent agent instructions.
- [`new-agent`](../new-agent/README.md) for a long-lived specialist with a tool boundary.
- [`new-hook`](../new-hook/README.md) for deterministic lifecycle reactions rather than an ordered workflow.

## License

No standalone license is declared for this skill directory. Before external distribution, apply the license required by the containing repository.
