# Target command formats and research

Last researched: 2026-08-20. Product command models change quickly. Re-check the linked primary documentation before writing or changing a command, and report an unsupported or plan-gated capability instead of guessing.

## Selection matrix

| Target | Native custom `/…` artifact | Best documented alternative when no native custom command exists | Do not claim |
| --- | --- | --- | --- |
| Antigravity | Markdown Workflow, invoked as `/workflow-name` | Rule for persistent behavior; Skill for reusable knowledge | A Rule is a command, or an undocumented file path works in the IDE |
| Codex | No user-authored `/name` artifact documented | Explicit Skill, invoked as `$skill-name` | `/skills` creates or invokes a custom command |
| ChatGPT Desktop App | No user-authored `/name` artifact documented | Skill, selected with `@skill-name` | A typed text convention is a native slash command |
| Zed | Explicit Skill, invoked as `/skill-name` | Skill remains the native reusable-procedure model | A separate custom-command file exists |
| OpenCode | Markdown or JSON command | Skill, agent, or automation when the task is richer or unattended | A command changes the permission policy |
| Qoder | Markdown custom command | Skill for automatic/contextual behavior; Dynamic Workflow for orchestration | A command is a TUI extension or automation trigger |
| Orca | No custom agent slash-command definition documented | Quick Command, or a command supplied by the launched CLI agent | Orca Quick Commands are agent slash commands |
| Cursor | Markdown file in `.cursor/commands/` or `~/.cursor/commands/` → `/name` | Rule (`.cursor/rules/`) for persistent always-on behavior | A Rule and a command are interchangeable |
| GitHub Copilot / VS Code | `.prompt.md` in `.github/prompts/` or user profile → `/name` | `copilot-instructions.md` for always-on project context | A prompt file changes the permission policy or replaces custom instructions |
| Windsurf | Markdown file in `.windsurf/workflows/` → `/name` in Cascade | `.windsurfrules` for persistent always-on behavior | A workflow file and a rules file serve the same purpose |
| Kiro | Steering file in `.kiro/steering/` with `inclusion: manual` → `/filename` | Steering with `inclusion: always` for persistent context; custom agents for complex, tool-using workflows | A separate commands directory exists in Kiro; manual steering files are natively invoked as slash commands |
| Google Agents CLI (Gemini CLI) | TOML file in `.gemini/commands/` or `~/.gemini/commands/` → `/name` | Agent Skill for richer reusable context with supporting scripts | A TOML command and an Agent Skill are interchangeable |

## Antigravity

Create a **Workflow** from the Agent panel’s **… → Customizations → Workflows** panel. Choose **Global** or **Workspace**, then provide a title, description, and ordered steps. The saved Markdown Workflow appears as `/workflow-name`; workflows can call other workflows and are limited to 12,000 characters. Use [the Antigravity template](../templates/antigravity-workflow.md) as the body outline.

Before saving, ensure that side effects such as deploy, publish, messaging, or deletion have an immediate approval gate. Confirm it appears in the Agent `/` list and invoke it with a read-only or non-production input.

