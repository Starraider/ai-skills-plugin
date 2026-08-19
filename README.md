# AI Skills Plugin

A portable [Agent Plugins 1.0.0](https://agent-plugins.org/) package containing reusable Agent Skills for prompt design, IDE-native agent creation, Skill authoring, and Agent Plugin creation.

## Included Skills

| Skill | Purpose |
| --- | --- |
| [`agent-plugin-builder`](skills/agent-plugin-builder/README.md) | Create, migrate, validate, package, and release Agent Plugins 1.0.0. |
| [`new-agent`](skills/new-agent/README.md) | Create least-privilege, IDE-native agents for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca. |
| [`new-prompt`](skills/new-prompt/README.md) | Create and improve ready-to-use LLM prompts. |
| [`new-skill`](skills/new-skill/README.md) | Create, validate, evaluate, and package portable Agent Skills. |

Compatible clients discover each immediate child of `skills/` that contains a valid `SKILL.md`. This package has no MCP servers, so it intentionally omits `mcp.json`.

## Install in supported IDEs and agents

This repository is a portable Agent Plugins 1.0.0 package. Its portable payload is
the root `plugin.json` plus the four directories directly below `skills/`; each
of those directories contains the required `SKILL.md` and any supporting files.
Keep an entire skill directory together when installing it—do not copy only its
`SKILL.md`, because some skills use scripts, templates, and references.

The clients below fall into two groups:

* **Bundle-aware clients** can consume this repository as a plugin directory.
* **Skill-aware clients** consume the directories in `skills/` individually. A
  client-native extension named “plugin” may use a different manifest and is not
  interchangeable with this portable package.

Before installing, clone or download a trusted copy of this repository and set
`PLUGIN_DIR` to its absolute path. The examples use POSIX shells; on Windows,
copy the same directories using Explorer or PowerShell.

```bash
git clone <repository-url> ai-skills-plugin
cd ai-skills-plugin
export PLUGIN_DIR="$PWD"
```

The following command is the manual-install pattern used throughout this guide.
It copies all four skill directories and preserves their bundled resources:

```bash
mkdir -p <skills-root>
cp -R "$PLUGIN_DIR"/skills/* <skills-root>/
```

### Antigravity

Antigravity IDE is bundle-aware. It requires a `plugin.json` at the plugin root
and discovers `skills/<skill-name>/SKILL.md`; this repository already has that
layout. See [Antigravity’s plugin documentation](https://antigravity.google/docs/ide/plugins?app=antigravity-ide-).

1. Open the target workspace in Antigravity.
2. Copy or symlink the **whole** `ai-skills-plugin` directory to one of these
   locations (the directory name is the plugin name):

   ```text
   <workspace>/.agents/plugins/ai-skills-plugin/   # workspace-only
   <workspace>/_agents/plugins/ai-skills-plugin/   # workspace-only alternative
   ~/.gemini/config/plugins/ai-skills-plugin/      # all workspaces
   ```

   For example:

   ```bash
   mkdir -p .agents/plugins
   ln -s "$PLUGIN_DIR" .agents/plugins/ai-skills-plugin
   ```

3. Confirm that the installed directory contains `plugin.json` and
   `skills/<skill-name>/SKILL.md`. No Antigravity-specific configuration is
   needed because this package has no MCP servers, hooks, or rules.
4. Antigravity scans these locations automatically. Reopen the workspace or
   start a new agent conversation if the skills list was already open; a full
   IDE restart is not documented as required.
5. Describe a matching task, or ask the agent to use one of the installed
   skills to verify discovery.

**Marketplace route:** Antigravity’s Customizations page installs Google-built
bundled plugins. This package is not currently listed there, so use the manual
route above.

### Codex

Codex supports reusable plugins through the shared Plugin Directory, but the
reliable local-development route is to install this package’s skills. The
required file for each installed skill is `SKILL.md` with `name` and
`description`; the optional `agents/openai.yaml` is not needed here. Official
OpenAI documentation describes the supported local locations and invocation
syntax in [Build skills](https://developers.openai.com/codex/skills).

1. Copy or symlink each immediate child of `skills/` to one of these skill
   roots:

   ```text
   <repository>/.agents/skills/<skill-name>/  # shared with this repository
   ~/.agents/skills/<skill-name>/             # personal, all repositories
   /etc/codex/skills/<skill-name>/             # administrator-managed, all users
   ```

   For a project-local install from this repository’s parent directory:

   ```bash
   mkdir -p ../your-project/.agents/skills
   cp -R "$PLUGIN_DIR"/skills/* ../your-project/.agents/skills/
   ```

2. Start Codex from that project (or reopen the project in the Codex IDE
   extension). Codex searches `.agents/skills` from the current directory up to
   the repository root.
3. Run `/skills` to confirm the four skills are visible, then invoke one with
   `$new-agent`, `$new-prompt`, `$new-skill`, or `$agent-plugin-builder`. Matching requests
   can also activate a skill automatically.
4. Codex normally detects skill changes automatically. Restart Codex only when
   a newly added skill fails to appear. If an administrator disables a local
   skill in `~/.codex/config.toml`, re-enable it there and restart Codex.

**Plugin Directory / marketplace route:** If this package is published as an
OpenAI plugin, install it from the Plugin Directory and follow any connection
prompt. In a managed workspace, an administrator must enable Plugins for the
role and make the plugin Available or Installed. This repository is not itself
a listed Plugin Directory entry, so there is no marketplace install button for
it today. See [Plugins in ChatGPT and Codex](https://help.openai.com/en/articles/20001256-plugins-in-chatgpt-and-codex).

### ChatGPT

ChatGPT installs standalone skills, not local filesystem plugin directories.
Upload the four skill directories separately; each must include its required
`SKILL.md` and all of its supporting files. The root `plugin.json` is for
portable package distribution and is not a replacement for a skill upload.
See [Skills in ChatGPT](https://help.openai.com/en/articles/20001066).

1. Create one archive per skill directory (or select the directory and all its
   files in the upload picker):

   ```bash
   (
     cd "$PLUGIN_DIR/skills"
     zip -r /tmp/agent-plugin-builder.zip agent-plugin-builder
     zip -r /tmp/new-agent.zip new-agent
     zip -r /tmp/new-prompt.zip new-prompt
     zip -r /tmp/new-skill.zip new-skill
   )
   ```

2. In ChatGPT, select **Plugins** in the sidebar, open the **Skills** tab, then
   choose **Create** → **Upload from your computer**.
3. Upload each skill archive and complete the safety review if ChatGPT marks it
   **Needs Review**. A blocked upload cannot be used.
4. Use `@` in a chat to select an installed skill, or send a request that
   matches its description. There is no client restart; the skill is available
   when ChatGPT finishes scanning it.

**Plugin Directory / marketplace route:** A published version can be installed
from the Plugin Directory after reviewing its included skills and any required
apps. Workspace administrators may need to enable the plugin for the user’s
role. This repository is not currently published there, so manual skill upload
is the applicable route.

### Zed

Zed consumes Agent Skills rather than portable plugin bundles. The required
unit is `SKILL.md` in one direct child directory of the skills root; copy all
four complete directories from this repository. Zed’s official [Skills
documentation](https://zed.dev/docs/ai/skills) covers the paths, Skills Manager,
and trust model.

1. Install globally or for one project:

   ```text
   ~/.agents/skills/<skill-name>/                 # global
   <worktree>/.agents/skills/<skill-name>/        # project-local
   ```

   ```bash
   mkdir -p .agents/skills
   cp -R "$PLUGIN_DIR"/skills/* .agents/skills/
   ```

2. If this is a project-local install, open the worktree in Zed and grant
   workspace trust; Zed deliberately excludes skills in untrusted worktrees.
3. Open **AI > Skills** (or the Agent panel’s Skills Manager) to confirm the
   skills appear. Type `/` or `@skill` in an agent message to invoke one.
4. Zed live-reloads additions and edits to skills, so no restart is required.

**Marketplace/import route:** Zed can import a single GitHub-hosted Markdown
skill and can use skills from skills.sh, but this repository is not a Zed
marketplace item. Prefer the manual directory copy so that scripts and
references travel with each skill.

### OpenCode

OpenCode has two different extension systems. Its native in-process plugins
are JavaScript/TypeScript modules with a default export containing `id` and
`setup`; this repository is **not** that kind of plugin. Install its Agent
Skills instead. The needed files are the complete
`<skill-name>/SKILL.md` directories. See the [OpenCode Agent Skills
guide](https://opencode.ai/docs/skills) and, for the distinct native plugin
format, [OpenCode plugins](https://opencode.ai/v2/docs/build/plugins).

1. Copy the skills to a native or compatible discovery location:

   ```text
   <project>/.opencode/skills/<skill-name>/        # OpenCode-native project scope
   ~/.config/opencode/skills/<skill-name>/         # OpenCode-native global scope
   <project>/.agents/skills/<skill-name>/          # compatible project scope
   ~/.agents/skills/<skill-name>/                  # compatible global scope
   ```

   ```bash
   mkdir -p .opencode/skills
   cp -R "$PLUGIN_DIR"/skills/* .opencode/skills/
   ```

2. Alternatively, keep this checkout in place and add it as an explicit skills
   source in `opencode.json` or `opencode.jsonc`:

   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "skills": ["/absolute/path/to/ai-skills-plugin/skills"]
   }
   ```

3. Ensure `opencode.json` does not deny the `skill` permission. A minimal
   configuration is:

   ```json
   { "permission": { "skill": "allow" } }
   ```

4. Start a new OpenCode session and check its available skills or invoke the
   matching skill. Files in watched configuration directories reload when they
   change; restart OpenCode after changing the configuration or if discovery
   does not refresh.

**Marketplace route:** There is no applicable npm/plugin marketplace install
for this package. Do not place its root `plugin.json` in `.opencode/plugins/`:
that directory expects a JavaScript or TypeScript OpenCode plugin entrypoint.

### Qoder

Qoder IDE supports both marketplace plugins and standalone skills. This
repository’s portable `plugin.json` is not Qoder’s optional
`.qoder-plugin/plugin.json` manifest, so the portable and lowest-risk route is
to install its skills. Each complete skill directory, including `SKILL.md`, is
required. Refer to [Qoder Skills](https://docs.qoder.com/extensions/skills) and
[Qoder Plugins](https://docs.qoder.com/extensions/plugins).

1. Copy the four skill directories to a user or project scope:

   ```text
   ~/.qoder/skills/<skill-name>/                 # all Qoder projects for this user
   <project>/.qoder/skills/<skill-name>/         # one project
   ```

   ```bash
   mkdir -p .qoder/skills
   cp -R "$PLUGIN_DIR"/skills/* .qoder/skills/
   ```

2. Restart Qoder IDE, then type `/` in Chat or Quest to verify the skills are
   loaded. A project-level skill with the same name takes precedence over a
   user-level skill.
3. Invoke a skill with `/new-agent`, `/new-prompt`, `/new-skill`, or
   `/agent-plugin-builder`, or let Qoder match it automatically from its
   description.

**Plugin marketplace/import route:** This repository is not currently listed
in Qoder Marketplace. Qoder’s **Plugins** settings can import a local plugin
folder and its native manifest is optional, but a Qoder-specific package should
use `.qoder-plugin/plugin.json` for stable metadata. Do not move or rename this
package’s portable root `plugin.json` just for Qoder; use the skill route above
unless a Qoder adapter is intentionally maintained.

### Orca

Orca installs and manages Agent Skills for its coding-agent workflows. This
package needs no Orca-specific manifest: install the complete skill directories
in a standard Agent Skills location. Orca’s [skills registry documentation](https://www.onorca.dev/docs/cli/skills)
describes the `npx skills add` workflow used for published repositories.

1. For a workspace, copy or symlink the skills into the workspace’s shared
   Agent Skills location; for a personal installation use the user location:

   ```text
   <workspace>/.agents/skills/<skill-name>/       # workspace
   ~/.agents/skills/<skill-name>/                 # user-wide
   ```

   ```bash
   mkdir -p .agents/skills
   cp -R "$PLUGIN_DIR"/skills/* .agents/skills/
   ```

2. Open the workspace in Orca and start a fresh Codex/agent task. The agent
   should advertise the installed skills and load a matching one on demand.
3. Orca documents background skill updates but does not require an IDE restart
   after a manual skill copy. Reopen the workspace or begin a new task if the
   current agent session does not refresh its catalog.

**Registry / marketplace route:** Orca’s public registry is installed with
`npx skills add` and requires a published repository plus a selected skill, for
example `npx skills add <repository-url> --skill new-prompt --global`. This
repository is not currently registered as an Orca install package, so use the
manual route. Orca does not document a separate external-plugin marketplace
format that can consume this root `plugin.json` directly.

### Verify the portable package before sharing

Run the strict validator before distributing the repository or creating the
archives used above:

```bash
python3 skills/agent-plugin-builder/scripts/validate_agent_plugin.py . --strict
```

## Validation

From the plugin root, run:

```bash
python3 skills/agent-plugin-builder/scripts/validate_agent_plugin.py . --strict
```

Validate individual Skills with the Agent Skills reference validator or their own bundled validation commands.

Create a deterministic portable archive and validate the extracted copy with:

```bash
python3 skills/agent-plugin-builder/scripts/package_agent_plugin.py . \
  --output /tmp/ai-skills-plugin.zip
```

## Standard boundary

Agent Plugins 1.0.0 standardizes the root manifest, Agent Skills, and optional MCP configuration. Client installation, permissions, enablement, and UI remain client-managed.
