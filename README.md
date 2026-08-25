# AI Skills Plugin

A portable [Agent Plugins 1.0.0](https://agent-plugins.org/) package containing reusable Agent Skills for AI-harness diagnosis, prompt design, IDE-native agent, hook, and slash-command creation, Skill authoring, and Agent Plugin creation.

## Installation

- [Install the complete Agent Plugin](plugin-installation.md) in Codex, Cursor,
  GitHub Copilot, or Visual Studio Code.
- [Install individual Agent Skills](skill-installation.md) in Antigravity,
  OpenCode, Windsurf, Zed, Trae, or Qoder.

## Included Skills

| Skill | Purpose |
| --- | --- |
| [`agent-plugin-builder`](skills/agent-plugin-builder/README.md) | Create, migrate, validate, package, and release Agent Plugins 1.0.0. |
| [`improve-my-ai-harness`](skills/improve-my-ai-harness/README.md) | Diagnose an AI-IDE problem, select the smallest suitable harness mechanism or combination, and produce a builder-routed implementation prompt. |
| [`new-agent`](skills/new-agent/README.md) | Create least-privilege, IDE-native agents for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca. |
| [`new-agents-md`](skills/new-agents-md/README.md) | Create concise, target-aware `AGENTS.md` repository instructions for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca. |
| [`new-hook`](skills/new-hook/README.md) | Decide whether an event hook is appropriate and create a target-native hook or supported alternative. |
| [`new-prompt`](skills/new-prompt/README.md) | Create and improve ready-to-use LLM prompts. |
| [`new-skill`](skills/new-skill/README.md) | Create, validate, evaluate, and package portable Agent Skills. |
| [`new-slash-command`](skills/new-slash-command/README.md) | Decide whether a reusable task should be a slash command and create the target-native command or supported alternative. |
| [`new-workflow`](skills/new-workflow/README.md) | Decide whether a workflow is appropriate and create a target-native workflow or supported alternative. |

Compatible clients discover each immediate child of `skills/` that contains a valid `SKILL.md`. This package has no MCP servers, so it intentionally omits `mcp.json`.

## Validation

From the plugin root, run:

```bash
python3 skills/agent-plugin-builder/scripts/validate_agent_plugin.py . --strict
```

Validate individual Skills with the Agent Skills reference validator or their own bundled validation commands.

Create a deterministic portable archive and validate the extracted copy with:

```bash
python3 skills/agent-plugin-builder/scripts/package_agent_plugin.py . \
  --output /tmp/ai-skills-plugin.zip
```

## Standard boundary

Agent Plugins 1.0.0 standardizes the root manifest, Agent Skills, and optional MCP configuration. Client installation, permissions, enablement, and UI remain client-managed.

## License

This project and all contained Agent Skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
