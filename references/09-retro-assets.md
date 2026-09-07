# Retro & Asset Reuse (1→N)

**Goal:** At the end of every delivery, leave behind assets the *next client* can
inherit — turning one-off field work into diminishing marginal cost. If the second
client costs as much to deploy as the first, the FDE loop hasn't closed. **Leaving
behind only a system is outsourcing; leaving behind reusable assets is FDE practice.**

> Take away industry understanding, never client data — "accounting standards are
> public; ledgers are private." Client #1 builds the asset; client N configures it.

## Inputs & outputs

| | |
|---|---|
| Inputs | this delivery's full set of artifacts (scope contract, architecture, evaluation, runbook, debug artifacts, feedback entries), deployment metrics |
| Outputs | `RETRO-<vertical>-<YYYYMMDD>` retro artifact, `AM-<domain>-vN.yaml` asset manifest, migration checklist, runbook lessons, leverage trend |
| Feeds into | next client delivery (asset reuse), `08-product-feedback.md` (platform gaps), `04-evaluation.md` (reused test sets folded into the Golden Set) |

## Step 1: Compare promise vs delivered <!--a:step1-->

Go back to the baseline in `02-scoping.md` and record what actually happened. **Do not
polish the gap — the gap is where the lesson lives.**

| Side | Content |
|---|---|
| Promised | baseline → target from scoping |
| Delivered | measured results in production |
| Gap | what changed and why |

## Step 2: Split the four layers — reusable vs client-specific <!--a:step2-->

Only the reusable half may travel to the next project; split honestly. Take each
deliverable apart into four layers, and only the middle two become assets:

| Layer | Content | Destination |
|---|---|---|
| Stable skeleton | generic flows, interface contracts, control logic | reusable asset |
| Industry constraints | domain rules, terminology, compliance patterns | industry profile / asset config |
| Client config | endpoints, credentials, org-specific values | client config, never extracted |
| Non-transferable | client data, names, contracts, private docs | destroyed or left on-site |

**Client data never enters assets:**

- No client names, people, identifiers, contract values, or real records in assets.
- Test data must be synthetic or thoroughly de-identified and re-labeled.
- Credentials and endpoints live in client config, never in an asset package.
- When in doubt, leave it out; a missing sample can be added, a leaked record cannot be recalled.

## Step 3: Six-requirement asset test <!--a:step3-->

A candidate becomes an asset only when all six hold:

| Requirement | Question |
|---|---|
| Clear I/O | an explicit input/output contract? |
| Configurable | are client-specific values externalized to config? |
| Versioned | semantic versioning and a changelog? |
| Tested | Golden Set / unit / fault-injection tests included? |
| Bounded | `applies_when` and `does_not_apply` scenarios stated? |
| Owned | a maintainer accountable for changes and problems? |

## Step 4: Choose the asset type <!--a:step4-->

| Asset type | Example | Reuse signal |
|---|---|---|
| Connector | SFTP watcher, SOAP bridge, MCP server | same protocol/interface across clients |
| Agent Skill | triage playbook, evidence-bound reply flow | same workflow across clients |
| Template | scope contract, runbook, eval report | same document shape every delivery |
| Engineering component | drift detector, retry/DLQ, audit log | same control logic needed repeatedly |
| Rule pack | compliance checks, validation regexes | same rules within an industry |
| Reference architecture | air-gapped LLM topology, network-hop design | same deployment shape |
| Delivery playbook | discovery script, UAT script, adoption plan | same people-process every time |

## Step 5: Build a versioned asset package <!--a:step5-->

Package with a manifest so the next FDE knows what they're adopting (template:
`templates/asset-manifest.yaml`, ID: `AM-<domain>-vN.yaml`):

