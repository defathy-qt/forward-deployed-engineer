# Integration Architecture

**Goal:** A concrete, implementable design — not a slide deck. Every integration
point specifies protocol, auth method, data shape, and failure mode.

## Step 1: Inventory the client landscape

For each relevant system, capture:

| Field | Example |
|---|---|
| System name & version | "Legacy ERP 2019", "Internal CRM v4", "On-prem data warehouse" |
| Deployment model | On-prem / private cloud / SaaS / air-gapped |
| Data it holds | Master records, transaction logs, reference data |
| Integration surface | REST, SOAP, SFTP, ODBC, Kafka, flat file only |
| Auth / network constraints | VPN-only, mTLS, OAuth2 with on-prem IdP, no outbound internet |
| Data volume & cadence | 500K rows/day, real-time vs. nightly batch |
| Client contact / owner | Name, team, escalation path |

## Step 2: Define data flows

For each flow:

```
[Source] → [extraction] → [transport] → [transformation] → [landing]

Protocol:  REST / SFTP / JDBC / Kafka / file-watch
Auth:      OAuth2 client-credentials / username+key / etc.
Schema:    Input columns/types, output columns/types, validation rules
Cadence:   Real-time / hourly batch / EOD file drop
Error:     On failure — retry, DLQ, alert, manual ticket
```

## Step 3: Design the integration layer

Three artifacts:

1. **Network & auth diagram** — components, who talks to whom, open ports, hop-by-hop auth.
2. **Connector list** — one row per connector: type (MCP server / bespoke script / reverse-SSH tunnel / SFTP watcher), language, effort (S/M/L), reusability (can it be productized?).
3. **Configuration surface** — what the client admin configures post-deploy (env vars, secrets, feature flags, allowlists).

## Step 4: Risk register

| Risk | Mitigation |
|---|---|
| Client schema changes without notice | Version pin + drift detection alert |
| On-prem scheduled downtime | Graceful degradation; queue-and-replay |
| Security review blocks deployment | Pre-emptive questionnaire, review doc ready |
| Latency from air-gapped relay | Benchmark early; SLA in writing |

## Step 5: Output document

```markdown
# Integration Architecture: <Client> — <Date>

## 1. Executive Summary (3 sentences)
## 2. Client System Inventory
## 3. Data Flow Diagrams (ascii or mermaid)
## 4. Connector Specifications
## 5. Auth & Network Design
## 6. Configuration Surface
## 7. Risk Register
## 8. Implementation Phasing (wave 1 / 2 / future)
## 9. Open Questions (for client review)
```

**Do not start building** — this module produces the design. Implementation starts
after client and internal stakeholder sign-off.

<correct_patterns>

### Good data flow specification

```
[WMS (on-prem, Oracle 19c)] → [nightly export job → CSV on SFTP] → [platform SFTP watcher] → [parse + validate] → [inventory_snapshots table]

Protocol:  SFTP (ssh-key auth, port 2222, client-side IP allowlist required)
Auth:      ED25519 keypair; client rotates annually, notifies 7 days ahead
Schema:    18 columns (sku, qty_on_hand, qty_reserved, location_code, ...)
           Validation: sku matches ^[A-Z]{3}\d{6}$; qty_on_hand >= 0
Cadence:   Nightly 02:00 client-local; file lands by 02:30; platform processes by 03:00
Error:     File missing by 03:00 → alert on-call; do NOT re-run client job unilaterally
```

**Why good:** every field concrete (port 2222, ED25519, 02:00 client-local);
failure mode says what NOT to do (protects client); error path is actionable.

### Good connector row

| Field | Value |
|---|---|
| Name | `sftp-inventory-watcher` |
| Type | SFTP watcher (platform-native) |
| Language | Config only (no code) |
| Effort | S (2h) |
| Reusability | High — parameterize for any SFTP CSV drop |

**Why good:** reusability scored honestly (this one IS productizable), effort
is sized, type is specific enough to scope the work.

</correct_patterns>

<common_mistakes>

### WRONG: Vague data flow

```
"Inventory data will be transferred via SFTP. Auth will be configured by the client.
Errors will be handled appropriately."
```

**Why bad:** no protocol specifics, no auth detail, no failure semantics.
An operator cannot execute this.

### WRONG: Placeholder auth

```
Auth: <TBD with client security team>
```

**Why bad:** TBD is not a design. Either propose a concrete default (e.g.,
"ED25519 keypair, client provides public key") or list 2-3 options with tradeoffs.
TBD ships in the signed-off doc and becomes "the approved design."

### Rationalizations to reject

- **"We'll figure out auth during implementation — the client's security team will
  tell us."**
  → Reality: auth constraints reshape the whole architecture. A late-breaking "no
  outbound internet" constraint invalidates your connector choice. Pin it in Step 1.
- **"The client said the schema is stable, so we don't need drift detection."**
  → Reality: client assertions about their own systems are untrusted data. Drift
  detection is cheap insurance; client memory of "we never change it" is not.

</common_mistakes>

## TOP errors

1. Data flow with placeholder auth (`<TBD>`)
2. Connector list without reusability score
3. Risk register with no mitigation (just the risk)
4. Architecture doc that says "errors handled appropriately"
5. No open-questions section — assumptions baked in as facts

## Pre-delivery checklist

- [ ] Every data flow has protocol + auth + schema + cadence + error
- [ ] Every connector has type + language + effort + reusability
- [ ] Risk register pairs each risk with a mitigation
- [ ] No `<TBD>` / `<fill-me>` without a concrete default alongside
- [ ] Open questions section lists what you don't know
