# Integration Architecture

**Goal:** A concrete, implementable design, not a slide deck. Every integration point
specifies protocol, auth, data shape, and failure mode; every choice that affects
evaluation or operations becomes an ADR; the design rests on a **stable business
model** so the Agent works against real objects instead of reading raw tables.

> This module turns the `02-scoping.md` loop into a buildable plan and feeds
> `04-evaluation.md` and `06-deployment-runbook.md`.

## Inputs & outputs

| | |
|---|---|
| Inputs | `SCP-<client>-vN` scope contract, discovery baseline, client system and org information |
| Outputs | `arch-<client-slug>-<YYYYMMDD>.md` architecture document; `ADR-NNNN-<slug>.md`; connector list (with reusability scoring) |
| Feeds into | `04-evaluation.md` (PoC vertical slice), `06-deployment-runbook.md` (deployment inputs) |

## Step 1: Inventory systems AND organization <!--a:step1-->

Record, for every relevant system:

| Field | Example |
|---|---|
| System name & version | "Legacy ERP 2019", "Internal CRM v4", "On-prem data warehouse" |
| Deployment model | on-prem / private cloud / SaaS / isolated network |
| Data it holds | master data, transaction logs, reference data |
| Integration surface | REST, SOAP, SFTP, ODBC, Kafka, flat-file only |
| Auth / network constraints | VPN-only, mTLS, OAuth2 with on-prem IdP, no outbound internet |
| Data volume & cadence | 500K rows/day, real-time vs nightly batch |
| Data quality & owner | completeness, freshness, who fixes dirty data, SLA |
| Client contact / owner | name, team, escalation path |

Systems alone aren't enough — the FDE must inherit the **organization** too: an
unfindable approver or undocumented offline workaround is the most common cause of
Pilot slippage.

| Organization fact | Why it matters |
|---|---|
| Change decision chain | who approves connectors, firewall ports, accounts separately |
| Real process vs paper process | where work leaves the system (Excel, group chat, private notes) |
| Ops ownership & on-call | who operates after launch, who gets paged at 3 AM |
| Change / freeze windows | month-end, audit, network-lock periods that block deploys |
| Procurement & security-review cycles | how long allowlists, licenses, pen-tests actually take |

## Step 2: Define data flows <!--a:step2-->

For each flow, specify:

```
[Source system] → [extraction] → [transport] → [transformation] → [landing]

Protocol:  REST / SFTP / JDBC / Kafka / file-watch
Auth:      OAuth2 client-credentials / username+key / etc.
Schema:    input columns/types, output columns/types, validation rules
Cadence:   real-time / hourly batch / EOD file drop
Error:     on failure — retry, DLQ, alert, manual ticket
```

## Step 3: Design the integration layer with an anti-corruption layer <!--a:step3-->

Produce three artifacts:

1. **Network & auth diagram** — components, what talks to what, open ports, per-hop auth.
2. **Connector list** — one row per connector: type (MCP server / bespoke script /
   reverse-SSH tunnel / SFTP watcher), language, effort (S/M/L), reusability
   (one-off / parameterizable / productizable — scored honestly).
3. **Configuration surface** — what the client admin must configure post-deploy
   (env vars, secrets, feature flags, allowlists).

Put an **anti-corruption layer** around every external system: adapt its protocol and
vocabulary to a stable internal interface so swapping a vendor never ripples into the
Agent and workflows.

Mark which connectors belong to the PoC's **minimal end-to-end slice** — don't build
the whole integration graph before the slice's assumptions are proven.

## Step 4: Model the business world (lightweight ontology layer) <!--a:step4-->

Don't make the Agent guess database fields. Define a stable business model —
objects, relations, actions, rules, permissions — and map every external field onto it.

| Element | Question | Example (order-fulfillment manufacturing) |
|---|---|---|
| Objects | Which entities exist? | orders, plants, lines, materials, stock, customers, owners |
| Relations | How do they connect? | order→material→line; batch→stock location |
| Actions | Who may do what? | propose transfer, adjust schedule, notify plant |
| Rules | Which deterministic constraints hold? | substitute materials must pass QA; over-limit → escalate |
| Permissions | Who can view / execute / write back? | planner proposes; owner approves; system account writes ERP |

The ontology organizes the business world but doesn't replace rules, workflows,
Agents, people, or source systems — it connects them.

