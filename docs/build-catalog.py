#!/usr/bin/env python3
"""
Build script for the People.ai LLM Skills Catalog.
Reads skill folders and generates skills.json for the catalog UI.

Usage: python3 build-catalog.py
"""

import json
import os
import re
from pathlib import Path

SKILLS_ROOT = Path(__file__).parent.parent
OUTPUT_FILE = Path(__file__).parent / "skills.json"

# Category mapping based on folder number ranges
CATEGORY_MAP = {
    range(1, 5): "account-research",
    range(5, 8): "opportunity-management",
    range(8, 10): "analytics",
    range(10, 11): "outreach",
    range(11, 12): "automation",
}

CATEGORIES = [
    {"id": "account-research", "name": "Account Research & Planning", "icon": "search"},
    {"id": "opportunity-management", "name": "Opportunity & Deal Management", "icon": "trending-up"},
    {"id": "analytics", "name": "Analytics & Performance", "icon": "bar-chart"},
    {"id": "outreach", "name": "Outreach & Communication", "icon": "mail"},
    {"id": "automation", "name": "Automation", "icon": "zap"},
]

PLATFORMS = [
    {"id": "claude-project", "name": "Claude.ai Project", "status": "supported", "file": "claude-project.md"},
    {"id": "claude-code", "name": "Claude Code", "status": "supported", "file": "skill.md"},
    {"id": "chatgpt-gpt", "name": "ChatGPT Custom GPT", "status": "supported", "file": "chatgpt-gpt.md"},
    {"id": "gemini", "name": "Google Gemini", "status": "coming-soon", "file": "gemini.md"},
]


def get_category(number: int) -> str:
    for num_range, category_id in CATEGORY_MAP.items():
        if number in num_range:
            return category_id
    return "other"


def extract_walkthrough(skill_dir: Path) -> dict | None:
    """Extract walkthrough structure from skill.md."""
    skill_md = skill_dir / "skill.md"
    if not skill_md.exists():
        return None

    text = skill_md.read_text()

    # Trim text to just the workflow section (stop at ## MCP Tools Reference, ## Rules, ## Output Guidelines, etc.)
    workflow_end = re.search(r"\n## (?:MCP Tools|Rules|Output Guidelines|Report Format|Important)", text)
    workflow_text = text[:workflow_end.start()] if workflow_end else text

    # Extract input type from SOURCE.md
    source_meta = parse_source_md(skill_dir / "SOURCE.md")
    input_label = source_meta.get("input", "Account name")

    # Map input labels to example values
    input_examples = {
        "account name": "Acme Corp",
        "opportunity name": "Acme Enterprise Renewal",
        "account name and opportunity": "Acme Corp",
        "account name, then opportunity selection": "Acme Corp",
    }
    example_input = input_examples.get(input_label.lower(), "Acme Corp")

    # Extract workflow steps from ### Step N headings
    step_pattern = r"### Step (\d+):?\s*(.+?)(?=\n)"
    step_matches = re.finditer(step_pattern, workflow_text)

    steps = []
    seen_tools = set()
    for match in step_matches:
        step_num = int(match.group(1))
        step_title = match.group(2).strip()

        # Get the content between this step heading and the next ### heading
        start = match.end()
        next_heading = re.search(r"\n### ", workflow_text[start:])
        end = start + next_heading.start() if next_heading else len(workflow_text)
        step_content = workflow_text[start:end]

        # Check if this step mentions parallel execution
        parallel = bool(re.search(r"parallel|simultaneous", step_content, re.IGNORECASE))

        # Extract backticked tool names (People.ai MCP tool pattern)
        tool_names = re.findall(r"`((?:find_|get_|ask_|account_|top_)\w+)`", step_content)
        # Deduplicate within this step (same tool mentioned multiple times)
        unique_tools = list(dict.fromkeys(tool_names))

        if unique_tools:
            for tool_name in unique_tools:
                # Skip if we already saw this tool in a previous step
                if tool_name in seen_tools:
                    continue
                seen_tools.add(tool_name)
                desc_match = re.search(
                    rf"`{re.escape(tool_name)}`\s*[—\-]+\s*(.+?)(?:\n|$)",
                    step_content,
                )
                desc = desc_match.group(1).strip() if desc_match else step_title
                steps.append({
                    "type": "tool",
                    "name": tool_name,
                    "description": desc,
                    "parallel": parallel,
                    "stepNum": step_num,
                })
        else:
            steps.append({
                "type": "analysis",
                "title": step_title,
                "stepNum": step_num,
            })

    # Extract output section headings from the output template area
    # Look for ### / #### / ##### headings after the last Step heading
    last_step = list(re.finditer(r"### Step \d+", workflow_text))
    output_area = text[last_step[-1].end():] if last_step else ""
    output_pattern = r"(?:###|####|#####)\s+(.+?)(?:\n)"
    output_sections = re.findall(output_pattern, output_area)
    output_sections = [
        s.strip() for s in output_sections
        if not re.match(r"step\s+\d+", s, re.IGNORECASE)
        and s.strip().lower() not in ("header", "rules", "important rules")
    ]

    has_custom_data = (skill_dir / "assets" / "walkthrough-data.json").exists()

    if not steps:
        return None

    return {
        "input": {"label": input_label, "example": example_input},
        "steps": steps,
        "outputSections": output_sections,
        "hasCustomData": has_custom_data,
    }


