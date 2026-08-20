---
name: new-workflow
description: Use when deciding whether a repeatable workflow is appropriate and when creating or revising a target-native workflow for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, Orca, Cursor, GitHub Copilot / VS Code, Windsurf, Kiro, or Google Agents CLI.
license: CC-BY-4.0
---

# New Workflow

## Outcome

Create one focused, repeatable workflow in the selected product's documented form, or recommend a smaller, better-supported mechanism. Produce the workflow definition or builder brief, its scope and invocation/trigger, explicit approval boundaries, and a representative verification plan.

## Workflow

1. Establish the workflow contract before selecting a mechanism.

   Resolve the target product; the repeated outcome; trigger (manual, schedule, external event, or agent lifecycle); inputs; ordered decisions/actions; expected output; project or personal scope; frequency; and whether the workflow may edit, execute commands, access the network, or make external writes. Also identify the review/approval point and what must stop or escalate.

   Ask one concise clarification question if the target, repeated outcome, or trigger is missing. Do not choose a target on the user's behalf.

   Completion: the workflow can be described as “when **trigger X** occurs, use **inputs Y** to produce **result Z**, stopping for **condition A**.”

2. Decide whether a workflow is the right abstraction.

   A workflow is appropriate when the work recurs, has a useful repeatable sequence or handoff, has an observable output, and can be reviewed or safely stopped. Prefer the smallest sufficient alternative when that test fails:

   - **One-off or exploratory work:** use a normal prompt or plan; do not fossilize an unproven process.
   - **Reusable reasoning or a context-dependent procedure:** use an Agent Skill; make side-effectful procedures explicit-only where the target supports it.
   - **A short manual prompt shortcut:** use a custom slash command.
   - **A standing specialist with tools, data, or long-lived ownership:** use an agent.
   - **A deterministic lifecycle reaction or standing access rule:** use a hook or permission policy.
   - **Time- or API-triggered unattended work:** use the target's task/automation/agent scheduling surface.
   - **Repository events, reproducibility, or merge gates:** use CI or a repository task.

   Explain the choice before creating an artifact when it is not a native workflow.

   Completion: the selected mechanism has a documented trigger, a bounded purpose, and no broader authority than the requested outcome.

3. Select exactly one target branch and read [target workflow formats and research](references/target-workflow-formats.md).

   - **Antigravity:** create a native Markdown Workflow through the IDE's Workflows customization panel; it is manually invoked as `/workflow-name`.
   - **Codex:** use an eligible ChatGPT Workspace Agent through the Workspace Agents plugin for a shared, scheduled, or API-triggered workflow. If it is unavailable, create an explicit Codex Skill for a reusable procedure; Codex does not document a separate local workflow file.
   - **ChatGPT / ChatGPT Desktop App:** for a manual reusable procedure in desktop chat, create an explicit Agent Skill (invoked via `@skill-name`). For governed multi-step work across tools or schedules, use a Workspace Agent (configured via web Agent Studio); use a Scheduled Task only for a simple time/API-triggered prompt without a reusable agent configuration.
   - **Zed:** create an explicit-invocation Agent Skill for a reusable procedure; Zed documents Skills—not a separate workflow artifact—for reusable task instructions.
   - **OpenCode:** create a Markdown custom command for a manually invoked prompt workflow. Use a skill or agent instead when the procedure needs conditional resources or a specialist tool boundary.
   - **Qoder:** create a Markdown custom command for a single-agent reusable procedure. Use Dynamic workflows from `/workflows` only for actual multi-agent decomposition and orchestration.
   - **Orca:** use Scheduled Automations for recurring prompts, or Orca Orchestration for a supervised multi-agent task graph. There is no generic local workflow file; load the version-matched Orca guide before mutating Orca state.
   - **Cursor:** create a Markdown command in `.cursor/commands/<name>.md` (project) or `~/.cursor/commands/<name>.md` (global) invoked as `/name`, or an explicit Agent Skill in `.cursor/skills/<name>/SKILL.md` (`disable-model-invocation: true`). For persistent rules use `.cursor/rules/<name>.mdc` (not a workflow); for UI chat personas use a Custom Mode.
   - **GitHub Copilot / VS Code:** create a `.prompt.md` file in `.github/prompts/<name>.prompt.md` (workspace) or user profile (global) with `agent: "agent"` and `tools: [...]` for multi-step agentic execution, invoked as `/name` in Copilot Chat. For CI/automated repository-wide workflows, use GitHub Actions (`.github/workflows/`).
   - **Windsurf:** create a native Markdown Workflow in `.windsurf/workflows/<name>.md` (project) or via **Customizations → Workflows**, invoked as `/name` in Cascade chat. Steps execute sequentially and can chain sub-workflows with "Call /sub-workflow". For persistent project rules, use `.windsurfrules`.
   - **Kiro:** create a manual steering workflow in `.kiro/steering/<name>.md` with frontmatter `inclusion: manual` (invoked as `/name`), or create a Custom Agent in `.kiro/agents/<name>.json` / `.kiro/agents/<name>.md` for tool-governed multi-step workflows. For event-triggered workflows, use `.kiro/hooks/`.
   - **Google Agents CLI (and Gemini CLI):** for an ADK-based multi-step agent workflow, create a design specification (`DESIGN_SPEC.md`) and scaffold with `agents-cli create <name>`, implementing `agent.py` and verifying with `agents-cli eval` before `agents-cli deploy`. For Gemini CLI prompt workflows, create a TOML command in `.gemini/commands/<name>.toml` (invoked as `/name`) using argument placeholders (`{args}`).

   Completion: one target-native representation and one scope are selected. The output names any availability or plan restriction instead of fabricating configuration.

