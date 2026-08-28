# new-skill

`new-skill` is an authoring workflow for building reliable, standards-compliant Agent Skills. Skills it creates are compatible with every IDE and agent that supports the [Agent Skills specification](https://agentskills.io/specification).

## What this skill solves

This skill turns skill design, validation, evaluation, and packaging into one focused workflow. Client-specific details are optional extensions, kept separate from the portable standard.

## Use when

- Creating a skill from a conversation, specification, or demonstrated workflow.
- Improving an existing skill's trigger accuracy, execution quality, or structure.
- Preparing a skill for any Agent Skills-compatible environment.
- Validating or packaging a standalone skill repository.

## Expected outputs

- A portable `SKILL.md` with focused routing metadata and executable instructions.
- A detailed human-facing README in every Skill directory, with the plugin root providing only a concise linked index and plugin-wide guidance.
- Optional `references/`, `scripts/`, and `templates/` only when they carry real work.
- Optional client-specific metadata only when a target environment requires it.
- Structural validation and an evaluation plan or results.

## Context requirements

Provide the desired capability or an existing skill path. Name a target environment only when its extension or installation convention matters. Repository-local instruction files remain authoritative for layout, licensing, and verification.

## Installation

Skills using the portable core work in every implementation of the Agent Skills standard. Install `new-skill/` in a location discovered by your client; the following are documented installation locations for selected clients:

| Client | Project scope | User scope |
| --- | --- | --- |
| Claude Code | `.claude/skills/new-skill/` | `~/.claude/skills/new-skill/` |
| Codex | `.agents/skills/new-skill/` | `~/.agents/skills/new-skill/` |
| Cursor | `.cursor/skills/new-skill/` or `.agents/skills/new-skill/` | `~/.cursor/skills/new-skill/` or `~/.agents/skills/new-skill/` |
| Antigravity | `.agents/skills/new-skill/` | `~/.gemini/config/skills/new-skill/` |
| OpenCode | `.opencode/skills/new-skill/` or `.agents/skills/new-skill/` | `~/.config/opencode/skills/new-skill/` or `~/.agents/skills/new-skill/` |
| Qoder | `.qoder/skills/new-skill/` | `~/.qoder/skills/new-skill/` |
| ChatGPT Desktop App | Upload the skill directory through Plugins → Skills in the desktop app | Install through the desktop app Skills UI |

See [client compatibility](references/client-compatibility.md) for invocation controls, precedence, alternate paths, and client-specific metadata.

## Usage

Invoke the skill explicitly where supported, or ask the agent to create or improve a skill. The workflow can scaffold a starting directory:

```bash
skills/new-skill/scripts/scaffold-skill.sh /tmp my-example-skill \
  "Use when producing a repeatable example output for a defined task."
```

Validate a portable standalone Skill:

```bash
skills/new-skill/scripts/validate-skill.sh /tmp/my-example-skill \
  --strict-portable
```

Package a validated skill without maintainer-only eval data:

```bash
python3 skills/new-skill/scripts/package-skill.py /tmp/my-example-skill \
  --output /tmp/my-example-skill.skill --strict-portable
```

## Example prompts

- "Create a project skill that reviews database migrations, with a validator script and three eval prompts."
- "Turn this deployment checklist into a manually invoked skill. Keep the runtime file short and put provider details in references."
- "Audit `skills/api-review/` for poor triggering, orphan references, incorrect documentation ownership, and portable metadata conflicts."

## Validation

Run `scripts/validate-skill.sh . --strict-portable` from this directory. The validator checks frontmatter, naming, the selected documentation profile, relative links, direct reference discoverability, eval structure, and portable compatibility.

## Sources

The authoring guidance is based on current primary documentation:

- [Agent Skills specification](https://agentskills.io/specification)
- [Agent Skills authoring best practices](https://agentskills.io/skill-creation/best-practices)
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
- [Using scripts in skills](https://agentskills.io/skill-creation/using-scripts)

## Related skills

- [`improve-my-ai-harness`](../improve-my-ai-harness/README.md) selects a Skill only when it is the smallest sufficient harness mechanism.
- [`new-plugin`](../new-plugin/README.md) assembles, validates, and releases a portable Agent Plugin containing one or more Skills.

## License

Licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
