#!/usr/bin/env python3
"""Build and verify a deterministic allowlisted Agent Plugin archive."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from typing import Iterable


MAINTAINER_PARTS = {
    ".git",
    ".github",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "__pycache__",
    "evals",
    "tests",
}
MAINTAINER_NAMES = {".DS_Store", "AGENTS.md"}
MAINTAINER_SUFFIXES = {".pyc", ".pyo"}
CLIENTS = "claude,codex,cursor,antigravity,opencode,qoder"


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr)
    return 1


def path_is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except (OSError, ValueError):
        return False


def safe_relative(value: str) -> Path:
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise ValueError(f"path must be a normalized plugin-relative path: {value}")
    if any(part in MAINTAINER_PARTS for part in pure.parts):
        raise ValueError(f"maintainer-only path cannot be packaged: {value}")
    return Path(*pure.parts)


def top_level_runtime_path(value: str) -> Path | None:
    if not value.startswith("./"):
        return None
    remainder = value[2:]
    if not remainder:
        return None
    relative = safe_relative(remainder)
    return Path(relative.parts[0])


def load_manifest(root: Path) -> dict[str, object]:
    data = json.loads((root / "plugin.json").read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("plugin.json must contain an object")
    return data


def inferred_roots(root: Path, manifest: dict[str, object]) -> set[Path]:
    selected: set[Path] = {Path("plugin.json")}
    for name in ("README.md", "mcp.json"):
        if (root / name).is_file():
            selected.add(Path(name))
    if (root / "skills").is_dir():
        selected.add(Path("skills"))
    for path in root.iterdir():
        if path.is_file() and path.name.startswith(("LICENSE", "NOTICE", "COPYING")):
            selected.add(Path(path.name))

    extensions = manifest.get("extensions")
    if isinstance(extensions, dict):
        for namespace in extensions:
            candidate = root / namespace
            if candidate.exists():
                selected.add(Path(namespace))

    mcp_file = root / "mcp.json"
    if mcp_file.is_file():
        mcp = json.loads(mcp_file.read_text(encoding="utf-8"))
        if isinstance(mcp, dict) and isinstance(mcp.get("mcpServers"), dict):
            for server in mcp["mcpServers"].values():
                if not isinstance(server, dict):
                    continue
                for field in ("command", "cwd"):
                    value = server.get(field)
                    if isinstance(value, str):
                        inferred = top_level_runtime_path(value)
                        if inferred is not None:
                            selected.add(inferred)
    return selected


def package_files(root: Path, selected_roots: Iterable[Path]) -> list[Path]:
    files: set[Path] = set()
    for relative_root in selected_roots:
        target = root / relative_root
        if not target.exists():
            raise ValueError(f"selected package path does not exist: {relative_root}")
        if not path_is_within(target, root):
            raise ValueError(f"selected package path escapes plugin root: {relative_root}")
        candidates = [target] if target.is_file() or target.is_symlink() else target.rglob("*")
        for path in candidates:
            relative = path.relative_to(root)
            if any(part in MAINTAINER_PARTS for part in relative.parts):
                continue
            if path.name in {".DS_Store"} or (path.name == "AGENTS.md" and relative == Path("AGENTS.md")) or path.suffix in MAINTAINER_SUFFIXES:
                continue
            if path.is_symlink():
                raise ValueError(f"refusing to package symlink: {relative}")
            if path.is_file():
                files.add(path)
    return sorted(files, key=lambda path: path.relative_to(root).as_posix())


def run_validation(root: Path, strict: bool = True) -> None:
    scripts_dir = Path(__file__).resolve().parent
    plugin_validator = scripts_dir / "validate_agent_plugin.py"
    skill_validator = scripts_dir.parents[1] / "new-skill" / "scripts" / "validate-skill.py"
    if not skill_validator.is_file():
        raise ValueError(f"full Skill validator not found: {skill_validator}")

    plugin_command = [sys.executable, str(plugin_validator), str(root)]
    if strict:
        plugin_command.append("--strict")
    subprocess.run(plugin_command, check=True)

    skills_dir = root / "skills"
    if not skills_dir.is_dir():
        return
    for child in sorted(skills_dir.iterdir()):
        if not child.is_dir() or not (child / "SKILL.md").is_file():
            continue
        subprocess.run(
            [
                sys.executable,
                str(skill_validator),
                str(child),
                "--clients",
                CLIENTS,
                "--strict-portable",
            ],
            check=True,
        )


def write_archive(root: Path, output: Path, plugin_name: str, files: list[Path]) -> None:
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.unlink(missing_ok=True)
    try:
        with zipfile.ZipFile(
            temporary,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for path in files:
                relative = Path(plugin_name) / path.relative_to(root)
                info = zipfile.ZipInfo(relative.as_posix())
                info.date_time = (1980, 1, 1, 0, 0, 0)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (path.stat().st_mode & 0xFFFF) << 16
                with path.open("rb") as source:
                    archive.writestr(info, source.read())
        os.replace(temporary, output)
    except Exception:
        temporary.unlink(missing_ok=True)
        raise


def verify_archive(output: Path, plugin_name: str) -> None:
    with tempfile.TemporaryDirectory(prefix="agent-plugin-package-") as temporary:
        destination = Path(temporary)
        with zipfile.ZipFile(output) as archive:
            for member in archive.infolist():
                member_path = PurePosixPath(member.filename)
                if member_path.is_absolute() or ".." in member_path.parts:
                    raise ValueError(f"unsafe archive member: {member.filename}")
                archive.extract(member, destination)
                mode = (member.external_attr >> 16) & 0xFFFF
                extracted_member = destination.joinpath(*member_path.parts)
                if mode and extracted_member.exists():
                    extracted_member.chmod(mode)
        extracted = destination / plugin_name
        run_validation(extracted)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Build and verify a deterministic Agent Plugin ZIP archive."
    )
    parser.add_argument("plugin_root", help="Path to the Agent Plugin source root")
    parser.add_argument("--output", required=True, help="Destination ZIP archive")
    parser.add_argument(
        "--include",
        action="append",
        default=[],
        help="Additional plugin-relative runtime path; repeat as needed",
    )
    parser.add_argument(
        "--expected-version",
        help="Require plugin.json.version to match this release version",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.plugin_root).expanduser().resolve()
    output = Path(args.output).expanduser().resolve()
    if not root.is_dir():
        return fail(f"plugin root is not a directory: {root}")

    try:
        manifest = load_manifest(root)
        plugin_name = manifest.get("name")
        if not isinstance(plugin_name, str) or not plugin_name:
            raise ValueError("plugin.json.name must be a non-empty string")
        if args.expected_version is not None and manifest.get("version") != args.expected_version:
            raise ValueError(
                "plugin.json.version does not match --expected-version: "
                f"{manifest.get('version')!r} != {args.expected_version!r}"
            )

        run_validation(root)
        selected = inferred_roots(root, manifest)
        selected.update(safe_relative(value) for value in args.include)
        files = package_files(root, selected)
        output.parent.mkdir(parents=True, exist_ok=True)
        write_archive(root, output, plugin_name, files)
        verify_archive(output, plugin_name)
    except (OSError, ValueError, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        output.unlink(missing_ok=True)
        return fail(str(exc))
    except subprocess.CalledProcessError as exc:
        output.unlink(missing_ok=True)
        return fail(f"validation command failed with exit code {exc.returncode}")

    print(f"Created {output} with {len(files)} files; extracted copy validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
