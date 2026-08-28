# MCP server configuration

Read this reference only when a plugin includes or changes MCP servers. The [Agent Plugins MCP guide](https://agent-plugins.org/plugin-authors/mcp-servers), [normative specification](https://agent-plugins.org/specification), and [canonical MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json) are authoritative.

## Root document

Root `mcp.json` is a closed object containing only these two required fields:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json",
  "mcpServers": {}
}
```

The schema version must match root `plugin.json`. Each `mcpServers` member is validated independently and matches exactly one closed transport variant.

## Stdio

```json
{
  "type": "stdio",
  "command": "./bin/validator",
  "args": ["--data", "${PLUGIN_DATA}/validator"],
  "env": {
    "CONFIG": "${PLUGIN_ROOT}/config.json"
  },
  "cwd": "${PLUGIN_ROOT}"
}
```

- Required: `type`, `command`. Optional: `args`, `env`, `cwd`. No other fields.
- `command` is one executable token, not a shell command. It is a bare executable name resolved by platform search rules or a plugin-relative path beginning with `./`. Placeholder expansion never applies to `command`.
- A bundled executable uses a `./` path and must resolve within the plugin root.
- `args` is an array of strings. `env` is an object with string values.
- `env` must not define the reserved `PLUGIN_ROOT` or `PLUGIN_DATA` keys.
- Omitted `cwd` means the plugin root. An explicit value begins with `./`, equals `${PLUGIN_ROOT}` or `${PLUGIN_DATA}`, or begins with one of those placeholders followed by `/`. It must remain within its selected root after resolution.

Clients provide `PLUGIN_ROOT` as the resolved package root and `PLUGIN_DATA` as a writable, persistent, client-managed data directory. They expand exact occurrences of these two placeholders once, non-recursively, in `args` elements, `env` values, and `cwd`. They do not expand them in `command`, environment keys, URLs, or headers. Unrecognized placeholder-like text remains literal.

Use `PLUGIN_ROOT` for bundled read-only code and configuration. Use `PLUGIN_DATA` for installed dependencies, generated code, caches, and persistent plugin state.

## Streamable HTTP and legacy SSE

```json
{
  "type": "streamable-http",
  "url": "https://deploy.example.com/mcp",
  "headers": {
    "X-Tenant": "public-tenant"
  }
}
```

- Required: `type`, `url`. Optional: literal `headers`. No other fields.
- Use `streamable-http` for the current remote transport. `sse` means deprecated MCP HTTP+SSE; client support is optional.
- The URL is absolute HTTP or HTTPS, with no user information or fragment. Non-loopback endpoints require HTTPS. HTTP is allowed only for host `localhost` or an IP literal in a loopback range.
- Header names and values are valid HTTP fields. Names are case-insensitive and must not be duplicated with different casing.
- Clients do not expand placeholders or environment variables in URLs or headers.

Headers and configured environment values are visible package data, not secret stores. Never embed credentials, bearer tokens, passwords, API keys, or other secrets. Agent Plugins 1.0.0 defines no portable OAuth or credential-reference fields; authentication discovery, user interaction, and credential storage remain client-managed.

## Failure boundaries

- Invalid top-level `mcp.json` disables MCP for the plugin but does not disable valid Skills.
- An invalid individual server disables only that entry.
- An unsupported transport or a start, connection, authentication, or handshake failure disables only that server.
- A conforming MCP-capable client supports at least one of stdio or Streamable HTTP and should support both; support for legacy SSE is optional.
