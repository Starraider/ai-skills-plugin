# Client compatibility

Last verified: 2026-08-19.

Use this reference when selecting install paths, frontmatter, invocation behavior, or client packaging. Client behavior changes; re-check the linked primary documentation before publishing compatibility claims.

## Portable core

Always apply [Agent Skills specification compliance](specification.md) first. Client sections below describe discovery paths and documented extensions; none may weaken the portable core.

Use this baseline in `SKILL.md`:

```yaml
---
name: skill-name
description: Use when the user needs a clearly bounded capability and name the relevant task contexts.
---
```

For cross-client output, avoid experimental `allowed-tools`, keep client policy in documented companion configuration, and include a detailed README in every Skill directory.

## Compatibility matrix

| Client | Project locations | User/global locations | Invocation | Material differences |
| --- | --- | --- | --- | --- |
| Claude Code | `.claude/skills/<name>/`; plugin `skills/<name>/`; nested project paths discovered on demand | `~/.claude/skills/<name>/` | Automatic by description; manual `/name` | Rich frontmatter extensions, arguments, shell injection, forked context, hooks, and tool controls |
| Codex | `.agents/skills/<name>/` from CWD through repository root | `~/.agents/skills/<name>/`; admin `/etc/codex/skills/<name>/` | Automatic by description; explicit `$name`; `/skills` lists | Optional `agents/openai.yaml`; plugins are the reusable distribution unit |
| Cursor | `.cursor/skills/<name>/` or `.agents/skills/<name>/`; nested locations are subtree-scoped | `~/.cursor/skills/<name>/` or `~/.agents/skills/<name>/` | Automatic by description; manual `/name` | Supports `paths` and `disable-model-invocation`; also reads selected Claude/Codex locations |
| Antigravity | `.agents/skills/<name>/` | `~/.gemini/config/skills/<name>/`; the IDE also recognizes open-standard user skills | Automatic by description; ask for available skills to verify | Name may default from directory, but portable output should include it; Antigravity CLI paths differ |
| OpenCode | `.opencode/skills/<name>/`, `.agents/skills/<name>/`, or `.claude/skills/<name>/` | `~/.config/opencode/skills/<name>/`, `~/.agents/skills/<name>/`, or `~/.claude/skills/<name>/` | Agent loads through the native `skill` tool | Only the five documented frontmatter fields are interpreted; permissions belong in `opencode.json` |
| Qoder | `.qoder/skills/<name>/` | `~/.qoder/skills/<name>/` | Automatic by description; manual `/name`; `/skills` lists | Project skill overrides a same-named user skill; CLI can reload with `/skills reload` |

## Claude Code

