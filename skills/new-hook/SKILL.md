---
name: new-hook
description: Use when deciding whether a lifecycle or event hook is the right solution, or when creating or revising one for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca. Select exactly one target and documented event model; recommend a Skill, plugin/app, permission policy, task, automation, or CI when a hook is unsupported or unsuitable.
---

# New Hook

## Outcome

Create one narrow, deterministic, and testable hook for a selected product, or explicitly recommend the better-supported alternative. Produce only the configuration and source files required for that target, with installation, trust/reload, and smoke-test instructions.

## Workflow

1. Establish the event contract before choosing a mechanism.

   Require the target product, the event that must cause the action, the input to inspect, the intended effect, project or user scope, and whether the hook may block, rewrite, write, send network traffic, or invoke an external service. Ask one concise clarification question if the target or trigger is missing.

   Completion: the desired behavior can be expressed as “when **event X** happens, inspect **input Y**, then **allow/block/transform/observe action Z**.”

2. Decide whether a hook is appropriate.

   A hook is appropriate only when all of these are true:

   - The behavior is deterministic and event-driven, rather than a judgment the model should make.
   - The chosen client documents an event at the required point in time.
   - The required effect is supported (for example, a pre-action guard may block; a post-action formatter cannot undo a completed action).
   - The work can be fast, idempotent where repeated events are possible, and safe if invoked unexpectedly or concurrently.

   Prefer another mechanism when any condition fails:

   - **Skill or instruction:** reusable reasoning, authoring guidance, or a workflow that needs context and judgment.
   - **Permission policy:** a standing allow/ask/deny rule that does not need custom inspection.
   - **MCP server, app, or plugin:** a new capability or a maintained integration rather than an event reaction.
   - **Task, worktree setup, CI, or scheduler:** a build/deploy/check that is tied to a worktree, commit, time, or repository event instead of an agent lifecycle event.
   - **ChatGPT:** do not invent a local lifecycle hook. Use a Skill for repeatable behavior, a Plugin/App/MCP integration for tools, or an approved scheduled/Workspace Agent workflow when that is the actual need.

   Explain the recommendation before creating files when it is not a hook.

   Completion: the selected mechanism has a documented trigger and the smallest sufficient authority.

3. Select exactly one target branch and read its operative details in [target hook formats and research](references/target-hook-formats.md).

   - **Antigravity:** configure a JSON command hook in workspace `.agents/hooks.json`, global `~/.gemini/config/hooks.json`, or a plugin `hooks.json` only when a plugin is requested.
   - **Codex:** use `<repo>/.codex/hooks.json` or inline hook tables in `<repo>/.codex/config.toml`; keep the two representations separate in one config layer.
   - **ChatGPT:** report that a comparable local lifecycle hook is not documented and take the alternative branch from step 2.
   - **Zed:** create or revise a `tasks.json` task with `hooks: ["create_worktree"]`; do not claim Zed has general agent lifecycle hooks.
   - **OpenCode:** create a TypeScript/JavaScript plugin, register it in `opencode.json` or `opencode.jsonc`, and use the documented runtime hook API.
   - **Qoder:** add the target-specific JSON configuration to `.qoder/settings.json`, `.qoder/settings.local.json`, or `~/.qoder/settings.json`; create the referenced handler.
   - **Orca:** use an existing compatible Codex or Claude hook for agent lifecycle behavior, or configure a Repository worktree-setup hook for post-worktree setup. Do not fabricate an Orca event-hook file.

   Completion: exactly one implementation model and one scope are selected; unsupported targets receive an alternative rather than pseudo-configuration.

4. Implement the smallest safe handler and registration.

   Read JSON from stdin only when the target sends it; parse only fields needed for the decision and validate their types. Make command paths explicit, quote path values, use a short timeout, write diagnostics to stderr, and emit only the target’s documented stdout shape. Prefer an exec-form command if the target supports it and shell parsing adds no value.

   Default to observation. For blocking hooks, block a precisely defined unsafe condition and return an actionable reason; never use a broad matcher or an unconditional deny as a substitute for permissions. For post-event work, make duplicate delivery harmless and do not claim it rolls back a completed tool call. Keep secret values out of config, source, logs, and hook output.

   Preserve unrelated settings and existing hooks. Never replace a whole shared settings file merely to add one hook.

   Completion: the handler, matcher, event, output contract, timeout, and scope each map to the stated event contract.

5. Verify loading, behavior, and the failure path.

   First validate syntax with the native parser or a language checker. Then follow the target’s reload/trust instructions in [target hook formats and research](references/target-hook-formats.md), trigger one representative event, and confirm the observable result. For a guard, test both an allowed input and a prohibited input; for a post-event hook, confirm it never claims to reverse the original action.

   Completion: the hook is loaded, its matcher fires only where expected, a normal request still succeeds, and the intended effect or block reason is observed.

## Safety

- A hook is executable code at a sensitive lifecycle boundary. Do not create or enable it without clear authority to edit the selected local configuration.
- Treat hooks as defense-in-depth, not a complete security boundary. Retain the client’s sandbox and permission controls.
- Do not place credentials in hook configuration, command strings, source, logs, or test fixtures. Use the target’s approved environment/secret mechanism and redact diagnostics.
- Never auto-run destructive commands, make external writes, or widen permissions merely because an event fires. Require an explicit condition and, where feasible, a user confirmation at the action boundary.
- Avoid network calls and long-running work in synchronous hooks. Use a background service, CI, task, scheduler, or plugin when latency, retries, durability, or observability matter.

## Resources

- [Target hook formats, decision limits, validation, and primary-source links](references/target-hook-formats.md)
