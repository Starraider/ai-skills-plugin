# new-plugin

Create, package, migrate, release, and validate portable Agent Plugins 1.0.0 without confusing the portable standard with client-owned behavior.

## What this skill solves

Agent Skills and MCP servers are reusable, but agent clients historically wrapped them in different manifests and discovery layouts. This skill turns a requested capability or an existing client-specific package into the small, deterministic Agent Plugins 1.0.0 structure while keeping non-portable behavior isolated.

## Use when

- Creating a new package for the Agent Plugins 1.0.0 standard.
- Adding or repairing root `plugin.json`, `skills/`, or `mcp.json` files.
- Migrating an existing plugin to a portable core while isolating client integrations.
- Auditing an Agent Plugin for manifest, discovery, MCP, path-containment, or secret-handling errors.
- Producing a deterministic archive that excludes maintainer-only material and validates after extraction.

Do not use it for an unrelated client-native plugin unless the user wants an Agent Plugins-compatible package or migration.

## Expected outputs

- A plugin root with a conforming `plugin.json`.
- Zero or more Agent Skills under immediate child directories of `skills/`.
- An optional root `mcp.json` using explicit stdio, Streamable HTTP, or legacy SSE transports.
- Optional documented reverse-domain client extensions.
- Structural validation results and clearly separated runtime/client compatibility findings.
- A clean archive and extracted-copy validation when packaging is requested.

## Context requirements

Provide the desired capability or an existing plugin directory, the intended output location, and any required Skill or MCP behavior. Name target clients only when client-specific extensions or compatibility testing are needed. Creating high-quality Skill instructions still requires the domain requirements those Skills should encode.

## Installation

This skill ships as part of the `ai-skills-plugin` Agent Plugins 1.0.0
package. Full per-client instructions are in the [package README](../../README.md).
Quick reference:

| Client | Install method | Skill discovery path |
|---|---|---|
| **Antigravity** | Copy/symlink plugin dir to `.agents/plugins/ai-skills-plugin/` or `~/.gemini/config/plugins/ai-skills-plugin/` | `skills/<skill-name>/SKILL.md` |
| **Cursor** | Copy/symlink plugin dir to `~/.cursor/plugins/local/ai-skills-plugin/`, then reload window | Auto-discovered from `plugin.json` |
| **GitHub Copilot / VS Code** | Add `"chat.pluginLocations": { "/path/to/ai-skills-plugin": true }` to `settings.json`, reload window | `skills/<skill-name>/SKILL.md` via `chat.pluginLocations` |
| **Kiro** | Powers panel → **Add Custom Power → Import power from a folder** → select plugin root | Auto-discovered from `plugin.json` |
| **Windsurf** | Copy skills to `.agents/skills/` or add path to `.windsurf/skills.json` | `.agents/skills/<skill-name>/SKILL.md` |
| **Codex** | Copy skills to `.agents/skills/<skill-name>/` in project or `~/.agents/skills/` | `SKILL.md` in each skill dir |
| **ChatGPT Desktop App** | Upload each `skills/<skill-name>/` directory via **Plugins → Skills → Create → Upload from your computer** | Per-skill upload |
| **OpenCode** | Copy skills to `.opencode/skills/` or `.agents/skills/`; or add `"skills": ["/path/to/.../skills"]` to `opencode.json` | `.opencode/skills/<skill-name>/SKILL.md` |
| **Qoder** | Copy skills to `.qoder/skills/<skill-name>/` or `~/.qoder/skills/<skill-name>/` | `.qoder/skills/<skill-name>/SKILL.md` |
| **Google Agents CLI** | `npx skills add /path/to/ai-skills-plugin [--global]` | Standard skills path |
| **Orca** | Copy skills to `.agents/skills/<skill-name>/` or `~/.agents/skills/<skill-name>/` | `.agents/skills/<skill-name>/SKILL.md` |
| **Zed** | Copy skills to `.agents/skills/<skill-name>/` or `~/.agents/skills/<skill-name>/`; grant workspace trust | `.agents/skills/<skill-name>/SKILL.md` |

Inside any Agent Plugins 1.0.0 package, this skill must be at the standard
discovery path:

```text
<plugin-root>/skills/new-plugin/
```

The directory must contain `SKILL.md` directly beneath it. A skills-capable
Agent Plugins client discovers it as an immediate child of `skills/`; the
standard intentionally leaves client installation and enablement UX unspecified.

For the **ChatGPT Desktop App**, which does not load local filesystem Agent
Plugins packages directly, install this skill through the Skill installation
flow: upload the complete `skills/new-plugin/` directory (with all
supporting scripts and references) via **Plugins → Skills → Create → Upload
from your computer**.

For standalone development in this repository, use the
`skills/new-plugin/` directory as the skill source.


## Example prompts

- "Create an Agent Plugins 1.0 package named `acme.release-tools` with a release-notes Skill and a local stdio MCP server in `./bin/release-tools`."
- "Migrate this client-specific plugin to the portable Agent Plugins layout, but keep its working hooks isolated until the target client has been tested."
- "Audit `/workspace/reporting-plugin` for Agent Plugins 1.0 conformance, including symlink escapes, invalid MCP transports, and package-visible secrets."
- "Add a Streamable HTTP MCP server to this existing plugin; authentication must remain client-managed."

## Validation

Validate this authoring skill:

```bash
skills/new-skill/scripts/validate-skill.sh \
  skills/new-plugin \
  --strict-portable
```

Validate a generated Agent Plugin without executing its code or contacting remote servers:

```bash
python3 skills/new-plugin/scripts/validate_agent_plugin.py \
  /path/to/plugin
```

Build and validate a deterministic portable archive:

```bash
python3 skills/new-plugin/scripts/package_agent_plugin.py \
  /path/to/plugin --output /tmp/plugin.zip
```

The plugin validator checks Agent Plugins 1.0.0 package semantics, basic Agent Skill frontmatter, and the required local README for every Skill. The packager composes it with full Skill validation and repeats those checks against a clean extracted copy. Test actual MCP startup and each client extension in its intended environment.

## Related skills

- [`new-skill`](../new-skill/README.md) is useful when a plugin's Agent Skills need deeper authoring, cross-client metadata, or evaluation work.
- [`improve-my-ai-harness`](../improve-my-ai-harness/README.md) selects the smallest harness architecture when the package contents are not yet decided.
- Client-native plugin creators remain appropriate for capabilities outside Agent Plugins 1.0.0, provided their output does not masquerade as the portable core.

## License

Licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).

## Sources

- [Agent Plugins documentation](https://agent-plugins.org/)
- [Agent Plugins Specification 1.0.0](https://agent-plugins.org/specification)
- [Agent Plugins JSON Schemas](https://agent-plugins.org/schemas)
- [Vercel: Introducing Agent Plugins](https://vercel.com/blog/introducing-agent-plugins)
- [Agent Skills specification](https://agentskills.io/specification)
