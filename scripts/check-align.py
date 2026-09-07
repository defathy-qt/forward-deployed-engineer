#!/usr/bin/env python3
"""Bilingual alignment checker for FDE skill v2 (merged from FDE-01 + FDE-02).

Per EN/CN reference pair `NN-name.md` / `NN-name.zh.md`:
  1. Structural counts are computed AFTER code fences are stripped, so a heading or
     table that lives inside an example template is not mistaken for a real section.
  2. Heading structure is compared as an ordered level sequence (## / ### / ####), not
     just a total.
  3. Explicit anchors (`<!--a:id-->`) must match exactly, in order.
  4. `correct_patterns` / `common_mistakes` tags must be open/close balanced in each
     file, and appear the same number of times in EN and ZH.
  5. Code-fence / table-row / checklist counts must match EN == ZH; fences balanced.
  6. Length ratio CN/EN is a soft warning outside [0.35, 2.2] (Chinese is dense).

Repo-wide scans (also reported as warnings):
  7. Internal cross-references (`NN-x.md`, `NN-x.zh.md`, `templates/...`) resolve to a
     real file or become warnings.
  8. Placeholder hygiene (`<TBD>`, `<fill-me>`, `<client_host>`, ...) is reported.

Usage:
    python scripts/check-align.py [dir] [--json] [--strict]
      dir     directory of EN/ZH module pairs (default: <repo>/references)
      --json  emit a machine-readable JSON report
      --strict  warnings fail the run (exit 1); structural errors always fail

Exit codes: 0 all structural checks pass (warnings allowed unless --strict);
            1 structural mismatch, or warnings under --strict; 2 usage error.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ANCHOR_RE = re.compile(r"<!--\s*a:([\w.\-]+)\s*-->")
HEADING_RE = re.compile(r"^(#{1,6})\s")
FENCE_RE = re.compile(r"^\s*```")
CHECKLIST_RE = re.compile(r"^\s*-\s*\[")
TABLEROW_RE = re.compile(r"^\s*\|")
TAGS = ("correct_patterns", "common_mistakes")

# Soft warning band for len(CN chars) / len(EN chars).
LEN_LOW, LEN_HIGH = 0.35, 2.2

# Unfinished tokens that must never survive into final guidance. Field-shaped
# template tokens (`<name, role>`, `<what we chose>) that illustrate a fillable
# shape are intentional and NOT flagged; `<TBD>`/`<fill-me>` are.
PLACEHOLDER_RX = re.compile(
    r"<TBD|<fill-me|<client_host|<platform_endpoint|<exact command"
)

# Inline code span: strips self-mentions such as "never write `<TBD>`".
INLINE_CODE_RX = re.compile(r"`[^`\n]+`")

# Reference to a sibling module or template path, e.g. `04-evaluation.md`,
# `skel.zh.md`, `templates/scope-contract.md`.
REF_RX = re.compile(r"\b([a-zA-Z0-9_./\-]+\.(?:zh\.)?md)\b")


def split_fence(lines):
    """Yield (line, in_fence). Inside-``` lines are structural no-ops."""
    in_fence = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            yield line, True
        else:
            yield line, in_fence


def count_patterns(text: str) -> dict:
    """Structural counters with fence stripping (FDE-02) + anchors + ratio."""
    lines = text.splitlines()
    headings = []
    code_fences = 0
    checklist = 0
    table_rows = 0
    tags = {f"{tag}_{k}": 0 for tag in TAGS for k in ("open", "close")}

    for line, in_fence in split_fence(lines):
        s = line.strip()
        if s.startswith("```"):
            code_fences += 1
            continue
        if in_fence:
            continue
        if (m := HEADING_RE.match(line)):
            headings.append(len(m.group(1)))
        if s.startswith("|"):
            table_rows += 1
        if CHECKLIST_RE.match(line):
            checklist += 1
        for tag in TAGS:
            if s == f"<{tag}>":
                tags[f"{tag}_open"] += 1
            elif s == f"</{tag}>":
                tags[f"{tag}_close"] += 1

    return {
        "headings": headings,
        "heading_levels": "".join(str(h) for h in headings),
        "anchors": ANCHOR_RE.findall(text),
        "code_fences": code_fences,
        "checklist": checklist,
        "table_rows": table_rows,
        "chars": len(text),
        **tags,
    }


def analyze(en_path: Path, zh_path: Path) -> dict:
    en = count_patterns(en_path.read_text(encoding="utf-8"))
    zh = count_patterns(zh_path.read_text(encoding="utf-8"))

    errors, warnings = [], []
    # Struct keys compared EN == ZH (fence-stripped counts + headings + tags).
    for key in ("heading_levels", "code_fences", "checklist", "table_rows"):
        if en[key] != zh[key]:
            errors.append(
                f"{key}: EN={en[key]} != CN={zh[key]}")

    for tag in TAGS:
        for kind in ("open", "close"):
            if en[f"{tag}_{kind}"] != zh[f"{tag}_{kind}"]:
                errors.append(
                    f"{tag} {kind}: EN={en[f'{tag}_{kind}']} != "
                    f"CN={zh[f'{tag}_{kind}']}")

    if en["anchors"] != zh["anchors"]:
        errors.append(f"anchor sequence mismatch: EN={en['anchors']} CN={zh['anchors']}")

    # Balance inside each file.
    for label, data in (("EN", en), ("CN", zh)):
        if data["code_fences"] % 2 != 0:
            errors.append(f"{label} has unbalanced code fences ({data['code_fences']})")
        for tag in TAGS:
            if data[f"{tag}_open"] != data[f"{tag}_close"]:
                errors.append(
                    f"{label} tag <{tag}> unbalanced: "
                    f"{data[f'{tag}_open']} open vs {data[f'{tag}_close']} close"
                )

    ratio = zh["chars"] / en["chars"] if en["chars"] else 0
    if not (LEN_LOW <= ratio <= LEN_HIGH):
        warnings.append(f"length ratio CN/EN={ratio:.2f} outside [{LEN_LOW}, {LEN_HIGH}]")

    return {
        "pair": f"{en_path.name} <-> {zh_path.name}",
        "errors": errors,
        "warnings": warnings,
        "metrics": {
            "headings": {"EN": len(en["headings"]), "CN": len(zh["headings"])},
            "anchors": {"EN": en["anchors"], "CN": zh["anchors"]},
            "code_fences": {"EN": en["code_fences"], "CN": zh["code_fences"]},
            "checklist": {"EN": en["checklist"], "CN": zh["checklist"]},
            "table_rows": {"EN": en["table_rows"], "CN": zh["table_rows"]},
            "chars": {"EN": en["chars"], "CN": zh["chars"]},
        },
        "length_ratio": round(ratio, 3),
    }


