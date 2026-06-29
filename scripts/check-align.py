#!/usr/bin/env python3
"""Check structural alignment between EN (.md) and CN (.zh.md) reference files.

For each `.md` file in the references directory that has a `.zh.md` sibling,
verifies that the two files have matching structure:
  - same count of section headers (## / ###)
  - same count of code fences (```)
  - same count of <correct_patterns> / <common_mistakes> tag pairs
  - same count of checklist items (- [ ])
  - same count of table rows (lines starting with |)

Text content is NOT compared — only structural counts, since the two files are
translations of each other. A mismatch means one side was edited and the other
was not updated (drift).

Usage:
    python check-align.py [references_dir]

Exit code 0 if all pairs align, 1 if any mismatch.
"""

import re
import sys
from pathlib import Path


def count_patterns(text: str) -> dict:
    """Return structural counts for a markdown file's text."""
    lines = text.splitlines()
    return {
        "sections": sum(1 for l in lines if re.match(r"^#{2,}\s", l)),
        "code_fences": sum(1 for l in lines if l.strip().startswith("```")),
        "correct_patterns_open": text.count("<correct_patterns>"),
        "correct_patterns_close": text.count("</correct_patterns>"),
        "common_mistakes_open": text.count("<common_mistakes>"),
        "common_mistakes_close": text.count("</common_mistakes>"),
        "checklist": sum(1 for l in lines if re.match(r"^\s*-\s*\[", l)),
        "table_rows": sum(1 for l in lines if l.strip().startswith("|")),
    }


def find_pairs(references_dir: Path) -> list:
    """Find (.md, .zh.md) pairs. Returns list of (en_path, zh_path, name)."""
    pairs = []
    for en_path in sorted(references_dir.glob("*.md")):
        if en_path.suffixes == [".zh", ".md"]:
            continue  # this IS a zh file, skip
        zh_path = en_path.with_suffix("").with_suffix(".zh.md")
        if zh_path.exists():
            pairs.append((en_path, zh_path, en_path.stem))
    return pairs


def check_pair(en_path: Path, zh_path: Path, name: str) -> tuple:
    """Check one pair. Returns (ok: bool, report: list[str])."""
    en = count_patterns(en_path.read_text(encoding="utf-8"))
    zh = count_patterns(zh_path.read_text(encoding="utf-8"))

    report = [f"{en_path.name} ↔ {zh_path.name}"]
    ok = True

    for key in en:
        if en[key] != zh[key]:
            ok = False
            report.append(f"  ✗ {key}: EN={en[key]} ≠ CN={zh[key]}")
        else:
            report.append(f"  ✓ {key}: {en[key]}")

    report.append(f"  {'OK' if ok else 'MISMATCH'}")
    return ok, report


def main():
    if len(sys.argv) > 1:
        references_dir = Path(sys.argv[1])
    else:
        references_dir = Path(__file__).parent.parent / "references"

    if not references_dir.is_dir():
        print(f"error: references dir not found: {references_dir}", file=sys.stderr)
        return 2

    pairs = find_pairs(references_dir)
    if not pairs:
        print(f"no .md/.zh.md pairs found in {references_dir}", file=sys.stderr)
        return 2

    print(f"Checking bilingual alignment for {references_dir}\n")

    all_ok = True
    aligned = 0
    for en_path, zh_path, name in pairs:
        ok, report = check_pair(en_path, zh_path, name)
        print("\n".join(report))
        print()
        if ok:
            aligned += 1
        else:
            all_ok = False

    print(f"Summary: {aligned}/{len(pairs)} pairs aligned")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