```yaml
asset_id: connector-sftp-watcher
name: SFTP CSV watcher with schema-pin and drift alert
type: connector
version: 1.2.0
semver_note: "major=breaking config; minor=new capability; patch=fix"
inputs: [sftp_endpoint, credentials_ref, schema_contract, schedule]
outputs: [validated_batch, drift_alert]
applies_when: "client drops CSVs on a fixed schedule via SFTP"
does_not_apply: ["streaming/Kafka", "binary formats", "client-push APIs"]
config_surface: [host, port, path, key_ref, schema_version, alert_channel]
tests:
  golden_set: assets/connector-sftp-watcher/golden/
  fault_injection: [missing_file, column_drift, malformed_row, duplicate_batch]
provenance:
  born_in_client: "de-identified delivery #3"
  reused_by: ["delivery #5", "delivery #7"]
owner: fde-platform-team
changelog: "CHANGELOG.md"
```

## Step 6: Measure product leverage <!--a:step6-->

Reuse must be measured, not claimed. The core KPI is *on-site effort per unit of value*
decreasing across projects:

| Metric | Definition |
|---|---|
| Reuse rate | share of a new deployment assembled from existing assets |
| Marginal FDE hours | on-site hours per delivery, trended per engagement |
| Asset coverage | available assets vs asset types actually needed |
| Defect escape | defects found after a reused asset is adopted (should trend down) |
| Product leverage | value delivered ÷ on-site hours invested (should trend up) |

```text
Deployment A: <months / hours to value>
Deployment B (same vertical): <months / hours to value>
Direction:  <should be down; if flat, the loop is not working>
```

If project #10 in the same pattern costs as much as #1, the loop fails the litmus test.

## Step 7: File product feedback for platform gaps <!--a:step7-->

If the engagement exposed a *platform* (not client) gap, route a de-identified,
outcome-oriented entry to `08-product-feedback.md`. The reverse holds too: recurring
feedback shapes distill into `09` assets — the two-way loop.

## Step 8: Write the migration checklist <!--a:step8-->

The startup sheet for the next project:

```text
Reuse as-is:  <entry, agent runtime, permission, reply scaffolding>
Rebuild only: <facts, project/source-rights, media, golden set>
Rewrite rules:<what is different for the new vertical>
```

## Step 9: Update runbook lessons <!--a:step9-->

Anything an incident taught you → write it into the runbook's lessons so the next
operator inherits it. On-site experience nobody writes down is lost to the next project.

## Step 10: Archive the retro artifact <!--a:step10-->

```json
{
  "retro_id": "RETRO-<vertical>-<YYYYMMDD>",
  "promised_vs_delivered": {"baseline": "...", "target": "...", "actual": "..."},
  "reusable_assets": ["skill:...", "connector:...", "template:...", "testset:..."],
  "client_specific_left_behind": ["...", "..."],
  "product_feedback_filed": ["FB-..."],
  "leverage": {"deployments": 2, "effort_trend": "down | flat | up"},
  "migration_checklist": "...",
  "runbook_lessons_added": ["..."]
}
```

## Templates / artifacts <!--a:template-->

- `templates/asset-manifest.yaml` — asset manifest (the Step 5 shape)
- `templates/postmortem.md` — receives severe-incident reviews; lessons flow into Step 9
- Artifact IDs: `AM-<domain>-vN.yaml`, `RETRO-<vertical>-<YYYYMMDD>`

**Gate note:** no baseline comparison, no honest split of client-specific content, no
asset extracted, no leverage trend recorded → the retro is not done. The retro artifact
is a mandatory close-out for every engagement, not an option.

<correct_patterns>

### Good asset split

> "Reuse: Feishu entry, agent runtime, permission scaffolding, reply patterns. Rebuild:
> course facts, project/source-rights, golden set. Left client-side: 3 one-off pricing
> rules."

**Why it's good:** the reusable half is named as assets; the client-specific half stays
behind; no wholesale copy, so the next project doesn't inherit one client's special-case
rules.

### Good leverage record

> "Project A (course Q&A): 6 FDE person-days to first value. Project B (same pattern,
> marketing Q&A): 2 FDE person-days. Reused entry + runtime + eval scaffolding."

**Why it's good:** effort per unit of value went down; that number is the proof the
loop is working.

### Good asset extraction

> "Three clients all drop CSVs on a fixed schedule via SFTP. Extract a parameterized
> `connector-sftp-watcher` (schema contract, schedule, alert channel as config); each
> client's host, key, and column mapping stay in their own config; replace real samples
> with files synthesized against the schema contract."

