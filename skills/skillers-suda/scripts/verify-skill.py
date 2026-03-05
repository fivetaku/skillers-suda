#!/usr/bin/env python3
"""Verify generated skill quality against skillers-suda standards."""
import sys
import os
import re
import json


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: verify-skill.py <path-to-SKILL.md>"}))
        sys.exit(1)

    skill_path = sys.argv[1]
    if not os.path.exists(skill_path):
        print(json.dumps({"error": f"File not found: {skill_path}"}))
        sys.exit(1)

    with open(skill_path, "r") as f:
        content = f.read()

    results = {
        "path": skill_path,
        "checks": [],
        "pass_count": 0,
        "fail_count": 0,
        "warn_count": 0,
    }

    # 1. Frontmatter
    fm_match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        fm = fm_match.group(1)
        add_check(results, "frontmatter_exists", "PASS", "YAML frontmatter found")

        if re.search(r"^name:", fm, re.MULTILINE):
            add_check(results, "name_field", "PASS", "name field exists")
        else:
            add_check(results, "name_field", "FAIL", "name field missing in frontmatter")

        desc_match = re.search(r"^description:\s*(.+)", fm, re.MULTILINE)
        if desc_match:
            desc = desc_match.group(1).strip()
            add_check(results, "description_field", "PASS", "description field exists")

            if "This skill should be used when" in desc:
                add_check(results, "third_person", "PASS", "Uses third-person format")
            else:
                add_check(
                    results,
                    "third_person",
                    "FAIL",
                    'Description should use "This skill should be used when..."',
                )

            triggers = re.findall(r'"([^"]+)"', desc)
            if len(triggers) >= 3:
                add_check(
                    results,
                    "trigger_phrases",
                    "PASS",
                    f"{len(triggers)} trigger phrases found",
                )
            elif len(triggers) >= 1:
                add_check(
                    results,
                    "trigger_phrases",
                    "WARN",
                    f"Only {len(triggers)} trigger phrases (recommend 3-5)",
                )
            else:
                add_check(
                    results,
                    "trigger_phrases",
                    "FAIL",
                    "No trigger phrases in quotes found",
                )
        else:
            add_check(
                results, "description_field", "FAIL", "description field missing"
            )
    else:
        add_check(results, "frontmatter_exists", "FAIL", "No YAML frontmatter found")

    # 2. Word count
    body = re.sub(r"^---\n.*?\n---\n?", "", content, count=1, flags=re.DOTALL)
    words = len(body.split())

    if 1500 <= words <= 2000:
        add_check(
            results, "word_count", "PASS", f"{words} words (target: 1,500-2,000)"
        )
    elif words <= 3000:
        add_check(
            results,
            "word_count",
            "WARN",
            f"{words} words (target: 1,500-2,000, max: 3,000)",
        )
    else:
        add_check(
            results,
            "word_count",
            "FAIL",
            f"{words} words exceeds 3,000 word maximum",
        )

    # 3. Imperative form (no second person)
    second_person = re.findall(
        r"\b(You should|You need to|You can|You must|You will|You have to)\b",
        body,
        re.IGNORECASE,
    )
    # Exclude code blocks and quotes
    code_blocks = re.findall(r"```.*?```", body, re.DOTALL)
    inline_quotes = re.findall(r'"[^"]*"', body)
    exclusions = " ".join(code_blocks + inline_quotes)
    real_violations = [
        sp
        for sp in second_person
        if sp not in exclusions
    ]

    if not real_violations:
        add_check(
            results, "imperative_form", "PASS", "No second-person phrases detected"
        )
    else:
        unique = list(set(real_violations))
        add_check(
            results,
            "imperative_form",
            "FAIL",
            f"Second-person detected: {', '.join(unique[:5])}",
        )

    # 4. Referenced files exist
    # Only match backtick-quoted paths like `references/file.md` or `scripts/file.py`
    skill_dir = os.path.dirname(os.path.abspath(skill_path))
    ref_mentions = re.findall(
        r"`(?:references|scripts|assets)/([A-Za-z0-9_\-/.]+)`", body
    )
    missing = []
    checked = set()
    dir_names = {"references", "scripts", "assets"}
    for ref_file in ref_mentions:
        ref_clean = ref_file.rstrip("`*])")
        # Skip template placeholders and bare directory names
        if "{" in ref_clean or ref_clean in dir_names:
            continue
        # Reconstruct full relative path from the backtick match
        # Re-match to get the directory prefix
        full_ref = None
        for d in dir_names:
            candidate = f"{d}/{ref_clean}"
            if f"`{candidate}`" in body:
                full_ref = candidate
                break
        if not full_ref:
            continue
        if full_ref in checked:
            continue
        checked.add(full_ref)
        ref_path = os.path.join(skill_dir, full_ref)
        if not os.path.exists(ref_path):
            missing.append(full_ref)

    if not ref_mentions:
        add_check(
            results,
            "references_listed",
            "WARN",
            "No references/scripts/assets mentioned in body",
        )
    elif not missing:
        add_check(
            results,
            "references_exist",
            "PASS",
            f"All {len(checked)} referenced paths verified",
        )
    else:
        add_check(
            results,
            "references_exist",
            "FAIL",
            f"Missing: {', '.join(missing[:5])}",
        )

    # 5. Progressive disclosure
    has_refs_section = bool(
        re.search(r"^##\s*(References|참조|Additional Resources)", body, re.MULTILINE)
    )
    if has_refs_section:
        add_check(
            results, "progressive_disclosure", "PASS", "References section found"
        )
    else:
        add_check(
            results,
            "progressive_disclosure",
            "WARN",
            "No References section found",
        )

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
