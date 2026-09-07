# Deployment Runbook

**Goal:** A runbook that requires judgment or tacit knowledge is incomplete. Every step
must be safe for a colleague on their first day to execute — including observability,
failure rehearsal, and a reversible change path.

> Deploying is not just pushing code — it is delivering an operating state that someone
> can observe, someone can take over, and someone can roll back. Rollback is four
> separate things — image, migration, config, flags — and the reverse of a deploy is
> not symmetric.

## Inputs & outputs

| | |
|---|---|
| Inputs | `arch-<client-slug>-<YYYYMMDD>.md` architecture + all ADRs, `EVAL-<client>-vN` eval report + frozen Golden Set, `PLT-<client>-vN` pilot plan + `UAT-<client>-vN` / approved autonomy level, client environment details + IT contact, platform version to deploy, known constraints (air-gapped? VPN-only? no outbound internet? Windows-only?), previous runbook, historical debug artifacts |
| Outputs | `runbook-<client>-vN` deploy runbook, `SLO-<client>-vN` SLO table, `PM-<client>-vN` postmortem, post-deploy revision markers |
| Feeds into | `07-client-debug.md` (issue log & triage), `09-retro-assets.md` (reusable-fix loop), `08-product-feedback.md` (platform gaps) |

## Step 1: Collect inputs <!--a:step1-->

| Input | Source |
|---|---|
| Integration architecture | `03-integration-architecture.md` output + all ADRs |
| Eval report & Golden Set | `04-evaluation.md` output; pass conditions to re-verify |
| Pilot plan & UAT records | `05-pilot-adoption.md` output; approved autonomy level |
| Client environment details | discovery notes (`01-discovery.md`), client IT contact |
| Platform version to deploy | release notes, changelog |
| Known constraints | air-gapped? VPN-only? no outbound internet? Windows-only? |
| Previous runbook | version control (diff the delta) |
| Historical debug artifacts | `07-client-debug.md` issue log |

## Step 2: Runbook template <!--a:step2-->

```markdown
# Deployment Runbook: <Client> — <Platform Version>

**Last updated:** YYYY-MM-DD
**Runbook version:** v<N>
**Owner:** <FDE name>
**Client contact:** <name, role, contact>
**Approved autonomy level:** shadow | assist | limited-auto | full-auto

## 0. Pre-flight check
- [ ] Architecture doc and ADRs reviewed and current
- [ ] Eval pass conditions on the frozen Golden Set re-verified
- [ ] Client environment access confirmed (VPN, SSH, dashboard)
- [ ] All prerequisites met (see Section 1)
- [ ] Maintenance window approved; rollback plan reviewed

## 1. Prerequisites
### 1.1 Client side
| Item | Requirement | How to verify | Owner |
|------|-------------|---------------|-------|
| ... | ... | ... | client / FDE |
### 1.2 Platform side
| Item | Requirement | How to verify | Owner |
|------|-------------|---------------|-------|

## 2. Environment preparation
### 2.1 Network & connectivity
# Verify VPN connectivity
ping <client_host>
# Verify outbound access (if applicable)
curl -v https://<platform_endpoint>/health
### 2.2 Secrets & config
| Secret / Config | Value source | How to set | Rotate? |
|------------------|--------------|------------|---------|
| ... | client-provided | `export VAR=...` or vault path | monthly |
### 2.3 Dependencies
# Exact install commands, versions pinned (offline bundle for air-gap, see 10-airgap-deploy.md)

## 3. Core deployment
Step by step, in order. For each step write:
- exact command or action
- expected output or success signal
- failure mode and immediate action

### 3.N <step name>
# Command
<exact command>
# Expected output
<what success looks like>
# If it fails
<what to check first>

## 4. Verification
### 4.1 Smoke tests       | Test | Command | Expected |
### 4.2 Data integrity    | Check | Query / command | Threshold |
### 4.3 Observability     metrics, structured logs, traces, audit events all streaming;
                           SLO dashboard live

## 5. Canary / staged rollout
Cohort order, promotion conditions, pause/rollback trigger lines (see Step 4).

## 6. Client handover
- [ ] Client contact confirms smoke passed
- [ ] Client contact has dashboard/monitoring access
- [ ] Client contact knows the escalation path
- [ ] Autonomy level and its boundaries explained in writing

## 7. Rollback
Trigger conditions; exact steps including migration downgrade, config revert, and flag
restore (see Step 4).

## 8. Post-deploy
- [ ] Runbook updated for actual deviations
- [ ] New debug artifacts archived; new Golden Set regression added (see 07-client-debug.md)
- [ ] Product feedback / asset proposals archived where needed
- [ ] Reusable fixes marked into 09-retro-assets.md — so the next runbook starts higher
```

