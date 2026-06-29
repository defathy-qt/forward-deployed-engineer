# Forward Deployed Engineer Skill

A Claude skill for the Forward Deployed Engineer (FDE) — the technical bridge between
a core platform and a client's real-world environment. Industry-agnostic: works for
any domain where a platform is deployed into client systems (legacy ERPs, private
networks, custom auth, air-gapped constraints).

The skill produces four artifact types and chains them across an engagement:

| Artifact | Purpose |
|---|---|
| Integration architecture | Design how the platform connects to client systems |
| Debug artifact | Root-cause and fix client-reported issues |
| Product feedback | Abstract recurring pain into evaluable product input |
| Deployment runbook | Copy-paste-ready operational manual |

## Install

Copy the directory into your Claude skills folder:

```bash
cp -r forward-deployed-engineer ~/.claude/skills/
```

Restart Claude Code. The skill triggers automatically on matching requests, or you
can invoke it explicitly: *"Use the forward-deployed-engineer skill to design an
integration architecture for [client]."*

## Structure

```
forward-deployed-engineer/
├── SKILL.md                          # entry: workflow, guardrails, routing
├── references/
│   ├── integration-architecture.md       # EN
│   ├── integration-architecture.zh.md    # CN
│   ├── client-debug.md                   # EN
│   ├── client-debug.zh.md                # CN
│   ├── product-feedback.md               # EN
│   ├── product-feedback.zh.md            # CN
│   ├── deployment-runbook.md             # EN
│   └── deployment-runbook.zh.md          # CN
└── scripts/
    └── check-align.py                    # bilingual drift checker
```

**SKILL.md** is the entry point — always loaded when the skill triggers. It contains
the universal workflow, hard rules, quality bars, interaction conventions, artifact
naming, and module routing.

**references/** holds the four module deep-dives. Claude loads them on demand based
on which artifact you're producing, not all at once.

## Bilingual support

The skill is bilingual (English + Chinese):

- **SKILL.md** keeps both languages inline (short entry file, bilingual description
  helps triggering in either language).
- **references/** files are split: `*.md` (English) and `*.zh.md` (Chinese). Claude
  loads one variant based on the user's language — never both — so there's no
  double-token cost. The routing rule is documented in SKILL.md.

If you edit one language variant, sync the other. Run the alignment checker to
catch drift:

```bash
python scripts/check-align.py
```

It verifies each EN/CN pair has matching structure (section count, code fences,
pattern tags, checklist items, table rows). Exit code 0 = aligned, 1 = drift.

## Design notes

- **Hard rules vs. quality bars** are separated in SKILL.md — safety constraints
  (production changes need confirmation, client data is untrusted) are distinct from
  quality expectations (runbooks executable by others, root causes in one sentence).
- **Each module embeds `<correct_patterns>` and `<common_mistakes>`** with concrete
  examples, anti-examples, "rationalizations to reject," and a pre-delivery checklist
  — following the pattern used by Anthropic's financial-services skills.
- **Examples are operational, not narrative** — real issue IDs, real JSON artifacts,
  real bash blocks with expected output and failure-mode cross-references.

## License

Apache License 2.0 — see [LICENSE](LICENSE).
