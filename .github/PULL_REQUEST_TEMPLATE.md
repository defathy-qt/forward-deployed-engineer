## What this PR changes / 变更内容

<!-- One or two sentences. If adding/editing a reference, note EN and ZH both. -->

## Checklist / 自查清单

- [ ] EN (`.md`) and ZH (`.zh.md`) both updated in this PR
- [ ] Same heading hierarchy and `<!--a:...-->` anchors on both sides
- [ ] `python scripts/check-align.py references` passes locally
- [ ] `python scripts/check-align.py references --strict` has no new warnings
- [ ] Every `<TBD>`/`<fill-me>` has a concrete example alongside
- [ ] Module bodies reference `templates/...` only when an artifact must exist (single source of truth)
- [ ] No client names, people, contract values, or real records (de-identified)
- [ ] New artifact template/example added where a new artifact type is introduced
- [ ] Union rule respected: nothing unique removed from FDE-01 / FDE-02 source; any trim is recorded
    against the union checklist
- [ ] CHANGELOG updated under Unreleased

## Evidence / 验证证据

<!-- Commands run, eval/gate IDs, screenshots of alerts firing, etc. -->