def find_pairs(references_dir: Path):
    pairs = []
    for en_path in sorted(references_dir.glob("*.md")):
        if en_path.name.endswith(".zh.md"):
            continue
        zh_path = en_path.with_name(en_path.name[:-3] + ".zh.md")
        if zh_path.exists():
            pairs.append((en_path, zh_path))
    return pairs


def scan_references(repo_root: Path, references_dir: Path):
    """Resolve internal cross-references against references/, templates/, root .md."""
    warnings = []
    existing = {p.name for p in references_dir.glob("*.md")}
    templates_dir = repo_root / "templates"
    templates_existing = {p.name for p in templates_dir.glob("*")}
    root_md = {p.name for p in repo_root.glob("*.md")}
    for path in sorted(references_dir.glob("*.md")):
        refs = set(REF_RX.findall(path.read_text(encoding="utf-8")))
        for ref in sorted(refs):
            if ref.startswith("templates/"):
                target = ref.split("/", 1)[1]
                if target not in templates_existing:
                    warnings.append(
                        f"  ? {path.name}: references '{ref}' (template not found)")
            elif ref not in existing and ref not in root_md:
                warnings.append(
                    f"  ? {path.name}: references '{ref}' (module not found)")
    return warnings


def scan_placeholders(repo_root: Path):
    """Report unfinished placeholder tokens in prose (not fences, not inline code)."""
    warnings = []
    for path in sorted(repo_root.glob("references/*.md")) + [repo_root / "SKILL.md"]:
        hits = []
        for i, (line, in_fence) in enumerate(
                split_fence(path.read_text(encoding="utf-8").splitlines()), 1):
            if in_fence:
                continue
            prose = INLINE_CODE_RX.sub("", line)
            if PLACEHOLDER_RX.search(prose):
                hits.append((i, line.strip()))
        if hits:
            warnings.append(f"  ! {path.name}: {len(hits)} placeholder token(s)")
            for i, line in hits[:3]:
                warnings.append(f"      L{i}: {line[:80]}")
    return warnings


def human_report(results, ref_warnings, ph_warnings) -> str:
    out = []
    for r in results:
        out.append(r["pair"])
        for e in r["errors"]:
            out.append(f"  X {e}")
        for w in r["warnings"]:
            out.append(f"  ! {w}")
        if not r["errors"] and not r["warnings"]:
            out.append("  OK structural alignment + length ratio")
        out.append(f"  -> {'MISMATCH' if r['errors'] else 'ALIGNED'}"
                   f" (ratio {r['length_ratio']})")
        out.append("")
    aligned = sum(1 for r in results if not r["errors"])
    out.append(f"Summary: {aligned}/{len(results)} pairs structurally aligned")
    if ref_warnings:
        out.append("Cross-reference warnings:")
        out.extend(ref_warnings)
    if ph_warnings:
        out.append("Placeholder warnings:")
        out.extend(ph_warnings)
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dir", nargs="?", help="references directory")
    parser.add_argument("--json", action="store_true", help="emit JSON report")
    parser.add_argument("--strict", action="store_true",
                        help="warnings become failures")
    args = parser.parse_args(argv)

    repo_root = Path(__file__).resolve().parent.parent
    references_dir = Path(args.dir) if args.dir else repo_root / "references"
    if not references_dir.is_dir():
        print(f"error: references dir not found: {references_dir}", file=sys.stderr)
        return 2
    pairs = find_pairs(references_dir)
    if not pairs:
        print(f"no .md/.zh.md pairs found in {references_dir}", file=sys.stderr)
        return 2

    results = [analyze(a, b) for a, b in pairs]
    ref_warnings = scan_references(repo_root, references_dir)
    ph_warnings = scan_placeholders(repo_root)

    if args.json:
        print(json.dumps(
            {
                "report": results,
                "cross_reference_warnings": ref_warnings,
                "placeholder_warnings": ph_warnings,
            },
            ensure_ascii=False, indent=2))
    else:
        print(f"Checking bilingual alignment for {references_dir}\n")
        print(human_report(results, ref_warnings, ph_warnings))

    structural_fail = any(r["errors"] for r in results)
    repo_warnings = bool(ref_warnings or ph_warnings)
    warning_fail = args.strict and (repo_warnings or any(r["warnings"] for r in results))
    return 1 if (structural_fail or warning_fail) else 0


if __name__ == "__main__":
    sys.exit(main())