# Target hook formats and research

Last verified: 2026-08-20. Re-check the linked primary documentation immediately before publishing or enabling a hook; lifecycle APIs are fast-moving and a hook has executable authority.

## Decision table

| Target | Use a hook when | Do not use it when | Native model |
| --- | --- | --- | --- |
| Antigravity | A command must run before/after a documented agent action or lifecycle point | The task needs model judgment, durable queues, or broad plugin functionality | JSON command hook |
| Codex | A local deterministic script must observe, gate, rewrite, or augment a documented lifecycle event | A permission rule or skill suffices, or the action involves hosted tools not on the local hook path | JSON or inline TOML command hook |
| ChatGPT Desktop App | Never claim a local lifecycle hook | The request needs repeatable behavior, scheduled work, or an integration | Skill, Plugin/App/MCP, or approved automation/workspace workflow |
| Zed | Only setup immediately after Zed creates a linked worktree | The desired trigger is an agent/tool/message lifecycle event | `tasks.json` `create_worktree` task hook |
| OpenCode | The behavior needs a plugin-level transform or runtime interception | A Skill, permission setting, or ordinary command is enough | TypeScript/JavaScript plugin API |
| Qoder | A documented IDE/CLI lifecycle event needs a deterministic handler | A static permission rule or a slow/durable workflow is better | JSON hook with command/http; CLI also has prompt/agent handlers |
| Orca | A compatible underlying agent hook or post-worktree setup command has the needed trigger | An Orca-native arbitrary event hook is assumed | Reused `.codex`/`.claude` hooks or Repository worktree setup |
| Cursor | A deterministic script must observe, gate, or augment a documented agent lifecycle event | A rule, permission setting, or MCP tool is sufficient | JSON command hook (`hooks.json`) |
| GitHub Copilot / VS Code | A deterministic script must intercept a documented agent session event | A prompt instruction, VS Code extension API, or MCP tool would be more appropriate | JSON command hook (`.github/hooks/*.json`) |
| Windsurf | Only blocking a shell-level tool call (`PreToolUse`) is needed | Any broader lifecycle intercept, subagent tracking, or post-response work is required | Limited JSON command hook (`hooks.json`); rules/workflows/MCP for everything else |
| Kiro | A documented IDE/CLI lifecycle event (file, tool, or agent) needs a deterministic handler or an agent prompt injection | A `.kiro/steering/` rule or an MCP integration would be more appropriate | JSON hook files under `.kiro/hooks/` with `command` or `agent` action types |
| Google Agents CLI (ADK) | A Python plugin callback must observe, gate, or transform tool calls, model calls, or agent events within a Runner | A separate microservice, CI job, or MCP tool integration would be more appropriate | `BasePlugin` subclass with callback methods registered in the Runner |

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

## ChatGPT Desktop App

As of this verification, the ChatGPT Desktop App’s documented reusable workflow mechanism is an Agent Skill (managed under Plugins → Skills); its Plugins can package Skills with Apps and app templates. The product documentation does not document a user-configured local pre/post tool or response lifecycle-hook file comparable to Codex, Antigravity, OpenCode, or Qoder.

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

Orca does not document an independent arbitrary event-hook configuration format. It runs a repository's existing `.claude/` and `.codex/` hook configurations when launching those agents in a worktree. For worktree provisioning, configure a Repository → Hooks setup command; it runs after a worktree is created. Orca-managed agent-status hooks are controlled by Settings → Agents and `orca agent hooks status|on|off --json`, not authored as application hooks.

For an agent lifecycle request, create a compatible Codex hook (or applicable Claude hook) and verify it in the exact agent Orca launches. For a setup request, configure the worktree hook through the Orca Repository settings and use an idempotent, safe command such as dependency setup or restoring a non-secret local configuration. Never claim an Orca setup command observes per-tool or per-response events.

