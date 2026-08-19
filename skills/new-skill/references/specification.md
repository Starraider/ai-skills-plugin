# Agent Skills specification compliance

Read this reference for every new skill or material revision. The [current Agent Skills specification](https://agentskills.io/specification) is normative. If this snapshot, a client extension, a template, or repository guidance disagrees with the current specification, follow the specification and update the stale material. When network access is unavailable, use this snapshot and do not claim that compliance was verified against the latest revision.

## Required structure

A skill is a directory whose name matches its required `SKILL.md` frontmatter `name`. `SKILL.md` contains YAML frontmatter followed by a non-empty Markdown instruction body. Other files and directories are optional.

## Frontmatter contract

The portable fields are:

- `name` (required): 1–64 characters; lowercase ASCII letters, digits, and single hyphens; no leading, trailing, or consecutive hyphens; exactly matches the parent directory.
- `description` (required): 1–1024 characters; says what the skill does and when to use it; include task language that supports accurate discovery.
- `license` (optional): a short license identifier or reference to a bundled license file.
- `compatibility` (optional): 1–500 characters describing genuine environment requirements. Omit it when there are none.
- `metadata` (optional): a mapping whose keys and values are strings. Use reasonably unique keys.
- `allowed-tools` (optional, experimental): a space-separated string of pre-approved tools. Treat it as a compatibility hint, never as a portable security boundary.

Do not put client-only fields in a portable `SKILL.md`. A client may add documented fields or companion configuration, but its extension cannot remove or weaken the portable requirements.

## Instructions and resources

Keep `SKILL.md` below 500 lines and, as recommended by the specification, below about 5,000 tokens. Put only instructions every relevant run needs in the body.

Use optional resources according to their runtime role:

- `scripts/` for executable code with explicit dependencies and helpful failures
- `references/` for focused documentation loaded only when needed
- `assets/` for templates, images, data, schemas, and other static resources
- additional directories only when the workflow or distribution format gives them a clear purpose

Reference files from `SKILL.md` with paths relative to the skill root. Keep references one level deep and avoid chains of references that hide required context.

## Compliance gate

Before declaring a generated skill complete:

1. Compare its frontmatter and layout with the current specification.
2. Run the bundled validator for repository, links, documentation, and client checks.
3. Run `skills-ref validate path/to/skill` when the reference validator is available.
4. Resolve every standards error. If an authoritative validator and this skill disagree, follow the current specification and report the validator discrepancy.
5. Label client-specific behavior accurately; do not present an extension as portable behavior.
