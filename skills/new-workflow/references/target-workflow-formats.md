# Target workflow formats and research

Last researched: 2026-08-19. Re-check the linked primary documentation before creating an artifact: workflow capabilities and UI surfaces change quickly.

## Selection matrix

| Target | Use for a manual reusable procedure | Use for scheduled / multi-agent work | Do not claim |
| --- | --- | --- | --- |
| Antigravity | Native Markdown Workflow | Use a workflow's explicit steps; choose a hook or task for an actual lifecycle/event reaction | Rules are workflows, or a project file path not documented by the IDE |
| Codex | Explicit Codex Skill | Eligible Workspace Agent via the Workspace Agents plugin | A separate local Codex workflow file exists |
| ChatGPT Desktop App | Explicit Agent Skill (`@skill-name`) | Workspace Agent (via web Agent Studio) for scheduled/API triggers; Scheduled Task for recurring prompts | A Task or desktop skill is a local workflow-file format |
| Zed | Explicit Agent Skill | Use a native agent, external automation, or CI when the work needs a trigger outside an agent request | Zed has a separate native workflow artifact |
| OpenCode | Markdown custom command | A Skill/agent for rich context; external scheduler/CI for unattended jobs | A custom command grants permissions or is an event trigger |
| Qoder | Markdown custom command | Dynamic workflow for true multi-agent orchestration; Headless mode/CI for unattended execution | The `/workflows` panel itself creates a custom command |
| Orca | A worktree task / agent prompt for one run | Scheduled Automation for recurring prompts; Orchestration for supervised multi-agent work | A portable `workflow` file or guessed automation syntax |

## Antigravity

Antigravity has a native workflow model: Markdown files with a title, description, and ordered instructions. Create it through the Agent panel’s **Customizations → Workflows** panel, choosing **Global** or **Workspace**. Invoke it as `/workflow-name`; one workflow may call another. Keep each workflow below the documented 12,000-character limit.

Write a short title/description and an ordered body using the workflow outline. Make deployment, notification, or publish steps approval-gated. Verify it appears in the Agent slash-command list, then run it with a non-production input.

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
