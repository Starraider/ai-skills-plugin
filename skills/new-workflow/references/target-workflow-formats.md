# Target workflow formats and research

Last researched: 2026-08-20. Re-check the linked primary documentation before creating an artifact: workflow capabilities, surfaces, and configuration models change quickly.

## Selection matrix

| Target | Use for a manual reusable procedure | Use for scheduled / multi-agent / automated work | Do not claim |
| --- | --- | --- | --- |
| Antigravity | Native Markdown Workflow (`/workflow-name`) | Use explicit workflow steps; choose a hook or task for actual lifecycle/event reaction | Rules are workflows, or an undocumented IDE project file path works |
| Codex | Explicit Codex Skill (`$skill-name`) | Eligible Workspace Agent via the Workspace Agents plugin | A separate local Codex workflow file format exists |
| ChatGPT Desktop App | Explicit Agent Skill (`@skill-name`) | Workspace Agent (via web Agent Studio) for scheduled/API triggers; Scheduled Task for recurring prompts | A Task or desktop skill is a local workflow-file format |
| Zed | Explicit Agent Skill (`/name` or `@skill`) | Use a native agent profile, external ACP agent, automation, or CI | Zed has a separate native workflow artifact |
| OpenCode | Markdown custom command (`/name`) | A Skill or Agent for rich context; external scheduler or CI for unattended jobs | A custom command grants permissions or is an event trigger |
| Qoder | Markdown custom command (`/name`) | Dynamic workflow for true multi-agent orchestration; Headless mode/CI for unattended execution | The `/workflows` panel itself creates a custom command |
| Orca | Worktree task / agent launch prompt for one run | Scheduled Automation for recurring prompts; Orchestration for supervised multi-agent work | A portable `workflow` file or guessed automation syntax |
| Cursor | Markdown command (`.cursor/commands/` → `/name`) or explicit Skill | Interactive Agent/Composer mode; CI or background tasks for unattended execution | `.cursor/rules/` (`.mdc`) is a workflow execution trigger |
| GitHub Copilot / VS Code | `.prompt.md` with `agent: "agent"` in `.github/prompts/` → `/name` | Agentic prompt workflow with tools; GitHub Actions (`.github/workflows/`) for CI/scheduled runs | `copilot-instructions.md` is a workflow file or overrides permissions |
| Windsurf | Native Markdown Workflow (`.windsurf/workflows/` → `/name`) | Sequential workflow execution with sub-workflow chaining (`Call /name`); CI for unattended jobs | `.windsurfrules` is a workflow file or workflows bypass approval prompts |
| Kiro | Steering file with `inclusion: manual` (`.kiro/steering/` → `/name`) | Custom Agent (`.kiro/agents/`) for tool-governed multi-step work; hooks (`.kiro/hooks/`) for events | A separate `.kiro/workflows/` directory exists |
| Google Agents CLI (Gemini CLI) | TOML command (`.gemini/commands/` → `/name`) or Agent Skill | ADK Python agent project (`agents-cli create/eval/run/deploy`) for orchestrated cloud workflows | A prompt file alone deploys an ADK agent without Python code |

## Antigravity

Antigravity has a native workflow model: Markdown files with a title, description, and ordered instructions. Create it through the Agent panel’s **Customizations → Workflows** panel, choosing **Global** or **Workspace**. Invoke it as `/workflow-name`; one workflow may call another. Keep each workflow below the documented 12,000-character limit.

Write a short title/description and an ordered body using [the workflow outline](../templates/workflow-outline.md). Make deployment, notification, or publish steps approval-gated. Verify it appears in the Agent slash-command list, then run it with a non-production input.

