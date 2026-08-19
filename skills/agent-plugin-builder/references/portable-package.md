# Portable package and manifest

Use this reference whenever creating, migrating, or repairing the plugin root. It summarizes Agent Plugins Specification 1.0.0; the [normative specification](https://agent-plugins.org/specification) and [canonical schemas](https://agent-plugins.org/schemas) win if this summary differs.

## Fixed package model

An Agent Plugin is one self-contained directory with exactly one portable manifest at root `plugin.json`. Version 1.0.0 defines only two portable component types:

```text
my-plugin/
├── plugin.json
├── skills/
│   └── summarize/
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── assets/
├── mcp.json
└── com.example.client/
```

- `skills/` is optional. Clients discover only immediate child directories containing a regular file named exactly `SKILL.md`; they do not search recursively for more skills.
- `mcp.json` is optional and exists only at the plugin root.
- A reverse-domain top-level directory may contain files owned by a particular client extension.
- Missing optional component locations are valid. A malformed component does not invalidate independent component types.
- `plugin.json` cannot redefine component locations or contain inline component configuration.

Every package-supplied path must resolve inside the filesystem-resolved plugin root. A plugin-relative configuration path begins with `./`. Symlinks may target paths within the package but must not escape it.

## Closed `plugin.json`

The minimal manifest is:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-plugin"
}
```

The only portable top-level fields are:

| Field | Required | Type or role |
| --- | --- | --- |
| `$schema` | yes | Exact canonical v1.0.0 manifest schema identifier |
| `name` | yes | Plugin identifier, 1–64 characters |
| `version` | no | String; Semantic Versioning recommended |
| `description` | no | Short string |
| `author` | no | Closed object with optional string `name`, `email`, and `url` |
| `homepage` | no | String |
| `repository` | no | String |
| `license` | no | String; SPDX identifier recommended |
| `keywords` | no | Array of strings |
| `extensions` | no | Object keyed by reverse-domain namespaces; every value is an object |

The schema is closed. Do not add `skills`, `mcpServers`, `hooks`, `commands`, `agents`, arbitrary client discovery metadata, or other client-native fields at the top level. An unknown field is a conformance error even though the loading specification tells clients to report and ignore an otherwise non-fatal unknown field.

Plugin names use lowercase ASCII letters, digits, hyphens, and periods. They begin and end with an alphanumeric character, contain 1–64 characters, and contain neither `--` nor `..`.

## Agent Skills

Each `skills/<name>/SKILL.md` follows the [Agent Skills specification](https://agentskills.io/specification), which remains the source of truth. In particular:

- The frontmatter `name` matches its parent directory, is 1–64 characters, uses lowercase letters, digits, and single hyphens, and does not begin or end with a hyphen.
- `description` is non-empty, no more than 1024 characters, and explains what the Skill does and when it applies.
- Skill-owned scripts, references, assets, and other resources remain beneath the Skill directory.
- An invalid Skill is skipped independently; it does not invalidate other Skills or MCP servers.

## Migration rule

Prefer an additive migration:

1. Add and validate root `plugin.json`.
2. Put reusable Agent Skills in immediate child directories under `skills/`.
3. Convert portable MCP connections to root `mcp.json` using explicit v1 transports.
4. Preserve hooks, commands, agents, LSP configuration, UI, discovery metadata, and other client-native files in their existing compatibility package or in a documented client extension.
5. Test the portable core and each client integration before removing legacy files.

The directory name and manifest name need not match under v1.0.0, though matching them reduces packaging ambiguity.
