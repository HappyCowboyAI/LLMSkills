#!/usr/bin/env python3
"""
Repo validator for the People.ai LLM Skills library.

Checks:
- Each numbered skill dir has required platform files.
- SOURCE.md contains key metadata (name/description/audience/input).
- MCP tool list in SOURCE.md is non-empty and is a subset of tools referenced in skill.md.
- assets listed in SOURCE.md exist in assets/ (if present).

Usage:
  python3 docs/validate-skills.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent
SKILL_DIR_RE = re.compile(r"^\d{2}-")

REQUIRED_FILES = [
    "SOURCE.md",
    "skill.md",
    "claude-project.md",
    "chatgpt-gpt.md",
    "copilot.md",
    "gemini.md",
]

TOOL_NAME_RE = re.compile(r"`([a-zA-Z_][\w]*)`")


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def section(text: str, header: str) -> str | None:
    m = re.search(rf"^##\s+{re.escape(header)}\s*\n(.+?)(?=^\s*##\s+|\Z)", text, re.M | re.S)
    if not m:
        return None
    value = re.sub(r"<!--.*?-->", "", m.group(1), flags=re.S).strip()
    return value or None


def parse_bullets(text: str) -> list[str]:
    items = [m.group(1).strip() for m in re.finditer(r"^\s*-\s+(.+?)\s*$", text, re.M)]
    normalized = []
    for it in items:
        if not it:
            continue
        # Common placeholders in templates
        if it.strip().lower() in {"none", "n/a", "na", "tbd"}:
            continue
        normalized.append(it)
    return normalized


def referenced_tools(skill_md: str) -> set[str]:
    # Conservative: collect all backticked identifiers and filter to People.ai-ish verbs.
    candidates = {m.group(1) for m in TOOL_NAME_RE.finditer(skill_md)}
    return {c for c in candidates if re.match(r"^(find_|get_|ask_|account_|top_)\w+$", c)}


def validate_skill_dir(d: Path) -> list[str]:
    errors: list[str] = []

    # Required files
    for f in REQUIRED_FILES:
        if not (d / f).exists():
            errors.append(f"missing required file `{f}`")

    source_path = d / "SOURCE.md"
    skill_path = d / "skill.md"

    if not source_path.exists() or not skill_path.exists():
        return errors

    source = read_text(source_path)
    skill = read_text(skill_path)

    # Required SOURCE sections
    for hdr in ("Description", "Audience", "Input"):
        if section(source, hdr) is None:
            errors.append(f"`SOURCE.md` missing or empty section `## {hdr}`")

    # SOURCE MCP tools list
    mcp_tools_raw = section(source, "MCP Tools Used")
    mcp_tools = parse_bullets(mcp_tools_raw) if mcp_tools_raw else []
    if not mcp_tools:
        errors.append("`SOURCE.md` has empty `## MCP Tools Used` list")

    # Compare tool list to skill.md references (best-effort)
    refs = referenced_tools(skill)
    if mcp_tools and refs:
        not_in_skill = [t for t in mcp_tools if t not in refs]
        if not_in_skill:
            errors.append(
                "`SOURCE.md` MCP tool(s) not referenced in `skill.md`: "
                + ", ".join(not_in_skill)
            )

    # Knowledge files existence (if declared)
    pkf_raw = section(source, "Project Knowledge Files")
    declared_files = parse_bullets(pkf_raw) if pkf_raw else []
    if declared_files:
        assets_dir = d / "assets"
        for item in declared_files:
            # allow "file (description)" forms
            filename = item.split("(", 1)[0].strip()
            if not filename or filename.lower() in {"none", "n/a", "na", "tbd"}:
                continue
            if filename and not (assets_dir / filename).exists():
                errors.append(f"declared knowledge file missing: `assets/{filename}`")

    return errors


def main() -> int:
    skill_dirs = sorted([p for p in ROOT.iterdir() if p.is_dir() and SKILL_DIR_RE.match(p.name)])
    all_errors: list[tuple[Path, list[str]]] = []

    for d in skill_dirs:
        errs = validate_skill_dir(d)
        if errs:
            all_errors.append((d, errs))

    if all_errors:
        print("LLMSkills validation failed.\n")
        for d, errs in all_errors:
            print(f"- {d.name}")
            for e in errs:
                print(f"  - {e}")
        print(f"\nFailed skills: {len(all_errors)}/{len(skill_dirs)}")
        return 1

    print(f"LLMSkills validation passed ({len(skill_dirs)} skills).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

