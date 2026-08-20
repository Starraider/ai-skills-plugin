#!/usr/bin/env python3
"""Validate and package one Agent Skill as a deterministic .skill archive."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Iterable


EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    "evals",
    "node_modules",
}
EXCLUDED_NAMES = {
    ".DS_Store",
    "AGENTS.md",
}
EXCLUDED_SUFFIXES = {
    ".pyc",
}


def package_files(skill_dir: Path) -> Iterable[Path]:
    for path in sorted(skill_dir.rglob("*")):
        relative = path.relative_to(skill_dir)
        if any(part in EXCLUDED_PARTS for part in relative.parts):
            continue
        if path.name in {".DS_Store"} or (path.name == "AGENTS.md" and relative == Path("AGENTS.md")) or path.suffix in EXCLUDED_SUFFIXES:
            continue
        if path.is_symlink():
            raise ValueError(f"refusing to package symlink: {relative}")
        if path.is_file():
            yield path


def validate(skill_dir: Path, clients: str, strict_portable: bool) -> None:
    validator = Path(__file__).with_name("validate-skill.py")
    command = [
        sys.executable,
        str(validator),
        str(skill_dir),
        "--clients",
        clients,
    ]
    if strict_portable:
        command.append("--strict-portable")
    subprocess.run(command, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and package a skill directory as a .skill ZIP archive."
    )
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument(
        "--output",
        help="Archive path; defaults to <skill-parent>/<skill-name>.skill",
    )
    parser.add_argument(
        "--clients",
        default="claude,codex,cursor,antigravity,opencode,qoder",
        help="Comma-separated client profiles passed to validation",
    )
    parser.add_argument(
        "--strict-portable",
        action="store_true",
        help="Reject client-specific SKILL.md frontmatter fields",
    )
    args = parser.parse_args()

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.is_dir():
        print(f"ERROR: skill directory does not exist: {skill_dir}", file=sys.stderr)
        return 1

    try:
        validate(skill_dir, args.clients, args.strict_portable)
    except subprocess.CalledProcessError:
        print("ERROR: validation failed; archive was not created", file=sys.stderr)
        return 1

    output = (
        Path(args.output).expanduser().resolve()
        if args.output
        else skill_dir.parent / f"{skill_dir.name}.skill"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")

    try:
        files = list(package_files(skill_dir))
        with zipfile.ZipFile(
            temporary,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9,
        ) as archive:
            for path in files:
                relative = Path(skill_dir.name) / path.relative_to(skill_dir)
                info = zipfile.ZipInfo(relative.as_posix())
                info.date_time = (1980, 1, 1, 0, 0, 0)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = (path.stat().st_mode & 0xFFFF) << 16
                with path.open("rb") as source:
                    archive.writestr(info, source.read())
        os.replace(temporary, output)
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        temporary.unlink(missing_ok=True)
        print(f"ERROR: package failed: {exc}", file=sys.stderr)
        return 1

    print(f"Created {output} with {len(files)} files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