## Step 5: Harden identity, authorization and audit <!--a:step5-->

"Can call the tool" ≠ "authorized to perform the action." Every high-risk action must
know who, why, and be traceable.

| Layer | Question | Control |
|---|---|---|
| Identity | who/what is calling (user or service)? | SSO, service accounts, tenant isolation |
| Authorization | what may this identity do? | least privilege, RBAC/ABAC, tool allowlist |
| Human auth gate | which actions need a person? | state-changing tools go through approval / two-person review |
| Audit | how is it traceable and non-repudiable? | tamper-evident logs: who→identity→rationale→tool+params→state→result |

Threats that must be explicitly mitigated: direct/indirect prompt injection, tool
privilege escalation, data exfiltration, retrieval-content poisoning. Read-only tools
stay read-only; state-changing tools always go through an auth gate.

## Step 6: Record architecture decisions (ADR) <!--a:step6-->

Any choice that is expensive to reverse, or affects evaluation/security/operations,
gets a one-page ADR before implementation:

```markdown
# ADR-NNNN: <decision title>
- Status: proposed | accepted | superseded by ADR-xxxx
- Context: <constraints that forced the choice, with evidence>
- Options: <A / B / C, one-line tradeoff each>
- Decision: <what we chose>
- Consequences: <what gets easier, what is locked in, what we can no longer do>
- Verification link: <which PoC/eval result or test confirmed it>
```

## Step 7: Risk register <!--a:step7-->

| Risk | Mitigation |
|---|---|
| Client schema changes without notice | schema-version pin + drift detection alert |
| On-prem system has scheduled downtime | graceful degradation; queue-and-replay |
| Security review blocks deployment | pre-emptive questionnaire and review doc |
| Air-gapped relay latency | benchmark early; agree SLA in writing |
| Ontology model wrong on real data | validate with 2+ real cases before full rollout |
| Org change leaves no approver | named approver + backup; lock cycle in advance |

## Step 8: Produce the document <!--a:step8-->

```markdown
# Integration Architecture: <Client> — <Date>

## 1. Executive Summary (3 sentences)
## 2. Client System & Organization Inventory
## 3. Data Flow Diagrams (ascii/mermaid) + anti-corruption boundaries
## 4. Connector Specifications (with reusability score and PoC-slice marking)
## 5. Business Ontology (object / relation / action / rule / permission)
## 6. Identity, Authorization & Audit Design
## 7. Auth & Network Design
## 8. Configuration Surface
## 9. ADR Index
## 10. Risk Register
## 11. Implementation Phasing (PoC slice / wave 1 / wave 2 / future)
## 12. Open Questions (for client review)
```

**Do not start building** — this module produces design only. Implementation starts
after client and internal stakeholders sign off, and the first thing built is the PoC
vertical slice.

## Templates / artifacts <!--a:template-->

- `templates/adr.md` — one-page ADR
- Artifact IDs: `arch-<client-slug>-<YYYYMMDD>.md`, `ADR-NNNN-<slug>.md`

**Gate note:** only proceed to `04-evaluation.md` when data-flow pentad, org inventory,
ontology, auth/audit chain, ADRs, and risk mitigations are complete and the PoC slice
is marked. Never design connectors for systems you haven't inventoried.

<correct_patterns>

### Good data-flow spec

```
[WMS (on-prem, Oracle 19c)] → [nightly export job → CSV on SFTP] → [platform SFTP watcher] → [parse + validate] → [inventory_snapshots table]

Protocol:  SFTP (ssh-key auth, port 2222, client-side IP allowlist required)
Auth:      ED25519 keypair; client rotates annually, notifies 7 days ahead
Schema:    18 columns (sku, qty_on_hand, qty_reserved, location_code, ...)
           Validation: sku matches ^[A-Z]{3}\d{6}$; qty_on_hand >= 0
Cadence:   Nightly 02:00 client-local; file lands by 02:30; platform processes by 03:00
Error:     File missing by 03:00 → alert on-call; do NOT re-run client job unilaterally
```

**Why it's good:** every field is concrete (port 2222, ED25519, 02:00 client-local);
the failure mode says what NOT to do (protecting the client); the error path is executable.

### Good connector row

