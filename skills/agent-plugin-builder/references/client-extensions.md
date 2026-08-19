# Client extensions

Read this reference only when the request requires client-specific manifest data or files. The [Agent Plugins client extensions guide](https://agent-plugins.org/plugin-authors/client-extensions) and [normative specification](https://agent-plugins.org/specification) are authoritative.

Agent Plugins 1.0.0 standardizes Skills and MCP servers, not hooks, commands, custom agents, LSP configuration, UI, discovery metadata, installation, permissions, or policy. A client can define those through a namespace it owns.

## Manifest data

Put client-owned data under root manifest `extensions`, keyed by a stable reverse-domain namespace documented by that client:

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "example-plugin",
  "extensions": {
    "com.example.client": {
      "setting": true
    }
  }
}
```

Every namespace value must be an object. Other clients ignore namespaces they do not implement without interpreting their content.

## Extension files

Client-owned files live in a top-level directory whose name exactly matches the namespace:

```text
example-plugin/
├── plugin.json
├── skills/
└── com.example.client/
    └── hooks/
        └── hooks.json
```

A client may define manifest data, a directory, or both. The namespace owner defines validation, loading, relationships, permissions, and failure handling.

## Authoring rules

- Use only a namespace and structure documented by the client that owns it; do not invent fields based on another client's format.
- Keep the namespace stable and base it on a domain controlled by the owning client.
- Do not move client-specific fields to the root of `plugin.json`.
- Do not describe extension content as portable or require unrelated clients to validate it.
- During migration, preserve known-working client files until the extension or compatibility package has been tested in that client.