4. Write the smallest reviewable workflow.

   Give it an action-oriented name and a description that names its trigger, inputs, and deliverable. Write a short, ordered procedure that states prerequisites, input validation, evidence to inspect, each consequential action, the expected output, verification, and stop/escalation conditions. Parameterize genuinely variable inputs; never hide destructive defaults inside a reusable prompt.

   Use [the workflow outline](templates/workflow-outline.md) or target-specific template in [templates](templates/) for the instructions/body. Adapt only the target's documented metadata and syntax from the reference. Keep an invocation-only workflow manual unless automatic activation is clearly safe and documented.

   Completion: a new operator can tell what starts the workflow, what it may do, what success looks like, and when human review is required.

5. Create only the requested artifact and preserve existing configuration.

   For local files, create the target-native file and parent directory only after checking for a same-named artifact. Do not overwrite an existing workflow, command, skill, or agent without explicit update authority. For ChatGPT, Antigravity UI workflows, or Orca configuration, produce a ready-to-paste builder brief first and perform UI/remote creation only with authority to make that external change.

   Completion: the artifact is in the requested scope, contains no secrets, and makes no unrelated configuration changes.

6. Verify discovery, execution, and the stop path.

   Follow the target-specific discovery/reload check in the reference. Invoke the workflow with a representative, low-risk input and confirm its deliverable. Test an invalid, missing, or approval-required input to prove the workflow pauses or escalates rather than proceeding. For scheduled or API-triggered workflows, validate the draft/preview or a non-production test before enabling the trigger.

   Completion: the target can discover the workflow, the happy path produces the declared result, and the safety boundary is observable; otherwise report the exact product or permission blocker.

## Safety

- Do not use a workflow merely to bypass sandbox, permission, or approval controls. Tool permissions and prompts are separate controls.
- Default to read-only and draft-only behavior. Require explicit authorization immediately before enabling schedules, API triggers, network side effects, deployment, publication, messaging, or other external writes.
- Never embed API keys, tokens, passwords, or personal credentials in instructions, command files, scheduled prompts, or examples.
- Keep workflows idempotent where repetition is possible. State the source of truth, prevent duplicate external writes, and stop on ambiguous inputs rather than guessing.
- Do not claim a format is portable across products. When a product lacks the requested workflow model, recommend the documented alternative.

## Resources

- [Target workflow formats, selection guidance, validation, and primary sources](references/target-workflow-formats.md)
- [Universal workflow instruction outline](templates/workflow-outline.md)
- [Windsurf native workflow template](templates/windsurf-workflow.md)
- [GitHub Copilot prompt workflow template](templates/copilot-prompt-workflow.md)
- [Cursor command workflow template](templates/cursor-workflow.md)
- [Kiro manual steering workflow template](templates/kiro-steering-workflow.md)
- [Gemini CLI TOML workflow template](templates/gemini-cli-workflow.toml)
- [Google Agents CLI / ADK workflow spec template](templates/google-agents-cli-workflow-spec.md)
