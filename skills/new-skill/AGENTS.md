# New Skill Authoring

## Purpose

- Provide one rigorous workflow for creating and improving portable agent skills.
- Cover Claude Code, Codex, Cursor, Antigravity, OpenCode, and Qoder without requiring separate authoring skills.

## Ownership

- `SKILL.md` owns the executable authoring workflow.
- A standalone Skill's `README.md` owns human-facing setup, compatibility, and usage guidance.
- A bundled Skill may rely on the owning Agent Plugin's root `README.md`.
- `references/` owns extended standards and client-specific details.
- `scripts/` owns deterministic validation and scaffolding helpers.
- `templates/` owns reusable bootstrap files.
- `evals/` owns maintainer-facing behavioral test cases.

## Local Contracts

- Use current primary sources for client-specific compatibility claims.
- Separate portable Agent Skills conventions from client-specific compatibility and metadata behavior.
- Do not cite or link to repositories excluded by the user.
- Keep runtime context lean through explicit progressive-disclosure links.
- Require a Skill-local README only for standalone Skills; keep bundled documentation at the owning plugin root unless the Skill needs an independent human surface.

## Work Guidance

- Prefer standards-compatible output and add client-specific files only when required.
- Make assumptions visible and fail validation on unsupported or contradictory metadata.

## Verification

- Run `scripts/validate-skill.sh` against this skill and against a generated fixture.
- Run the bundled structural eval checks and verify all Markdown links and template placeholders.

## Child DOX Index

- No child DOX files.