def parse_source_md(path: Path) -> dict:
    """Parse SOURCE.md to extract metadata."""
    if not path.exists():
        return {}

    text = path.read_text()
    metadata = {}

    # Extract name from first heading (single line only)
    name_match = re.search(r"^#\s+([^\n]+)", text, re.MULTILINE)
    if name_match:
        metadata["name"] = name_match.group(1).strip()

    # Extract section content between ## headers
    section_patterns = {
        "description": r"## Description\s*\n(.+?)(?=\n##|\Z)",
        "audience": r"## Audience\s*\n(.+?)(?=\n##|\Z)",
        "input": r"## Input\s*\n(.+?)(?=\n##|\Z)",
        "mcp_tools": r"## MCP Tools Used\s*\n(.+?)(?=\n##|\Z)",
    }

    for key, pattern in section_patterns.items():
        match = re.search(pattern, text, re.MULTILINE | re.DOTALL)
        if match:
            # Strip HTML comments and clean up
            value = re.sub(r"<!--.*?-->", "", match.group(1), flags=re.DOTALL).strip()
            if not value:
                continue
            if key == "audience":
                metadata[key] = [a.strip() for a in value.split(",")]
            elif key == "mcp_tools":
                tools = re.findall(r"^-\s*(.+)", value, re.MULTILINE)
                metadata[key] = [t.strip() for t in tools if t.strip()]
            else:
                metadata[key] = value

    return metadata


def extract_instructions(path: Path) -> str | None:
    """Extract the instructions section from a platform file (after the --- delimiter)."""
    if not path.exists():
        return None

    text = path.read_text()

    # Find content after the first --- delimiter
    parts = text.split("\n---\n", 1)
    if len(parts) == 2:
        return parts[1].strip()

    # If no delimiter, return everything after the first heading block
    return text.strip()


def get_setup_steps(platform_id: str, skill_name: str) -> list[str]:
    """Return default setup steps per platform."""
    if platform_id == "claude-project":
        return [
            "Open Claude.ai and create a new Project",
            f"Name it '{skill_name}'",
            "Paste the custom instructions (use the Copy button)",
            "Upload any knowledge files from the assets/ folder",
            "Ensure the People.ai MCP integration is connected (Settings > Integrations)",
            "Open a conversation and type an account name",
        ]
    elif platform_id == "claude-code":
        return [
            "Copy the skill instructions to your CLAUDE.md or skill file",
            "Ensure People.ai MCP is configured in your Claude Code settings",
            "Run Claude Code and invoke the skill",
        ]
    elif platform_id == "chatgpt-gpt":
        return [
            "Go to ChatGPT and click 'Explore GPTs' > 'Create'",
            f"Name your GPT '{skill_name}'",
            "Paste the instructions (use the Copy button)",
            "Configure Actions for each People.ai MCP tool listed",
            "Save and test with an account name",
        ]
    return []


def list_assets(skill_dir: Path) -> list[str]:
    """List files in the assets/ folder."""
    assets_dir = skill_dir / "assets"
    if not assets_dir.exists():
        return []
    return [f.name for f in assets_dir.iterdir() if f.is_file()]


def build_catalog():
    """Main build function."""
    skills = []

    # Find all numbered skill directories
    skill_dirs = sorted(
        [d for d in SKILLS_ROOT.iterdir() if d.is_dir() and re.match(r"\d{2}-", d.name)],
        key=lambda d: d.name,
    )

    for skill_dir in skill_dirs:
        number = int(skill_dir.name.split("-")[0])
        skill_id = skill_dir.name

        # Parse metadata from SOURCE.md
        meta = parse_source_md(skill_dir / "SOURCE.md")

        # Build platform entries
        platforms = {}
        has_any_platform = False

        for platform in PLATFORMS:
            file_path = skill_dir / platform["file"]
            instructions = extract_instructions(file_path)

            if instructions and platform["status"] == "supported":
                has_any_platform = True
                platforms[platform["id"]] = {
                    "instructions": instructions,
                    "setupSteps": get_setup_steps(
                        platform["id"], meta.get("name", skill_id)
                    ),
                }
            else:
                platforms[platform["id"]] = None

        walkthrough = extract_walkthrough(skill_dir)

        # Determine skill status
        if has_any_platform:
            status = "ready"
        else:
            status = "draft"

        skill = {
            "id": skill_id,
            "number": f"{number:02d}",
            "name": meta.get("name", skill_id.replace("-", " ").title()),
            "category": get_category(number),
            "description": meta.get("description", ""),
            "audience": meta.get("audience", []),
            "input": meta.get("input", ""),
            "mcpTools": meta.get("mcp_tools", []),
            "mcpConnectors": ["People.ai MCP"],
            "projectKnowledgeFiles": list_assets(skill_dir),
            "status": status,
            "platforms": platforms,
            "walkthrough": walkthrough,
        }
        skills.append(skill)

    catalog = {
        "catalog": {
            "title": "People.ai LLM Skills Catalog",
            "version": "1.0",
            "lastUpdated": "2026-03-04",
            "mcpSetupUrl": "https://help.people.ai/en/?q=mcp",
            "platforms": [
                {k: v for k, v in p.items() if k != "file"} for p in PLATFORMS
            ],
        },
        "categories": CATEGORIES,
        "skills": skills,
    }

    OUTPUT_FILE.write_text(json.dumps(catalog, indent=2))
    print(f"Generated {OUTPUT_FILE} with {len(skills)} skills")
    for s in skills:
        platform_count = sum(1 for v in s["platforms"].values() if v is not None)
        print(f"  {s['number']} {s['name']}: {s['status']} ({platform_count} platforms)")


if __name__ == "__main__":
    build_catalog()
