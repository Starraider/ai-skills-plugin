# Installing individual Agent Skills

Use this guide when an IDE supports
[Agent Skills](https://agentskills.io/specification) but does not document
support for [Agent Plugins 1.0.0](https://agent-plugins.org/specification).
Installing a skill means copying its complete directory, not only `SKILL.md`.
Keep any `scripts/`, `references/`, `assets/`, templates, and other files beside
it.

The examples use these placeholders:

- `<download-directory>`: a local clone or extracted download containing skills
- `<skill-name>`: the skill directory name, which should match `name` in
  `SKILL.md`
- `<project-root>`: the root of the project that should use the skill

For a repository that contains several skills under `skills/`, copy one skill
with this general pattern:

```bash
git clone <skill-repository-url> <download-directory>
mkdir -p <skill-root>
cp -R <download-directory>/skills/<skill-name> <skill-root>/
```

On Windows PowerShell, use `New-Item -ItemType Directory -Force <skill-root>`
and `Copy-Item -Recurse` instead. Review `SKILL.md` and bundled scripts before
copying them.

## Antigravity

Google documents global and workspace skills in its
[Antigravity Skills codelab](https://codelabs.developers.google.com/getting-started-with-antigravity-skills).

| Scope   | Skill root                       |
| ------- | -------------------------------- |
| Global  | `~/.gemini/config/skills/`       |
| Project | `<project-root>/.agents/skills/` |

Copy the complete `<skill-name>/` directory into the chosen skill root. Restart
Antigravity or open a new agent session if the skill does not appear.

## OpenCode

OpenCode documents its native and compatibility paths in
[Agent Skills](https://opencode.ai/docs/skills).

| Scope   | Recommended skill root             |
| ------- | ---------------------------------- |
| Global  | `~/.config/opencode/skills/`       |
| Project | `<project-root>/.opencode/skills/` |

OpenCode also scans `~/.agents/skills/` and `<project-root>/.agents/skills/`.
Those paths are useful when several compatible agents share the same skills.
Start a new OpenCode session after installation if the catalog does not refresh.

## Windsurf

Windsurf documents both scopes in
[Cascade Skills](https://docs.windsurf.com/windsurf/cascade/skills).

| Scope   | Skill root                         |
| ------- | ---------------------------------- |
| Global  | `~/.codeium/windsurf/skills/`      |
| Project | `<project-root>/.windsurf/skills/` |

You can also create the destination through **Cascade > Customizations >
Skills** by choosing **+ Global** or **+ Workspace**, then replace the generated
skill directory with the complete skill you want to install. Invoke a skill
explicitly with `@<skill-name>` when testing it.

## Zed

Zed uses the cross-client `.agents` locations documented in
[Agent Skills](https://zed.dev/docs/ai/skills).

| Scope   | Skill root                       |
| ------- | -------------------------------- |
| Global  | `~/.agents/skills/`              |
| Project | `<project-root>/.agents/skills/` |

Each skill must be an immediate child of the skill root. Zed does not discover a
skill nested below a category directory. Project skills load only after you
trust the worktree. Open **AI > Skills** in Zed settings to confirm discovery.

## Trae

Trae documents skill creation and import in
[Skills](https://docs.trae.ai/ide/skills).

| Scope   | Skill root                     |
| ------- | ------------------------------ |
| Global  | `~/.trae/skills/`              |
| Project | `<project-root>/.trae/skills/` |

Copy the complete skill directory into the selected root, then refresh skill
discovery in Trae settings or restart the IDE. The China edition uses
`~/.trae-cn/skills/` for global skills; its project path remains
`.trae/skills/`.

## Qoder

Qoder CLI documents both locations in
[Skills](https://docs.qoder.com/cli/Skills).

| Scope   | Skill root                      |
| ------- | ------------------------------- |
| Global  | `~/.qoder/skills/`              |
| Project | `<project-root>/.qoder/skills/` |

After copying the skill directory, start a new Qoder session or run:

```text
/skills reload
```

Run `/skills` to confirm that Qoder discovered it. Qoder gives a user-level
skill precedence when a project-level skill has the same name.

## Updating or removing a skill

To update a skill, replace its whole directory with the newer version, then
reload or restart the client. Avoid mixing files from different releases.

To remove a skill, delete only that skill's directory from the relevant skill
root. Check the resolved path before deleting it, especially when the directory
is a symlink.