| Field | Value |
|---|---|
| Name | `sftp-inventory-watcher` |
| Type | SFTP watcher (platform-native) |
| Language | config only (no code) |
| Effort | S (2h) |
| Reusability | productizable — parameterizable for any scheduled SFTP CSV drop |

**Why it's good:** reusability scored honestly (this one genuinely is productizable),
effort quantified, type specific enough to estimate from.

### Good ontology fragment

| Element | Entry |
|---|---|
| Object | `order`, `material`, `line`, `stock` |
| Relation | `order requires material`; `batch located_at location` |
| Action | `propose_stock_transfer` (planner) → `approve` (owner) |
| Rule | substitute materials must have `passed_qa == true` |
| Permission | system write-back only via `sys-erp` account, with audit |

**Why it's good:** the Agent stops guessing raw columns and works on governed objects;
every change has an owner and a rule, so "deterministic result" survives at runtime.

### Good ADR

```markdown
# ADR-0007: Parse client exports with "locked schema + drift alert", not lenient parsing
- Status: accepted
- Context: client WMS added a column unannounced (see ISS-atlas-20260629-01)
- Options: A) lenient adaptive (fragile, silent data loss) B) locked schema + alert
- Decision: B; strict parse against pinned v2; column-count change blocks load and alerts
- Consequences: new columns require coordinated migration; silent corruption impossible
- Verification: Golden Set GS-014/GS-027 pass; fault injection FI-03
```

**Why it's good:** makes a seemingly-reversible choice explicit, records the tradeoff
and the evidence behind it, and links the decision to eval results.

</correct_patterns>

<common_mistakes>

### Mistake: vague data flow

```
"Inventory data will be transferred via SFTP. Auth will be configured by the client.
Errors will be handled appropriately."
```

**Why it's bad:** no protocol detail, no auth detail, no failure semantics. Ops can't execute it.

### Mistake: placeholder auth

```
Auth: <TBD with client security team>
```

**Why it's bad:** TBD is not a design. Give a concrete default (e.g. "ED25519 keypair,
client provides public key") or 2–3 options with tradeoffs. A TBD ships with the
architecture doc and becomes "the approved design."

### Mistake: Agent reading raw tables

> "Let the Agent query the ERP tables directly — fewer hops."

**Why it's bad:** the Agent inherits every vendor's field names, encodings and
inconsistencies and breaks when schemas change. Map external fields onto the stable
business model and let the Agent operate it behind the anti-corruption layer.

### Rationalizations to reject

- **"We'll sort auth at implementation time; the client security team will tell us."**
  → Reality: auth constraints reshape the whole architecture. A late "no internet"
  constraint invalidates your connector choices. Lock it in Step 1.
- **"The client says the schema is stable; no drift detection needed."**
  → Reality: the client's assertion about its own systems is untrusted data. Drift
  detection is cheap insurance; "we never change anything" is a memory, not evidence.
- **"Org-process issues aren't engineering; skip them in the design."**
  → Reality: unfindable approvers and unrecorded offline workarounds are the most
  common cause of Pilot slippage. The organization is part of the architecture.

</common_mistakes>

## TOP errors <!--a:top-->

1. Placeholder auth (`<TBD>`) in data flows
2. No business ontology — Agent pointed directly at raw tables
3. Connector reusability scores missing or dishonest
4. Risk register without mitigations (risks only)
5. Architecture doc says "errors handled appropriately"
6. Missing org inventory (approvers, real process, ops ownership, freeze windows)
7. State-changing tools without a human auth gate / audit
8. Expensive decisions without an ADR
9. Building the full integration graph before the PoC slice is proven
10. No open-questions section — assumptions treated as facts

## Pre-delivery checklist <!--a:checklist-->

- [ ] Every data flow has the pentad (protocol + auth + schema + cadence + error)
- [ ] Every connector has the four fields (type + language + effort + reusability)
- [ ] Org inventory covers approvers, real process, ops, freeze windows
- [ ] Anti-corruption layer and ontology defined (object/relation/action/rule/permission)
- [ ] Identity→authorization→human-auth-gate→audit chain designed; state changes always gated
- [ ] PoC-slice connectors marked; later phases explicitly deferred
- [ ] High-cost / security-affecting choices have an ADR with evidence
- [ ] Every risk has a mitigation
- [ ] No `<TBD>` / `<fill-me>` without a concrete default
- [ ] Open questions list the unknowns