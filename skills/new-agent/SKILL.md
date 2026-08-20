---
name: new-agent
description: Use when the user wants to create a specialized agent for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca. Require the target product and the agent's specific capabilities, then create the smallest supported agent definition and give product-appropriate verification steps. Do not treat skills, rules, or generic prompts as agents unless the selected product documents that model.
license: CC-BY-4.0
---

# New Agent

## Outcome

Create a clearly scoped, least-privilege agent for exactly one requested target: Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca. Produce the native configuration or a ready-to-paste builder specification, plus discovery and smoke-test instructions. Do not create, publish, or enable a remote ChatGPT agent without the user's explicit approval.

## Workflow

1. Establish the agent contract before writing a definition.

   Require both of the following. If either is missing, ask one concise clarification question rather than choosing on the user's behalf:

   - **Target IDE/product:** Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca. If the user names a product with multiple agent surfaces, identify the requested one.
   - **Specific capabilities:** the agent's single responsibility, expected inputs and deliverable, tools or integrations it needs, and whether it may edit files, run commands, or make external writes.

   Also resolve a name, project versus personal scope, model preference if material, and whether the agent is a main agent, profile, subagent, or external command. Explain any unsupported capability or missing account permission before generating files.

   Completion: the purpose, target surface, scope, and least-privilege tool set are unambiguous.

2. Select the target's documented agent representation.

   Read [target formats and research](references/target-formats.md). Use only the branch for the selected product:

   - **Antigravity:** create a Markdown custom agent at `.agents/agents/<name>/agent.md` for a workspace or `~/.gemini/config/agents/<name>/agent.md` for a user. Use the Antigravity template.
   - **Codex:** when the supported local runtime exposes custom agent definitions, create `.codex/agents/<name>.toml` (or `~/.codex/agents/<name>.toml`) from the Codex template. Otherwise, do not falsely substitute a Skill: offer a ChatGPT Workspace Agent only if its workspace plugin is available, or explain that the current Codex surface cannot load the requested local agent.
   - **ChatGPT / ChatGPT Desktop App:** distinguish a Custom GPT from a Workspace Agent. Explain that both are authored through OpenAI's web builder / Agent Studio interfaces (not local desktop configuration files) and can be accessed in the ChatGPT Desktop App once created. Generate a complete builder brief—name, description, instructions, starters, knowledge, tools, least-privilege action constraints, and test prompts—then ask for confirmation before creating or publishing it in the browser or Workspace Agents app.
   - **Zed:** distinguish a native Zed Agent profile (tools/model for the Zed Agent) from an ACP external agent process. Generate the applicable `settings.json` fragment; use the Zed profile template or an `agent_servers` command entry. Do not imply an ACP entry creates a new LLM agent implementation.
   - **OpenCode:** create `.opencode/agents/<name>.md` for project scope or `~/.config/opencode/agents/<name>.md` for user scope. Use the OpenCode template and explicit permissions.
   - **Qoder:** create `.qoder/agents/<name>.md` for project scope or `~/.qoder/agents/<name>.md` for user scope. Use the Qoder template; include only tools, skills, and MCP servers the user requires.
   - **Orca:** create an Orca custom CLI-agent launch specification: name, verified binary or command, arguments, and optional safe startup hook. Orca registers a CLI agent in its Settings UI; it does not define the agent's internal behavior, so create the underlying CLI agent configuration first if one is needed.

   Completion: exactly one native representation is selected, and the output does not claim portability across IDEs.

3. Write a focused system instruction and capabilities boundary.

   Write the body prompt for the selected agent, not a generic persona. State its responsibility, inputs to inspect, ordered operating rules, expected deliverable, verification required, and stop/return conditions. Keep selection metadata (name and description) separate from operating instructions.

   Start read-only. Add file writes, shell access, web access, MCP servers, apps, actions, or other external-write capability only when the user explicitly requires it. For any external write, require confirmation immediately before the action unless the target has a stricter documented approval control.

   Completion: every permission maps to a stated capability; no enabled tool is speculative.

4. Create the artifact and keep side effects within scope.

   For local IDE definitions, create only the chosen file and parent directory. Preserve an existing same-named definition unless the user explicitly asked to update it. For ChatGPT or Orca UI definitions, present the configuration and the exact creation steps; use an available native connector or UI only after the user has authorized the remote/UI change.

   Completion: the artifact is at the requested scope, contains no secrets, and has no unrelated configuration changes.

5. Verify discovery and behavior.

   Follow the selected target's validation steps in [target formats and research](references/target-formats.md). Verify discovery first, then invoke the agent explicitly with one representative request. Confirm that a read-only agent does not gain edit or command access and that any expected integration is both configured and authorized.

   Completion: the agent is visible in the target UI/CLI, handles its representative task, and respects the declared tool boundary; otherwise report the exact discovery or permission blocker.

## Safety

- Never invent a client-specific agent schema or claim that an `AGENTS.md`, a Rule, a Skill, or an MCP server is itself a custom agent.
- Do not store API keys, OAuth tokens, or passwords in agent files, startup hooks, prompts, templates, or generated commands.
- Treat apps, actions, MCP servers, shell access, and write permissions as capability grants, not as instructions. Keep them least-privilege and subject to the target's approval system.
- ChatGPT creation, sharing, publishing, schedules, API triggers, and connector changes are external state changes. Obtain explicit user authority for each requested action.
- If the request has no specific capability or no selected target product, stop and ask for it. Do not create a generic cross-IDE agent.

## Resources

- [Target formats, validation, and source research](references/target-formats.md)
- [Antigravity Markdown agent template](templates/antigravity-agent.md)
- [Codex TOML agent template](templates/codex-agent.toml)
- [OpenCode Markdown agent template](templates/opencode-agent.md)
- [Qoder Markdown agent template](templates/qoder-agent.md)
- [Zed settings templates](templates/zed-agent-settings.jsonc)
