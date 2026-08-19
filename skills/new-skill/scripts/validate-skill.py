#!/usr/bin/env python3
"""Validate a portable Agent Skill and selected client extensions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple


CLIENTS = {
    "claude",
    "codex",
    "cursor",
    "antigravity",
    "opencode",
    "qoder",
}

PORTABLE_FIELDS = {
    "name",
    "description",
    "license",
    "compatibility",
    "metadata",
    "allowed-tools",
}

CLAUDE_FIELDS = {
    "when_to_use",
    "argument-hint",
    "arguments",
    "disable-model-invocation",
    "user-invocable",
    "disallowed-tools",
    "model",
    "effort",
    "context",
    "agent",
    "hooks",
    "paths",
    "shell",
}

CURSOR_FIELDS = {
    "disable-model-invocation",
    "paths",
    "globs",
}

CLIENT_EXTENSION_FIELDS = {
    "claude": CLAUDE_FIELDS,
    "codex": set(),
    "cursor": CURSOR_FIELDS,
    "antigravity": set(),
    "opencode": set(),
    "qoder": set(),
}

README_SECTIONS = {
    "What this skill solves",
    "Use when",
    "Expected outputs",
    "Context requirements",
    "Installation",
    "Example prompts",
    "Validation",
    "Related skills",
    "License",
}

LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
TOP_LEVEL_PATTERN = re.compile(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$")


class Reporter:
    def __init__(self) -> None:
        self.errors = 0
        self.warnings = 0

    def ok(self, message: str) -> None:
        print(f"OK: {message}")

    def warn(self, message: str) -> None:
        self.warnings += 1
        print(f"WARNING: {message}")

    def error(self, message: str) -> None:
        self.errors += 1
        print(f"ERROR: {message}")


def split_frontmatter(text: str) -> Tuple[List[str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with a YAML frontmatter delimiter")
    for index in range(1, min(len(lines), 80)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1 :])
    raise ValueError("SKILL.md frontmatter has no closing delimiter")


def strip_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_frontmatter(lines: Sequence[str]) -> Tuple[Dict[str, str], List[str]]:
    fields: Dict[str, str] = {}
    duplicates: List[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip() or line.lstrip().startswith("#") or line[:1].isspace():
            index += 1
            continue
        match = TOP_LEVEL_PATTERN.match(line)
        if not match:
            index += 1
            continue
        key, raw_value = match.group(1), (match.group(2) or "")
        if key in fields:
            duplicates.append(key)
        if raw_value in {">", ">-", ">|", "|", "|-"}:
            block: List[str] = []
            index += 1
            while index < len(lines):
                candidate = lines[index]
                if candidate and not candidate[:1].isspace():
                    break
                block.append(candidate.strip())
                index += 1
            separator = "\n" if raw_value.startswith("|") else " "
            fields[key] = separator.join(part for part in block if part).strip()
            continue
        fields[key] = strip_scalar(raw_value)
        index += 1
    return fields, duplicates


def parse_clients(raw: str) -> Set[str]:
    selected = {item.strip().lower() for item in raw.split(",") if item.strip()}
    unknown = selected - CLIENTS
    if unknown:
        raise ValueError(f"unknown clients: {', '.join(sorted(unknown))}")
    return selected


def markdown_files(skill_dir: Path) -> Iterable[Path]:
    for path in skill_dir.rglob("*.md"):
        if "templates" not in path.relative_to(skill_dir).parts:
            yield path


def check_links(skill_dir: Path, reporter: Reporter) -> None:
    checked = 0
    for source in markdown_files(skill_dir):
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if (
                not target
                or target.startswith(("#", "http://", "https://", "mailto:", "app://"))
            ):
                continue
            target = target.split("#", 1)[0]
            resolved = (source.parent / target).resolve()
            checked += 1
            if not resolved.exists():
                reporter.error(
                    f"broken relative link in {source.relative_to(skill_dir)}: {raw_target}"
                )
    reporter.ok(f"checked {checked} relative Markdown links")


def section_body(text: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\s*$([\s\S]*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE,
    )
    return match.group(1) if match else ""


def check_readme(skill_dir: Path, reporter: Reporter, documentation_profile: str) -> None:
    readme = skill_dir / "README.md"
    if not readme.is_file():
        if documentation_profile == "standalone":
            reporter.error("README.md is required for a standalone Skill")
        else:
            reporter.ok("bundled Skill uses the owning Agent Plugin README")
        return
    text = readme.read_text(encoding="utf-8")
    headings = set(re.findall(r"^## (.+?)\s*$", text, flags=re.MULTILINE))
    missing = README_SECTIONS - headings
    if missing:
        reporter.error(f"README.md missing sections: {', '.join(sorted(missing))}")
    else:
        reporter.ok("README.md contains all required sections")
    prompt_lines = [
        line
        for line in section_body(text, "Example prompts").splitlines()
        if re.match(r"^\s*(?:[-*+]|\d+\.)\s+\S", line)
    ]
    if len(prompt_lines) < 3:
        reporter.error("README.md must contain at least three example prompts")
    else:
        reporter.ok(f"README.md contains {len(prompt_lines)} example prompts")


def check_references(skill_dir: Path, skill_text: str, reporter: Reporter) -> None:
    references_dir = skill_dir / "references"
    if not references_dir.is_dir():
        return
    reference_files = sorted(references_dir.rglob("*.md"))
    for path in reference_files:
        relative = path.relative_to(skill_dir).as_posix()
        if relative not in skill_text:
            reporter.error(f"reference is not directly discoverable from SKILL.md: {relative}")
    if reference_files:
        reporter.ok(f"checked direct discovery for {len(reference_files)} references")


def check_scripts(skill_dir: Path, reporter: Reporter) -> None:
    scripts_dir = skill_dir / "scripts"
    if not scripts_dir.is_dir():
        return
    for path in scripts_dir.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix == ".sh" and not path.stat().st_mode & 0o111:
            reporter.error(f"shell script is not executable: {path.relative_to(skill_dir)}")
        if path.suffix in {".sh", ".py"}:
            first_line = path.read_text(encoding="utf-8").splitlines()[:1]
            if not first_line or not first_line[0].startswith("#!"):
                reporter.warn(f"script has no shebang: {path.relative_to(skill_dir)}")


def check_evals(skill_dir: Path, skill_name: str, reporter: Reporter) -> None:
    evals_file = skill_dir / "evals" / "evals.json"
    if not evals_file.is_file():
        return
    try:
        data = json.loads(evals_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        reporter.error(f"evals/evals.json is invalid: {exc}")
        return
    if not isinstance(data, dict):
        reporter.error(
            "evals/evals.json must use the canonical object format with skill_name and evals"
        )
        return
    if data.get("skill_name") != skill_name:
        reporter.error("evals/evals.json skill_name must match SKILL.md name")
    evals = data.get("evals")
    if not isinstance(evals, list) or not evals:
        reporter.error("evals/evals.json must contain a non-empty evals list")
        return
    required = {"id", "kind", "prompt", "expected_output", "files", "expectations"}
    valid_kinds = {"representative", "edge-case", "near-miss", "regression"}
    ids = []
    kinds: Set[str] = set()
    for index, case in enumerate(evals, start=1):
        if not isinstance(case, dict):
            reporter.error(f"eval case {index} must be an object")
            continue
        missing = required - set(case)
        if missing:
            reporter.error(
                f"eval case {index} missing fields: {', '.join(sorted(missing))}"
            )
        ids.append(case.get("id"))
        kind = case.get("kind")
        if kind not in valid_kinds:
            reporter.error(
                f"eval case {index} kind must be one of: {', '.join(sorted(valid_kinds))}"
            )
        else:
            kinds.add(kind)
        if not isinstance(case.get("files"), list):
            reporter.error(f"eval case {index} files must be an array")
        expectations = case.get("expectations")
        if (
            not isinstance(expectations, list)
            or not expectations
            or not all(isinstance(item, str) and item.strip() for item in expectations)
        ):
            reporter.error(f"eval case {index} must have objective expectations")
    if len(ids) != len(set(ids)):
        reporter.error("eval case IDs must be unique")
    missing_kinds = {"representative", "edge-case", "near-miss"} - kinds
    if missing_kinds:
        reporter.error(
            "eval suite must cover representative, edge-case, and near-miss behavior; missing: "
            + ", ".join(sorted(missing_kinds))
        )
    reporter.ok(f"checked {len(evals)} evaluation cases")


def validate(args: argparse.Namespace) -> int:
    reporter = Reporter()
    skill_dir = Path(args.skill_dir).expanduser().resolve()
    if not skill_dir.is_dir():
        reporter.error(f"skill directory does not exist: {skill_dir}")
        return 1

    try:
        selected_clients = parse_clients(args.clients)
    except ValueError as exc:
        reporter.error(str(exc))
        return 1

    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        reporter.error("SKILL.md is required")
        return 1

    skill_text = skill_file.read_text(encoding="utf-8")
    try:
        frontmatter_lines, body = split_frontmatter(skill_text)
        fields, duplicates = parse_frontmatter(frontmatter_lines)
    except ValueError as exc:
        reporter.error(str(exc))
        return 1

    if duplicates:
        reporter.error(f"duplicate frontmatter fields: {', '.join(sorted(set(duplicates)))}")

    allowed_fields = set(PORTABLE_FIELDS)
    for client in selected_clients:
        allowed_fields.update(CLIENT_EXTENSION_FIELDS[client])
    unknown_fields = set(fields) - allowed_fields
    if unknown_fields:
        reporter.error(f"unsupported frontmatter fields: {', '.join(sorted(unknown_fields))}")

    extension_fields = set(fields) - PORTABLE_FIELDS
    if args.strict_portable and extension_fields:
        reporter.error(
            "strict portable mode rejects client extensions: "
            + ", ".join(sorted(extension_fields))
        )

    name = fields.get("name", "")
    if not name:
        reporter.error("frontmatter name is required")
    elif not NAME_PATTERN.fullmatch(name) or len(name) > 64:
        reporter.error("name must match ^[a-z0-9]+(-[a-z0-9]+)*$ and be at most 64 characters")
    else:
        reporter.ok(f"valid skill name: {name}")
        if name != skill_dir.name:
            reporter.error(f"frontmatter name '{name}' does not match directory '{skill_dir.name}'")

    description = fields.get("description", "")
    if not description:
        reporter.error("frontmatter description is required")
    elif len(description) > 1024:
        reporter.error(f"description is {len(description)} characters; maximum is 1024")
    else:
        reporter.ok(f"description is {len(description)} characters")

    compatibility = fields.get("compatibility", "")
    if compatibility and len(compatibility) > 500:
        reporter.error(f"compatibility is {len(compatibility)} characters; maximum is 500")

    if "globs" in fields:
        reporter.warn("Cursor accepts legacy 'globs', but new skills should use 'paths'")
    if "allowed-tools" in fields and {"opencode", "antigravity", "qoder"} & selected_clients:
        reporter.warn("allowed-tools is not interpreted consistently by all selected clients")

    for field in sorted(extension_fields):
        unsupported = {
            client
            for client in selected_clients
            if field not in CLIENT_EXTENSION_FIELDS[client]
        }
        if unsupported:
            reporter.warn(
                f"'{field}' is ignored by selected clients: {', '.join(sorted(unsupported))}"
            )

    line_count = len(skill_text.splitlines())
    if line_count > 500:
        reporter.error(f"SKILL.md is {line_count} lines; maximum recommended size is 500")
    else:
        reporter.ok(f"SKILL.md is {line_count} lines")

    word_count = len(re.findall(r"\b[\w'-]+\b", body))
    if word_count > 1000:
        reporter.warn(f"SKILL.md body is {word_count} words; inspect for progressive disclosure")
    else:
        reporter.ok(f"SKILL.md body is {word_count} words")

    for path in [skill_file, skill_dir / "README.md"]:
        if not path.is_file():
            continue
        path_text = path.read_text(encoding="utf-8")
        if re.search(r"\{\{[^}]+\}\}", path_text):
            reporter.error(f"unresolved template placeholder in {path.name}")
        if re.search(r"\bTODO\b", path_text):
            reporter.error(f"unresolved TODO marker in {path.name}")

    check_readme(skill_dir, reporter, args.documentation_profile)
    check_references(skill_dir, skill_text, reporter)
    check_scripts(skill_dir, reporter)
    check_evals(skill_dir, name, reporter)
    check_links(skill_dir, reporter)

    print(
        f"RESULT: {reporter.errors} error(s), {reporter.warnings} warning(s), "
        f"clients={','.join(sorted(selected_clients)) or 'portable'}"
    )
    return 1 if reporter.errors else 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate a portable Agent Skill and selected client extensions."
    )
    parser.add_argument("skill_dir", help="Path to the skill directory")
    parser.add_argument(
        "--clients",
        default="claude,codex,cursor,antigravity,opencode,qoder",
        help="Comma-separated client profiles",
    )
    parser.add_argument(
        "--strict-portable",
        action="store_true",
        help="Reject client-specific SKILL.md frontmatter fields",
    )
    parser.add_argument(
        "--documentation-profile",
        choices=("standalone", "bundled"),
        default="standalone",
        help=(
            "Require a Skill-local README for standalone Skills, or allow the owning "
            "Agent Plugin README to document a bundled Skill"
        ),
    )
    return parser


if __name__ == "__main__":
    sys.exit(validate(build_parser().parse_args()))
