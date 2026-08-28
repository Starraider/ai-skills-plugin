---
name: agent-plugin-builder
description: Create, package, migrate, release, or validate portable Agent Plugins 1.0.0 containing Agent Skills and optional MCP servers. Use when building an agent plugin, adding plugin.json or mcp.json, converting a client-specific plugin to the open standard, producing a clean archive, or auditing v1 conformance. Do not use for purely client-owned installation or enablement.
license: CC-BY-4.0
---

# Agent Plugin Builder

## Outcome

Produce a self-contained Agent Plugins 1.0.0 directory whose portable components can be discovered independently by compatible clients. Keep client-owned capabilities outside the portable core.

## Workflow

1. Establish the package contract.

   Inspect the request, existing files, and repository instructions. Identify the plugin root, manifest metadata, Agent Skills, MCP servers, target clients, client-specific capabilities, and validation commands. Treat installation, permissions, policy, UI, hooks, commands, and custom agents as client-owned unless a newer specification explicitly standardizes them.

   If the requested schema version is not `1.0.0`, consult that version's normative specification and schemas instead of adapting this skill's pinned rules.

   Completion: every requested capability is classified as a portable Skill, portable MCP server, documented client extension, or out-of-scope client behavior.

2. Create or repair the portable package.

   Read [the portable package reference](references/portable-package.md). For a new empty destination, optionally run:

   ```bash
   python3 scripts/scaffold_agent_plugin.py /path/to/plugin \
     --name example-plugin \
     --version 0.1.0 \
     --description "What the plugin provides."
   ```

   Use exactly one root `plugin.json`. Preserve valid user metadata, reject unknown top-level fields, and keep every package-supplied path inside the plugin root. During migration, add the portable layout without deleting working legacy files until the target clients have been tested.

   Completion: `plugin.json` declares the canonical v1.0.0 schema and a valid name, and the package does not depend on a manifest-defined component path.

3. Add only the components the plugin needs.

   Put each Agent Skill in an immediate child directory at `skills/<skill-name>/SKILL.md` and follow the Agent Skills specification. Every Skill must include its own detailed `README.md`; keep its scripts, references, assets, and other skill-owned files within that skill directory. Keep the root plugin README to plugin-wide guidance and a concise linked summary of each Skill.

   When MCP is requested, read [the MCP configuration reference](references/mcp-servers.md) before creating root `mcp.json`. Use explicit transports, separate the executable `command` from `args`, use only the portable plugin variables in supported fields, and never put credentials in package-visible configuration.

   When a required capability is client-specific, read [the client extension reference](references/client-extensions.md). Add only namespaces and fields documented by the owning client. Do not invent a namespace contract.

   Completion: every Skill is directly discoverable and has a detailed local README, every MCP entry matches one closed transport variant, and every non-portable capability is isolated from the portable core.

4. Validate structure and behavior.

   Run the bundled zero-dependency validator:

   ```bash
   python3 scripts/validate_agent_plugin.py /path/to/plugin
   ```

   Also validate every discovered Agent Skill with `skills-ref validate` or the repository's existing skill validator when available. Exercise bundled stdio commands from the declared working directory and test remote MCP endpoints only when the user has authorized the connection. Test each target client's extension separately.

   Completion: structural checks pass, every discovered Skill passes full validation with its local README, referenced package files remain contained, and any untested runtime or client behavior is reported explicitly.

5. Package or release when requested.

   Read [packaging and release](references/packaging-and-release.md). Classify every top-level path as portable runtime, human documentation, a documented client extension, or maintainer-only. Build from an explicit allowlist and validate a clean extracted copy:

   ```bash
   python3 scripts/package_agent_plugin.py /path/to/plugin \
     --output /path/to/plugin.zip
   ```

   Keep root `plugin.json` as the only plugin-version source unless a real consumer requires another copy. Merge a version change before creating its tag, preserve repository signing and hooks, and stop a multi-plugin release batch after the first failure.

   Completion: the archive contains every runtime dependency, no maintainer-only material, and its extracted copy passes plugin and full Skill validation.

6. Hand off the package.

   Report the plugin root, schema version, portable components, client extensions, commands run, and remaining compatibility assumptions. Do not claim that a valid package is installed, trusted, enabled, or supported by a particular client without verifying that client state.

   Completion: the user can distinguish validated portable conformance from client-specific or runtime verification.

## Safety

- The scaffolder refuses to write into a non-empty directory; do not bypass that guard without explicit overwrite authority.
- Preserve legacy client files during migrations until replacements have been verified.
- Treat `env` and HTTP headers as visible package data. Never embed passwords, tokens, API keys, OAuth credentials, or other secrets.
- Do not execute bundled code or contact remote MCP endpoints merely to validate JSON structure.
- Reject package paths that resolve outside the plugin root, including escaping symlinks.
- Resolve the source directory before editing; never patch a client-managed installed copy or cache.

## Resources

- When the needed harness artifact is not yet clear, use [`improve-my-ai-harness`](../improve-my-ai-harness/README.md) to select the smallest sufficient mechanism before packaging it.
- Use [`new-skill`](../new-skill/README.md) to author or materially revise the Agent Skills that this package contains.
- [Portable package and manifest](references/portable-package.md)
- [MCP server configuration](references/mcp-servers.md)
- [Client extensions](references/client-extensions.md)
- [Packaging and release](references/packaging-and-release.md)
- `scripts/scaffold_agent_plugin.py` creates a minimal v1.0.0 manifest in a new or empty directory.
- `scripts/validate_agent_plugin.py` checks the v1.0.0 manifest, Skill discovery, MCP entries, path containment, and common secret hazards without executing plugin code.
- `scripts/package_agent_plugin.py` builds a deterministic allowlisted archive and validates its extracted copy.
