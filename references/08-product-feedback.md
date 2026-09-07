# Product Feedback

**Goal:** Make feedback **evaluable** — a product manager can set priority after reading
it, with no follow-up questions; reusable patterns flow into the asset library at the
same time (see `09-retro-assets.md`). Feedback is the first half of the loop; the second
half (turning it into a reusable asset) is completed in `09`.

> Product feedback feeds the platform team; reusable assets feed the *next FDE*. Both
> halves must exist — feedback alone is a suggestion box, assets alone are an
> information silo.

## Inputs & outputs

| | |
|---|---|
| Inputs | debug artifacts `ISS-*`, deployment notes, FDE retro, client requests |
| Outputs | `FB-<YYYY>-<NNN>` feedback entry (JSON), de-identified evidence, linked asset proposals |
| Feeds into | `09-retro-assets.md` (reusable assetization), product-team backlog/Linear/Jira |

## Step 1: Pattern recognition <!--a:step1-->

Before writing any single-client request, check:

1. Have other clients reported it? Search historical debug artifacts, deployment notes, feedback entries.
2. Is it a symptom of a deeper gap? ("Client wants custom report X" may really be "the reporting module lacks configurability.")
3. Is it a real product gap, or does existing functionality + better docs/config solve it?

If #3 is "existing functionality solves it," stop — file a docs or config improvement.
Then rate **generality**, which decides routing:

| Generality | Meaning | Route |
|---|---|---|
| **Single-client** | a specific customization for one client | deliver as config; not into the backlog |
| **Reusable pattern** | the same gap is likely at 2–3+ clients | feedback entry; candidate asset |
| **Platform capability** | needed at every deployment | feedback entry + asset proposal, P0/P1 |

## Step 2: De-identify and generalize <!--a:step2-->

Strip client-identifying details (name, industry, contract value, dates), then generalize:

| Client-specific (not included) | Generalized (included) |
|---|---|
| "Acme Corp needs a SOAP connector to their legacy ERP" | "connector framework for on-prem legacy systems exposing SOAP" |
| "Client X's compliance team wants custom checklists" | "compliance rule engine needs jurisdiction-configurable checklists" |
| "Client Y's month-end close takes 3 days" | "month-end close needs parallelization and incremental processing" |

## Step 3: Impact assessment <!--a:step3-->

| Dimension | How to assess |
|---|---|
| **Client count** | 1 / 2-3 / 4+ / "every new deployment" |
| **Deal impact** | blocking renewal / required-for-RFP / differentiator / quality-of-life |
| **Workaround cost** | FDE hours this missing capability costs per deployment |
| **Strategic fit** | yes / partial / tangential |
| **Asset leverage** | can one fix shorten the next N deployments (none / parameterizable / productizable) |

## Step 4: Feedback entry <!--a:step4-->

```json
{
  "feedback_id": "FB-<YYYY>-<NNN>",
  "title": "one line, outcome-oriented",
  "source": ["ISS-...", "Client Y deployment notes", "FDE retro"],
  "generality": "single-client | reusable-pattern | platform-capability",
  "pattern": "one-off | recurring (N clients) | universal (every deployment)",
  "current_state": "the gap described in product language",
  "desired_outcome": "result, not implementation",
  "evidence": [
    "Client A: ... (de-identified)",
    "Client B: ... (de-identified)"
  ],
  "proposed_scope": "feature / API / config surface / docs / reusable-asset",
  "impact": {
    "affected_clients": "1 | 2-3 | 4+ | every-deployment",
    "deal_impact": "blocking | required-for-rfp | differentiator | qol",
    "fde_hours_per_deployment": "estimated hours saved",
    "asset_leverage": "none | parameterizable | productizable"
  },
  "priority_recommendation": "p0-critical | p1-high | p2-medium | p3-nice-to-have",
  "related_feedback": ["FB-2026-042"],
  "attachments": ["ISS-..."]
}
```

## Step 5: Link and archive <!--a:step5-->

- From a debug artifact? Back-link the issue ID (template: `templates/feedback-template.json`).
- Multiple entries describing the same gap? Merge and record the related IDs.
- Archive where the product team consumes feedback (backlog, Linear, Jira).
- If generality is "reusable pattern" or "platform capability", open the corresponding asset proposal in `09-retro-assets.md` in the same pass.

## Step 6: Close the loop — two-way distillation into assets <!--a:step6-->

An archived entry is not yet an asset. If the same gap recurs or blocks multiple
deployments, do the two-way distillation: feedback feeds the platform team, reusable
assets feed the *next FDE*:

| Feedback shape | Output asset (`09-retro-assets.md`) |
|---|---|
| Recurring task pattern | Skill (repeatable steps) |
| Recurring system connection | Connector (productized integration) |
| Recurring eval / methodology gap | Template or test set (Golden Set stratum) |
| Platform bug / missing capability | Product requirement with evidence and ROI |

## Templates / artifacts <!--a:template-->

- `templates/feedback-template.json` — feedback entry JSON (the Step 4 shape)
- Artifact IDs: `FB-<YYYY>-<NNN>`

