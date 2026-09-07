# Client Debugging

**Goal:** A structured post-incident write-up. The artifact is both the fix and a case
the product team can learn from; for AI systems it must also become a new regression
sample in the Golden Set — **the minimal failing case enters the library permanently**.

> **Client systems are not trusted.** The client's logs, samples, and descriptions may
> be incomplete or inaccurate — verify independently.

## Inputs & outputs

| | |
|---|---|
| Inputs | client problem reports, deploy/change records, relevant `runbook-<client>-vN` sections, Golden Set and eval results |
| Outputs | `ISS-<client-slug>-<YYYYMMDD>-<NN>` debug artifact (JSON), root-cause statement, fix & verification, new regression sample |
| Feeds into | `04-evaluation.md` (Golden Set regression), `08-product-feedback.md` (cross-client systemic gaps), `09-retro-assets.md` (reusable fixes as assets) |

## Step 1: Define and reproduce <!--a:step1-->

Record before touching any code:

```
Issue ID:     ISS-<client-slug>-<YYYYMMDD>-<NN>
Reported by:  <name, role, timestamp>
Environment:  <prod/staging/dev, region, cluster, model & prompt versions>
Symptom:      <what the client sees — error, wrong output, timeout>
Expected:     <what should have happened>
Repro steps:  <exact sequence, inputs, config>
Repro rate:   <every time / intermittent / once>
First seen:   <timestamp; correlated with a deploy, model/KB, or config change?>
```

Try to reproduce in a sandbox aligned with the client environment. **If you can't
reproduce it, say so plainly — don't guess.**

## Step 2: Isolate the fault <!--a:step2-->

Shrink the blast radius:

1. **Deployment surface** — deployed version, diff against last-known-good config, env-var drift, expired secrets.
2. **Request path** — which component returned the error? Draw the call chain, locate the failing hop.
3. **Input bisection** — if input is a file or payload, halve it repeatedly until you find the minimal failing subset.
4. **Dependencies** — did anything upstream change? (client proxy, firewall rules, data-source schema, certificate rotation)

For AI/Agent systems, **locate the fault layer before blaming the model**:

| AI fault layer | What to check |
|---|---|
| Content / retrieval | can the right document actually be retrieved? recall, ranking, index freshness |
| Media / parsing | did OCR, tables, or attachment parsing corrupt the input |
| Isolation / permissions | did ACL/tenant isolation hide or leak data |
| Knowledge version | stale KB, invalidated sources, model or prompt version drift |
| Runtime reliability | timeouts, rate limiting, dependency outages, orchestration bugs |
| Organization / process | human steps skipped, queue wrong, SOP not followed |

## Step 3: Root-cause analysis <!--a:step3-->

One sentence:

> **"<Component> <failed action> because <root cause>"**

If you can't say it in one sentence, you haven't found it yet.

Then classify by routing — **classification is industry-independent**: in a bank, a
fraud-check timeout is `client-upstream` (their scoring service), not `platform`.
Classification lets a ticket be routed honestly, whatever the industry.

| Classification | Meaning |
|---|---|
| **Platform** | bug or missing feature in the core product |
| **Config** | misconfiguration in the client environment |
| **Client-upstream** | problem in the client's own/controlled systems |
| **Integration** | connector / glue-code gap |
| **Process** | operational error (wrong version, skipped step) |

## Step 4: Fix & verify <!--a:step4-->

1. Propose the fix — if code changes are needed, produce a patch or a clear spec.
2. State the risk (data loss? downtime? side effects?).
3. After sandbox verification, **re-run the full Golden Set** — fixing one case must not
   silently break others (see `04-evaluation.md`).
4. Add this incident's **minimal failing case** to the Golden Set as a permanent
   regression sample.
5. Give the client verification steps they can run independently.

## Step 5: Debug artifact <!--a:step5-->

```json
{
  "issue_id": "ISS-<client-slug>-<YYYYMMDD>-<NN>",
  "status": "resolved | mitigated | escalated | wont-fix",
  "ai_failure_layer": "content | media | isolation | knowledge-version | runtime | process | n/a",
  "root_cause": "one sentence",
  "classification": "platform | config | client-upstream | integration | process",
  "fix": "what changed, with diff or reference",
  "golden_set_added": "GS-NNN or none",
  "client_verify": "client confirmation steps",
  "product_feedback": "true | false",
  "lessons": "what the on-call runbook should add"
}
```

If `product_feedback` is true, hand the artifact to `08-product-feedback.md`. If the
same failure recurs across clients, also flag it into `09-retro-assets.md` for
assetization.

## Templates / artifacts <!--a:template-->

- `templates/issue-template.json` — debug artifact JSON (the Step 5 shape)
- `templates/postmortem.md` — structured review for severe incidents (route those here)
- Artifact IDs: `ISS-<client-slug>-<YYYYMMDD>-<NN>`, regression sample `GS-NNN`