Source: [Antigravity Workflows](https://antigravity.google/docs/ide/workflows?app=antigravity-ide).

## Codex

Codex does not document user-created literal `/name` commands. Use an **Agent Skill** for a reusable manual procedure. Create a portable `SKILL.md` with `name` and `description`, install it in `.agents/skills/<name>/` for a repository or `~/.agents/skills/<name>/` for the user, and set `policy.allow_implicit_invocation: false` in optional `agents/openai.yaml` when it must remain explicit-only.

In Codex CLI or the IDE extension, run `/skills` to browse skills or type `$` to mention one, for example `$review-api`. Use [the explicit Skill template](../templates/explicit-skill.md). Restart only if Codex does not detect the change automatically.

Source: [Build skills for ChatGPT and Codex](https://developers.openai.com/codex/skills).

## ChatGPT Desktop App

In the ChatGPT Desktop App, the documented reusable-procedure model is an **Agent Skill**, not a user-created slash command. Upload the skill directory or archive in **Plugins → Skills → Create → Upload from your computer** (or create it with chat/editor), then select the skill in a conversation by typing `@`. Build the same portable Skill payload as for Codex, using [the explicit Skill template](../templates/explicit-skill.md), and make it clear in the delivery that invocation is `@skill-name` rather than `/skill-name`.

Creation, upload, installation, sharing, connector changes, or publishing affect external/local state. Draft the builder brief and request authority immediately before taking those actions. Verify availability by opening the Skills tab in the desktop app and selecting the skill in a harmless conversation.

Sources: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt), [Build skills for ChatGPT and Codex](https://developers.openai.com/codex/skills).

## Zed

Zed exposes **Agent Skills** directly as slash commands. Create `<worktree>/.agents/skills/<name>/SKILL.md` for a trusted project or `~/.agents/skills/<name>/SKILL.md` globally. Use the portable Skill body and set `disable-model-invocation: true` in frontmatter when the task must run only after the user types `/name`; the same skill may also be invoked with `@skill`.

Use [the explicit Skill template](../templates/explicit-skill.md). Create it through **AI → Skills**, the built-in `/create-skill`, or manually. Confirm it appears in the Skills Manager and invoke `/name` with harmless input. Do not edit an existing skill without explicit authorization: Zed protects Skill files from agent writes.

Source: [Zed Agent Skills](https://zed.dev/docs/ai/skills).

## OpenCode

Create a Markdown file at `.opencode/commands/<name>.md` for the project or `~/.config/opencode/commands/<name>.md` globally. Its filename becomes `/name`; the body becomes the prompt template. `description`, `agent`, and `model` are optional frontmatter. The same commands can instead be defined in `opencode.json`/`opencode.jsonc`.

Use [the OpenCode template](../templates/opencode-command.md). `$ARGUMENTS` and `$1`, `$2`, and so on support stable arguments. `!\`command\`` inserts shell output and `@path` includes file contents—use neither with untrusted input, secrets, or destructive commands. Confirm the command list shows `/name`, invoke a read-only test, and retain the existing OpenCode permission policy.

Source: [OpenCode Commands](https://opencode.ai/docs/commands/).

## Qoder

Create a Markdown file at `.qoder/commands/<name>.md` for a project or `~/.qoder/commands/<name>.md` for the user. It requires a `description` frontmatter field; `name` is optional display metadata because the invocation name comes from the file path. The body is the prompt submitted when the user types `/name`.

Use [the Qoder template](../templates/qoder-command.md). After adding or editing a command in a running CLI, use `/commands` to reload and inspect it. Invoke the command with a safe input. Qoder’s command documentation says user-level commands override project-level commands of the same name; check both scopes before adding a name.

Sources: [Qoder CLI Commands](https://docs.qoder.com/cli/commands), [Qoder IDE Custom Commands](https://docs.qoder.com/user-guide/commands).

## Orca

Orca hosts CLI agents in terminal tabs and does not document a custom agent slash-command definition. Use **Settings → Quick Commands** or the worktree tab bar’s **Add command** to create a global or project-scoped Quick Command. It can run a terminal command or a reusable launch-time prompt for agents such as Codex and Claude. Use it for a stable terminal action such as `pnpm test` or a repeated launch prompt.

If the user needs `/name` inside the agent conversation, create the command in the launched agent according to that agent’s documentation—for example, use a Codex Skill or an OpenCode command. Make clear that this is provided by the embedded agent, not by Orca. Validate first with a non-mutating command and do not run an external or destructive Quick Command without explicit authorization.

Sources: [Orca Terminal and Quick Commands](https://www.onorca.dev/docs/terminal), [Orca supported agents](https://www.onorca.dev/docs/agents/supported).

## Cursor

Create a **Markdown file** at `.cursor/commands/<name>.md` for the project or `~/.cursor/commands/<name>.md` globally. The filename (without extension) becomes the `/name` slash command that appears in the Cursor Chat and Agent panel. No frontmatter is required; the file body is the prompt submitted to the agent. Project-level and global commands are merged; project commands with the same name override global ones.

Use [the Cursor command template](../templates/cursor-command.md). Keep files under ~150 lines for context efficiency. Do not include secrets, destructive shell interpolation, or file references pointing to untrusted paths. Confirm the command appears in the `/` autocomplete list in the chat input and invoke it with a read-only or non-production input. Cursor rules (`.cursor/rules/`) serve a different purpose—they apply automatically and persistently; do not conflate them with slash commands.

Source: [Cursor Custom Commands](https://www.cursor.com/chat/commands).

## GitHub Copilot / VS Code

Create a **`.prompt.md` file** at `.github/prompts/<name>.prompt.md` for the workspace or in the VS Code user profile for global availability. The filename stem (the part before `.prompt.md`) becomes the `/name` slash command in Copilot Chat. Optional YAML frontmatter fields: `description` (shown in the autocomplete list), `name` (overrides the filename-derived invocation name), `agent` (`"agent"` enables multi-step agentic mode), `argument-hint`, and `tools` (list of tools the prompt may access, e.g. `[search, web]`).

Enable prompt files by setting `"chat.promptFiles": true` in VS Code `settings.json`. Additional workspace prompt directories can be configured via `chat.promptFilesLocations`. Use [the Copilot prompt template](../templates/copilot-prompt.md). After creating or editing a file, type `/` in Copilot Chat to confirm the command appears. For always-on project-wide context, use `copilot-instructions.md` instead—prompt files are for explicit, per-task invocation only. Do not put API keys, passwords, or destructive defaults in a prompt file.

Sources: [GitHub Copilot prompt files](https://code.visualstudio.com/docs/copilot/copilot-customization#_prompt-files), [VS Code Copilot Customization](https://code.visualstudio.com/docs/copilot/copilot-customization).

## Windsurf

Create a **Markdown file** at `.windsurf/workflows/<name>.md` for the project. The filename (without extension) becomes the `/name` slash command in the Cascade chat. The file body contains structured Markdown steps that Cascade executes when the command is invoked. Workflows can reference other workflows by including an instruction such as "Call /other-workflow-name". No frontmatter is required for basic use.

Use [the Windsurf workflow template](../templates/windsurf-workflow.md). Workflows may be created manually or through the Windsurf IDE via **Customizations → Workflows → + Workflow**. For always-on project behavior, use `.windsurfrules` instead. For cross-project user standards, use the global memories directory (`~/.codeium/windsurf/memories/global_rules.md`). After adding or editing a workflow file, confirm the command appears in the Cascade `/` autocomplete and invoke it with a non-destructive input.

Source: [Windsurf Workflows](https://docs.windsurf.com/windsurf/customization).

## Kiro

Kiro has **no separate commands directory**. The native slash-command model uses **steering files** with `inclusion: manual` in their YAML frontmatter. Create a Markdown file at `.kiro/steering/<name>.md` for the workspace or `~/.kiro/steering/<name>.md` globally. Set `inclusion: manual` as the first frontmatter field. The filename stem becomes the `/name` slash command in the Kiro agent chat. The file body provides context, instructions, or a procedure that is injected into the agent's context on demand.

```yaml
---
inclusion: manual
---
```

Use [the Kiro steering template](../templates/kiro-steering.md). Other inclusion modes (`always`, `fileMatch`) serve different purposes—do not use them for on-demand slash commands. For complex, tool-using workflows with specific permissions and models, create a **Custom Agent** in `.kiro/agents/`. After adding or editing a steering file, type `/` in the Kiro chat to confirm the command appears and invoke it with a harmless input. Do not embed secrets or destructive shell instructions in a steering file.

Sources: [Kiro Steering](https://kiro.dev/docs/steering/), [Kiro Slash Commands](https://kiro.dev/docs/slash-commands/).

## Google Agents CLI (Gemini CLI)

Create a **TOML file** at `.gemini/commands/<name>.toml` for the project or `~/.gemini/commands/<name>.toml` globally. The filename (without extension) becomes the `/name` slash command in the Gemini CLI. For namespaced commands, place the file in a subdirectory: `~/.gemini/commands/git/commit.toml` → `/git:commit`. Required field: `prompt` (the instruction sent to the model, multi-line strings use `"""`). Optional field: `description` (shown when listing commands). Use `{{args}}` in the prompt body to inject user-supplied arguments at runtime.

```toml
description = "One-line description of what the command does."

prompt = """
Your prompt here.

Inputs: {{args}}
"""
```

Use [the Gemini CLI command template](../templates/gemini-cli-command.toml). After adding or editing a TOML file, run `/commands reload` inside the CLI to pick up changes without restarting. Run `/commands list` to verify the command is registered. Invoke the command with a safe, read-only input. Project-level commands override global commands of the same name. Do not put secrets, passwords, or destructive shell interpolation in the `prompt` field. Note: `google-agents-cli` (`uvx google-agents-cli`) is a separate ADK lifecycle tool and is not the same as custom Gemini CLI slash commands.

Sources: [Gemini CLI Custom Commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md), [Gemini CLI Configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md).