Source: [Antigravity Workflows](https://antigravity.google/docs/ide/workflows?app=antigravity-ide).

## Codex

Codex exposes reusable procedures as Agent Skills. Create an explicit skill when the sequence is context-dependent but user-triggered; follow the `new-skill` workflow and use `agents/openai.yaml` with `policy.allow_implicit_invocation: false` when explicit-only Codex invocation is required.

For Business or Enterprise workspaces with the **Workspace Agents** plugin enabled, create or edit a ChatGPT Workspace Agent as the repeatable workflow. It can be shared, scheduled, and API-triggered according to workspace permissions. Drafts may be edited through the plugin, while preview/run and some deployment controls stay in ChatGPT Agent Studio. If the plugin is absent, report that limitation instead of inventing a local workflow definition.

Verify a Skill with `/skills` and explicit invocation. Verify a Workspace Agent with its ChatGPT preview before sharing or enabling a schedule/API trigger.

Sources: [Codex Skills](https://developers.openai.com/codex/skills), [ChatGPT Workspace Agents](https://help.openai.com/en/articles/20001143/).

## ChatGPT Desktop App and ChatGPT

In the ChatGPT Desktop App, the native mechanism for a manual, user-invoked reusable procedure is an **Agent Skill** (`SKILL.md`), installed via **Plugins → Skills** and selected in desktop chat conversations by typing `@skill-name`.

For an organizational, multi-step governed process with named tools, guardrails, integrations, and schedules or API triggers, configure a **Workspace Agent** via ChatGPT’s web Agents area / Agent Studio. In **Agents**, create a draft, review its plan, add only necessary tools/files/skills, and preview representative inputs before creating or publishing it. Once published, Workspace Agents can be interacted with across ChatGPT surfaces including the Desktop App. Keep write actions at **Always ask** unless the user explicitly authorizes a narrower exception.

Use a **Scheduled Task** only for a simple prompt that should recur at a time/cadence or through the supported API. Tasks cannot use GPTs or file uploads and are limited to ten active tasks. Do not claim that the ChatGPT Desktop App has a local workflow definition file or treat a Scheduled Task as a general workflow file.

Creating, sharing, changing connectors, enabling a schedule, and adding an API trigger are external state changes. Produce a builder brief and obtain authority immediately before those changes.

Sources: [Workspace Agents](https://help.openai.com/en/articles/20001143/), [Scheduled Tasks](https://help.openai.com/en/articles/10291617-tasks-inchatgpt), [Skills in ChatGPT](https://help.openai.com/en/articles/20001066).

## Zed

Zed documents **Agent Skills** as reusable task instructions and explicitly calls out test-driven-development and deploy/release procedures as workflow-like use cases. Create a project skill at `<worktree>/.agents/skills/<name>/SKILL.md` or a global skill at `~/.agents/skills/<name>/SKILL.md`. For a workflow that must be manually selected—especially deploy or release—set `disable-model-invocation: true`; users can then invoke it with `/name` or `@skill`.

Use the Skills Manager or the skill creator to save it at the intended scope. Project skills require workspace trust and the agent cannot modify skill files without explicit authorization. Confirm it appears in the Skills Manager and run the explicit command with a harmless input.

Source: [Zed Skills](https://zed.dev/docs/ai/skills).

## OpenCode

Use a Markdown custom command for a compact, manually invoked prompt workflow. Create `.opencode/commands/<name>.md` for a project or `~/.config/opencode/commands/<name>.md` globally. The filename becomes `/name`; the Markdown body is the prompt template. `description`, `agent`, and `model` are optional frontmatter fields. Use `$ARGUMENTS` or positional arguments only where they improve a stable interface.

Do not use shell-output interpolation for unreviewed user input, secrets, or destructive defaults. A command does not grant permissions: retain the agent's permission policy. Verify by opening the command list and invoking it with a read-only test input.

Source: [OpenCode Commands](https://opencode.ai/docs/commands/).

## Qoder

For a compact single-agent workflow, create a Markdown custom command at `.qoder/commands/<name>.md` for the project or `~/.qoder/commands/<name>.md` for the user. It requires `name` and `description` frontmatter and a Markdown system prompt body. Reload with `/commands` and invoke as `/name`.

Use **Dynamic workflows** from `/workflows` only when the task actually needs agents to divide work, share results, and advance a multi-agent plan. Use the UI and re-check its current guidance rather than inventing a workflow-file schema. For headless, scheduled, or CI-like execution, use Qoder’s documented headless or scheduling facilities and preconfigure only the minimum permissions.

Sources: [Qoder Commands](https://docs.qoder.com/cli/commands), [Qoder Working Modes](https://docs.qoder.com/cli/working-modes).

## Orca

Orca is a worktree-native IDE for launching existing CLI agents; it does not document a generic portable workflow-definition file. For a recurring prompt against a repository or existing worktree, use **Scheduled Automations**. For a supervised multi-agent graph, use **Orchestration**. For one coding run, create a worktree task and give the chosen agent a bounded prompt.

Before modifying Orca, use the `orca-cli` skill for automations or the `orchestration` skill for task graphs. Each loads the current binary’s version-matched guide using `orca skills get ...`; do not guess commands or configuration syntax. Verify drafts with a low-risk prompt and retain human review before enabling recurring execution, mutation, or external actions.

Sources: [Orca CLI overview](https://www.onorca.dev/docs/cli/overview), [Orca skills registry and orchestration](https://www.onorca.dev/docs/cli/skills), [Orca worktrees](https://www.onorca.dev/docs/model/worktrees).

## Cursor

In Cursor, repeatable manual workflows are defined as **Markdown commands** in `.cursor/commands/<name>.md` for a project or `~/.cursor/commands/<name>.md` globally. The filename stem becomes the `/name` slash command in Cursor Chat, Agent, and Composer. The file body contains ordered, step-by-step instructions.

For a richer, context-dependent procedure that includes supporting scripts or reference files, create an **Agent Skill** in `.cursor/skills/<name>/SKILL.md` or `.agents/skills/<name>/SKILL.md` with `disable-model-invocation: true`.

Cursor rules (`.cursor/rules/<name>.mdc`) serve a different purpose: they provide persistent, always-on or glob-matched project context and coding conventions to any active mode; they are not invocation-triggered workflows. Custom Modes (configured in Settings → Features → Chat → Custom Modes) define agent personas with tool permission boundaries, but are UI-configured rather than version-controlled workflow files.

Use [the Cursor workflow template](../templates/cursor-workflow.md). Keep workflow files concise and focused. Verify by confirming the command appears in the `/` autocomplete list in Cursor Chat and executing it with a read-only input.

Sources: [Cursor Custom Commands](https://www.cursor.com/chat/commands), [Cursor Agent Skills](https://cursor.com/docs/skills), [Cursor Rules](https://www.cursor.com/en/docs/context/rules).

## GitHub Copilot / VS Code

In GitHub Copilot and VS Code, user-invoked prompt workflows are defined as **Prompt Files** (`.prompt.md`) located in `.github/prompts/<name>.prompt.md` (project) or the VS Code user profile (global). The filename stem becomes the `/name` slash command in Copilot Chat.

To turn a prompt file into an autonomous, multi-step agentic workflow, set `agent: "agent"` and specify allowed `tools` (e.g. `[search, codebase, fetch]`) in the YAML frontmatter. Enable prompt files by setting `"chat.promptFiles": true` in VS Code `settings.json`.

For automated, scheduled, or event-driven repository workflows (e.g. nightly builds, PR validation, automated releases), use **GitHub Actions** (`.github/workflows/*.yml`) or Copilot Workspace agents. For deterministic editor build and test tasks, use VS Code tasks (`.vscode/tasks.json`). `copilot-instructions.md` provides always-on repository context, not an on-demand workflow.

Use [the Copilot prompt workflow template](../templates/copilot-prompt-workflow.md). Verify by typing `/` in Copilot Chat, confirming the workflow command appears, and running a test execution with read-only inputs.

Sources: [GitHub Copilot Prompt Files](https://code.visualstudio.com/docs/copilot/copilot-customization#_prompt-files), [VS Code Copilot Customization](https://code.visualstudio.com/docs/copilot/copilot-customization).

## Windsurf

Windsurf provides a native **Workflows** feature. Workflows are Markdown files located in `.windsurf/workflows/<name>.md` at the project level, or created via the IDE through **Customizations → Workflows → + Workflow**. The filename stem becomes the `/name` slash command in Cascade chat.

When invoked, Cascade executes the ordered steps in the workflow file sequentially. Workflows can reference and chain other workflows by including instructions such as "Call /<sub-workflow-name>".

For always-on project rules and style guidelines, use `.windsurfrules`. For cross-project persistent standards, use global memories (`~/.codeium/windsurf/memories/global_rules.md`). Workflows do not bypass Cascade's safety prompts for destructive edits or terminal execution.

Use [the Windsurf workflow template](../templates/windsurf-workflow.md). Verify by checking that the workflow appears in Cascade's `/` autocomplete list and running a representative test with non-destructive inputs.

Sources: [Windsurf Workflows](https://docs.windsurf.com/windsurf/customization), [Windsurf Memories and Rules](https://docs.windsurf.com/windsurf/memories-and-rules).

## Kiro

Kiro supports two primary native workflow mechanisms depending on complexity:

1. **Manual Steering Workflows (`.kiro/steering/<name>.md`)**: for prompt-based, on-demand procedures. Set `inclusion: manual` in the YAML frontmatter. The filename stem becomes the `/name` slash command in Kiro agent chat. When invoked, Kiro injects the ordered procedural instructions into the agent context.
2. **Custom Agents (`.kiro/agents/<name>.json` or `.kiro/agents/<name>.md`)**: for multi-step, tool-using, or governed workflows. Configure specific tool capabilities (`read`, `write`, `shell`), permission rules, resources (including steering files), and model parameters.
3. **Event-driven workflows**: use **Kiro hooks** (`.kiro/hooks/*.json`) for automated reactions to IDE lifecycle events (e.g. `PostFileSave`, `PreToolUse`).

Do not claim that a separate `.kiro/workflows/` directory exists. Use [the Kiro steering workflow template](../templates/kiro-steering-workflow.md). Verify by typing `/` in Kiro chat, selecting the workflow, and running a harmless test prompt.

Sources: [Kiro Steering](https://kiro.dev/docs/steering/), [Kiro Custom Agents](https://kiro.dev/docs/agents/custom-agents), [Kiro Slash Commands](https://kiro.dev/docs/slash-commands/).

## Google Agents CLI (and Gemini CLI)

There are two distinct workflow surfaces to understand:

1. **Google Agents CLI (`google-agents-cli` / ADK)**: A full lifecycle framework for building, evaluating, and deploying production agent workflows implemented with the **Google Agent Development Kit (ADK)** in Python (`agent.py`, `pyproject.toml`, `DESIGN_SPEC.md`). Use this for multi-step agent graphs, orchestrated tool pipelines, and cloud-deployed workflows.
   - Scaffold with `agents-cli create <workflow-name>`.
   - Specify the design in `DESIGN_SPEC.md` using [the Google Agents CLI workflow spec template](../templates/google-agents-cli-workflow-spec.md).
   - Evaluate multi-step behavior with `agents-cli eval --agent <name> --test-set evals/<name>_eval.json`.
   - Run locally with `agents-cli run --agent <name>`.
   - Deploy to Cloud Run or Google Cloud Agent Platform with `agents-cli deploy`. Running `uvx google-agents-cli setup` injects ADK workflow skills into supported coding assistants.
2. **Gemini CLI Custom Commands (`.gemini/commands/<name>.toml`)**: For compact, user-invoked prompt workflows in the Gemini CLI. Create `.gemini/commands/<name>.toml` (project) or `~/.gemini/commands/<name>.toml` (global). The filename becomes `/name` (or `/subfolder:name` for subdirectories). Use `prompt` with `{{args}}` argument placeholders and optional `description`. Reload with `/commands reload`. Use [the Gemini CLI workflow template](../templates/gemini-cli-workflow.toml).

Do not claim that a Markdown or TOML file alone deploys an ADK agent workflow without Python code. Require explicit user approval before triggering cloud deployment, publishing to the Gemini Enterprise Agent Registry, or enabling external writes.

Sources: [google-agents-cli](https://github.com/google/agents-cli), [ADK documentation](https://google.github.io/adk-docs/), [Gemini CLI Commands](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md), [Gemini CLI Configuration](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md).
