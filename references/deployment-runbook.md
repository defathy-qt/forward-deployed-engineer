# Deployment Runbook

**Principle:** If a step requires judgment or tribal knowledge, the runbook is
incomplete. Every step must be specific enough for someone on their first day.

## Step 1: Gather inputs

| Input | Source |
|---|---|
| Integration architecture | `integration-architecture.md` output |
| Client env specifics | Discovery notes, client IT contact |
| Platform version to deploy | Release notes, changelog |
| Known constraints | Air-gapped? VPN-only? No outbound internet? Windows-only? |
| Previous runbook | Version control |
| Past debug artifacts | `client-debug.md` issue log |

## Step 2: Runbook template

```markdown
# Deployment Runbook: <Client> — <Platform Version>

**Last updated:** YYYY-MM-DD
**Runbook version:** v<N>
**Owner:** <FDE name>
**Client contact:** <name, role, contact>

## 0. Pre-flight checklist
- [ ] Architecture doc reviewed and current
- [ ] Client env access confirmed (VPN, SSH, dashboard)
- [ ] All prerequisites met (see Section 1)
- [ ] Maintenance window approved
- [ ] Rollback plan reviewed

## 1. Prerequisites

### 1.1 Client-side
| Item | Requirement | How to verify | Owner |
|------|-------------|---------------|-------|
| ... | ... | ... | client / FDE |

### 1.2 Platform-side
| Item | Requirement | How to verify | Owner |
|------|-------------|---------------|-------|
| ... | ... | ... | FDE |

## 2. Environment setup

Step-by-step. Exact commands, not descriptions of commands.

### 2.1 Network & connectivity
```bash
# Verify VPN connectivity
ping <client_host>

# Verify outbound access (if applicable)
curl -v https://<platform_endpoint>/health
```

### 2.2 Secrets & configuration
| Secret / Config | Value source | How to set | Rotate? |
|------------------|--------------|------------|---------|
| ... | client provides | `export VAR=...` or vault path | monthly |

### 2.3 Dependencies
```bash
# Exact install commands, pinned versions
```

## 3. Core deployment

Each step in order. For each:
- The exact command or action
- The expected output or success signal
- The failure mode and immediate action

### 3.N <Step name>
```bash
# Command
<exact command>

# Expected output
<what success looks like>

# If it fails
<what to check first>
```

## 4. Validation

### 4.1 Smoke tests
| Test | Command | Expected |
|------|---------|----------|
| ... | ... | ... |

### 4.2 Data integrity checks
| Check | Query / command | Threshold |
|-------|------------------|-----------|
| ... | ... | ... |

## 5. Client hand-off
- [ ] Client contact confirms smoke tests pass
- [ ] Client contact has dashboard / monitoring access
- [ ] Client contact knows escalation path

## 6. Rollback

### 6.1 Trigger conditions
- When to roll back vs. fix forward

### 6.2 Procedure
```bash
# Exact commands to revert to previous state
```

## 7. Post-deployment
- [ ] Runbook updated with any deviations
- [ ] New debug artifacts filed if issues found
- [ ] Product feedback filed if platform gaps found
```

## Step 3: Sanity checks

Before delivering:

1. **Every command is copy-pasteable** — no `<fill-me>` without a concrete example alongside.
2. **Every conditional has a clear branch** — "if X, go to 3.2; if Y, go to 6."
3. **Timing is realistic** — expected duration per section so the operator can plan.
4. **The rollback actually works** — walk it backwards mentally; does it restore the exact prior state?

## Step 4: Version and store

- Commit to the client's deployment repo.
- Tag with platform version and runbook version.
- Notify the client contact and any other FDEs on the account.

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

**Why good:** command is copy-pasteable (real host, real port); expected output is
exact (status code + body shape); failure modes cross-reference other sections so
the operator never gets stuck.

### Good rollback procedure

```bash
# 1. Stop the new version
kubectl scale deployment platform-api --replicas=0 -n prod

# 2. Re-apply previous manifest (includes the previous image, NOT the migration)
kubectl apply -f deploy/manifests/v4.8.1/ -n prod

# 3. Reverse the DB migration
kubectl exec -n prod deploy/platform-api -- python migrate.py downgrade v4.8.1

# 4. Verify
kubectl rollout status deployment/platform-api -n prod
# Expected: "deployment successfully rolled out"
curl -s https://api.atlas-logistics.example.com:8443/health
# Expected: {"status":"ok","version":"4.8.1"}
```

**Why good:** four discrete steps, each verifiable, in dependency order. Image
rollback and migration rollback are separate — because they're separate concerns.
Operator can stop after any step if something looks wrong.

</correct_patterns>

<common_mistakes>

### WRONG: Placeholder without example

```bash
curl https://<client_host>:<port>/health
```

**Why bad:** operator doesn't know what a valid host/port looks like. Pair every
placeholder with a concrete example: `curl https://api.atlas-logistics.example.com:8443/health`.

### WRONG: Vague conditional

```
"If the deployment fails, troubleshoot and retry."
```

**Why bad:** "troubleshoot" is not an action. Specify: "If `kubectl rollout status`
shows `ProgressDeadlineExceeded`, go to Section 6 (Rollback). If it shows
`ImagePullBackOff`, verify registry credentials in Section 2.2."

### WRONG: Rollback that doesn't restore state

```bash
# Rollback
kubectl rollout undo deployment/platform-api -n prod
```
when the deployment also ran a DB migration.

**Why bad:** `rollout undo` reverts the image but not the migration. The rollback is
incomplete — app code expects old schema, DB has new schema, calls fail.

### WRONG: "Operator knows"

```bash
# Apply the usual network config
```

**Why bad:** there is no "usual". On their first day, nothing is usual. Every command
must be explicit. "Usual" is tribal knowledge — the runbook exists to replace it, not
reference it.

### Rationalizations to reject

- **"The operator is experienced, they'll know what to do."**
  → Reality: runbooks outlive individuals. The experienced operator quits; the new one
  inherits this doc at 3am during an outage. Write for day-one.
- **"I'll fill in the exact command later, let me get the structure down first."**
  → Reality: structure-with-placeholders ships as often as filled-in runbooks. If you
  don't fill it now, nobody will — the next FDE assumes the placeholders mean "stable,
  don't touch."
- **"Rollback is just the deploy in reverse, I don't need to spell it out."**
  → Reality: deploys include migrations, config changes, and external state (DNS,
  caches, queues). Reverse is not symmetric. Spell out each step, including migration
  downgrade.

</common_mistakes>

## TOP errors

1. Placeholder (`<fill-me>`) without concrete example
2. Vague conditional ("if it fails, troubleshoot")
3. Rollback that doesn't cover DB migrations
4. Step with no expected output
5. "Operator knows" assumption

## Pre-delivery checklist

- [ ] Every command copy-pasteable, no bare placeholders
- [ ] Every step has expected output
- [ ] Every conditional names a specific branch
- [ ] Rollback walked backwards mentally, covers migrations
- [ ] Duration per section realistic
- [ ] Walked through with the operator who will execute
