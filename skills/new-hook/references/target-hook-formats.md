# Target hook formats and research

Last verified: 2026-08-19. Re-check the linked primary documentation immediately before publishing or enabling a hook; lifecycle APIs are fast-moving and a hook has executable authority.

## Decision table

| Target | Use a hook when | Do not use it when | Native model |
| --- | --- | --- | --- |
| Antigravity | A command must run before/after a documented agent action or lifecycle point | The task needs model judgment, durable queues, or broad plugin functionality | JSON command hook |
| Codex | A local deterministic script must observe, gate, rewrite, or augment a documented lifecycle event | A permission rule or skill suffices, or the action involves hosted tools not on the local hook path | JSON or inline TOML command hook |
| ChatGPT | Never claim a local lifecycle hook | The request needs repeatable behavior, scheduled work, or an integration | Skill, Plugin/App/MCP, or approved automation/workspace workflow |
| Zed | Only setup immediately after Zed creates a linked worktree | The desired trigger is an agent/tool/message lifecycle event | `tasks.json` `create_worktree` task hook |
| OpenCode | The behavior needs a plugin-level transform or runtime interception | A Skill, permission setting, or ordinary command is enough | TypeScript/JavaScript plugin API |
| Qoder | A documented IDE/CLI lifecycle event needs a deterministic handler | A static permission rule or a slow/durable workflow is better | JSON hook with command/http; CLI also has prompt/agent handlers |
| Orca | A compatible underlying agent hook or post-worktree setup command has the needed trigger | An Orca-native arbitrary event hook is assumed | Reused `.codex`/`.claude` hooks or Repository worktree setup |

## Common design rules

Write the event contract before code. State the event, matcher/filter, inputs examined, output/effect, duration bound, idempotency behavior, and authority boundary. Match narrowly and start with observation; then add a precise block or transformation only when the platform supports it.

Keep a synchronous handler fast. Do not perform retries, polling, unbounded scans, package installs, or network-dependent work in a pre-action guard. Parse stdin as untrusted JSON, log diagnostics to stderr without secrets, and print only target-protocol output to stdout. Treat any post-action hook as unable to undo the action it observed.

## Antigravity

Use `.agents/hooks.json` for workspace scope or `~/.gemini/config/hooks.json` for the user. A plugin may instead contain `hooks.json` at its root. The file maps a named hook to event arrays. `PreToolUse` and `PostToolUse` can filter tool names with a regex matcher; `PreInvocation`, `PostInvocation`, and `Stop` do not use the matcher. The handler is a command, receives JSON on stdin, and must return JSON on stdout.