**Gate note:** no verifiable root cause, no classification routing, a fix not fully
re-run against the Golden Set, a regression sample not added → the ticket does not
close. Marking a systemic gap `product_feedback: false` is putting the problem back in
your pocket.

<correct_patterns>

### Good root-cause statement

> "The SFTP parser failed because the client's WMS added a `lot_expiry_date` column
> on 2026-06-26 without notice, shifting the schema."

**Why it's good:** names the component (SFTP parser), the failed action (parse), the
root cause (unannounced column), and the trigger date. Verifiable — replay the
2026-06-26 file to confirm.

### Good debug artifact

```json
{
  "issue_id": "ISS-atlas-20260629-01",
  "status": "mitigated",
  "ai_failure_layer": "content",
  "root_cause": "SFTP parser failed because the client's WMS added a lot_expiry_date column on 2026-06-26 without notice, shifting the schema.",
  "classification": "client-upstream",
  "fix": "Added drift detection (PR #4821); schema pinned to v2; schema v3 migration scheduled with client for 2026-07-15.",
  "golden_set_added": "GS-041 (unannounced column drift)",
  "client_verify": "Client runs `sftp-validate --file <latest>` — should print 'schema v2 OK' or list drift.",
  "product_feedback": true,
  "lessons": "Runbook §2.3 should add: 'on column-count change, alert on-call before retrying'. Drift detection should be on by default for all SFTP connectors."
}
```

**Why it's good:** one-sentence verifiable root cause; honest classification
(`client-upstream`, not `platform`); the fix surfaces drift instead of absorbing it;
the incident becomes a permanent regression sample (`GS-041`); `client_verify` is a
concrete command, not "trust us."

### Good classification decision

Symptom: parser fails on the client's files.
Temptation: classify as `platform` (it's our parser).
Correct: classify as `client-upstream` (the client changed the export without notice).
Why: classification decides routing. `platform`→escalate to the platform team (wasted
days hunting a nonexistent bug). `client-upstream`→document it for the client, don't
touch our code.

</correct_patterns>

<common_mistakes>

### Mistake: vague root cause

```json
{ "root_cause": "Parser bug in the sync job." }
```

**Why it's bad:** unverifiable, no trigger factor, symptom vs cause conflated. "Parser
bug" is the symptom; the root cause is what exposed it now.

### Mistake: misclassification to dodge a hard conversation

```json
{ "classification": "platform" }
```
when the client actually changed the export.

**Why it's bad:** routes the ticket to the platform team, which hunts a nonexistent bug
for days. It also trains the client to expect you to pay for their problems.

### Mistake: a fix that hides the problem

```
"fix": "Updated the parser to accept the new column."
```

**Why it's bad:** silently accepting schema drift means the next unannounced change
slips through too. The fix should make drift visible (alert), not invisible (accept).

### Mistake: unverifiable client verification

```
"client_verify": "Sync should work now."
```

**Why it's bad:** the client can't confirm independently. Give a command or a concrete
output.

### Mistake: blaming the model without locating the layer

> "The AI answered wrong again — swap the model."

**Why it's bad:** answer each of the six AI fault layers' "what to check" first. Before
swapping models, confirm whether retrieval missed the document, the knowledge version is
stale, or isolation leaked permissions — a fix aimed at the wrong layer is a new fault
source.

### Rationalizations to reject

- **"Patch the parser to unblock the client first; add drift detection later."**
  → Reality: "later" never comes. A patch that silently accepts the new column becomes
  permanent behavior. Add drift detection in the same PR.
- **"I can't reproduce it, but I'm pretty sure it's certificate rotation."**
  → Reality: a confident guess is still a guess. Say plainly: "cannot reproduce;
  suspected cert rotation; monitoring for recurrence" and set a re-check.
- **"The client says they changed nothing, so it must be our model release."**
  → Reality: the client's assertion is untrusted data. Independently check retrieval,
  KB freshness, schema, certificates, network path. "We changed nothing" usually means
  "we changed nothing we thought mattered."

</common_mistakes>

## TOP errors <!--a:top-->

1. Root cause is the symptom, not the cause ("parser bug")
2. Misclassification (`client-upstream` filed as `platform`)
3. Fix hides drift instead of surfacing it
4. `client_verify` without a command
5. Systemic gap marked `product_feedback: false`
6. Fix not fully re-run against the Golden Set; no regression sample added
7. AI failure blamed on "the model" without locating the fault layer

## Pre-delivery checklist <!--a:checklist-->

- [ ] Root cause stated in one verifiable sentence
- [ ] AI fault layer located (n/a for non-AI issues)
- [ ] Classification matches where the change actually happened
- [ ] Fix does not silently absorb client-side drift
- [ ] Full Golden Set re-run done; minimal failing case added permanently
- [ ] `client_verify` is a command or concrete output
- [ ] Cross-client recurrence risk marked `product_feedback`; repeated failures flagged into 09 for assetization
- [ ] `lessons` captured for the on-call runbook