## Step 3: Minimal observability set & SLO <!--a:step3-->

All four signal classes must be live before launch — **an AI system you cannot observe
cannot be safely automated**:

| Signal | Minimal content |
|---|---|
| Metrics | request volume, latency, error rate, human-takeover rate, token/cost |
| Structured logs | one correlation id across the whole chain; input class, decision, output |
| Traces | per-hop latency: retrieval→model→tools→actions |
| Audit events | who/what executed what action on what data, before/after values (queryable, tamper-evident) |

Define one small SLO table with the client (template: `templates/slo-table.md`); **every SLO has an alert and an Owner**:

```
SLI: share of assisted triage completed without human correction
SLO: rolling 7-day ≥97%        Alert: 1h continuous <95% → page on-call
SLI: unsafe-action count      SLO: 0                        Alert: any occurrence → page and freeze autonomy
SLI: end-to-end P95 latency   SLO: ≤8s                      Alert: 15min continuous >12s
```

## Step 4: Fault injection & change governance <!--a:step4-->

**Rehearse failures before the client meets them.** In staging, inject at least five
classes and record system behavior: data conflict (schema drift / duplicate keys),
dependency failure (downstream timeout / outage), duplicate execution (retry / double
submit), approval/version anomaly (outdated SOP, wrong model version), evidence
invalidation (cited document deleted / expired). Every class must **degrade safely or
alert — never produce silently**.

Production change governance:

1. **Canary / staged** — smallest cohort first; promote only while SLO holds (cohort order and trigger lines written into runbook Section 5).
2. **Promotion conditions pre-written** — metrics and time window, not gut feel.
3. **Pause and rollback trigger lines numeric** — rollback covers **image, data migration, config, and feature flags** — four separate things.
4. **Every incident gets a Postmortem** (template: `templates/postmortem.md`) → one fix, one runbook update, one new Golden Set regression (see `07-client-debug.md`).

### Deploy four-exit decision record

Every staged promotion is a gate; decide with the same four-exit vocabulary as
evaluation and record the evidence:

| Exit | Condition | Action |
|---|---|---|
| **Continue** | current cohort meets SLO, no new crashes | promote the next cohort |
| **Narrow** | some dimensions pass but risk is elevated | hold current scale, pause expansion |
| **Revise** | direction holds, a fault class is fixable forward | fix, then re-promote from the current cohort (no skipping) |
| **Stop (rollback)** | SLO crosses the rollback line | execute Section 7 rollback to an verifiable prior state |

```markdown
# Deploy four-exit decision record: <Client> — <release vN> <date>
- Exit: <continue / narrow / revise / stop-rollback>
- Basis: <this cohort's SLO numbers, alert count, fault-injection / real-fault observations>
- Decider: <named; a rollback needs no approval — on-call executes it immediately>
```

## Step 5: Sanity check <!--a:step5-->

Before delivery:

1. **Every command copy-pasteable** — each `<fill-me>` has a concrete example.
2. **Every condition branch explicit** — "if X, jump to Section 3.2; if Y, jump to Section 7", never "troubleshoot and retry".
3. **Time realistic** — each section notes expected duration so operators can plan.
4. **Rollback really works** — walk it backward in your head: image, migration, config, flags — can each restore the exact prior state?
5. **Observability and SLO alerts proven to fire**, not merely configured.

## Step 6: Version & archive <!--a:step6-->

- Commit to the client's deployment repository.
- Tag with platform version and runbook version.
- Notify the client contact and other FDEs on this client.
- Mark **reusable fixes** into `09-retro-assets.md` and systemic gaps into `08-product-feedback.md` — so the next runbook starts higher (FDE-02 loop).

## Templates / artifacts <!--a:template-->

- `templates/deployment-runbook.md` (if stored separately) — runbook skeleton; this module's body is the template
- `templates/slo-table.md` — SLO table
- `templates/postmortem.md` — incident review
- Artifact IDs: `runbook-<client>-vN`, `SLO-<client>-vN`, `PM-<client>-vN`

**Gate note:** no four signal classes, no SLO alert proven to fire, no five-class fault
injection rehearsal, no rollback rehearsal covering image+migration+config+flags → no
production deploy. A runbook full of placeholders is just as "approved" as a real one.

<correct_patterns>

### Good step block

```bash
# Command
curl -v https://api.atlas-logistics.example.com:8443/health

# Expected output
< HTTP/2 200
< {"status":"ok","version":"4.8.2"}

# If it fails
# — Connection refused → check VPN (Section 2.1)
# — 401              → check secret rotation (Section 2.2)
# — 404              → wrong endpoint, verify against arch doc Section 5
```