Primary source: [Extend Claude with skills](https://code.claude.com/docs/en/skills).

Claude Code follows the open standard and adds:

- `when_to_use`, `argument-hint`, `arguments`
- `disable-model-invocation`, `user-invocable`
- `allowed-tools`, `disallowed-tools`
- `model`, `effort`, `context`, `agent`, `hooks`, `paths`, `shell`
- argument substitutions such as `$ARGUMENTS`, `$0`, named arguments, and Claude-specific environment placeholders
- dynamic shell context using Claude syntax

Use these fields only for a Claude-specific branch. `disable-model-invocation: true` is appropriate for side-effectful or intentionally manual commands. Project trust and user permissions still govern tool execution.

Claude watches existing skill directories for `SKILL.md` changes. Restart if a newly created top-level skills directory is not detected. Personal skills override project skills with the same name; plugin skills are namespaced.

## Codex

Primary source: [Agent Skills in Codex](https://developers.openai.com/codex/skills).

Codex exposes skills in the CLI, IDE extension, and app. It scans `.agents/skills` from the launch directory upward to the repository root, supports symlinked skill directories, and loads the full body only after selection.

Use `agents/openai.yaml` only when Codex presentation or dependency metadata is needed:

```yaml
interface:
  display_name: "Human-readable name"
  short_description: "Short UI description"
  default_prompt: "Optional starter prompt"
policy:
  allow_implicit_invocation: true
```

The same file can declare icons and tool dependencies. Keep paths relative to the skill. Set `allow_implicit_invocation: false` for explicit-only Codex behavior; do not assume this controls other clients.

Use a Codex plugin when the skill needs reusable installation, multiple bundled skills, app mappings, or MCP configuration. Keep the underlying skill independently valid.

## Cursor

Primary sources: [Cursor Agent Skills](https://cursor.com/docs/skills), [Cursor 2.4 release notes](https://cursor.com/changelog/2-4).

Cursor accepts the open-standard directories and additionally reads compatible `.claude/skills/`, `.codex/skills/`, and their user-level counterparts. Prefer `.cursor/skills/` for Cursor-only work or `.agents/skills/` for a shared project skill.

Cursor-specific fields:

- `paths`: glob or list of globs that surfaces a skill only for matching files. New skills should use `paths`, not legacy `globs`.
- `disable-model-invocation: true`: excludes the skill from automatic matching while preserving explicit `/name` use.
- `metadata`: additional key-value data.

Nested `.cursor/skills/` or `.agents/skills/` directories are automatically scoped to their containing subtree. Avoid also adding redundant `paths` unless a narrower scope is required.

## Antigravity

Primary sources: [Antigravity Skills documentation](https://antigravity.google/docs/skills), [Google's authoring codelab](https://codelabs.developers.google.com/getting-started-with-antigravity-skills).

Antigravity indexes the YAML metadata and loads the Markdown body on demand. Its documentation treats `description` as mandatory and allows `name` to default from the directory; include both for portability. Scripts should be referenced by relative path.

For the Antigravity IDE, use `.agents/skills/` at project scope. Google's codelab documents `~/.gemini/config/skills/` for global IDE skills.

Antigravity CLI is a distinct surface. The same codelab documents `.agent/skills/` (singular) for project scope and `~/.gemini/antigravity-cli/skills/` for global scope. Do not silently substitute CLI paths when the user asked for the IDE; verify the current product documentation because these locations have changed during rollout.

## OpenCode

Primary source: [OpenCode Agent Skills](https://opencode.ai/docs/skills).

OpenCode recognizes only these frontmatter fields:

- `name`
- `description`
- `license`
- `compatibility`
- `metadata`

Unknown fields are ignored. This makes a Claude or Cursor extension nonfunctional rather than portable behavior. If the selected clients include OpenCode, move access policy to `opencode.json`:

```json
{
  "permission": {
    "skill": {
      "*": "allow",
      "internal-*": "deny",
      "experimental-*": "ask"
    }
  }
}
```

OpenCode walks project locations upward to the git worktree and loads global locations in parallel. Ensure names are unique across discovered locations.

## Qoder

Primary sources: [Qoder CLI Skills](https://docs.qoder.com/en/cli/Skills), [Qoder IDE Skills](https://docs.qoder.com/ja/extensions/skills).

Qoder requires `name` and `description`; the documented limits and naming rules match the open standard. It supports auxiliary reference files, scripts, and templates. Project-level skills override user-level skills of the same name.

For Qoder CLI, use `/skills reload` after edits in a running session. For the IDE, restart and inspect the `/` list when a new skill is not detected. QoderWork is a separate product with a different `~/.qoderwork/skills/` location; do not use that path for Qoder IDE or CLI.

Qoder recommends recording version changes. Put human-facing history in the README or changelog unless the runtime genuinely needs it; duplicating release history in `SKILL.md` wastes invoked context.

## Cross-client decisions

- For all six clients, use only the portable core and install or symlink the same directory into each discovery path.
- For explicit-only invocation, create client overlays: Claude/Cursor use `disable-model-invocation`, Codex uses `agents/openai.yaml`, and OpenCode uses permission configuration. Antigravity and Qoder do not document an equivalent portable switch.
- For tool restrictions, configure the client's permission system. Do not treat frontmatter as a security boundary.
- For reusable distribution, package the portable skill payload first, then add client manifests around it. Never fork the behavioral instructions unless clients truly require different execution.
