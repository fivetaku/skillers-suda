#!/usr/bin/env python3
"""Verify generated agent file quality against skillers-suda standards."""
import sys
import os
import re
import json


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: verify_agent.py <path-to-agent.md>"}))
        sys.exit(1)

    agent_path = sys.argv[1]
    if not os.path.exists(agent_path):
        print(json.dumps({"error": f"File not found: {agent_path}"}))
        sys.exit(1)

    with open(agent_path, "r") as f:
        content = f.read()

    results = {
        "path": agent_path,
        "checks": [],
        "pass_count": 0,
        "warn_count": 0,
        "fail_count": 0,
    }

    # 1. Frontmatter exists
    fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        add_check(results, "frontmatter_exists", "PASS", "YAML frontmatter found")

        # 2. name field
        name_match = re.search(r"^name:\s*(.+)", fm, re.MULTILINE)
        if name_match and name_match.group(1).strip():
            name_value = name_match.group(1).strip()
            add_check(results, "name_field", "PASS", f"name field exists: {name_value}")
        elif name_match:
            name_value = None
            add_check(results, "name_field", "FAIL", "name field exists but is empty")
        else:
            name_value = None
            add_check(results, "name_field", "FAIL", "name field missing in frontmatter")

        # 3. description field (20+ chars)
        desc_match = re.search(r"^description:\s*(.+)", fm, re.MULTILINE)
        if desc_match:
            desc = desc_match.group(1).strip()
            if len(desc) >= 20:
                add_check(results, "description_field", "PASS", f"description field exists ({len(desc)} chars)")
            else:
                add_check(results, "description_field", "FAIL", f"description too short: {len(desc)} chars (minimum 20)")
        else:
            add_check(results, "description_field", "FAIL", "description field missing in frontmatter")

        # 4. model field (valid values)
        valid_models = {"inherit", "haiku", "sonnet", "opus"}
        model_match = re.search(r"^model:\s*(.+)", fm, re.MULTILINE)
        if model_match:
            model_value = model_match.group(1).strip()
            if model_value in valid_models:
                add_check(results, "model_field", "PASS", f"model field valid: {model_value}")
            else:
                add_check(results, "model_field", "FAIL", f"model field invalid: '{model_value}' (must be one of: {', '.join(sorted(valid_models))})")
        else:
            add_check(results, "model_field", "FAIL", "model field missing in frontmatter")

        # 5. tools field (WARN — if present must be array)
        tools_match = re.search(r"^tools:\s*(.+)", fm, re.MULTILINE)
        tools_block_match = re.search(r"^tools:\s*\n((?:[ \t]+-[^\n]+\n?)+)", fm, re.MULTILINE)
        if tools_block_match or tools_match:
            # Check for YAML list form: either block (- item) or inline ([...])
            if tools_block_match:
                add_check(results, "tools_field", "PASS", "tools field exists as array (block style)")
            else:
                inline_val = tools_match.group(1).strip()
                if inline_val.startswith("["):
                    add_check(results, "tools_field", "PASS", "tools field exists as array (inline style)")
                else:
                    add_check(results, "tools_field", "WARN", f"tools field exists but may not be array: '{inline_val}'")
        # tools is optional — no check if absent

    else:
        add_check(results, "frontmatter_exists", "FAIL", "No YAML frontmatter found")
        name_value = None
        # Skip all frontmatter-dependent checks, add FAILs
        add_check(results, "name_field", "FAIL", "Cannot check: no frontmatter")
        add_check(results, "description_field", "FAIL", "Cannot check: no frontmatter")
        add_check(results, "model_field", "FAIL", "Cannot check: no frontmatter")

    # Strip frontmatter for body checks
    body = re.sub(r"^---\n.*?\n---\n?", "", content, count=1, flags=re.DOTALL)

    # 6. role_section (FAIL) — "## 역할" or "## Role"
    if re.search(r"^##\s+(역할|Role)\s*$", body, re.MULTILINE):
        add_check(results, "role_section", "PASS", "Role section found")
    else:
        add_check(results, "role_section", "FAIL", "No '## 역할' or '## Role' section found in body")

    # 7. rnr_section (WARN) — "## R&R" or "### 해야 할 것"
    if re.search(r"^##\s+R&R\s*$", body, re.MULTILINE) or re.search(r"^###\s+해야 할 것\s*$", body, re.MULTILINE):
        add_check(results, "rnr_section", "PASS", "R&R section found")
    else:
        add_check(results, "rnr_section", "WARN", "No '## R&R' or '### 해야 할 것' section found")

    # 8. word_count (WARN) — body 500-1500 words
    words = len(body.split())
    if 500 <= words <= 1500:
        add_check(results, "word_count", "PASS", f"{words} words (target: 500-1,500)")
    elif words < 500:
        add_check(results, "word_count", "WARN", f"{words} words — too short (target: 500-1,500)")
    else:
        add_check(results, "word_count", "WARN", f"{words} words — too long (target: 500-1,500)")

    # 9. filename_match (WARN) — filename (no ext) matches name field
    filename_no_ext = os.path.splitext(os.path.basename(agent_path))[0]
    if name_value:
        if filename_no_ext == name_value:
            add_check(results, "filename_match", "PASS", f"Filename matches name field: '{filename_no_ext}'")
        else:
            add_check(results, "filename_match", "WARN", f"Filename '{filename_no_ext}' does not match name field '{name_value}'")
    else:
        add_check(results, "filename_match", "WARN", "Cannot check filename match: name field missing or empty")

    # Summary
    summary = "PASS" if results["fail_count"] == 0 else "FAIL"
    results["summary"] = summary
    results["message"] = (
        f"{results['pass_count']} passed, "
        f"{results['fail_count']} failed, "
        f"{results['warn_count']} warnings"
    )

    print(json.dumps(results, indent=2, ensure_ascii=False))
    sys.exit(0 if summary == "PASS" else 1)


def add_check(results, name, status, message):
    results["checks"].append({"name": name, "status": status, "message": message})
    if status == "PASS":
        results["pass_count"] += 1
    elif status == "FAIL":
        results["fail_count"] += 1
    else:
        results["warn_count"] += 1


if __name__ == "__main__":
    main()
