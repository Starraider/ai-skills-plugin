#!/usr/bin/env python3
"""Validate an Agent Plugins 1.0.0 package without executing plugin code."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import urlsplit


PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
MCP_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/mcp.schema.json"
PLUGIN_FIELDS = {
    "$schema",
    "name",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "extensions",
}
AUTHOR_FIELDS = {"name", "email", "url"}
NAME_PATTERN = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HEADER_NAME_PATTERN = re.compile(r"^[!#$%&'*+.^_`|~0-9A-Za-z-]+$")
SENSITIVE_NAME_PATTERN = re.compile(
    r"(?:authorization|api[-_]?key|access[-_]?token|client[-_]?secret|password|passwd)",
    re.IGNORECASE,
)


class Reporter:
    def __init__(self) -> None:
        self.findings: list[dict[str, str]] = []

    def add(self, level: str, location: str, message: str) -> None:
        self.findings.append({"level": level, "location": location, "message": message})

    def error(self, location: str, message: str) -> None:
        self.add("error", location, message)

    def warn(self, location: str, message: str) -> None:
        self.add("warning", location, message)

    def ok(self, location: str, message: str) -> None:
        self.add("ok", location, message)

    @property
    def errors(self) -> int:
        return sum(item["level"] == "error" for item in self.findings)

    @property
    def warnings(self) -> int:
        return sum(item["level"] == "warning" for item in self.findings)


def is_string(value: Any) -> bool:
    return isinstance(value, str)


def load_json(path: Path, reporter: Reporter, location: str) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        reporter.error(location, f"cannot read file: {exc}")
    except json.JSONDecodeError as exc:
        reporter.error(location, f"invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}")
    return None


def path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def check_package_paths(root: Path, reporter: Reporter) -> None:
    try:
        paths = list(root.rglob("*"))
    except OSError as exc:
        reporter.error("plugin", f"cannot traverse package: {exc}")
        return
    for path in paths:
        if not path_is_within(path, root):
            reporter.error(str(path.relative_to(root)), "filesystem-resolved path escapes plugin root")


def validate_manifest(root: Path, reporter: Reporter) -> dict[str, Any] | None:
    path = root / "plugin.json"
    if not path.exists():
        reporter.error("plugin.json", "required root manifest is missing")
        return None
    if not path.is_file() or not path_is_within(path, root):
        reporter.error("plugin.json", "manifest must resolve to a regular file inside plugin root")
        return None
    data = load_json(path, reporter, "plugin.json")
    if data is None:
        return None
    if not isinstance(data, dict):
        reporter.error("plugin.json", "top level must be an object")
        return None

    unknown = sorted(set(data) - PLUGIN_FIELDS)
    if unknown:
        reporter.error("plugin.json", f"closed schema rejects fields: {', '.join(unknown)}")
    if data.get("$schema") != PLUGIN_SCHEMA:
        reporter.error("plugin.json.$schema", f"must equal {PLUGIN_SCHEMA}")
    name = data.get("name")
    if not is_string(name) or not (1 <= len(name) <= 64) or not NAME_PATTERN.fullmatch(name):
        reporter.error(
            "plugin.json.name",
            "must be 1-64 lowercase letters, digits, hyphens, or periods; start and end "
            "alphanumerically; and contain no '--' or '..'",
        )

    for field in ("version", "description", "homepage", "repository", "license"):
        if field in data and not is_string(data[field]):
            reporter.error(f"plugin.json.{field}", "must be a string")

    if "author" in data:
        author = data["author"]
        if not isinstance(author, dict):
            reporter.error("plugin.json.author", "must be an object")
        else:
            author_unknown = sorted(set(author) - AUTHOR_FIELDS)
            if author_unknown:
                reporter.error(
                    "plugin.json.author", f"closed object rejects fields: {', '.join(author_unknown)}"
                )
            for field, value in author.items():
                if field in AUTHOR_FIELDS and not is_string(value):
                    reporter.error(f"plugin.json.author.{field}", "must be a string")

    if "keywords" in data and (
        not isinstance(data["keywords"], list)
        or not all(is_string(item) for item in data["keywords"])
    ):
        reporter.error("plugin.json.keywords", "must be an array of strings")

    if "extensions" in data:
        extensions = data["extensions"]
        if not isinstance(extensions, dict):
            reporter.error("plugin.json.extensions", "must be an object")
        else:
            for namespace, value in extensions.items():
                if not isinstance(value, dict):
                    reporter.error(f"plugin.json.extensions.{namespace}", "must be an object")
                if "." not in namespace:
                    reporter.warn(
                        f"plugin.json.extensions.{namespace}",
                        "namespace does not look like a stable reverse-domain identifier",
                    )

    if reporter.errors == 0:
        reporter.ok("plugin.json", "manifest satisfies the Agent Plugins 1.0.0 shape")
    return data


def parse_frontmatter(text: str) -> tuple[dict[str, str], str | None]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "SKILL.md must start with YAML frontmatter"
    closing = next((index for index in range(1, min(len(lines), 100)) if lines[index].strip() == "---"), None)
    if closing is None:
        return {}, "SKILL.md frontmatter has no closing delimiter"
    fields: dict[str, str] = {}
    index = 1
    while index < closing:
        line = lines[index]
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            index += 1
            continue
        key, raw = match.group(1), (match.group(2) or "").strip()
        if raw in {">", ">-", "|", "|-"}:
            block: list[str] = []
            index += 1
            while index < closing and (not lines[index] or lines[index][0].isspace()):
                block.append(lines[index].strip())
                index += 1
            fields[key] = ("\n" if raw.startswith("|") else " ").join(block).strip()
            continue
        if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in {"'", '"'}:
            try:
                raw = json.loads(raw) if raw[0] == '"' else raw[1:-1].replace("''", "'")
            except json.JSONDecodeError:
                return {}, f"invalid quoted value for frontmatter field {key}"
        fields[key] = raw
        index += 1
    return fields, None


def validate_skills(root: Path, reporter: Reporter) -> None:
    skills = root / "skills"
    if not skills.exists():
        reporter.ok("skills/", "optional component is absent")
        return
    if not skills.is_dir() or not path_is_within(skills, root):
        reporter.error("skills/", "must resolve to a directory inside plugin root")
        return

    discovered = 0
    for child in sorted(skills.iterdir()):
        if not child.is_dir() or not path_is_within(child, root):
            continue
        skill_file = child / "SKILL.md"
        if not skill_file.exists():
            continue
        discovered += 1
        location = f"skills/{child.name}/SKILL.md"
        if not skill_file.is_file() or not path_is_within(skill_file, root):
            reporter.error(location, "must resolve to a regular file inside plugin root")
            continue
        try:
            fields, error = parse_frontmatter(skill_file.read_text(encoding="utf-8"))
        except OSError as exc:
            reporter.error(location, f"cannot read skill: {exc}")
            continue
        if error:
            reporter.error(location, error)
            continue
        name = fields.get("name", "")
        description = fields.get("description", "")
        if not SKILL_NAME_PATTERN.fullmatch(name) or len(name) > 64:
            reporter.error(f"{location}.name", "must be a valid Agent Skills name")
        elif name != child.name:
            reporter.error(f"{location}.name", f"must match parent directory '{child.name}'")
        if not description or len(description) > 1024:
            reporter.error(f"{location}.description", "must contain 1-1024 characters")

    for nested in skills.rglob("SKILL.md"):
        try:
            depth = len(nested.relative_to(skills).parts)
        except ValueError:
            continue
        if depth > 2:
            reporter.warn(str(nested.relative_to(root)), "nested Skill is not discovered by Agent Plugins")
    reporter.ok("skills/", f"discovered {discovered} immediate-child Agent Skill(s)")


def relative_path_is_safe(value: str, prefix: str) -> bool:
    remainder = value[len(prefix) :]
    if remainder.startswith("/"):
        remainder = remainder[1:]
    parts = PurePosixPath(remainder or ".").parts
    depth = 0
    for part in parts:
        if part in {"", "."}:
            continue
        if part == "..":
            depth -= 1
            if depth < 0:
                return False
        else:
            depth += 1
    return True


def validate_stdio(server: dict[str, Any], location: str, root: Path, reporter: Reporter) -> None:
    allowed = {"type", "command", "args", "env", "cwd"}
    unknown = sorted(set(server) - allowed)
    if unknown:
        reporter.error(location, f"stdio variant rejects fields: {', '.join(unknown)}")
    command = server.get("command")
    if not is_string(command) or not command:
        reporter.error(f"{location}.command", "must be a non-empty executable token")
    elif command.startswith("./"):
        if not relative_path_is_safe(command, "./"):
            reporter.error(f"{location}.command", "plugin-relative command escapes the plugin root")
        else:
            target = root / command[2:]
            if target.exists() and not path_is_within(target, root):
                reporter.error(f"{location}.command", "resolved command escapes the plugin root")
    elif "/" in command or "\\" in command:
        reporter.error(
            f"{location}.command", "must be a bare executable name or begin with './'"
        )

    args = server.get("args")
    if args is not None and (not isinstance(args, list) or not all(is_string(item) for item in args)):
        reporter.error(f"{location}.args", "must be an array of strings")

    env = server.get("env")
    if env is not None:
        if not isinstance(env, dict) or not all(is_string(k) and is_string(v) for k, v in env.items()):
            reporter.error(f"{location}.env", "must be an object with string values")
        else:
            for key, value in env.items():
                if key in {"PLUGIN_ROOT", "PLUGIN_DATA"}:
                    reporter.error(f"{location}.env.{key}", "reserved variable must be client-supplied")
                if SENSITIVE_NAME_PATTERN.search(key) and value and "${" not in value:
                    reporter.warn(
                        f"{location}.env.{key}", "appears to contain package-visible credential data"
                    )

    cwd = server.get("cwd")
    if cwd is not None:
        if not is_string(cwd):
            reporter.error(f"{location}.cwd", "must be a string")
        else:
            prefixes = ("./", "${PLUGIN_ROOT}", "${PLUGIN_DATA}")
            prefix = next(
                (
                    candidate
                    for candidate in prefixes
                    if cwd == candidate or cwd.startswith(candidate + ("" if candidate == "./" else "/"))
                ),
                None,
            )
            if prefix is None or not relative_path_is_safe(cwd, prefix):
                reporter.error(
                    f"{location}.cwd",
                    "must stay beneath './', ${PLUGIN_ROOT}, or ${PLUGIN_DATA}",
                )


def is_loopback_host(host: str | None) -> bool:
    if host is None:
        return False
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def validate_remote(server: dict[str, Any], location: str, reporter: Reporter) -> None:
    allowed = {"type", "url", "headers"}
    unknown = sorted(set(server) - allowed)
    if unknown:
        reporter.error(location, f"remote variant rejects fields: {', '.join(unknown)}")
    url = server.get("url")
    if not is_string(url) or not url:
        reporter.error(f"{location}.url", "must be a non-empty absolute HTTP or HTTPS URL")
    else:
        parsed = urlsplit(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            reporter.error(f"{location}.url", "must be an absolute HTTP or HTTPS URL")
        if parsed.username is not None or parsed.password is not None:
            reporter.error(f"{location}.url", "must not contain user information")
        if parsed.fragment:
            reporter.error(f"{location}.url", "must not contain a fragment")
        if parsed.scheme == "http" and not is_loopback_host(parsed.hostname):
            reporter.error(f"{location}.url", "non-loopback endpoints must use HTTPS")

    headers = server.get("headers")
    if headers is not None:
        if not isinstance(headers, dict) or not all(is_string(k) and is_string(v) for k, v in headers.items()):
            reporter.error(f"{location}.headers", "must be an object with string values")
        else:
            seen: set[str] = set()
            for key, value in headers.items():
                normalized = key.lower()
                if not HEADER_NAME_PATTERN.fullmatch(key):
                    reporter.error(f"{location}.headers.{key}", "invalid HTTP header name")
                if normalized in seen:
                    reporter.error(f"{location}.headers.{key}", "duplicates a header with different casing")
                seen.add(normalized)
                if any(ord(char) < 32 and char != "\t" or ord(char) == 127 for char in value):
                    reporter.error(f"{location}.headers.{key}", "invalid control character in header value")
                if SENSITIVE_NAME_PATTERN.search(key) and value:
                    reporter.warn(
                        f"{location}.headers.{key}", "appears to contain package-visible credential data"
                    )


def validate_mcp(root: Path, reporter: Reporter) -> None:
    path = root / "mcp.json"
    if not path.exists():
        reporter.ok("mcp.json", "optional component is absent")
        return
    if not path.is_file() or not path_is_within(path, root):
        reporter.error("mcp.json", "must resolve to a regular file inside plugin root")
        return
    data = load_json(path, reporter, "mcp.json")
    if data is None:
        return
    if not isinstance(data, dict):
        reporter.error("mcp.json", "top level must be an object")
        return
    unknown = sorted(set(data) - {"$schema", "mcpServers"})
    if unknown:
        reporter.error("mcp.json", f"closed schema rejects fields: {', '.join(unknown)}")
    if data.get("$schema") != MCP_SCHEMA:
        reporter.error("mcp.json.$schema", f"must equal {MCP_SCHEMA}")
    servers = data.get("mcpServers")
    if not isinstance(servers, dict):
        reporter.error("mcp.json.mcpServers", "must be an object")
        return
    for name, server in servers.items():
        location = f"mcp.json.mcpServers.{name}"
        if not isinstance(server, dict):
            reporter.error(location, "must be an object")
            continue
        server_type = server.get("type")
        if server_type == "stdio":
            validate_stdio(server, location, root, reporter)
        elif server_type in {"streamable-http", "sse"}:
            validate_remote(server, location, reporter)
            if server_type == "sse":
                reporter.warn(location, "legacy SSE transport is deprecated and client support is optional")
        else:
            reporter.error(f"{location}.type", "must be stdio, streamable-http, or sse")
    reporter.ok("mcp.json", f"checked {len(servers)} MCP server entr{'y' if len(servers) == 1 else 'ies'}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate Agent Plugins 1.0.0 structure without running plugin code."
    )
    parser.add_argument("plugin_root", help="Path to the plugin root")
    parser.add_argument("--strict", action="store_true", help="Return failure for warnings too")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.plugin_root).expanduser()
    reporter = Reporter()
    if not root.is_dir():
        reporter.error("plugin", f"not a directory: {root}")
    else:
        root = root.resolve()
        check_package_paths(root, reporter)
        validate_manifest(root, reporter)
        validate_skills(root, reporter)
        validate_mcp(root, reporter)

    failed = reporter.errors > 0 or (args.strict and reporter.warnings > 0)
    if args.format == "json":
        print(
            json.dumps(
                {
                    "ok": not failed,
                    "plugin_root": str(root),
                    "errors": reporter.errors,
                    "warnings": reporter.warnings,
                    "findings": reporter.findings,
                },
                indent=2,
            )
        )
    else:
        for item in reporter.findings:
            print(f"{item['level'].upper()}: {item['location']}: {item['message']}")
        print(
            f"RESULT: {reporter.errors} error(s), {reporter.warnings} warning(s), "
            f"strict={'yes' if args.strict else 'no'}"
        )
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
