# new-agent

`new-agent` creates one specialized agent in the native form supported by Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca.

## What this skill solves

The term “agent” is overloaded across IDEs. This skill first identifies the requested target and its actual agent surface, then produces a smallest-possible, least-privilege configuration rather than an incompatible prompt, rule, or skill.

## Use when

- Creating a focused coding, review, planning, research, or operations agent for one supported product.
- Turning a defined capability and tool boundary into a native agent profile, subagent, configuration, or builder brief.
- Reviewing an existing custom agent for excessive tools, unclear routing, or incorrect location.

Do not use it to create a reusable Agent Skill, a project-wide instruction file, an MCP server, or an IDE extension without an agent definition.

## Expected outputs

- A native local agent file, settings fragment, or an exact ChatGPT/Orca builder specification.
- A system prompt aligned to the stated capability and tool boundary.
- Discovery, explicit-invocation, and least-privilege verification steps.

## Context requirements

The user must state:

- the target: Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca;
- the agent’s specific capabilities, including its responsibility, expected result, and required tools; and
- its intended scope: one project or the user’s environment.

The skill asks for missing required information rather than selecting a target or granting capabilities by default.

## Installation

Install the entire `new-agent/` directory as an Agent Skill. In this repository it is already packaged at `skills/new-agent/`; compatible clients discover the skill through the enclosing Agent Plugin. See the containing repository’s [installation guidance](../../README.md#install-in-supported-ides-and-agents).

## Example prompts

- “Create a **Qoder** project-level `api-reviewer` agent. It should inspect API specifications and source code, return severity-ranked findings, and use only Read, Grep, and Glob.”
- “Create an **OpenCode** personal `test-planner` subagent. It may read code and run targeted test commands, but it must not edit files or access the web.”
- “Create a **ChatGPT Workspace Agent** for weekly customer-feedback summaries. It needs read-only Google Drive access and web search, but must not write to any app or publish yet.”
- “Configure a **Zed** native Ask-style agent profile with read/search tools only, using our existing OpenAI-compatible provider.”
- “Add an **Orca** custom CLI agent that starts the verified `my-agent --interactive` command in the active worktree.”

## Validation

Run the structural validation from the repository root:

```bash
skills/new-skill/scripts/validate-skill.sh skills/new-agent \
  --clients codex,antigravity,opencode,qoder
```

Then follow the target-specific discovery and explicit-invocation checks in [target formats and research](references/target-formats.md). The bundled eval cases cover a representative agent request, a least-privilege boundary, and a missing-target near miss.

## Sources

The product-specific formats were checked on 2026-08-19 against current documentation: [Antigravity custom agents](https://antigravity.google/docs/cli/commands/agents), [ChatGPT Workspace Agents](https://help.openai.com/en/articles/20001143), [ChatGPT GPT builder](https://help.openai.com/en/articles/8554397-), [Zed Agent Profiles](https://zed.dev/docs/ai/agent-profiles), [Zed External Agents](https://zed.dev/docs/ai/external-agents), [OpenCode Agents](https://opencode.ai/docs/agents), [Qoder Custom Agent](https://docs.qoder.com/extensions/subagent), [Qoder Subagents](https://docs.qoder.com/cli/subagent), and [Orca custom CLI agents](https://www.onorca.dev/docs/agents/custom-cli). See the skill’s reference for the operative per-target details and Codex caveat.

## Related skills

- [`new-skill`](../new-skill/README.md) for a reusable Agent Skill instead of an IDE-native agent.
- [`agent-plugin-builder`](../agent-plugin-builder/README.md) for packaging Skills and supported components into a portable Agent Plugin.

## License

No standalone license is declared for this skill directory. Before external distribution, apply the license required by the containing repository.
