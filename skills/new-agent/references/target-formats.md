# Target formats and validation

Last researched: 2026-08-19. Treat the linked vendor documentation as authoritative when it differs from this reference.

## Agent taxonomy

An Agent Skill, always-on project instruction, rule, MCP server, custom GPT, subagent definition, IDE profile, ACP process, and CLI launcher are not interchangeable. Choose the representation the user explicitly requested and name the distinction when it affects the result.

## Antigravity

Antigravity custom agents are Markdown files with YAML frontmatter. For a workspace use `.agents/agents/<name>/agent.md`; for the user scope use `~/.gemini/config/agents/<name>/agent.md`. The CLI documentation describes selecting and discovering them from `/agents`; the same workspace convention is used by Antigravity’s agent surfaces.

Minimum frontmatter is `name` and `description`; add only documented fields such as `subagent: true` when delegation is required. Use [the Antigravity template](../templates/antigravity-agent.md). Verify by reopening `/agents` or the IDE custom-agent selector, then selecting or explicitly invoking the agent.

Sources: [Agents command](https://antigravity.google/docs/cli/commands/agents), [Background tasks and subagents](https://antigravity.google/docs/cli/subagents).

## Codex

Codex has distinct local subagents, Skills, and ChatGPT Workspace Agents. Do not substitute one for another.

For a local custom subagent on a runtime that supports it, use `.codex/agents/<name>.toml` at project scope or `~/.codex/agents/<name>.toml` at user scope. Include `name`, `description`, and `developer_instructions`; only add model, reasoning-effort, sandbox, or other Codex configuration keys when the installed runtime supports them. Start a new session and check the local agent chooser or configuration diagnostics before asserting discovery. Use [the Codex template](../templates/codex-agent.toml).

The current public official documentation clearly supports a separate **Workspace Agents plugin in Codex** for eligible Business and Enterprise workspaces: it can create/update drafts, but preview/run and some deployment controls remain in ChatGPT/Agent Studio. When that plugin is not available, report that limitation rather than claiming a local TOML agent is available in every Codex surface.

Sources: [Workspace Agents in ChatGPT and Codex](https://help.openai.com/en/articles/20001143), [Codex Skills](https://developers.openai.com/codex/skills). The local TOML format should be rechecked against the installed Codex version before use because it is not currently described in the above public OpenAI help page.

## ChatGPT

There are two native agent surfaces:

- A **Custom GPT**: available in eligible Business, Enterprise, and Edu workspaces with the relevant permissions. Create in the GPT builder, configure name/description/starters, instructions, optional knowledge, capabilities, and either apps or actions (not both), then Preview before saving.
- A **Workspace Agent**: built from ChatGPT’s Agents area. It can use tools, apps, custom MCPs, skills, files, channels, schedules, and API triggers according to workspace permission. Keep write actions set to confirmation unless the user explicitly approves a narrower policy.

Generate a builder brief, do not create it automatically. Ask before remote creation, sharing, publishing, schedule/API-trigger configuration, or connector changes. Verify in Preview with the agreed representative prompt.

Sources: [Creating and editing GPTs](https://help.openai.com/en/articles/8554397-), [Workspace Agents](https://help.openai.com/en/articles/20001143).

## Zed

Zed’s native Agent uses **Agent Profiles** to choose a default model and available built-in/MCP tools. Generate an `agent.profiles` settings fragment for a native profile. A profile does not itself grant execution permission; Zed Tool Permissions remain a separate control.

For an external ACP-compatible agent, generate an `agent_servers.<name>` object with `type: "custom"`, command, arguments, and environment. This registers an external agent process; it does not create its underlying AI implementation. Use [the Zed settings templates](../templates/zed-agent-settings.jsonc). Verify by opening `agent: manage profiles` or Agent Settings → External Agents and running one representative request.

Sources: [Agent Profiles](https://zed.dev/docs/ai/agent-profiles), [External Agents](https://zed.dev/docs/ai/external-agents), [Agent Settings](https://zed.dev/docs/ai/agent-settings).

## OpenCode

Create Markdown agents in `.opencode/agents/<name>.md` for a project or `~/.config/opencode/agents/<name>.md` for the user. The file name defines the agent name. Frontmatter supports `description`, `mode` (`primary` or `subagent`), `model`, `temperature`, and `permission`; the Markdown body is the system prompt. Use [the OpenCode template](../templates/opencode-agent.md).

For quick authoring, `opencode agent create` asks for scope, description, permissions, and writes the Markdown file. Verify with the agent selector; invoke a subagent by `@name` and confirm a denied permission cannot execute.

Source: [OpenCode Agents](https://opencode.ai/docs/agents).

## Qoder

Create Markdown custom agents at `.qoder/agents/<name>.md` for a project or `~/.qoder/agents/<name>.md` for the user. Required frontmatter is `name` and `description`; the body is the system prompt. `tools`, `disallowedTools`, `model`, `skills`, `mcpServers`, `maxTurns`, `timeoutMins`, and `isolation: worktree` are optional and should be used only when needed. Use [the Qoder template](../templates/qoder-agent.md).

In the IDE, `/create-agent <requirement>` can create one interactively. In the CLI, `/agents` → User or Project → Create new agent is the recommended path. Reload after a manual change with `/agents reload`; verify discovery in `/agents` or `qodercli agents list`, then invoke by explicit name before relying on automatic matching.

Sources: [Qoder Custom Agent](https://docs.qoder.com/extensions/subagent), [Qoder CLI Subagents](https://docs.qoder.com/cli/subagent).

## Orca

Orca treats a CLI program as an agent launcher. Open Settings → Agents → Add custom agent, set the display name, verified binary/command, default arguments, and only a safe optional startup hook. Orca launches the command with the current worktree as working directory; it does not define the CLI agent’s system prompt or permissions.

Create the underlying agent’s own configuration first if its capabilities must be specialized. Verify by selecting the agent from the terminal combobox in a disposable worktree and confirm the command starts with the expected working directory.

Source: [Add a custom CLI agent](https://www.onorca.dev/docs/agents/custom-cli).