**Why it's good:** copy-pasteable command (real host, real port); precise expected
output (status code + body shape); failure modes cross-reference other sections so ops
never gets stuck.

### Good rollback steps (image + migration + flags separated)

```bash
# 1. Stop the new version
kubectl scale deployment platform-api --replicas=0 -n prod
# 2. Re-apply previous manifest (includes the previous image, NOT the migration)
kubectl apply -f deploy/manifests/v4.8.1/ -n prod
# 3. Reverse the DB migration
kubectl exec -n prod deploy/platform-api -- python migrate.py downgrade v4.8.1
# 4. Reset feature flags to previous baseline
kubectl exec -n prod deploy/platform-api -- python flags.py restore v4.8.1
# 5. Verify
kubectl rollout status deployment/platform-api -n prod
curl -s https://api.atlas-logistics.example.com:8443/health
# Expected: {"status":"ok","version":"4.8.1"}
```

**Why it's good:** five clear steps, each verifiable, dependency-ordered. Image,
migration, and flags are separate actions — rollback is asymmetric, each must be written
out, and ops can stop at any step.

### Good observability confirmation

```
2026-07-14 staging environment confirmed:
- Metrics: 14 series visible on the dashboard, 30s refresh (screenshot attached)
- Logs:    correlation id 8c2... links the 6 ingest→retrieve→answer lines
- Traces:  4 hops visible, P95 6.2s
- Audit:   test action AT-001 recorded before/after values, queryable for compliance
- Alerts:  14:22 deliberately breached SLO; on-call paged within 48s
```

**Why it's good:** observability is proven by "actively manufacturing one failure,"
not by assuming config works; every signal has evidence and a timestamp.

</correct_patterns>

<common_mistakes>

### Mistake: placeholder without an example

```bash
curl https://<client_host>:<port>/health
```

**Why it's bad:** ops can't tell what a valid host/port looks like. Give a concrete
example per placeholder: `curl https://api.atlas-logistics.example.com:8443/health`.

### Mistake: vague condition

```
"If the deployment fails, troubleshoot and retry."
```

**Why it's bad:** "troubleshoot" is not an action. Write it concretely: if
`kubectl rollout status` shows `ProgressDeadlineExceeded`, jump to Section 7 (rollback).
If it shows `ImagePullBackOff`, check the registry credentials in Section 2.2.

### Mistake: rollback that can't restore state

```bash
kubectl rollout undo deployment/platform-api -n prod
```
but the deploy also ran a DB migration and flipped feature flags.

**Why it's bad:** `rollout undo` only reverts the image. The application expects the old
schema and old flags — calls fail in hard-to-diagnose ways. Rollback must cover image +
migration + config + flags.

### Mistake: "ops knows"

```bash
# Apply the usual network config
```

**Why it's bad:** there is no "usual." Day one has no usual. Every command must be
explicit. "Usual" is tacit knowledge — the runbook exists to replace it, not reference it.

### Rationalizations to reject

- **"Ops is experienced; they know what to do."**
  → Reality: runbooks outlive people. The veteran quits; the newcomer inherits this
  document during a 3 AM outage. Write for day one.
- **"Fault injection on a first launch is overkill."**
  → Reality: these five fault classes are exactly what production serves up first.
  Staging rehearsal costs hours; production triage costs days plus lost trust.
- **"We'll fill in the exact commands later; get the structure out first."**
  → Reality: a structure full of placeholders ships as easily as a filled-in runbook.
  If you don't fill it now, nobody will.
- **"Rollback is just the reverse of deploy; no need to write it."**
  → Reality: deploys include migrations, flags, and external state (DNS, cache,
  queues). The reverse is asymmetric — write it step by step.

</common_mistakes>

## TOP errors <!--a:top-->

1. Placeholders (`<fill-me>`) without a concrete example
2. Vague conditions ("if it fails, troubleshoot")
3. Rollback missing migration / flags / config revert
4. Steps without expected output
5. Observability configured but never proven to fire
6. Five fault classes never rehearsed
7. Assumes "ops knows"
8. No reusable fixes handed back post-deploy (the shared base never grows)

## Pre-delivery checklist <!--a:checklist-->

- [ ] Every command copy-pasteable, no bare placeholders
- [ ] Every step has an expected output
- [ ] Every condition branch explicit (incl. "if it fails, jump to which section")
- [ ] Rollback walked backward in the head, covering image + migration + config + flags
- [ ] Four observability signal classes live; SLO alerts proven to fire
- [ ] Five fault classes injected and results recorded
- [ ] Canary promotion / pause / rollback trigger lines numeric and agreed in advance
- [ ] Durations realistic per section; walked through with the executing ops engineer
- [ ] Post-deploy: runbook updated, debug artifacts archived, reusable fixes marked into 09, gaps written into 08