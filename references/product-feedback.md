# Product Feedback

**Goal:** Make feedback **evaluable** — a product manager reads it and decides
priority without asking for clarification.

## Step 1: Pattern recognition

Before writing up a single client's request, check:

1. Has another client reported this? Search past debug artifacts, deployment notes, feedback entries.
2. Is it a symptom of a deeper gap? ("client wants custom report X" may actually be "reporting module lacks configurability")
3. Is it a true product gap, or can existing features solve it with better docs/config?

If #3 is "existing features solve it," stop — file a documentation or configuration
improvement instead.

## Step 2: De-identify and generalize

Strip client-specific identifiers (names, industries, contract values, dates). Then
generalize:

| Client-specific (DO NOT INCLUDE) | Generalized (INCLUDE) |
|---|---|
| "Acme Corp needs a SOAP connector to their legacy ERP" | "Connector framework for legacy on-prem systems exposing SOAP" |
| "Client X's compliance team wants a custom checklist" | "Compliance rules engine needs configurable checklists per jurisdiction" |
| "Client Y's month-end close takes 3 days" | "Month-end close workflow needs parallelization and incremental processing" |

## Step 3: Impact assessment

| Dimension | How to assess |
|---|---|
| **Client count** | 1 / 2-3 / 4+ / "every new deployment" |
| **Deal impact** | Blocking renewal / Required for RFP / Differentiator / Nice-to-have |
| **Workaround cost** | FDE hours consumed per deployment in absence |
| **Strategic fit** | yes / partial / tangential |

## Step 4: Feedback entry

```json
{
  "feedback_id": "FB-<YYYY>-<NNN>",
  "title": "one-line, outcome-oriented",
  "source": ["ISS-...", "deployment notes for Client Y", "FDE retro"],
  "pattern": "one-off | recurring (N clients) | universal (every deployment)",
  "current_state": "the gap, in product terms",
  "desired_outcome": "outcome, not implementation",
  "evidence": [
    "Client A: ... (de-identified)",
    "Client B: ... (de-identified)"
  ],
  "proposed_scope": "feature / API / config surface / docs",
  "impact": {
    "affected_clients": "1 | 2-3 | 4+ | every-deployment",
    "deal_impact": "blocking | required-for-rfp | differentiator | qol",
    "fde_hours_per_deployment": "estimated hours saved"
  },
  "priority_recommendation": "p0-critical | p1-high | p2-medium | p3-nice-to-have",
  "related_feedback": ["FB-2026-042"],
  "attachments": ["ISS-..."]
}
```

## Step 5: Link and file

- Came from a debug artifact? Link back to the issue ID.
- Multiple entries describing the same gap? Merge, note related IDs.
- File where the product team consumes feedback (backlog, Linear, Jira).

<correct_patterns>

### Good feedback entry (excerpt)

```json
{
  "feedback_id": "FB-2026-042",
  "title": "Drift detection for SFTP connectors should be on by default",
  "source": ["ISS-atlas-20260629-01", "ISS-beta-20260418-02", "FDE retro 2026-06"],
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
    "fde_hours_per_deployment": "3-5h per deployment troubleshooting drift"
  },
  "priority_recommendation": "p1-high",
  "related_feedback": []
}
```

**Why good:**
- Title is outcome-oriented ("drift detection on by default"), not "add a flag."
- `pattern` quantified honestly (3 clients in 6 months, with sources).
- Evidence de-identified — three concrete instances without naming clients.
- `desired_outcome` describes the result, not the API shape.
- Impact concrete (3-5h per deployment) — the PM can size the ROI.
- Priority honest (P1, not P0 — not blocking a deal, but real recurring cost).

### Good de-identification

| Raw (DO NOT FILE) | De-identified (FILE) |
|---|---|
| "Acme Corp's WMS added lot_expiry_date on 2026-06-26" | "Client A: unannounced column addition (date withheld)" |
| "Bank ABC's compliance team wants a custom KYC checklist" | "Client B: compliance team needs configurable checklists" |

**Why good:** strips name + industry + date, keeps the technical shape. The product
team can act on the de-identified form without knowing which client.

</correct_patterns>

<common_mistakes>

### WRONG: Naming the client

```
"evidence": ["Acme Corp's WMS added a column on 2026-06-26..."]
```

**Why bad:** violates de-identification. Internal artifacts get forwarded to PMs,
execs, sometimes external slides. Once a client name is in writing, it spreads.

### WRONG: Writing the implementation

```
"proposed_scope": "Add a `drift_detection_enabled` boolean to the SFTP connector config, default true, with a `drift_alert_threshold` int field..."
```

**Why bad:** this prescribes the API shape. The product team may have a better design
(event-driven, not a boolean). Describe the outcome ("drift detection on by default"),
not the implementation.

### WRONG: Inflating priority

```
"priority_recommendation": "p0-critical"
```
on a quality-of-life improvement.

**Why bad:** trains the product team to ignore your priorities. When a real P0 lands
(data loss, security), it's drowned in fake P0s.

### WRONG: Lying on `pattern`

```
"pattern": "recurring (N clients)"
```
when only one client has reported it, but it's a big client.

**Why bad:** `pattern` quantifies breadth. Lying here misroutes prioritization. Say
"one-off (large client, high ARR)" if that's the truth — that's still useful signal.

### Rationalizations to reject

- **"I'll mark it P0 so they actually look at it."**
  → Reality: cry-wolf P0s train the team to ignore you. When a real P0 lands, it's
  drowned. Use P1-high for "important but not blocking" — it's still seen.
- **"It's only one client, but it's a big client, so I'll say 'recurring'."**
  → Reality: pattern field quantifies how many clients. Lying here misroutes
  prioritization and erodes trust in the field. Say "one-off (large client)" if
  that's the truth.
- **"I'll describe the implementation so they can just build it — saves a round trip."**
  → Reality: you're an FDE, not the product owner. Your evidence shapes the spec; the
  product team owns the design. An implementation that's wrong wastes more time than
  an outcome that's right.

</common_mistakes>

## TOP errors

1. Client name in evidence
2. Implementation prescribed instead of outcome
3. Priority inflated (P0 for non-blocking)
4. `pattern` field lied ("recurring" for one-off)
5. No `fde_hours_per_deployment` — impact unquantified

## Pre-delivery checklist

- [ ] No client names, industries, or contract values
- [ ] Title is outcome-oriented, not implementation
- [ ] `pattern` quantified honestly
- [ ] `impact` has all three fields
- [ ] Priority honest relative to evidence
- [ ] Linked back to source debug artifact
