# Installing Agent Plugins

This guide covers plugins that follow
[Agent Plugins 1.0.0](https://agent-plugins.org/specification). The standard
fixes the package layout and portable component formats, but each client
controls installation, trust, updates, and scope.

The examples use these placeholders:

- `<plugin-repository-url>`: the Git URL of an Agent Plugin repository
- `<plugin-name>`: the `name` from the root `plugin.json`
- `<marketplace-name>`: the client-specific marketplace that distributes the
  plugin

For this repository, the source URL is
`https://github.com/Starraider/ai-skills-plugin` and the plugin name
is `ai-skills-plugin`.

Review the plugin before installing it. A plugin can contain instructions,
scripts, and MCP server definitions that cause code to run on your machine.

## Compatibility

Verified on 25 August 2026 against the
[Agent Plugins compatible-client list](https://agent-plugins.org/compatible-clients)
and each product's documentation.

| Client             | 1.0.0 support | Installation                 |
| ------------------ | ------------- | ---------------------------- |
| Antigravity        | No            | [Skills][antigravity-skills] |
| Codex              | Yes           | Plugin instructions below    |
| Cursor             | Yes           | Plugin instructions below    |
| GitHub Copilot     | Yes           | Plugin instructions below    |
| Visual Studio Code | Yes           | Plugin instructions below    |
| OpenCode           | No            | [Skills][opencode-skills]    |
| Windsurf           | No            | [Skills][windsurf-skills]    |
| Zed                | No            | [Skills][zed-skills]         |
| Trae               | No            | [Skills][trae-skills]        |
| Qoder              | No            | [Skills][qoder-skills]       |

"No documented support" means that the client is not listed as a compatible
Agent Plugins client and its own documentation does not claim conformance. It
may have a product-specific extension system also called plugins. That is not
the same format. For example, Qoder uses `.qoder-plugin/plugin.json`, while
Agent Plugins 1.0.0 requires `plugin.json` at the package root. See the
[Qoder plugin reference](https://docs.qoder.com/cli/plugins-reference).

This repository is an Agent Plugin package, not a plugin marketplace. VS Code
can install it directly from its Git URL, and Cursor can load a local clone.
Codex CLI and GitHub Copilot CLI require a marketplace entry. If the plugin has
not been published in a marketplace available to those clients, use the linked
individual-skill installation until a marketplace entry exists.

## Codex

Codex is listed as an Agent Plugins client and can load portable skills and MCP
servers from a conforming package. OpenAI distributes plugins through the plugin
directory and configured marketplaces. See the
[OpenAI plugin documentation](https://developers.openai.com/plugins) and the
[Codex skills documentation](https://developers.openai.com/codex/skills).

### Global installation in Codex

For a plugin published in the shared plugin directory:

1. Open **Plugins** in the ChatGPT desktop app or Codex.
2. Find the plugin, review its contents and permissions, and select **Install**.
3. Start a new Codex task if the plugin's skills do not appear in the current
   task.

Codex CLI can install from a configured marketplace:

```bash
codex plugin marketplace add <owner>/<marketplace-repository>
codex plugin list
codex plugin add <plugin-name>@<marketplace-name>
```

Run `codex plugin marketplace --help` and `codex plugin add --help` for the
commands supported by your installed Codex version.

The plugin repository and a marketplace repository are different things. If a
plugin is available only as an ordinary Git repository, its publisher must list
it in a Codex-compatible marketplace or the shared plugin directory before
`codex plugin add` can install it. Until then, install its skills individually
with the
[Codex skill locations](https://developers.openai.com/codex/skills#where-codex-loads-local-skills).

### Project-specific use in Codex

Codex does not currently document a repository-scoped plugin installation.
Plugin installation is user or workspace account state. For a project-only
setup, install the plugin's individual skills under
`<project-root>/.agents/skills/` as described in the
[Codex skill documentation](https://developers.openai.com/codex/skills#where-codex-loads-local-skills).
Commit that directory if the team should receive the same skills.

## Cursor

Cursor supports Agent Plugins alongside Cursor's own plugin format. A conforming
root `plugin.json` loads without conversion. See
[Cursor's plugin documentation](https://cursor.com/docs/plugins).

### Global installation in Cursor

From a configured marketplace:

1. Open **Customize** in the Cursor sidebar.
2. Find the plugin and select **Install**.
3. Choose **User** scope to make it available in every project.

For a local plugin or a Git repository that is not in a marketplace, clone it
into Cursor's local plugin directory:

```bash
git clone <plugin-repository-url> ~/.cursor/plugins/local/<plugin-name>
```

Restart Cursor or run **Developer: Reload Window**. Cursor documents
`~/.cursor/plugins/local/` as a local testing location, so marketplace
installation is the better choice for managed updates.

### Project-specific installation in Cursor

1. Open the target project in Cursor.
2. Open **Customize** and find the plugin in a configured marketplace.
3. Select **Install**, then choose **Project** scope.

Use **Customize** to filter installed items by user or workspace scope. A team
marketplace can distribute either Agent Plugins or Cursor Plugins, but team
marketplace availability depends on the Cursor plan.

## GitHub Copilot

GitHub Copilot supports the portable Agent Plugins format in Copilot CLI, the
Copilot app, and the cloud agent. VS Code also discovers plugins installed by
Copilot CLI. See
[GitHub's plugin overview](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
and
[installation guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-finding-installing).

### Global installation in GitHub Copilot

Register the marketplace if Copilot does not already know it, then install the
plugin:

```bash
copilot plugin marketplace add <owner>/<marketplace-repository>
copilot plugin install <plugin-name>@<marketplace-name>
copilot plugin list
```

The interactive equivalents are `/plugin marketplace add`, `/plugin install`,
and `/plugin list`.

### Project-specific installation in GitHub Copilot

Declare the marketplace and plugin in
`<project-root>/.github/copilot/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "<marketplace-name>": {
      "source": {
        "source": "github",
        "repo": "<owner>/<marketplace-repository>"
      }
    }
  },
  "enabledPlugins": {
    "<plugin-name>@<marketplace-name>": true
  }
}
```

Commit the file when the repository should recommend the same plugin to
contributors. Copilot cloud agent uses this repository-level configuration.
Local clients may still ask each user to trust or install the marketplace.

## Visual Studio Code

VS Code recognizes Agent Plugins 1.0.0 by the root manifest schema. It can
install from a marketplace, a Git repository, or a local directory. See
[Agent plugins in VS Code](https://code.visualstudio.com/docs/agent-customization/agent-plugins).

### Global installation in VS Code

To install directly from Git:

1. Run **Chat: Install Plugin From Source** from the Command Palette.
2. Enter `<plugin-repository-url>`.
3. Review the trust prompt and confirm the installation.

To use a marketplace instead, open the Extensions view, search for
`@agentPlugins`, choose a plugin, and select **Install**. You can also open
**Chat: Open Customizations**, select **Plugins**, and browse the marketplace
there.

### Project-specific installation in VS Code

VS Code installs the plugin files for the user, then stores enablement
separately for each workspace:

1. Install the plugin from source or a marketplace.
2. Open the target workspace.
3. Open **Chat: Open Customizations** and select **Plugins**.
4. Enable the plugin for this workspace and disable its global enablement if it
   should not run elsewhere.

For a team-managed project, use `.github/copilot/settings.json` with
`extraKnownMarketplaces` and `enabledPlugins`, as shown in the GitHub Copilot
section. This recommends the plugin to contributors; it does not silently bypass
their trust decision.

For local development, clone the plugin anywhere and register its absolute
directory in user or workspace settings:

```jsonc
{
  "chat.pluginLocations": {
    "/absolute/path/to/my-plugin": true,
  },
}
```

Set `chat.plugins.enabled` to `true` if plugin support has been disabled in the
current VS Code profile.

[antigravity-skills]: skill-installation.md#antigravity
[opencode-skills]: skill-installation.md#opencode
[qoder-skills]: skill-installation.md#qoder
[trae-skills]: skill-installation.md#trae
[windsurf-skills]: skill-installation.md#windsurf
[zed-skills]: skill-installation.md#zed