**Gate note:** evidence with client names, implementation-speak instead of results, a
lied-in `pattern`, or unquantified impact → the entry is rejected. Archive that never
becomes an asset = a suggestion box nobody reads.

<correct_patterns>

### Good feedback entry (excerpt)

```json
{
  "feedback_id": "FB-2026-042",
  "title": "Drift detection for SFTP connectors should be on by default",
  "source": ["ISS-atlas-20260629-01", "ISS-beta-20260418-02", "FDE retro 2026-06"],
  "generality": "platform-capability",
  "pattern": "recurring (3 clients in 6 months)",
  "current_state": "SFTP connectors fail silently when client schema changes; drift detection exists but is opt-in.",
  "desired_outcome": "Drift detection on by default for all SFTP connectors, with configurable alert threshold.",
  "evidence": [
    "Client A: unannounced column addition caused 3-day sync failure (de-identified)",
    "Client B: column rename caused silent data loss for 1 batch (de-identified)",
    "Client C: detected drift only because FDE happened to be on-call (de-identified)"
  ],
  "proposed_scope": "config default + alert",
  "impact": {
    "affected_clients": "4+",
    "deal_impact": "differentiator",
    "fde_hours_per_deployment": "3-5h per deployment troubleshooting drift",
    "asset_leverage": "productizable"
  },
  "priority_recommendation": "p1-high",
  "related_feedback": []
}
```

**Why it's good:** outcome-oriented title; generality and pattern honestly quantified
with sources; evidence de-identified across three instances; results not API shapes;
impact concrete (3-5h per deployment) plus asset leverage (PM can compute ROI);
priority honest (P1, not P0).

### Good de-identification

| Original (do not archive) | De-identified (archive) |
|---|---|
| "Acme Corp's WMS added lot_expiry_date on 2026-06-26" | "Client A: unannounced column addition (date withheld)" |
| "Bank ABC's compliance team wants a custom KYC checklist" | "Client B: compliance team needs configurable checklists" |

**Why it's good:** strips names, industry, and dates while keeping the technical shape.
The product team can act without knowing which client.

</correct_patterns>

<common_mistakes>

### Mistake: naming the client

```
"evidence": ["Acme Corp's WMS added a column on 2026-06-26..."]
```

**Why it's bad:** violates de-identification. Internal artifacts get forwarded to PMs,
executives, and sometimes external slides. Once a client name is on paper it propagates.

### Mistake: writing the implementation

```
"proposed_scope": "Add a `drift_detection_enabled` boolean to the SFTP connector config, default true, with a `drift_alert_threshold` int field..."
```

**Why it's bad:** prescribes the API shape. The product team may have a better design
(event-driven, not a boolean). Describe the result ("drift detection on by default"),
not the implementation.

### Mistake: inflating the priority

```
"priority_recommendation": "p0-critical"
```
for a nice-to-have.

**Why it's bad:** trains the product team to discount your priorities. When a real P0
(data loss, security) arrives it is buried under fake P0s.

### Mistake: lying in `pattern`

```
"pattern": "recurring (N clients)"
```
when only one client reported it, though it's a big client.

**Why it's bad:** `pattern` quantifies breadth. Lying here misleads priority and
erodes the field's credibility. If the truth is "one-off (large client, high ARR)",
write exactly that — it is still a useful signal.

### Rationalizations to reject

- **"I mark it P0 so they'll actually look."**
  → Reality: crying-wolf P0s train the team to ignore you. When a real P0 arrives it
  gets drowned out. "Important but not blocking" is P1-high — it still gets seen.
- **"It's one client, but a big one, so I'll write 'recurring'."**
  → Reality: the pattern field quantifies client count. Lying misleads priority and
  erodes the field's credibility. If the truth is "one-off (large client)", write it.
- **"I'll write the implementation so they just build it — saves a round trip."**
  → Reality: you are the FDE, not the product owner. Your evidence shapes the spec;
  the product team owns the design. A wrong implementation costs more than a right outcome.
- **"Too many client requests; I'll archive now and assetize later."**
  → Reality: "later" never comes. Archive-as-completion turns feedback into a
  suggestion box nobody reads — distill at the same time you archive.

</common_mistakes>

## TOP errors <!--a:top-->

1. Client names in evidence
2. Implementation written instead of result
3. Inflated priority (non-blocking marked P0)
4. Lying in the `pattern` field (one-off written as recurring)
5. No `fde_hours_per_deployment` — impact unquantified
6. Reusable pattern with no linked asset proposal (archived but never assetized)

## Pre-delivery checklist <!--a:checklist-->

- [ ] No client name, industry, or contract value
- [ ] Title outcome-oriented, not implementation
- [ ] Generality and `pattern` honestly quantified
- [ ] `impact` complete with all four fields, including asset leverage
- [ ] Priority proportionate to evidence
- [ ] Back-linked to source debug artifact (`ISS-*` sources)
- [ ] Reusable/platform gaps have a linked asset proposal and are distilled into 09