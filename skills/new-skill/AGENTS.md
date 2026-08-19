# New Skill Authoring

## Purpose

- Provide one rigorous workflow for creating and improving portable agent skills.
- Produce portable Agent Skills for every implementation of the Agent Skills specification, with client extensions only when explicitly required.

## Ownership

- `SKILL.md` owns the executable authoring workflow.
- Every Skill's `README.md` owns detailed human-facing setup, compatibility, and usage guidance.
- An owning Agent Plugin's root `README.md` owns plugin-wide documentation and a concise linked Skill index.
- `references/` owns extended standards and client-specific details.
- `scripts/` owns deterministic validation and scaffolding helpers.
- `templates/` owns reusable bootstrap files.
- `evals/` owns maintainer-facing behavioral test cases.

## Local Contracts

- Treat the current Agent Skills specification as normative for every generated or revised Skill; client extensions may add behavior but never replace required portable fields.
- Use current primary sources for client-specific compatibility claims.
- Separate portable Agent Skills conventions from client-specific compatibility and metadata behavior.
- Do not cite or link to repositories excluded by the user.
- Keep runtime context lean through explicit progressive-disclosure links.
- Require a detailed Skill-local README for every Skill. Keep plugin-wide information and short linked Skill summaries at the owning plugin root.

## Work Guidance

- Prefer standards-compatible output and add client-specific files only when required.
- Make assumptions visible and fail validation on unsupported or contradictory metadata.

## Verification

- Run `scripts/validate-skill.sh` against this skill and against valid and invalid generated fixtures.
- Run `skills-ref validate` when the reference validator is available.
- Run the bundled structural eval checks and verify all Markdown links and template placeholders.