**Why it's good:** clean separation of skeleton, industry shape, and client config; the
asset is config-driven; test data is synthetic by construction.

### Good manifest (excerpt)

```yaml
asset_id: skill-evidence-bound-triage
version: 0.4.0
applies_when: "operators must reply with citations bound to controlled internal sources"
does_not_apply: ["open-web retrieval", "unfounded numeric forecasting"]
tests: {golden_set: golden/v3, result_floor: 0.85, unsafe_action_floor: 0}
provenance: {born_in_client: "de-identified #2", reused_by: ["#4", "#6", "#9"]}
owner: fde-platform-team
```

**Why it's good:** the boundary (`does_not_apply`) is as explicit as the capability;
tests carry numeric floors; provenance shows real reuse without naming clients; an
owner exists.

</correct_patterns>

<common_mistakes>

### Mistake: copying client customization into an asset / wholesale cloning

```
"Copy Acme's integration directory, rename it, and send it to the next client."
```
```
"Clone the course Q&A and just swap the course name."
```

**Why it's bad:** client endpoints, credentials, schema quirks, one-off rules, and data
all leak into the "asset"; the next deployment inherits unexplainable behavior and
buried compliance risk. Extract the skeleton, rebuild the scenario-specific parts, and
externalize the rest.

### Mistake: asset without owner or boundaries

```
"Make a shared folder; people grab whatever scripts look useful."
```

**Why it's bad:** no versioning, no tests, no applicability notes, no maintainer — it's
a graveyard, not a library. Without an owner and a does-not-apply boundary, assets get
misused in scenarios they were never designed for.

### Mistake: retro as a victory lap

> "Project's done, great job everyone, next."

**Why it's bad:** a retro that records only wins captures no lesson. The gap (Step 1)
and the failures are the most valuable output.

### Mistake: not measuring leverage

> "Don't know if it's getting cheaper — we just deliver."

**Why it's bad:** without an effort/value trend you can't tell FDE practice from premium
outsourcing. The leverage curve is only visible when measured.

### Rationalizations to reject

- **"We'll generalize after a few more clients; copy-paste for now."**
  → Reality: copy-paste compounds divergence; after three copies there is no common
  asset left to generalize. Extract on the second use — that's when the pattern is real.
- **"They're just internal sample files; real data tests more realistically."**
  → Reality: internal folders get shared, screenshotted, used in demos. Whatever the
  intent, real data inside an asset is a data-boundary violation. Use synthetic data.
- **"Tracking reuse metrics is bureaucracy; we know we reuse a lot."**
  → Reality: unmeasured reuse is just a feeling. Marginal hours and reuse rate are the
  only evidence the 1→N loop is actually working.

</common_mistakes>

## TOP errors <!--a:top-->

1. Client config/data copied into a "reusable" asset (wholesale clone with client rules)
2. Asset missing one of the six requirements (especially no owner, no `does_not_apply`)
3. Retro records only wins — no gap, no failure
4. Leverage not measured — can't distinguish FDE from outsourcing
5. No semantic version or changelog
6. Migration checklist unwritten, runbook lessons unupdated → the next project relearns the same failure

## Pre-delivery checklist <!--a:checklist-->

- [ ] Promise vs delivered compared against the baseline
- [ ] Deliverables split into skeleton/industry/client/non-transferable; reusable vs client-specific split honestly
- [ ] Candidate passes the six asset requirements
- [ ] Asset type chosen; manifest has `applies_when`/`does_not_apply`, version, changelog, named owner
- [ ] Tests attached (Golden Set / fault injection) with numeric floors
- [ ] Zero client data; samples all synthetic or de-identified; credentials in client config
- [ ] Leverage (effort-per-value trend) and reuse metrics recorded; provenance de-identified
- [ ] Platform gaps filed to product feedback as outcome-oriented entries
- [ ] Migration checklist written (reuse / rebuild / rewrite)
- [ ] Runbook lessons updated from incidents
- [ ] Retro artifact archived and linked