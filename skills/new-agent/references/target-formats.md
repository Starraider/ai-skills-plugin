# Target formats and validation

Last researched: 2026-08-20. Treat the linked vendor documentation as authoritative when it differs from this reference.

## Agent taxonomy

An Agent Skill, always-on project instruction, rule, MCP server, custom GPT, subagent definition, IDE profile, ACP process, and CLI launcher are not interchangeable. Choose the representation the user explicitly requested and name the distinction when it affects the result.

## Antigravity

Antigravity custom agents are Markdown files with YAML frontmatter. For a workspace use `.agents/agents/<name>/agent.md`; for the user scope use `~/.gemini/config/agents/<name>/agent.md`. The CLI documentation describes selecting and discovering them from `/agents`; the same workspace convention is used by Antigravity's agent surfaces.

Minimum frontmatter is `name` and `description`; add only documented fields such as `subagent: true` when delegation is required. Use [the Antigravity template](../templates/antigravity-agent.md). Verify by reopening `/agents` or the IDE custom-agent selector, then selecting or explicitly invoking the agent.

Sources: [Agents command](https://antigravity.google/docs/cli/commands/agents), [Background tasks and subagents](https://antigravity.google/docs/cli/subagents).

## Codex

Codex has distinct local subagents, Skills, and ChatGPT Workspace Agents. Do not substitute one for another.

For a local custom subagent on a runtime that supports it, use `.codex/agents/<name>.toml` at project scope or `~/.codex/agents/<name>.toml` at user scope. Include `name`, `description`, and `developer_instructions`; only add model, reasoning-effort, sandbox, or other Codex configuration keys when the installed runtime supports them. Start a new session and check the local agent chooser or configuration diagnostics before asserting discovery. Use [the Codex template](../templates/codex-agent.toml).

The current public official documentation clearly supports a separate **Workspace Agents plugin in Codex** for eligible Business and Enterprise workspaces: it can create/update drafts, but preview/run and some deployment controls remain in ChatGPT/Agent Studio. When that plugin is not available, report that limitation rather than claiming a local TOML agent is available in every Codex surface.

Sources: [Workspace Agents in ChatGPT and Codex](https://help.openai.com/en/articles/20001143), [Codex Skills](https://developers.openai.com/codex/skills). The local TOML format should be rechecked against the installed Codex version before use because it is not currently described in the above public OpenAI help page.

## ChatGPT and ChatGPT Desktop App

There are two native agent surfaces in the ChatGPT ecosystem:

- A **Custom GPT**: available in eligible Business, Enterprise, and Edu workspaces with the relevant permissions. Created and configured in the web GPT builder (name, description, starters, instructions, optional knowledge files, capabilities, and either apps or actions), then tested in Preview before saving.
- A **Workspace Agent**: built from ChatGPT's web Agents area / Agent Studio. It can use tools, apps, custom MCPs, skills, files, channels, schedules, and API triggers according to workspace permission. Keep write actions set to confirmation unless the user explicitly approves a narrower policy.

Both Custom GPTs and Workspace Agents are configured and authored through OpenAI's web builder interfaces rather than local filesystem configuration files in the desktop app, but can be invoked and interacted with directly inside the ChatGPT Desktop App once published or shared. Generate a builder brief rather than attempting to write a local configuration file. Ask before remote creation, sharing, publishing, schedule/API-trigger configuration, or connector changes. Verify in Preview with the agreed representative prompt.

Sources: [Creating and editing GPTs](https://help.openai.com/en/articles/8554397-), [Workspace Agents](https://help.openai.com/en/articles/20001143).

## Zed

Zed's native Agent uses **Agent Profiles** to choose a default model and available built-in/MCP tools. Generate an `agent.profiles` settings fragment for a native profile. A profile does not itself grant execution permission; Zed Tool Permissions remain a separate control.

For an external ACP-compatible agent, generate an `agent_servers.<name>` object with `type: "custom"`, command, arguments, and environment. This registers an external agent process; it does not create its underlying AI implementation. Use [the Zed settings templates](../templates/zed-agent-settings.jsonc). Verify by opening `agent: manage profiles` or Agent Settings → External Agents and running one representative request.

Sources: [Agent Profiles](https://zed.dev/docs/ai/agent-profiles), [External Agents](https://zed.dev/docs/ai/external-agents), [Agent Settings](https://zed.dev/docs/ai/agent-settings).

## Cursor

Cursor distinguishes two native agent customization surfaces. Do not substitute one for another.

- **Custom Mode** (the closest native "agent" surface): defined through Settings → Features → Chat → Custom Modes. Each Custom Mode has a name, description, system instructions, preferred model, tool permissions (file edit, terminal, MCP, web search), and an optional keybinding. Custom Modes are UI-configured and live in Cursor's application settings; they are not standalone files and are not version-controlled by default.
- **Project rule (`.mdc` file)**: a Markdown file with YAML frontmatter stored in `.cursor/rules/<name>.mdc`. Frontmatter fields are `description`, `globs` (file glob array), and `alwaysApply` (boolean). The Markdown body is the instruction set. Rules are version-controlled and can be scoped to always-on, intelligently applied, glob-matched, or manually @-mentioned. A rule is **not** an agent; it provides persistent project context to any active mode.
- **Legacy `.cursorrules`**: the root-level `.cursorrules` file is deprecated. Migrate to `.cursor/rules/`.

Generate a Custom Mode specification (name, system instructions, model, tool permissions) for a persona-style agent request. Generate a `.mdc` file for a project-knowledge or conventions request. Explain the distinction when the user conflates rules with agent modes. Use [the Cursor mode template](../templates/cursor-mode.mdc). Verify by opening the Chat sidebar mode dropdown and selecting the new mode, then issuing one representative request.

Sources: [Cursor rules](https://www.cursor.com/en/docs/context/rules), [Cursor Custom Modes](https://www.cursor.com/en/docs/chat/custom-modes).

## GitHub Copilot / VS Code

GitHub Copilot supports distinct customization surfaces in VS Code. Do not substitute one for another.

- **Custom agent (`.agent.md`)**: the primary agent surface. Create `.github/agents/<name>.agent.md` at repository scope or the equivalent path in the user profile directory for cross-workspace agents. YAML frontmatter supports `name`, `description`, `tools` (list of tool identifiers such as `githubRepo`, `codebase`, `terminalLastCommand`), and `model`. The Markdown body is the system prompt. The agent appears in the Copilot agent picker once the file is present. Use [the Copilot agent template](../templates/copilot-agent.md).
- **Repository instructions (`.github/copilot-instructions.md`)**: always-on guidance for all Copilot interactions in the repository. Not a named agent; do not use it as a substitute for a `.agent.md` file.
- **Path-scoped instructions (`.instructions.md`)**: Markdown files placed in subdirectories or named locations with an optional `applyTo` frontmatter field. These provide context for specific file paths, not for creating a named agent.
- **Copilot Extension**: a full VS Code extension using the Copilot SDK for TypeScript/Python/.NET. Use only when the `.agent.md` surface cannot meet the stated requirements.

Generate a `.agent.md` file for a named-agent request and a builder brief for a Copilot Extension only when the user explicitly requires custom runtime behavior. Do not use the Copilot Extension path for a request that a `.agent.md` file can satisfy. Verify by opening the Copilot Chat agent picker (Configure Custom Agents…) and selecting the new agent, then invoking it with one representative request.

Sources: [GitHub Copilot custom agents](https://docs.github.com/en/copilot/customizing-copilot/building-a-custom-copilot-agent), [Copilot instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot).

## Windsurf

Windsurf's Cascade does not support named discrete agent files in the same way as other IDE-native agents. The closest equivalent is a **named rule file** inside `.windsurf/rules/` with a focused persona and strict operating constraints, combined with Cascade's Memories system for session-persistent context.

- **Project-wide rules (`.windsurfrules`)**: a single Markdown file at the project root. Cascade reads it on every request. Suitable for a single focused persona in a project.
- **Named rule file (`.windsurf/rules/<name>.md`)**: a Markdown file with an activation mode (Always On, or on-demand). Use XML-style tags to group role, operating rules, and boundaries for clarity. This is the recommended surface for a reusable, named agent persona because it is scoped and version-controlled.
- **Global rules**: managed through Windsurf Settings → AI → Global Rules; stored in `global_rules.md`. Apply globally across all workspaces. Do not use global rules for project-specific agents.
- **Cascade Memories**: auto-captured context that persists across sessions. Not a configuration file; not a substitute for a rule. Alert the user to review and prune Memories when updating agent rules.

Explain to the user that Windsurf does not have a discrete named-agent file format equivalent to `.agent.md` or a Custom Mode. The rule-file approach with XML grouping and Always On activation is the nearest supported equivalent. Use [the Windsurf rules template](../templates/windsurf-rules.md). Verify by reloading the workspace and confirming the rule appears active in Windsurf Settings → Workspace AI Rules, then issuing one representative request to Cascade.

Sources: [Windsurf rules documentation](https://docs.windsurf.com/windsurf/memories-and-rules), [Windsurf settings](https://docs.windsurf.com/windsurf/settings).

## Kiro

Kiro supports custom agents defined as JSON or Markdown files in `.kiro/agents/` (project scope) or `~/.kiro/agents/` (user scope). The filename (without extension) becomes the agent name unless overridden by the `name` field.

- **JSON format (`.kiro/agents/<name>.json`)**: use for programmatic generation or strict data structure needs. Key fields: `name`, `description`, `prompt` (system instruction string), `model`, `tools` (array of allowed tool names such as `"read"`, `"write"`, `"shell"`), `permissions.rules` (capability-level allow/deny rules including shell command glob patterns), `resources` (array of file or glob URIs, including `.kiro/steering/` documents), and `mcpServers`.
- **Markdown format (`.kiro/agents/<name>.md`)**: YAML frontmatter for the structured fields; Markdown body for the system prompt. Functionally equivalent to JSON; prefer for complex, human-readable prompts.
- **Steering files (`.kiro/steering/*.md`)**: project-wide always-on context documents (e.g., `product.md`, `tech.md`, `structure.md`). Include them in `resources` to inject them into the agent's context without embedding the content in the prompt. Not a substitute for the agent definition itself.
- **Hooks (`.kiro/hooks/*.json`)**: event-driven automation (e.g., `PostFileSave`, `PreToolUse`). Not agent definitions; do not conflate with custom agents.

Start with `tools: ["read"]` and only add `"write"` or `"shell"` when the user explicitly requires it. Use permission rules to restrict shell access to specific command patterns. Use [the Kiro agent template](../templates/kiro-agent.json). Local project agents take precedence over same-named global agents. Kiro hot-reloads changes without a session restart. Run `/upgrade-agent` if migrating an older configuration. Verify by selecting the agent from the Kiro agent picker and invoking it with one representative request.

Sources: [Kiro custom agents](https://kiro.dev/docs/agents/custom-agents), [Kiro steering](https://kiro.dev/docs/steering/overview), [Kiro hooks](https://kiro.dev/docs/hooks/overview).

## Google Agents CLI

The Google Agents CLI (`agents-cli`, package `google-agents-cli`) is a lifecycle tool for building, evaluating, and deploying agents implemented with the **Google Agent Development Kit (ADK)**. It is not an IDE-native agent runtime itself; the agent logic is Python code in `agent.py`, scaffolded by the CLI.

There are two surfaces to distinguish:

- **ADK agent project** (the actual agent): a Python project with `agent.py` (agent logic), `pyproject.toml` (dependencies), and optionally `DESIGN_SPEC.md` / `AGENTS.md` (design contract). The coding assistant does not define behavior in a single YAML or Markdown frontmatter file; it authors Python using ADK patterns. Produce a design specification from [the Google Agents CLI spec template](../templates/google-agents-cli-spec.md), then scaffold the project with the CLI.
- **agents-cli skills injected into a coding assistant**: running `uvx google-agents-cli setup` installs the CLI and injects ADK-specific skills (scaffold, eval, deploy, publish, observability, workflow) into the connected coding assistant. These are not custom agents in the IDE; they are skill bundles.

Workflow:
1. Produce a design specification (`DESIGN_SPEC.md`) that describes the agent's responsibility, inputs, deliverable, tools, ADK model, and deployment target.
2. Run `agents-cli create <agent-name>` to scaffold the Python project.
3. Implement the agent logic in `agent.py` following ADK patterns.
4. Run `agents-cli eval` with a test set to verify behavior before deployment.
5. Run `agents-cli deploy` (requires a Google Cloud project with Agent Platform and Cloud Run APIs enabled) or `agents-cli run` for local-only use.

Do not claim that a Markdown file or a rules file alone constitutes a deployed Google Agents CLI agent. The Python implementation is required. For a local prototype only, an AI Studio API key is sufficient; cloud deployment requires a Google Cloud project. Ask before triggering deployment, publishing to the Gemini Enterprise Agent Registry, or making infrastructure changes.

Sources: [google-agents-cli repository](https://github.com/google/agents-cli), [ADK documentation](https://google.github.io/adk-docs/), [Google Agents CLI blog announcement](https://blog.google/technology/google-deepmind/google-agents-cli/).

## OpenCode

Create Markdown agents in `.opencode/agents/<name>.md` for a project or `~/.config/opencode/agents/<name>.md` for the user. The file name defines the agent name. Frontmatter supports `description`, `mode` (`primary` or `subagent`), `model`, `temperature`, and `permission`; the Markdown body is the system prompt. Use [the OpenCode template](../templates/opencode-agent.md).

For quick authoring, `opencode agent create` asks for scope, description, permissions, and writes the Markdown file. Verify with the agent selector; invoke a subagent by `@name` and confirm a denied permission cannot execute.

Source: [OpenCode Agents](https://opencode.ai/docs/agents).

## Qoder

Create Markdown custom agents at `.qoder/agents/<name>.md` for a project or `~/.qoder/agents/<name>.md` for the user. Required frontmatter is `name` and `description`; the body is the system prompt. `tools`, `disallowedTools`, `model`, `skills`, `mcpServers`, `maxTurns`, `timeoutMins`, and `isolation: worktree` are optional and should be used only when needed. Use [the Qoder template](../templates/qoder-agent.md).

In the IDE, `/create-agent <requirement>` can create one interactively. In the CLI, `/agents` → User or Project → Create new agent is the recommended path. Reload after a manual change with `/agents reload`; verify discovery in `/agents` or `qodercli agents list`, then invoke by explicit name before relying on automatic matching.

Sources: [Qoder Custom Agent](https://docs.qoder.com/extensions/subagent), [Qoder CLI Subagents](https://docs.qoder.com/cli/subagent).

## Orca

Orca treats a CLI program as an agent launcher. Open Settings → Agents → Add custom agent, set the display name, verified binary/command, default arguments, and only a safe optional startup hook. Orca launches the command with the current worktree as working directory; it does not define the CLI agent's system prompt or permissions.

Create the underlying agent's own configuration first if its capabilities must be specialized. Verify by selecting the agent from the terminal combobox in a disposable worktree and confirm the command starts with the expected working directory.

Source: [Add a custom CLI agent](https://www.onorca.dev/docs/agents/custom-cli).