Source: [Orca Agent hooks & memory](https://www.onorca.dev/docs/agents/hooks-memory).

## Cursor

Hooks are defined in `hooks.json` at `.cursor/hooks.json` (project, committed to the repository) or `~/.cursor/hooks.json` (user-level, applies to all projects). Cursor loads both and runs all matching hooks. Hooks communicate via stdio JSON: Cursor sends event data on stdin; the handler writes a JSON response to stdout. For blocking events (`beforeShellExecution`, `preToolUse`, `beforeReadFile`, `beforeMCPExecution`, `beforeSubmitPrompt`), Cursor waits for the handler to exit before proceeding.

```json
{
  "version": 1,
  "hooks": {
    "beforeShellExecution": [
      {
        "command": "./.cursor/hooks/check-command.sh",
        "timeout": 10
      }
    ]
  }
}
```

Documented events include agent lifecycle events (`sessionStart`, `stop`), tool use events (`preToolUse`, `postToolUse`, `postToolUseFailure`), shell-specific events (`beforeShellExecution`, `afterShellExecution`), file events (`beforeReadFile`, `afterFileEdit`), MCP events (`beforeMCPExecution`, `afterMCPExecution`), prompt events (`beforeSubmitPrompt`), reasoning events (`afterAgentResponse`, `afterAgentThought`), and subagent events (`subagentStart`, `subagentStop`). Cloud Agent support may differ; verify against the cloud support matrix before relying on hooks for automated CI/CD-like workflows.

For blocking hooks: exit code `2` blocks and provides stderr as the reason; exit code `0` allows; any other non-zero fails open unless `failClosed: true` is set. Cursor also reads Claude Code hook configuration if the third-party config option is enabled in Settings → Rules, Skills, Subagents.

Debug hooks using the **Hooks** output channel in Cursor (Output panel). Validate JSON syntax before loading; test with a matching event and then a non-matching event.

Source: [Cursor Hooks](https://www.cursor.com/en/docs/context/hooks).

## GitHub Copilot / VS Code

Hooks are defined in `.json` files inside `.github/hooks/` (project-level, loaded for all team members) or the user-level directory (varies by surface; `~/.copilot/hooks/` in the CLI context). VS Code discovers and loads all `.json` files in `.github/hooks/` automatically. Hooks communicate via stdio JSON: VS Code sends event data on stdin; the handler writes a JSON response to stdout. Default timeout is 30 seconds.

```json
{
  "version": 1,
  "hooks": {
    "PreToolUse": [
      {
        "type": "command",
        "command": "./scripts/validate-tool.sh",
        "timeout": 15
      }
    ]
  }
}
```

Documented events include `sessionStart`, `sessionEnd` (or `stop`), `userPromptSubmitted`, `preToolUse`, `postToolUse`, `preCompact`, `subagentStart`, `subagentStop`, and `stop`. For `preToolUse`, the response can include a `permissionDecision` field (`allow`, `ask`, or `deny`) to dynamically control the agent's action.

Ensure hook scripts are executable (`chmod +x`). Debug hooks using the **Developer: Show Agent Debug Logs** command in VS Code. Use MCP servers or the Language Model Tools API when a deeper programmatic integration is required rather than an event-shell hook.

Source: [GitHub Copilot agent hooks](https://code.visualstudio.com/docs/copilot/copilot-customization#_agent-hooks).

## Windsurf

Windsurf (Codeium Cascade) does not expose a general agent lifecycle hook API. It provides a **limited command hook** for shell-command blocking only. Define hooks in `~/.codeium/windsurf/hooks.json` (user) or `.windsurf/hooks.json` (workspace). The file follows a `version` + `hooks` structure using the `PreToolUse` event with a `matcher` regex and a command handler.

```json
{
  "version": 1,
  "hooks": {
    "PreToolUse": [
      {
        "command": ".windsurf/hooks/check-command.sh",
        "matcher": "Bash|Write|Edit",
        "failClosed": true,
        "timeout": 5
      }
    ]
  }
}
```

The handler receives a JSON payload via stdin containing `tool_name` and `tool_input`. Exit code `0` allows; exit code `2` blocks and surfaces stderr as the reason; exit code `1` or other non-zero may not block correctly—always use `2` for intentional blocks. There is no documented `postToolUse`, `sessionStart`, `stop`, `subagentStart`, or similar general lifecycle event for the Cascade agent.

For any broader lifecycle need—such as post-response formatting, session initialization, or context injection—use `.windsurfrules` (behavioral rules), `.windsurf/workflows/` (multi-step task sequences), or MCP servers (tool integrations). Debug hooks through the Output → Hooks panel in the Windsurf IDE.

Source: [Windsurf Memories and Rules](https://docs.windsurf.com/windsurf/memories-and-rules).

## Kiro

Hooks are stored as individual `.json` files inside `.kiro/hooks/` (project scope; shared across Kiro IDE, CLI, and web). Each file follows a versioned schema (`"version": "v1"`) and contains a `hooks` array. Each hook entry has a `name`, `trigger`, an optional `matcher` (regex on tool name or file path), and an `action` of type `command` or `agent`.

```json
{
  "version": "v1",
  "hooks": [
    {
      "name": "lint-on-save",
      "trigger": "PostFileSave",
      "matcher": "\\.(ts|tsx)$",
      "action": {
        "type": "command",
        "command": "npx eslint --fix"
      }
    }
  ]
}
```

Documented triggers include file events (`FileCreate`, `PostFileSave`, `FileDelete`), tool events (`PreToolUse`, `PostToolUse`, including MCP tool hooks), agent/task events (`PromptSubmit`, `AgentStop`, `PreTaskExecution`, `PostTaskExecution`), and a manual trigger via the IDE Agent Hooks panel. Some triggers (e.g., `AgentSpawn`) are CLI-only; `PreTaskExecution` and `PostTaskExecution` are IDE-only.

For `PreToolUse` with a `command` action: exit code `0` allows; exit code `2` blocks and sends stderr to the agent as feedback. The handler receives session context via stdin as JSON. An `agent` action type injects a prompt into the conversation rather than running a shell command.

Use the IDE Agent Hooks panel or natural language conversation to create hooks instead of editing JSON manually. If migrating from an older Kiro version, run `kiro-cli agent migrate` to convert embedded hooks to the new per-file format. Restart the IDE after configuration changes.

Sources: [Kiro Agent Hooks](https://kiro.dev/docs/hooks/), [Kiro Hooks reference](https://kiro.dev/docs/reference/hooks).

## Google Agents CLI (ADK)

The Google Agent Development Kit (ADK) uses Python plugin callbacks rather than a JSON hook file. Implement a `BasePlugin` subclass and register it with the `Runner` that manages the agent. The plugin's callback methods intercept the corresponding lifecycle point.

```python
from google.adk.plugins import BasePlugin
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from typing import Any, Optional

class ToolLoggerPlugin(BasePlugin):
    name = "tool-logger"

    async def before_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
    ) -> Optional[dict]:
        # Return None to proceed; return a dict to short-circuit and use it as the result.
        print(f"BEFORE: {tool.name}({tool_args})", flush=True)
        return None

    async def after_tool_callback(
        self,
        *,
        tool: BaseTool,
        tool_args: dict[str, Any],
        tool_context: ToolContext,
        tool_response: dict,
    ) -> Optional[dict]:
        # Return None to pass the original result through; return a dict to replace it.
        print(f"AFTER: {tool.name} -> {tool_response}", flush=True)
        return None
```

Documented callback hooks include `before_tool_callback` / `after_tool_callback` (tool calls), `before_model_callback` / `after_model_callback` (LLM requests), `on_event` (any agent event), and session/agent lifecycle callbacks depending on the ADK version. Note that some built-in model tools (e.g., `VertexAiSearchTool`, `GoogleSearchTool`) execute server-side and **do not** trigger client-side callbacks.

Register the plugin with the runner:

```python
from google.adk.runners import Runner

runner = Runner(
    agent=root_agent,
    app_name="my-app",
    session_service=session_service,
    plugins=[ToolLoggerPlugin()],
)
```

Requires ADK ≥ 1.26.0 for correct registration in live (bi-directional streaming) mode. Do not perform heavy blocking work inside synchronous callbacks. Avoid network-dependent work; use background services or Cloud Tasks for durable side effects. Do not store credentials or secrets in plugin source or logs.

Sources: [ADK Callbacks](https://google.github.io/adk-docs/callbacks/), [ADK Plugins](https://google.github.io/adk-docs/plugins/), [ADK GitHub](https://github.com/google/adk-python).
