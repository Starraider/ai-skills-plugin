---
name: new-slash-command
description: Use when deciding whether a reusable task should be a slash command and when creating or revising a target-native command or the documented alternative for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca.
license: CC-BY-4.0
---

# New Slash Command

## Outcome

Create one safe, target-native, manually invoked shortcut for a repeated task—or explain why a slash command is the wrong mechanism and produce the smallest documented alternative. Deliver the decision, artifact or ready-to-paste builder brief, scope, invocation syntax, and a low-risk verification plan.

## Workflow

1. Establish the command contract before choosing a mechanism.

   Resolve the target product; desired outcome; intended invocation; required arguments and context; project or user scope; whether the command may read, edit, run shell commands, access the network, or make external writes; and the success and approval boundary. Inspect existing command, skill, agent, workflow, and configuration files before proposing a name.

   Ask one concise clarification question only when the target, desired outcome, or requested scope is missing. Do not infer an IDE or silently overwrite an existing same-named artifact.

   Completion: the request can be stated as “when the user explicitly invokes **X** with inputs **Y**, produce **Z**, and stop before **A**.”

2. Decide whether a slash command is the right abstraction.

   Use a slash command only when a user explicitly starts a compact, repeatable prompt or short procedure with a stable purpose, useful arguments, and a reviewable outcome. Prefer the smallest sufficient alternative when that test fails:

   - **One-off, exploratory, or still-changing work:** use a normal prompt or plan.
   - **Reusable instructions, domain knowledge, supporting scripts, or a context-dependent procedure:** use an Agent Skill. Make it explicit-only where the target documents that behavior.
   - **Persistent behavior or coding standards:** use a rule/instructions file.
   - **A long-lived specialist with its own tools, permissions, or context:** use an agent.
   - **Event-driven behavior:** use a hook, permission policy, CI, or automation—not a command.
   - **Scheduled, API-triggered, or unattended work:** use a task, automation, CI, or target-native orchestration.
   - **Multiple agents with delegation, shared state, or approvals:** use a workflow/orchestration feature.

   A command does not grant permissions or make side effects safe. For deploy, publish, delete, message, payment, or credential-affecting work, default to drafting or asking for approval immediately before the irreversible action.

   Completion: the recommendation names one mechanism, its trigger, and why a smaller or broader alternative is unsuitable.

3. Select exactly one target branch and read [target command formats and research](references/target-command-formats.md) before writing an artifact.

   - **Antigravity:** create a native Markdown Workflow; users invoke it as `/workflow-name`.
   - **Codex:** create an explicit Agent Skill; users invoke it with `$skill-name` (not a user-defined `/name` command).
   - **ChatGPT / ChatGPT Desktop App:** create an Agent Skill; users invoke it with `@skill-name` in desktop chat (not a user-defined `/name` command).
   - **Zed:** create an explicit Agent Skill with `disable-model-invocation: true`; users invoke it as `/skill-name`.
   - **OpenCode:** create a native Markdown custom command.
   - **Qoder:** create a native Markdown custom command.
   - **Orca:** create a Quick Command for a terminal command or launch-time agent prompt. If a slash command is required, create it in the hosted CLI agent using that agent's own documented extension model; Orca itself has no documented custom agent slash-command artifact.

   Completion: one current, documented target representation and scope are selected. For unsupported literal slash commands, state that limitation and use only the named alternative.

4. Write the smallest useful, explicit artifact.

   Use an action-oriented, collision-free lowercase name. Include a one-line purpose, the expected inputs, ordered instructions, the deliverable, verification, and stop/escalation conditions. Parameterize only stable inputs; do not use shell interpolation, file references, or tool calls for unreviewed input, secrets, or destructive defaults. Reuse the matching template in [templates](templates/) where the target supports a local file.

   Create only the requested local artifact after checking for a name collision. For product UI actions such as ChatGPT skill creation, Antigravity workflow creation, or Orca Quick Commands, produce a ready-to-paste builder brief first; make the external change only when authorized.

   Completion: the command or alternative is scoped correctly, contains no secrets, has no unrequested external side effects, and its body is understandable without hidden context.

5. Verify discovery, a safe happy path, and a stop path.

   Follow the target-specific reload/discovery instructions in [target command formats and research](references/target-command-formats.md). Invoke it with harmless or read-only input and confirm the stated deliverable. Test a missing argument, ambiguous target, or approval-required action and confirm it pauses, asks, or exits safely.

   Completion: the target can discover the artifact, the representative run follows its contract, and the safety boundary is observable. Otherwise report the exact version, permission, or product limitation.

## Safety

- Do not create a command that bypasses a client sandbox, permission model, approval prompt, or administrative restriction.
- Treat command definitions as executable prompt configuration. Read existing definitions before editing and never overwrite a same-named command, skill, or workflow without explicit authority.
- Never put tokens, passwords, API keys, personal data, or destructive shell interpolation in a command body or example.
- For an unavailable native command model, do not emulate a slash command with undocumented files or claim that a skill, workflow, agent, or Quick Command is a native slash command.

## Resources

- [Target command formats, alternatives, verification, and primary sources](references/target-command-formats.md)
- [Antigravity workflow template](templates/antigravity-workflow.md)
- [Portable explicit Skill template for Codex, ChatGPT, and Zed](templates/explicit-skill.md)
- [OpenCode command template](templates/opencode-command.md)
- [Qoder command template](templates/qoder-command.md)
