# AI Skills Plugin

A portable [Agent Plugins 1.0.0](https://agent-plugins.org/) package containing reusable Agent Skills for prompt design, Skill authoring, and Agent Plugin creation.

## Included Skills

| Skill | Purpose |
| --- | --- |
| `agent-plugin-builder` | Create, migrate, validate, package, and release Agent Plugins 1.0.0 |
| `new-prompt` | Create and improve ready-to-use LLM prompts |
| `new-skill` | Create, validate, evaluate, and package portable Agent Skills |
| `skill-creator` | Create or update Codex Skills with scoped instructions and resources |
| `writing-great-skills` | Reference guidance for predictable Skill authoring |

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