```json
{
  "safe-bash": {
    "PreToolUse": [
      {
        "matcher": "run_command",
        "hooks": [
          {
            "type": "command",
            "command": "./.agents/hooks/check-command.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

For a pre-tool guard, use its `decision` output (`allow`, `deny`, or `ask`) only as documented. Test by piping a representative JSON object into the handler and then triggering the matching agent tool. Inspect loaded hooks with `/hooks`.

Sources: [Hooks](https://antigravity.google/docs/hooks), [IDE plugins](https://antigravity.google/docs/ide/plugins?app=antigravity-ide-).

## Codex

Use `<repo>/.codex/hooks.json` for a project hook or `~/.codex/hooks.json` for a user hook. The same layer can instead use inline `[[hooks.<Event>]]` tables in `config.toml`; do not use both representations in one layer. Codex merges matching hooks from active sources, runs matching command hooks concurrently, and requires review/trust for non-managed hooks.

```json
{
  "description": "Optional local safety hook.",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "^Bash$",
        "hooks": [
          {
            "type": "command",
            "command": "/usr/bin/python3 \"$(git rev-parse --show-toplevel)/.codex/hooks/check_command.py\"",
            "timeout": 10,
            "statusMessage": "Checking command"
          }
        ]
      }
    ]
  }
}
```

Important events include `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PermissionRequest`, `PostToolUse`, `PreCompact`, `PostCompact`, `SubagentStart`, `SubagentStop`, `Stop`, and `SessionEnd`. `PreToolUse` receives fields including `tool_name` and `tool_input`; it can block a supported local tool by returning a JSON `hookSpecificOutput` with `permissionDecision: "deny"` and a reason. It can add context or return an allowed `updatedInput`; it cannot ask. Hosted tools do not use this local hook path, so do not represent it as an exhaustive security boundary.

Validate JSON with `jq empty .codex/hooks.json`, review/trust the discovered hook in Codex, then run a safe matching command and a deliberately prohibited one. Keep the handler output small.

Sources: [Codex Hooks](https://developers.openai.com/codex/hooks), [Codex configuration](https://developers.openai.com/codex/config-reference).

## ChatGPT

As of this verification, ChatGPT’s documented reusable workflow mechanism is a Skill; its Plugins can package Skills with Apps and app templates. The product documentation does not document a user-configured local pre/post tool or response lifecycle-hook file comparable to Codex, Antigravity, OpenCode, or Qoder.

Do not write fictitious `hooks.json`, browser-script, or webhook configuration for a ChatGPT “hook.” Explain the constraint and choose the request’s real mechanism: a Skill for deterministic operating guidance, a Plugin/App/MCP tool for an integration, or an approved scheduled/Workspace Agent workflow for a time-triggered outcome. Creation, connection, scheduling, publication, and external writes remain user-authorized operations.

Sources: [Skills in ChatGPT](https://help.openai.com/en/articles/20001066), [Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex).

## Zed

Zed documents a task hook—not a general agent lifecycle hook. Register a task template in the normal global or worktree-local `tasks.json` and add `"hooks": ["create_worktree"]`. It runs after Zed creates a linked Git worktree and receives `ZED_WORKTREE_ROOT` and `ZED_MAIN_GIT_WORKTREE`.

```json
[
  {
    "label": "copy .env into new worktree",
    "command": "cp",
    "args": ["$ZED_MAIN_GIT_WORKTREE/.env", "$ZED_WORKTREE_ROOT/.env"],
    "hooks": ["create_worktree"],
    "reveal": "no_focus",
    "hide": "on_success"
  }
]
```

Use this only for setup that is safe to run after every created worktree. Test it with a disposable linked worktree and verify source/destination paths before copying any sensitive local files.

Source: [Zed Tasks—Hooks](https://zed.dev/docs/tasks#hooks).

## OpenCode

OpenCode hooks are code in a TypeScript/JavaScript plugin. Add the local module or package to the `plugins` array in `opencode.json` or `opencode.jsonc`; a local entry starts with `./` or `../` and resolves from that config file. Export `Plugin.define` as the module default.

```ts
import { Plugin } from "@opencode-ai/plugin"

export default Plugin.define({
  id: "acme.command-guard",
  setup: async (ctx) => {
    await ctx.tool.hook("execute.before", (event) => {
      if (event.tool !== "bash" || typeof event.input !== "object" || event.input === null) return
      // Inspect or replace event.input only when the target API permits it.
    })
  },
})
```

Runtime hooks include session context, HTTP request/response, and tool execution before/after callbacks. Hook failures fail the intercepted operation, so catch expected errors inside the callback and keep it fast. Use transform hooks when changing configuration rather than intercepting a live operation. Install compatible dependencies locally and verify activation with `opencode2 api get /api/plugin` where the V2 API is available.

Source: [OpenCode Plugins](https://opencode.ai/v2/docs/build/plugins).

## Qoder

Add `hooks` to `~/.qoder/settings.json`, `.qoder/settings.json`, or `.qoder/settings.local.json`. These sources merge. The IDE and JetBrains plugin document twelve events and `command`/`http` handler types; Qoder CLI supports additional events and handler types, so choose the requested surface before using a CLI-only feature.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".qoder/hooks/check-command.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

Handlers receive JSON over stdin. In the CLI, exit `0` means success, exit `2` blocks events that support blocking and sends stderr feedback to the agent, and other nonzero exits are non-blocking errors. Use executable/quoted command paths, no secrets in headers or logs, and an `http` handler only after explicit authority for the outbound request. Restart the IDE after configuration edits; use `/hooks` to inspect registered hooks.

Sources: [Qoder IDE Hooks](https://docs.qoder.com/extensions/hooks), [Qoder CLI Hooks](https://docs.qoder.com/cli/hooks).

## Orca

Orca does not document an independent arbitrary event-hook configuration format. It runs a repository’s existing `.claude/` and `.codex/` hook configurations when launching those agents in a worktree. For worktree provisioning, configure a Repository → Hooks setup command; it runs after a worktree is created. Orca-managed agent-status hooks are controlled by Settings → Agents and `orca agent hooks status|on|off --json`, not authored as application hooks.

For an agent lifecycle request, create a compatible Codex hook (or applicable Claude hook) and verify it in the exact agent Orca launches. For a setup request, configure the worktree hook through the Orca Repository settings and use an idempotent, safe command such as dependency setup or restoring a non-secret local configuration. Never claim an Orca setup command observes per-tool or per-response events.

Source: [Orca Agent hooks & memory](https://www.onorca.dev/docs/agents/hooks-memory).
