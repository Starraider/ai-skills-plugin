#!/usr/bin/env bash

set -euo pipefail

usage() {
    echo "Usage: $0 [--bundled] <output-parent> <skill-name> <description>"
    echo "Example: $0 /tmp release-notes 'Use when drafting release notes from merged changes.'"
    echo "Bundled: $0 --bundled /tmp release-notes 'Use when drafting release notes from merged changes.'"
}

PROFILE="standalone"
if [[ "${1:-}" == "--bundled" ]]; then
    PROFILE="bundled"
    shift
fi

if [[ $# -ne 3 ]]; then
    usage
    exit 2
fi

OUTPUT_PARENT="$1"
SKILL_NAME="$2"
DESCRIPTION="$3"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DESTINATION="$OUTPUT_PARENT/$SKILL_NAME"

if ! [[ "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "ERROR: skill name must use lowercase letters or digits separated by single hyphens" >&2
    exit 1
fi

if [[ ${#SKILL_NAME} -gt 64 ]]; then
    echo "ERROR: skill name must be at most 64 characters" >&2
    exit 1
fi

if [[ -z "$DESCRIPTION" || ${#DESCRIPTION} -gt 1024 ]]; then
    echo "ERROR: description must contain 1-1024 characters" >&2
    exit 1
fi

if [[ -e "$DESTINATION" ]]; then
    echo "ERROR: destination already exists: $DESTINATION" >&2
    exit 1
fi

mkdir -p "$DESTINATION"

python3 - "$SKILL_ROOT/templates" "$DESTINATION" "$SKILL_NAME" "$DESCRIPTION" "$PROFILE" <<'PY'
from pathlib import Path
import sys

templates = Path(sys.argv[1])
destination = Path(sys.argv[2])
name = sys.argv[3]
description = sys.argv[4]
profile = sys.argv[5]
title = name.replace("-", " ").title()

replacements = {
    "{{SKILL_NAME}}": name,
    "{{SKILL_TITLE}}": title,
    "{{DESCRIPTION}}": description,
}

outputs = [("SKILL.md.template", "SKILL.md")]
if profile == "standalone":
    outputs.append(("README.md.template", "README.md"))

for source_name, target_name in outputs:
    text = (templates / source_name).read_text(encoding="utf-8")
    for old, new in replacements.items():
        text = text.replace(old, new)
    (destination / target_name).write_text(text, encoding="utf-8")
PY

echo "Created $DESTINATION"
echo "Next: replace TODO markers, add only needed support files, then run:"
if [[ "$PROFILE" == "bundled" ]]; then
    echo "  $SCRIPT_DIR/validate-skill.sh $DESTINATION --documentation-profile bundled"
else
    echo "  $SCRIPT_DIR/validate-skill.sh $DESTINATION"
fi
