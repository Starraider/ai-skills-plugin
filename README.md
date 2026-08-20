# AI Skills Plugin

A portable [Agent Plugins 1.0.0](https://agent-plugins.org/) package containing reusable Agent Skills for AI-harness diagnosis, prompt design, IDE-native agent, hook, and slash-command creation, Skill authoring, and Agent Plugin creation.

## Included Skills

| Skill | Purpose |
| --- | --- |
| [`agent-plugin-builder`](skills/agent-plugin-builder/README.md) | Create, migrate, validate, package, and release Agent Plugins 1.0.0. |
| [`improve-my-ai-harness`](skills/improve-my-ai-harness/README.md) | Diagnose an AI-IDE problem, select the smallest suitable harness mechanism or combination, and produce a builder-routed implementation prompt. |
| [`new-agent`](skills/new-agent/README.md) | Create least-privilege, IDE-native agents for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca. |
| [`new-agents-md`](skills/new-agents-md/README.md) | Create concise, target-aware `AGENTS.md` repository instructions for Antigravity, Codex, ChatGPT, Zed, OpenCode, Qoder, or Orca. |
| [`new-hook`](skills/new-hook/README.md) | Decide whether an event hook is appropriate and create a target-native hook or supported alternative. |
| [`new-prompt`](skills/new-prompt/README.md) | Create and improve ready-to-use LLM prompts. |
| [`new-skill`](skills/new-skill/README.md) | Create, validate, evaluate, and package portable Agent Skills. |
| [`new-slash-command`](skills/new-slash-command/README.md) | Decide whether a reusable task should be a slash command and create the target-native command or supported alternative. |
| [`new-workflow`](skills/new-workflow/README.md) | Decide whether a workflow is appropriate and create a target-native workflow or supported alternative. |

Compatible clients discover each immediate child of `skills/` that contains a valid `SKILL.md`. This package has no MCP servers, so it intentionally omits `mcp.json`.

## Install in supported IDEs and agents

This repository is a portable Agent Plugins 1.0.0 package. Its portable payload is
the root `plugin.json` plus the nine directories directly below `skills/`; each
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
It copies all nine skill directories and preserves their bundled resources:

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
3. Run `/skills` to confirm the nine skills are visible, then invoke one with
   `$improve-my-ai-harness`, `$new-agent`, `$new-agents-md`, `$new-hook`, `$new-prompt`, `$new-skill`, `$new-slash-command`, `$new-workflow`, or `$agent-plugin-builder`. Matching requests
   can also activate a skill automatically.
4. Codex normally detects skill changes automatically. Restart Codex only when
   a newly added skill fails to appear. If an administrator disables a local
   skill in `~/.codex/config.toml`, re-enable it there and restart Codex.


### ChatGPT Desktop App

The ChatGPT Desktop App (on macOS and Windows) installs standalone Agent Skills rather than loading local filesystem Agent Plugins 1.0.0 package directories directly. Because the desktop app does not support importing raw local plugin bundles containing `plugin.json`, install this package according to the individual Skill installation workflow: upload each of the nine skill directories separately. Each upload must include its required `SKILL.md` and all supporting files, references, templates, and scripts. The root `plugin.json` is for portable package distribution and is not a replacement for a skill upload. See [Skills in ChatGPT](https://help.openai.com/en/articles/20001066).

1. Create one archive per skill directory (or select the directory and all its
   files in the upload picker):

   ```bash
   (
     cd "$PLUGIN_DIR/skills"
     zip -r /tmp/agent-plugin-builder.zip agent-plugin-builder
     zip -r /tmp/improve-my-ai-harness.zip improve-my-ai-harness
     zip -r /tmp/new-agent.zip new-agent
     zip -r /tmp/new-agents-md.zip new-agents-md
     zip -r /tmp/new-hook.zip new-hook
     zip -r /tmp/new-prompt.zip new-prompt
     zip -r /tmp/new-skill.zip new-skill
     zip -r /tmp/new-slash-command.zip new-slash-command
     zip -r /tmp/new-workflow.zip new-workflow
   )
   ```

2. In the ChatGPT Desktop App, select **Plugins** in the sidebar (or navigate via **Settings → Plugins**), open the **Skills** tab, then choose **Create** → **Upload from your computer**.
3. Upload each skill archive or directory and complete the safety review if the desktop app marks it **Needs Review**. A blocked upload cannot be used.
4. Use `@` in a desktop chat session to select an installed skill, or send a request that matches its description. There is no client restart; the skill is available when the ChatGPT Desktop App finishes scanning it. Note that skills installed in the desktop app do not automatically sync across web or mobile surfaces and are managed locally within the desktop application.


### Zed

Zed consumes Agent Skills rather than portable plugin bundles. The required
unit is `SKILL.md` in one direct child directory of the skills root; copy all
nine complete directories from this repository. Zed’s official [Skills
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

> **Note:** Do not place this package's root `plugin.json` in `.opencode/plugins/` — that directory expects a JavaScript or TypeScript OpenCode plugin entrypoint, not an Agent Plugins 1.0.0 package.

### Qoder

Qoder IDE supports both marketplace plugins and standalone skills. This
repository’s portable `plugin.json` is not Qoder’s optional
`.qoder-plugin/plugin.json` manifest, so the portable and lowest-risk route is
to install its skills. Each complete skill directory, including `SKILL.md`, is
required. Refer to [Qoder Skills](https://docs.qoder.com/extensions/skills) and
[Qoder Plugins](https://docs.qoder.com/extensions/plugins).

1. Copy the nine skill directories to a user or project scope:

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
3. Invoke a skill with `/improve-my-ai-harness`, `/new-agent`, `/new-agents-md`, `/new-hook`, `/new-prompt`, `/new-skill`, `/new-slash-command`, `/new-workflow`,
   or `/agent-plugin-builder`, or let Qoder match it automatically from its
   description.

### Cursor

Cursor is bundle-aware and loads this repository as a complete Agent Plugins
1.0.0 package. It distinguishes between portable Agent Plugins (root
`plugin.json`) and Cursor-native plugins (`.cursor-plugin/plugin.json`); this
repository is a portable package. See [Cursor Plugins
documentation](https://cursor.com/docs/plugins).

1. Copy or symlink the whole `ai-skills-plugin` directory to the local plugins
   folder:

   ```text
   ~/.cursor/plugins/local/ai-skills-plugin/   # macOS / Linux
   %USERPROFILE%\.cursor\plugins\local\ai-skills-plugin\   # Windows
   ```

   ```bash
   mkdir -p ~/.cursor/plugins/local
   ln -s "$PLUGIN_DIR" ~/.cursor/plugins/local/ai-skills-plugin
   ```

2. Reload the window to trigger discovery: open the Command Palette
   (`Cmd+Shift+P` / `Ctrl+Shift+P`) and run **Developer: Reload Window**, or
   restart Cursor. Hot-reload is not supported for local plugins.
3. Open **Customize** in the sidebar (or **Settings → Plugins**) and confirm
   that `ai-skills-plugin` appears under **Installed**.


### GitHub Copilot and VS Code

GitHub Copilot and VS Code share the same plugin loading mechanism. The
reliable local-development route registers the plugin directory in VS Code's
`settings.json`. See [GitHub Copilot Agent Plugins
documentation](https://docs.github.com/en/copilot/using-github-copilot/using-agent-plugins)
and [VS Code chat plugin settings](https://code.visualstudio.com/docs/copilot/agent-plugins).

1. Open VS Code's `settings.json` (Command Palette → **Preferences: Open User
   Settings (JSON)**) and add the plugin path:

   ```json
   "chat.plugins.enabled": true,
   "chat.pluginLocations": {
     "/absolute/path/to/ai-skills-plugin": true
   }
   ```

   Replace `/absolute/path/to/ai-skills-plugin` with `$PLUGIN_DIR`'s value.

2. Reload VS Code (**Developer: Reload Window**). Copilot reads
   `chat.pluginLocations` on startup; changes require a reload.
3. Verify in the Chat view: click the gear icon → **Configure Skills** and
   confirm the nine skills appear. Any `mcp.json` servers (this package has
   none) would appear in the MCP server list.


**Enterprise note:** Workspace and enterprise administrators can restrict
available plugins with the `chat.plugins.paths` policy or via
`enabledPlugins` / `strictKnownMarketplaces` managed settings. Confirm that
local plugin paths are allowed in managed environments before using this route.

### Windsurf

Windsurf's Cascade agent discovers skills from standard `.agents/skills/`
paths and from explicit entries in the project-level `.windsurf/skills.json`.
MCP servers are managed separately via `~/.codeium/windsurf/mcp_config.json`
(this package has none). See [Windsurf documentation](https://docs.codeium.com/windsurf).

**Option A — Standard discovery path (recommended):**

1. Copy the nine skill directories to the project or global discovery path:

   ```text
   <project>/.agents/skills/<skill-name>/          # project-local
   ~/.agents/skills/<skill-name>/                  # global
   ```

   ```bash
   mkdir -p .agents/skills
   cp -R "$PLUGIN_DIR"/skills/* .agents/skills/
   ```

2. Open or reopen the project in Windsurf. Cascade picks up new skills from
   watched directories without an IDE restart.

**Option B — Explicit `skills.json` reference:**

Add the plugin's skills directory to `.windsurf/skills.json` so the path
travels with the repository:

```json
{
  "skills": ["/absolute/path/to/ai-skills-plugin/skills"]
}
```

Windsurf reloads this file when it changes; a full restart is not required.

### Kiro

Kiro calls Agent Plugins **"Powers"** and supports importing a local folder
containing a `plugin.json` directly through its Powers panel. Manual skill
directory placement also works. See [Kiro Powers
documentation](https://kiro.dev/docs/powers).

**GUI route (recommended):**

1. Open the **Powers panel** in Kiro (click the ghost-with-lightning-bolt
   icon in the activity bar).
2. Select **Add Custom Power → Import power from a folder**.
3. Choose the `ai-skills-plugin` root directory (the folder that contains
   `plugin.json`).
4. Click **Install**. Kiro reads the `plugin.json`, discovers all skills under
   `skills/`, and activates them immediately.

**Manual skill route:**

```text
<workspace>/.kiro/skills/<skill-name>/   # workspace-specific
~/.kiro/skills/<skill-name>/             # global
```

```bash
mkdir -p .kiro/skills
cp -R "$PLUGIN_DIR"/skills/* .kiro/skills/
```


**Note:** Kiro also supports a legacy `POWER.md` format; the `plugin.json`
route is recommended for new installations.

### Google Agents CLI

The Google Agents CLI (`agents-cli`) consumes Agent Plugins 1.0.0 packages
as skill bundles that teach the CLI's built-in coding assistant how to perform
ADK (Agent Development Kit) lifecycle tasks. This package's skills are
independent of the ADK but load through the same mechanism.

**Prerequisites:** Python 3.11+, Node.js, and `uv`.

1. Install and set up the CLI (one-time):

   ```bash
   uvx google-agents-cli setup
   ```

2. Register this package's skills globally via the `npx skills add` command:

   ```bash
   npx skills add /absolute/path/to/ai-skills-plugin --global
   ```

   Or, for a project-local install, run from the project directory without
   `--global`:

   ```bash
   npx skills add /absolute/path/to/ai-skills-plugin
   ```

3. Confirm that the skills are visible inside the agents CLI's coding-assistant
   context. No CLI restart is required; skills are discovered at session start.

**Note:** The `agents-cli` does not provide a universal `agents-cli install`
command for arbitrary Agent Plugins packages. Discovery is handled by the
`npx skills add` pathway above, which registers the `skills/` directory from
the package.

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

## License

This project and all contained Agent Skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).

