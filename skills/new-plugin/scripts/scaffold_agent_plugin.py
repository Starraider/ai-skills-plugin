#!/usr/bin/env python3
"""Create a minimal Agent Plugins 1.0.0 manifest safely."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
NAME_PATTERN = re.compile(r"^(?!.*(?:--|\.\.))[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?$")


def non_empty(value: str) -> str:
    if not value:
        raise argparse.ArgumentTypeError("value must not be empty")
    return value


def valid_name(value: str) -> str:
    if len(value) > 64 or not NAME_PATTERN.fullmatch(value):
        raise argparse.ArgumentTypeError(
            "name must be 1-64 lowercase ASCII letters, digits, hyphens, or periods; "
            "it must start and end alphanumerically and contain no '--' or '..'"
        )
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create plugin.json for an Agent Plugins 1.0.0 package."
    )
    parser.add_argument("output", help="Exact plugin root to create or populate")
    parser.add_argument("--name", required=True, type=valid_name, help="Plugin name")
    parser.add_argument("--version", type=non_empty, help="Plugin version string")
    parser.add_argument("--description", type=str, help="Short plugin description")
    parser.add_argument("--author-name", type=str)
    parser.add_argument("--author-email", type=str)
    parser.add_argument("--author-url", type=str)
    parser.add_argument("--homepage", type=str)
    parser.add_argument("--repository", type=str)
    parser.add_argument("--license", dest="license_name", type=str)
    parser.add_argument(
        "--keyword", action="append", default=[], help="Repeat for multiple keywords"
    )
    parser.add_argument(
        "--format", choices=("text", "json"), default="text", help="Result format"
    )
    return parser


def fail(message: str, output_format: str) -> int:
    if output_format == "json":
        print(json.dumps({"ok": False, "error": message}))
    else:
        print(f"ERROR: {message}", file=sys.stderr)
    return 1


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.output).expanduser()

    if root.exists() and not root.is_dir():
        return fail(f"output exists and is not a directory: {root}", args.format)
    if root.is_dir() and any(root.iterdir()):
        return fail(f"refusing to write into non-empty directory: {root}", args.format)

    manifest: dict[str, object] = {"$schema": PLUGIN_SCHEMA, "name": args.name}
    for field in ("version", "description", "homepage", "repository"):
        value = getattr(args, field)
        if value is not None:
            manifest[field] = value
    if args.license_name is not None:
        manifest["license"] = args.license_name

    author = {
        field: value
        for field, value in (
            ("name", args.author_name),
            ("email", args.author_email),
            ("url", args.author_url),
        )
        if value is not None
    }
    if author:
        manifest["author"] = author
    if args.keyword:
        manifest["keywords"] = args.keyword

    try:
        root.mkdir(parents=True, exist_ok=True)
        manifest_path = root / "plugin.json"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    except OSError as exc:
        return fail(f"could not create manifest: {exc}", args.format)

    result = {
        "ok": True,
        "plugin_root": str(root.resolve()),
        "manifest": str(manifest_path.resolve()),
        "schema_version": "1.0.0",
    }
    if args.format == "json":
        print(json.dumps(result))
    else:
        print(f"Created {manifest_path.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
