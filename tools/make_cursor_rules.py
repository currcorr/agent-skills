#!/usr/bin/env python3
"""Generate Cursor Project Rules (.mdc stubs) from the skills in this repo.

Each skill becomes one thin "Agent Requested" rule: the rule's description
mirrors the SKILL.md description (Cursor's agent selects rules by
description, like Claude Code selects skills), and the body just points at
the real SKILL.md. Skills stay the single source of truth; re-run this after
adding or renaming skills.

Usage:
    python tools/make_cursor_rules.py [output_dir] [--skills-path PREFIX]

Defaults: output_dir = ./cursor-rules ; PREFIX = ~/skills
Then copy/symlink the output into each workspace's .cursor/rules/.
"""

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MAX_DESC = 700  # keep rule descriptions scannable for Cursor's selector


def parse_frontmatter(text):
    """Minimal YAML frontmatter reader for name/description (stdlib only)."""
    if not text.startswith("---"):
        return {}
    lines = text.split("\n")
    fields, i = {}, 1
    while i < len(lines) and lines[i].strip() != "---":
        line = lines[i]
        if ":" in line and not line.startswith(" "):
            key, _, rest = line.partition(":")
            key, rest = key.strip(), rest.strip()
            if rest in ("|", ">", "|-", ">-"):  # block scalar: gather indented lines
                block = []
                i += 1
                while i < len(lines) and (lines[i].startswith("  ") or not lines[i].strip()):
                    if lines[i].strip() == "---":
                        break
                    block.append(lines[i].strip())
                    i += 1
                fields[key] = " ".join(b for b in block if b)
                continue
            if rest[:1] in "\"'" and rest[-1:] == rest[:1] and len(rest) > 1:
                rest = rest[1:-1].replace('\\"', '"')
            fields[key] = rest
        i += 1
    return fields


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    out = Path(args[0]) if args else REPO / "cursor-rules"
    prefix = "~/skills"
    if "--skills-path" in sys.argv:
        prefix = sys.argv[sys.argv.index("--skills-path") + 1]
    out.mkdir(parents=True, exist_ok=True)

    count = 0
    for skill_md in sorted(REPO.glob("*/SKILL.md")):
        meta = parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
        name = meta.get("name", skill_md.parent.name)
        desc = " ".join(meta.get("description", "").split())
        if not desc:
            print(f"  skipped {name}: no description")
            continue
        if len(desc) > MAX_DESC:
            desc = desc[: MAX_DESC - 1].rsplit(" ", 1)[0] + "…"
        desc = desc.replace('"', "'")
        (out / f"{name}.mdc").write_text(
            f"""---
description: "{desc}"
alwaysApply: false
---

This rule maps to an Agent Skill. Before doing this task, read and follow
the full instructions in `{prefix}/{skill_md.parent.name}/SKILL.md`
(including any referenced files in that folder). That file is the source of
truth; this rule is only the trigger.
""")
        count += 1

    print(f"Wrote {count} rule stubs to {out}/")
    print(f"Install per workspace:  mkdir -p .cursor/rules && cp {out}/*.mdc .cursor/rules/")
    print("Re-run this script whenever skills are added, renamed, or re-described.")


if __name__ == "__main__":
    main()
