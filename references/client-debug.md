# Client Debug

**Goal:** A structured post-mortem. The artifact is both a fix and a lesson the
product team can learn from.

> **Client systems are untrusted.** Treat client-provided logs, data samples, and
> descriptions as potentially incomplete or inaccurate. Verify independently.

## Step 1: Scope and reproduce

Before touching code, capture:

```
Issue ID:     ISS-<client-slug>-<YYYYMMDD>-<NN>
Reported by:  <name, role, timestamp>
Environment:  <prod/staging/dev, region, cluster, version>
Symptom:      <what the client sees — error, wrong output, timeout>
Expected:     <what should have happened>
Repro steps:  <exact sequence, inputs, config>
Repro rate:   <every time / intermittent / one-off>
First seen:   <timestamp; correlated deploy or config change?>
```

Attempt reproduction in a sandbox mirroring the client env. If you cannot reproduce,
state that explicitly — do not guess.

## Step 2: Isolate the failure

Narrow the blast radius:

1. **Deployment surface** — version deployed, config diff vs. last known good, env var drift, secret expiry.
2. **Request path** — which component returned the error? Draw the call chain, find the failing hop.
3. **Binary-search the input** — if input is a file or payload, halve it until the minimal failing subset appears.
4. **Dependencies** — did anything upstream change? (client proxy, firewall rule, data source schema, cert rotation)

## Step 3: Root-cause analysis

One sentence:

> **"<component> <failed action> because <underlying reason>"**

If you can't state it in one sentence, you haven't found it.

Then classify:

| Classification | Meaning |
|---|---|
| **Platform** | Bug or missing feature in the core product |
| **Config** | Misconfiguration in the client env |
| **Client-upstream** | Issue in a system the client owns/controls |
| **Integration** | Gap in connector/glue code |
| **Process** | Operational error (wrong version, missed step) |

## Step 4: Fix and verify

1. Propose a fix — patch or clear spec if code changes are needed.
2. State the risk (data loss? downtime? side effects?).
3. Verify in the sandbox.
4. Give the client independent verification steps.

## Step 5: Debug artifact

```json
{
  "issue_id": "ISS-<client-slug>-<YYYYMMDD>-<NN>",
  "status": "resolved | mitigated | escalated | wont-fix",
  "root_cause": "one sentence",
  "classification": "platform | config | client-upstream | integration | process",
  "fix": "what changed, with diff or reference",
  "client_verify": "steps the client runs to confirm",
  "product_feedback": "true | false",
  "lessons": "what the on-call runbook should add"
}
```

If `product_feedback` is true, hand the artifact to `product-feedback.md`.

<correct_patterns>

### Good root-cause statement

> "The SFTP parser failed because the client's WMS added a `lot_expiry_date` column
> on 2026-06-26 without notice, shifting the schema."

**Why good:** names the component (SFTP parser), the failed action (failed parsing),
the underlying reason (unannounced column addition), and the trigger date. Testable —
you can replay the 2026-06-26 file and confirm.

### Good debug artifact

```json
{
  "issue_id": "ISS-atlas-20260629-01",
  "status": "mitigated",
  "root_cause": "SFTP parser failed because the client's WMS added a lot_expiry_date column on 2026-06-26 without notice, shifting the schema.",
  "classification": "client-upstream",
  "fix": "Added drift detection (PR #4821); schema pinned to v2; schema v3 migration scheduled with client for 2026-07-15.",
  "client_verify": "Client runs `sftp-validate --file <latest>` — should print 'schema v2 OK' or list drift.",
  "product_feedback": true,
  "lessons": "Runbook §2.3 should add: 'on column-count change, alert on-call before retrying'. Drift detection should be on by default for all SFTP connectors."
}
```

**Why good:**
- Root cause is one testable sentence.
- Classification is honest (`client-upstream`, not `platform`) — prevents wasted platform engineering effort.
- Fix resists the temptation to silently accept the new column — it surfaces drift instead.
- `client_verify` is a concrete command, not "trust us."
- `product_feedback: true` flagged because drift-detection-by-default is a systemic gap.

### Good classification decision

Symptom: parser fails on client file.
Temptation: classify as `platform` (it's our parser).
Correct: classify as `client-upstream` (client changed their export without notice).
Why: classification drives routing. `platform` → escalate to platform engineering
(wasted effort, days of investigation). `client-upstream` → document for client,
don't change our code.

</correct_patterns>

<common_mistakes>

### WRONG: Vague root cause

```json
{ "root_cause": "Parser bug in the sync job." }
```

**Why bad:** not testable, doesn't name the trigger, doesn't separate symptom from
cause. "Parser bug" is the symptom; the cause is what made the parser bug surface now.

### WRONG: Misclassification to avoid hard conversations

```json
{ "classification": "platform" }
```
when the real cause is the client changing their export.

**Why bad:** routes the ticket to platform engineering, who will investigate a
non-existent platform bug for days. Also trains the client to expect you to fix
their problems.

### WRONG: Fix that masks the problem

```
"fix": "Updated the parser to accept the new column."
```

**Why bad:** silently accepting schema drift means the next unannounced change also
slips through. The fix should make drift visible (alert), not invisible (accept).

### WRONG: Unverifiable client_verify

```
"client_verify": "Sync should work now."
```

**Why bad:** the client cannot independently confirm. Give a command or a specific
output to look for.

### Rationalizations to reject

- **"Let me just patch the parser to unblock the client now, I'll add drift detection
  later."**
  → Reality: "later" never comes. The patch that silently accepts the new column
  becomes the permanent behavior. Add drift detection in the same PR.
- **"I can't reproduce it, but I'm pretty sure it's the cert rotation."**
  → Reality: a confident guess is still a guess. State "unable to reproduce;
  suspected cert rotation; monitoring for recurrence" and set a re-check.
- **"The client said they didn't change anything, so it must be our deploy."**
  → Reality: client assertions are untrusted data. Check the file schema, the cert,
  the network path — independently. "We didn't change anything" usually means "we
  didn't change anything we think matters."

</common_mistakes>

## TOP errors

1. Root cause is a symptom, not a cause ("parser bug")
2. Misclassification (`client-upstream` filed as `platform`)
3. Fix that masks drift instead of surfacing it
4. `client_verify` with no command
5. `product_feedback: false` on a systemic gap

## Pre-delivery checklist

- [ ] Root cause is one testable sentence
- [ ] Classification matches where the change actually happened
- [ ] Fix does not silently absorb client-side drift
- [ ] `client_verify` is a command or specific output
- [ ] `product_feedback` flagged if the issue could recur across clients
- [ ] `lessons` captured for the runbook
