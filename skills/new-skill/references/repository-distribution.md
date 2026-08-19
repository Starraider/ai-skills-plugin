# Repository, plugin, and artifact guidance

Use this reference when a skill will live in its own repository, be installed by others, or be released as an artifact. Do not impose repository machinery on a project-local skill that only needs a directory.

## Choose the distribution unit

- **Skill directory:** best for project-local or personal use.
- **Repository:** best for independent ownership, history, review, releases, or multiple installation methods.
- **Agent Plugin:** best when bundling multiple Skills or pairing Skills with portable MCP configuration.

Keep the portable Skill directory canonical. Agent Plugin metadata describes the package and must not duplicate Skill behavior.

## Recommended Agent Plugin source tree

```text
theme-plugin/
├── plugin.json
├── README.md
├── LICENSE
├── skills/
│   ├── capability-a/
│   │   ├── SKILL.md
│   │   ├── references/
│   │   ├── scripts/
│   │   └── assets/
│   └── capability-b/
│       └── SKILL.md
├── mcp.json                       # optional
├── com.example.client/            # optional documented extension
├── tests/skills/<name>/evals.json # maintainer-only
└── .github/workflows/             # maintainer-only
```

Only create directories the package or its maintainers actually use. A bundled Skill normally relies on the root README; give it a local README only when it is independently consumed.

## Recommended standalone repository

```text
standalone-skill/
├── skills/<name>/
│   ├── SKILL.md
│   ├── README.md
│   ├── references/
│   ├── scripts/
│   └── templates/
├── evals/
├── .github/workflows/
├── CONTRIBUTING.md
├── SECURITY.md
├── LICENSE
└── README.md
```

Use only the files the project needs. A single-skill repository may place the skill at the root if its target clients and installer support that layout, but `skills/<name>/` makes client packaging and multi-skill growth clearer.

The repository README should identify the problem, trigger contexts, outputs, inputs, validation, supported clients, at least three example prompts, related skills, contributing process, security contact, and license. If the Skill directory has its own README, keep repository-level details at the root and runtime-adjacent usage beside the Skill.

## Licensing

Choose a license deliberately and record it in both the repository and `SKILL.md` when appropriate. If code and written content use different licenses, provide separate license files and an unambiguous path-to-license mapping. Do not claim a license inherited from a source unless its terms and attribution are preserved.

## Package contents

For an Agent Plugin, ship runtime material through an explicit allowlist:

- root `plugin.json`
- immediate children of `skills/` and their required resources
- optional root `mcp.json` and executables or data it references
- documented reverse-domain extension directories
- root README, license, and attribution files

For a standalone Skill archive, ship `SKILL.md`, directly referenced resources, its README, and required license or attribution files.

Exclude development-only material unless consumers need it at runtime:

- evaluation workspaces and transcripts
- CI and release configuration
- caches, virtual environments, dependencies, and editor state
- release scripts and maintainer-only reports

Use an explicit package allowlist. Validate a clean extracted copy, not just the source tree, so missing runtime files and accidental internal leakage are both caught.

## Source and installed copies

Edit the source worktree, never an installed cache or generated package. Resolve symlinks and locate the repository before changing a skill. If only an installed copy exists, create a writable source workspace and tell the user where it came from.

Preserve unrelated work in dirty trees. Do not bypass signing, hooks, or verification to force a release.

## Versioning and release

Use semantic versioning when consumers pin releases:

- patch: corrections with no intended workflow expansion
- minor: backward-compatible capability or trigger expansion
- major: renamed skills, incompatible output contracts, removed behavior, or installation changes

Recommended release sequence:

1. Update skill, README, changelog, manifests, and package metadata together.
2. Validate the source and a clean packaged copy.
3. Run representative evals and record intentional compatibility changes.
4. Merge the version change before creating the tag.
5. Create a signed tag where project policy supports it.
6. Build checksums and provenance for public executable artifacts.
7. Publish once and verify installation from the release artifact.

Do not reuse a published version or tag. For multiple repositories, prepare a dry-run manifest and obtain approval before broad release operations.

## Discovery metadata

Keep runtime routing in `SKILL.md`. Put public summaries, classification, screenshots, and search metadata in the plugin README, root manifest, or a documented client extension.

Useful non-runtime classifications:

- action level: read-only, suggests changes, modifies files, runs commands, or writes externally
- risk level: low, medium, or high
- supported clients and versions
- expected outputs and context requirements

Maintain one canonical source for each fact and generate or cross-check downstream views. Do not let discovery text contradict the Skill.

## Repository quality checks

Before release, verify:

- `SKILL.md` and all READMEs agree on scope and installation.
- Every support file is included, linked, and licensed.
- Contributing and security guidance exist or are explicitly delegated.
- Pull-request checks cover structure, links, scripts, and package contents.
- Root `plugin.json` validates and every immediate child Skill has a matching name.
- No secrets, local paths, caches, or evaluation data ship.
- The release artifact installs and is discovered in each claimed client.
