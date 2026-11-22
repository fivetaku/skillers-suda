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

    with open(skill_path, "r", encoding="utf-8") as f:
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

        desc = extract_description(fm)
        if desc:
            add_check(results, "description_field", "PASS", "description field exists")
            check_description(results, desc)
        else:
            add_check(
                results, "description_field", "FAIL", "description field missing"
            )
    else:
        add_check(results, "frontmatter_exists", "FAIL", "No YAML frontmatter found")

    # 2. Length — upper bounds only (progressive disclosure: shorter is better)
    body = re.sub(r"^---\n.*?\n---\n?", "", content, count=1, flags=re.DOTALL)
    words = len(body.split())
    lines = len(content.splitlines())
    size = f"{words} words, {lines} lines"

    if words > HARD_MAX_WORDS or lines > HARD_MAX_LINES:
        add_check(
            results,
            "word_count",
            "FAIL",
            f"{size} — far above the limit (hard max {HARD_MAX_WORDS:,} words / "
            f"{HARD_MAX_LINES} lines). Move detail into references/",
        )
    elif words > MAX_WORDS or lines > MAX_LINES:
        add_check(
            results,
            "word_count",
            "WARN",
            f"{size} — above {MAX_LINES} lines / {MAX_WORDS:,} words. "
            "Shorter is better; move detail into references/",
        )
    else:
        add_check(
            results,
            "word_count",
            "PASS",
            f"{size} (limit: {MAX_LINES} lines / {MAX_WORDS:,} words; shorter is better)",
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


# Body size limits. No lower bound: a short skill that does its job is the goal.
MAX_LINES = 500
MAX_WORDS = 5000
HARD_MAX_LINES = 1000
HARD_MAX_WORDS = 10000

# Claude Code truncates/rejects descriptions above this length.
MAX_DESCRIPTION_CHARS = 1024

# "When to use" markers (English third-person forms and Korean equivalents).
WHEN_PATTERNS = [
    r"\bused? when\b",
    r"\buse (this|it)\b",
    r"\bwhen the user\b",
    r"\bwhenever\b",
    r"\bfor requests?\b",
    r"\btrigger",
    r"때",
    r"경우",
    r"요청",
    r"트리거",
]

# Boilerplate that says "when" but nothing about "what".
BOILERPLATE = re.compile(
    r"this skill should be used when the user asks (to|about|for)?", re.IGNORECASE
)


def extract_description(fm):
    """Return the description value, supporting single-line and block scalars."""
    lines = fm.split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^description:\s*(.*)$", line)
        if not m:
            continue
        value = m.group(1).strip()
        if value in ("", ">", "|", ">-", "|-", ">+", "|+"):
            parts = []
            for nxt in lines[i + 1 :]:
                if nxt.strip() == "" or nxt.startswith((" ", "\t")):
                    parts.append(nxt.strip())
                else:
                    break
            value = " ".join(p for p in parts if p)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        return value.strip()
    return ""


def check_description(results, desc):
    """Check the two elements a description needs: what it does + when to use it.

    Quoted trigger phrases are optional; the measured run_loop optimization
    result takes precedence over any wording rule here.
    """
    if len(desc) > MAX_DESCRIPTION_CHARS:
        add_check(
            results,
            "description_length",
            "FAIL",
            f"{len(desc)} chars exceeds {MAX_DESCRIPTION_CHARS}",
        )
    else:
        add_check(
            results,
            "description_length",
            "PASS",
            f"{len(desc)} chars (max {MAX_DESCRIPTION_CHARS})",
        )

    has_when = any(re.search(p, desc, re.IGNORECASE) for p in WHEN_PATTERNS)

    # "What": prose left after removing quoted triggers and the when-boilerplate.
    prose = re.sub(r'"[^"]*"|“[^”]*”', " ", desc)
    prose = BOILERPLATE.sub(" ", prose)
    prose_words = [w for w in re.split(r"[\s,.;:()—\-]+", prose) if w]
    has_what = len(prose_words) >= 4

    if has_what and has_when:
        add_check(
            results,
            "description_what_when",
            "PASS",
            "Description states what the skill does and when to use it",
        )
    else:
        missing = []
        if not has_what:
            missing.append("what it does (a sentence beyond the trigger list)")
        if not has_when:
            missing.append("when to use it (e.g. 'Use when ...')")
        add_check(
            results,
            "description_what_when",
            "WARN",
            "Description should state " + " and ".join(missing),
        )

    triggers = re.findall(r'"([^"]+)"', desc)
    add_check(
        results,
        "trigger_phrases",
        "PASS",
        f"{len(triggers)} quoted trigger phrases (optional; "
        "run_loop optimization result wins)",
    )


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
