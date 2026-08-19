# Target command formats and research

Last researched: 2026-08-19. Product command models change quickly. Re-check the linked primary documentation before writing or changing a command, and report an unsupported or plan-gated capability instead of guessing.

## Selection matrix

| Target | Native custom `/…` artifact | Best documented alternative when no native custom command exists | Do not claim |
| --- | --- | --- | --- |
| Antigravity | Markdown Workflow, invoked as `/workflow-name` | Rule for persistent behavior; Skill for reusable knowledge | A Rule is a command, or an undocumented file path works in the IDE |
| Codex | No user-authored `/name` artifact documented | Explicit Skill, invoked as `$skill-name` | `/skills` creates or invokes a custom command |
| ChatGPT | No user-authored `/name` artifact documented | Skill, selected with `@skill-name` | A typed text convention is a native slash command |
| Zed | Explicit Skill, invoked as `/skill-name` | Skill remains the native reusable-procedure model | A separate custom-command file exists |
| OpenCode | Markdown or JSON command | Skill, agent, or automation when the task is richer or unattended | A command changes the permission policy |
| Qoder | Markdown custom command | Skill for automatic/contextual behavior; Dynamic Workflow for orchestration | A command is a TUI extension or automation trigger |
| Orca | No custom agent slash-command definition documented | Quick Command, or a command supplied by the launched CLI agent | Orca Quick Commands are agent slash commands |

## Antigravity

Create a **Workflow** from the Agent panel’s **… → Customizations → Workflows** panel. Choose **Global** or **Workspace**, then provide a title, description, and ordered steps. The saved Markdown Workflow appears as `/workflow-name`; workflows can call other workflows and are limited to 12,000 characters. Use [the Antigravity template](../templates/antigravity-workflow.md) as the body outline.

Before saving, ensure that side effects such as deploy, publish, messaging, or deletion have an immediate approval gate. Confirm it appears in the Agent `/` list and invoke it with a read-only or non-production input.

Source: [Antigravity Workflows](https://antigravity.google/docs/ide/workflows?app=antigravity-ide).

## Codex

Codex does not document user-created literal `/name` commands. Use an **Agent Skill** for a reusable manual procedure. Create a portable `SKILL.md` with `name` and `description`, install it in `.agents/skills/<name>/` for a repository or `~/.agents/skills/<name>/` for the user, and set `policy.allow_implicit_invocation: false` in optional `agents/openai.yaml` when it must remain explicit-only.

In Codex CLI or the IDE extension, run `/skills` to browse skills or type `$` to mention one, for example `$review-api`. Use [the explicit Skill template](../templates/explicit-skill.md). Restart only if Codex does not detect the change automatically.

Source: [Build skills for ChatGPT and Codex](https://developers.openai.com/codex/skills).

## ChatGPT

ChatGPT’s documented reusable-procedure model is an **Agent Skill**, not a user-created slash command. Create it in **Plugins → Skills → Create** (with chat, editor, or upload), then select the skill in a conversation by typing `@`. Build the same portable Skill payload as for Codex, using [the explicit Skill template](../templates/explicit-skill.md), and make it clear in the delivery that invocation is `@skill-name` rather than `/skill-name`.

Creation, upload, installation, sharing, connector changes, or publishing affect external state. Draft the builder brief and request authority immediately before taking those actions. Verify availability by opening the Skills tab and selecting the skill in a harmless conversation.

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
