# new-skill

`new-skill` is a single authoring workflow for building reliable Agent Skills across Claude Code, Codex, Cursor, Antigravity, OpenCode, and Qoder. It combines intent capture, portable metadata, progressive disclosure, validation, evaluation, and documentation profiles for standalone and Agent Plugin-bundled Skills.

## What this skill solves

Skill creation guidance is often split between writing advice, client documentation, evaluation tooling, and repository conventions. This skill turns those concerns into one workflow and keeps client-specific details behind a compatibility reference.

## Use when

- Creating a skill from a conversation, specification, or demonstrated workflow.
- Consolidating several overlapping authoring skills into one.
- Improving an existing skill's trigger accuracy, execution quality, or structure.
- Preparing a skill for one or more supported IDEs.
- Validating or packaging a standalone skill repository.

## Expected outputs

- A portable `SKILL.md` with focused routing metadata and executable instructions.
- A human-facing README for a standalone Skill, or root-plugin documentation for a bundled Skill.
- Optional `references/`, `scripts/`, and `templates/` only when they carry real work.
- Client-specific metadata where required.
- Structural validation and an evaluation plan or results.

## Context requirements

Provide the desired capability or an existing skill path. For client-specific output, name the target IDEs. Repository-local instruction files remain authoritative for layout, licensing, and verification.

## Installation

Install the `new-skill/` directory in a location discovered by your client:

| Client | Project scope | User scope |
| --- | --- | --- |
| Claude Code | `.claude/skills/new-skill/` | `~/.claude/skills/new-skill/` |
| Codex | `.agents/skills/new-skill/` | `~/.agents/skills/new-skill/` |
| Cursor | `.cursor/skills/new-skill/` or `.agents/skills/new-skill/` | `~/.cursor/skills/new-skill/` or `~/.agents/skills/new-skill/` |
| Antigravity | `.agents/skills/new-skill/` | `~/.gemini/config/skills/new-skill/` |
| OpenCode | `.opencode/skills/new-skill/` or `.agents/skills/new-skill/` | `~/.config/opencode/skills/new-skill/` or `~/.agents/skills/new-skill/` |
| Qoder | `.qoder/skills/new-skill/` | `~/.qoder/skills/new-skill/` |

See [client compatibility](references/client-compatibility.md) for invocation controls, precedence, alternate paths, and client-specific metadata.

## Usage

Invoke the skill explicitly where supported, or ask the agent to create or improve a skill. The workflow can scaffold a starting directory:

```bash
skills/new-skill/scripts/scaffold-skill.sh /tmp my-example-skill \
  "Use when producing a repeatable example output for a defined task."
```

Validate a standalone Skill against selected clients:

```bash
skills/new-skill/scripts/validate-skill.sh /tmp/my-example-skill \
  --clients claude,codex,cursor,antigravity,opencode,qoder
```

For a Skill whose human documentation lives at its Agent Plugin root:

```bash
skills/new-skill/scripts/validate-skill.sh /path/to/plugin/skills/my-skill \
  --documentation-profile bundled --strict-portable
```

Package a validated skill without maintainer-only eval data:

```bash
python3 skills/new-skill/scripts/package-skill.py /tmp/my-example-skill \
  --output /tmp/my-example-skill.skill --strict-portable
```

## Example prompts

- "Create a project skill that reviews database migrations in Codex and OpenCode, with a validator script and three eval prompts."
- "Turn this deployment checklist into a manually invoked Claude Code and Cursor skill. Keep the runtime file short and put provider details in references."
- "Audit `skills/api-review/` for poor triggering, orphan references, incorrect documentation ownership, and cross-client metadata conflicts."

## Validation

Run `scripts/validate-skill.sh . --clients claude,codex,cursor,antigravity,opencode,qoder` from this directory. The validator checks frontmatter, naming, the selected documentation profile, relative links, direct reference discoverability, eval structure, and selected-client compatibility.

## Sources

The compatibility guide is based on current primary documentation:

- [Agent Skills specification](https://agentskills.io/specification)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Codex skills](https://developers.openai.com/codex/skills)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
- [Google Antigravity Skills](https://antigravity.google/docs/skills)
- [OpenCode Agent Skills](https://opencode.ai/docs/skills)
- [Qoder Skills](https://docs.qoder.com/en/cli/Skills)

## Related skills

None required. This skill intentionally consolidates the complete skill-authoring workflow.

## License

No standalone license is declared for this skill directory. Before external distribution, add or document the license required by the containing repository.
