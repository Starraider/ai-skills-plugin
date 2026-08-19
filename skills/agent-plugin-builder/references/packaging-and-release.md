# Packaging and release

Use this reference when producing a portable archive or preparing a versioned Agent Plugin release. Agent Plugins standardizes the package contents, not publication, installation, or enablement.

## Separate source from payload

Classify each source path before packaging:

- **Portable runtime:** root `plugin.json`, immediate-child Skills and their resources, optional root `mcp.json`, and executables or data referenced by MCP configuration.
- **Human documentation:** root README, licenses, notices, and attribution.
- **Client extension:** only a documented reverse-domain extension directory declared by the owning client.
- **Maintainer-only:** CI, tests, evals, caches, editor state, release helpers, and development reports.

Package the first three classes and exclude the fourth. A top-level runtime path outside the fixed component locations must be included explicitly with `--include`; never widen the allowlist merely because a directory exists.

## Source safety

Resolve symlinks and locate the editable source before changing files. Do not edit generated archives or client-managed installed copies and caches. If only an installed copy exists, create a source workspace and record its origin before modifying it.

Preserve unrelated local changes, signing configuration, and repository hooks. Do not bypass verification to force a release.

## Build and verify

Run:

```bash
python3 scripts/package_agent_plugin.py /path/to/plugin \
  --output /path/to/plugin.zip
```

The packager:

1. validates the source plugin;
2. validates every immediate-child Skill with the bundled documentation profile;
3. builds a deterministic archive from an explicit allowlist;
4. rejects symlinks and paths that escape the plugin root;
5. extracts into a clean temporary directory; and
6. repeats plugin and Skill validation against the extracted copy.

Use `--include <relative-path>` for additional runtime roots that are not inferred from `mcp.json`. Use `--expected-version X.Y.Z` when a release must match a planned version.

## Version and tag discipline

Use root `plugin.json.version` as the plugin version source. Do not duplicate the version into each Skill's metadata unless an identified consumer requires it.

For a versioned release:

1. update the manifest and human documentation together;
2. validate the source and clean archive;
3. run representative, edge-case, and near-miss evals for changed behavior;
4. merge the version change before creating its tag;
5. create a signed tag when repository policy supports signing;
6. publish once and verify the released archive; and
7. never reuse a published version or tag.

For a batch affecting multiple plugins, prepare a manifest of roots, current versions, target versions, validation results, and execution order. Obtain approval before publishing the batch and stop after the first failure.

## Integrity

For public archives containing executable code, produce checksums and provenance in the same release job before making the files available. Verification must bind the provenance to the exact source repository, not merely to a broad organization namespace.
