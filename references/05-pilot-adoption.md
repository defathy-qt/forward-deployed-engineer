# Controlled Pilot & Organizational Adoption

**Goal:** Advance the evaluation-passing PoC to real users inside a tight fence; grant
autonomy only as fast as the evidence supports; end with a system that is operated,
owned, and actually used. **Going live is a technical event; adoption is the delivery.**

> A system that runs but nobody uses is a failed deliverable no matter how reliable it
> is. Pilots need boundaries, autonomy needs evidence, launch needs gates, adoption
> needs design, and handover needs written accountability.

## Inputs & outputs

| | |
|---|---|
| Inputs | `EVAL-<client>-vN` eval report (residual risks), `SCP-<client>-vN` scope contract, `arch-<client-slug>-<YYYYMMDD>.md` architecture and `ADR-*` |
| Outputs | `PLT-<client>-vN` pilot plan, `UAT-<client>-vN` acceptance record, `PM-<client>-vN` adoption-metric snapshot, handover record (incl. Land & Expand seeds) |
| Feeds into | `06-deployment-runbook.md` (production deploy), `09-retro-assets.md` (retro & asset feedback), `08-product-feedback.md` (systemic gaps) |

## Step 1: Design the Pilot fence <!--a:step1-->

Pilot is not a bigger demo — it is real users doing real work. The fence must decide
explicitly on six axes — **limited users, limited scenarios, limited data, limited
actions, limited time, success evidence** (FDE-02's six boundaries) — and add a circuit
breaker plus daily review on top (FDE-01's four axes):

```markdown
# Pilot Plan: <Client> — <Outcome> v<N>   (template: `templates/pilot-plan.md`)
- Limited users:   <named cohort, e.g., 6 operators on one shift; who is excluded>
- Limited scenarios:<which tasks are in/out; commercial-promise tasks explicitly out>
- Limited data:    <which channels/sources/windows; what never enters>
- Limited actions: <advice only / human confirm; list the write-backs allowed in-fence>
- Limited time:    <start/end, review checkpoints, max window before the decision>
- Success metrics: <business + safety metrics, thresholds inherited from evaluation;
                    also state "what evidence permits expansion">
- Circuit breaker: <who flips the kill switch; what they fall back to>
- Daily review:    <what to read each morning: takeover log, unsafe actions,
                    refusal cases, SLO>
```

Every residual risk from the eval report (`04-evaluation.md`) maps to a fence constraint
or a daily-review item — unproven gaps must be closed, not waved through.

## Step 2: Train by role <!--a:step2-->

One system, different people, different ways of learning to trust it. Give each role its
own script and make them practice — no slide decks:

| Role | What they must learn |
|---|---|
| Manager | metrics, risks, autonomy decisions (when to promote / narrow / stop) |
| Domain expert | review, correct, carry professional risk |
| Frontline user | entry point, applicable tasks, reading evidence/citations, when to hand off to a human |
| Operations | monitoring, incident handling, rollback path |

Users who never learned how to take over either trust blindly or refuse blindly — both destroy the value ledger.

## Step 3: Build the feedback loop <!--a:step3-->

Every production miss becomes a labeled sample routed to the right owner — knowledge or
system — instead of a silent annoyance:

```text
Feedback entry:   <inside the existing entry point, one click>
Failure labels:  <wrong evidence / wrong conclusion / wrong context / unsafe action /
                  needs multimodality / ...>
Routing:         <knowledge gap → knowledge owner; systemic defect → engineering>
Response SLA:    <who turns it around and writes back a fix sample within what time>
```

Routing and structure details live in `08-product-feedback.md`; fixed samples are
authenticated and stored permanently (`07-client-debug.md`) and trigger a Golden Set
regression (`04-evaluation.md`).

## Step 4: Grant autonomy matching evidence <!--a:step4-->

Grant autonomy level by level. **Every promotion needs stronger evidence, tighter
human control, steadier reliability guarantees, and a named accountable person.**
Autonomy follows evidence, not enthusiasm:

| Level | The system may… | Evidence required before promotion |
|---|---|---|
| **L0 Shadow** | observe only; humans do all the work, system logs "what it would have done" | evaluation pass conditions met; Golden Set frozen |
| **L1 Assist** | suggest; a human decides and executes every action | suggestion precision targets met in the observation window; unsafe suggestions = 0 |
| **L2 Limited auto** | execute low-risk in-fence actions; everything else human-confirm | UAT passed; SLO + alerts live; rollback rehearsed; written Owner sign-off |
| **L3 Full auto (in-fence)** | run within the fence without per-action confirmation | L2 ran stable for the agreed period; fault injection passed; audit verified; named risk acceptor |

At every level, **high-risk / low-confidence / boundary cases route to a human** — a
model's "reasonable answer" is not authorization. L3 never silently crosses the fence:
expanding scope = the new scope restarts from L1.

## Step 5: Run the business UAT <!--a:step5-->

UAT is done by **business users on their own real tasks**, not the FDE clicking through
a happy path (template: `templates/uat-checklist.md`, per the acceptance criteria agreed
in `02-scoping.md`):

- Scripted tasks cover normal, anomaly, and refusal/escalation paths.
- Users must be able to see the evidence/citations and know how to take over.
- Record per task: pass/fail, time, confidence, and every verbal objection.
- UAT conclusion is signed in writing by the business Owner, listing known limitations.

```text
User task: <real goal>
Steps:     <what the user actually does>
Expected:  <what a correct result looks like>
Sign-off:  <named owner, date>
```

## Step 6: Production launch gates <!--a:step6-->

Each item below is **evidence, not a claim**; missing one blocks launch:

| Gate | Required evidence |
|---|---|
| Evaluation | frozen Golden Set meets thresholds; regression clean |
| Fence | scope/action limits enforced in configuration |
| Autonomy | approved level matches Step 4 evidence, signed |
| Observability | metrics/logs/traces/audit live; alerts proven to fire |
| Reliability | five fault-injection classes passed (see `06-deployment-runbook.md`); degradation path known |
| Rollback | manual rollback rehearsed; covers migration and flags |
| Security | permissions, audit retention, data-boundary checks signed |
| Accountability | business & technical Owners, on-call named in writing |

## Step 7: Measure adoption, drive adoption <!--a:step7-->

**Measure behavior first; talk value later.** Adoption describes behavior, not login counts:

| Metric | Answers |
|---|---|
| Usage | do they actually use it? |
| Task completion | does it complete the intended work? |
| Direct acceptance | is the output accepted unmodified? |
| Human intervention | how much still needs a person? |

Push adoption deliberately — a system nobody uses is shelfware:

| Adoption lever | Concrete action |
|---|---|
| Role-based training | see Step 2; run another round at launch |
| Embedded in workflow | opens inside the existing tool, not a separate website |
| Embedded in incentives | usage/acceptance quality enters team KPIs; "use it or not" fails |
| Feedback channel | one obvious "wrong answer" entry; response SLA (Step 3) |
| Seed users | a seed user per shift/group coaches peers |
| Usage metrics | weekly four-metric + business-metric snapshot `PM-<client>-vN` |

## Step 8: Handover & Land & Expand <!--a:step8-->

Complete a formal handover before the FDE exits (a farewell email transfers no accountability):

1. **Knowledge:** runbooks, ADRs, known limitations, escalation tree.
2. **Operations:** on-call rotation, dashboards, alert ownership, credentials (written into the `06-deployment-runbook.md` runbook).
3. **Accountability:** business Owner (content & outcome) + technical/system Owner (running & on-call) + escalation path (who to page, in what order) — all signed.
4. **Expansion seeds:** record the next two candidate workflows with their baseline numbers — in-fence usage data is the expansion evidence.
5. **Asset hand-back:** reusable parts into `09-retro-assets.md`; systemic gaps into `08-product-feedback.md`.

## Step 9: Four-exit decision at pilot end <!--a:gate-->

When the pilot window ends or any stop condition fires, decide with the same four-exit
vocabulary as evaluation and record the evidence (see `04-evaluation.md` Step 7):

| Exit | Condition | Next step |
|---|---|---|
| **Continue** | gates all passed, adoption metrics met, residual risk acceptable | expand to a bigger fence / next round; L3 only as evidence accrues |
| **Narrow** | value holds but only in a smaller scope / low-risk fence | shrink roles/scenarios/actions and keep running |
| **Revise** | direction holds, one layer's evidence failed | fix that layer back in 04/05 and re-test |
| **Stop** | adoption fails or value is falsified | record the evidence, hand to retro 09, do not keep pushing |

```markdown
# Four-exit decision record: <Client> — <Pilot name> <date>
- Exit: <continue / narrow / revise / stop>
- Basis: <gate evidence, four metrics, residual-risk list, circuit-breaker trip count>
- Risk acceptor: <named>
- Next actions & owners: <who does what by when>
```

## Templates / artifacts <!--a:template-->

- `templates/pilot-plan.md` — pilot fence plan (users/scenarios/data/actions/time/success)
- `templates/uat-checklist.md` — business UAT checklist and sign-off
- `templates/adoption-plan.md` — adoption plan (training/embedding/incentives/seeds/metrics)
- Artifact IDs: `PLT-<client>-vN`, `UAT-<client>-vN`, `PM-<client>-vN`

**Gate note:** no fence, no circuit breaker, no daily review, no business-signed UAT,
no evidence for all eight gates → no entry to `06-deployment-runbook.md`. Going live is
not the end of the project; adoption is.

<correct_patterns>

### Good Pilot fence

```
Users:   graveyard-shift triage group (6); the shift lead is NOT on the auto path
Scenarios:order-exception triage only; price/promises/finance excluded
Data:    domestic orders, order types R-01..R-04, last 90 days
Actions: advice only; no ERP write-back; escalation drafts send only with one human click
Period:  2026-07-21 → 2026-08-04, review every 2 days, hard stop 08-04
Success: uncorrected rate ≥95%, unsafe suggestions = 0, handling time ≤10 min
         → permits expansion to the next shift
Breaker: on-call flips flag pilot_enabled=false; falls back to manual within 1 min
Daily:   read takeover log, refusal cases, SLO dashboard before the 09:30 standup
```

**Why it's good:** every axis named with numbers; success states "what evidence permits
expansion"; the breaker is one action; the daily review names specific materials;
exclusions are as explicit as inclusions.

### Good autonomy decision

> "Promote triage suggestions from L1 to L2 for order types R-01/R-02 only: 10 shadow
> days at 97.4% precision, 0 unsafe suggestions; UAT signed 08-01; SLO alert confirmed
> firing 07-31; rollback rehearsed 08-02; ops director accepts residual risk in writing.
> R-03/R-04 stay at L1."

**Why it's good:** promotes per case type, cites dated evidence item by item, and keeps
the weaker-evidence scope at a lower level instead of promoting everything at once.

### Good six-boundary pilot (FDE-02 view)

```text
Users:    3 named sales reps
Scenarios:course-fact questions only; commercial promises excluded
Data:     one course corpus
Actions:  read-and-answer only; no write-back, no external send
Cycle:    2 weeks; success = median time-to-answer < 1h AND ≥ 1 real use/day
```

**Why it's good:** every boundary is a decision; "no write-back / no commercial
promises" protects the business while the system earns trust.

### Good adoption snapshot

> "Week 2: 3/3 sales reps using daily; 80% of answers accepted unmodified; 2 escalations,
> both commercial-promise type (correctly handed to a human). Green light: expand to 10."

**Why it's good:** behavioral metrics, not logins; the escalation record proves the
boundary works in the right direction.

</correct_patterns>

<common_mistakes>

### Mistake: Pilot treated as a big demo

```
"Let everyone run it for two weeks and see."
```

**Why it's bad:** no fence, no breaker, no daily review — when it fails it explodes at
full load in front of real customers, with no evidence chain to learn from. Usage
habits, knowledge errors, permission bugs, and system faults all amplify simultaneously.

### Mistake: launch to the whole team at once

```text
Pilot: "Roll the whole team out and see."
```

**Why it's bad:** a full rollout makes failure sources impossible to isolate. A bounded
pilot is what lets you tell "knowledge error" from "permission bug" from "system fault."

### Mistake: autonomy granted faster than evidence

```
"UAT looked great, just let it write back to the ERP."
```

**Why it's bad:** skipping L0/L1/L2 evidence, rollback rehearsal, and written risk
acceptance. One wrong write-back destroys more trust than a month of correct
suggestions builds. Autonomy follows evidence, not enthusiasm.

### Mistake: high-risk action without human review

> "Let the Agent decide and execute refunds itself, faster."

**Why it's bad:** a model's "reasonable answer" is not authorization. High-risk actions
need human review and an audit chain (see `03-integration-architecture.md`); one mistake
becomes one business incident. At every level, high-risk routes to a human.

### Mistake: going live treated as the end of the project

```
"Deploy Friday; FDE exits Monday."
```

**Why it's bad:** without training, workflow embedding, incentives, seed users, and
weekly usage review, the system quietly becomes shelfware. Adoption work starts at launch.

### Mistake: "adopted" = "entry point exists"

> "The entry point is live and everyone has access, so it's adopted."

**Why it's bad:** an existing entry point is not a used one. Measure usage, completion,
acceptance, and intervention before claiming adoption.

### Rationalizations to reject

- **"Pilot users will eventually cover everyone anyway; no need for a fence."**
  → Reality: an unfenced pilot turns every unknown failure into a production incident.
  The fence is the device that lets you learn fast without burning trust.
- **"Users will figure it out; formal training is overhead."**
  → Reality: users who never learned to take over either trust blindly or refuse
  blindly. Training is part of the deliverable.
- **"Handover is just a wrap-up email."**
  → Reality: a wrap-up email transfers no accountability. Written dual-owner
  acceptance, a live on-call path, and rehearsed operations are what handover means.
  If nobody owns knowledge and the system after launch, adoption doesn't hold.
- **"Nobody's using the pilot because everyone's busy; let's wait."**
  → Reality: adoption isn't waited into existence, it's designed — embedded in the
  workflow, embedded in incentives, seeded with users. All three are required.

</common_mistakes>

## TOP errors <!--a:top-->

1. Pilot without a fence / one-click breaker / daily review (or pilot = "roll everyone out")
2. Autonomy promoted faster than evidence; high-risk actions without human review
3. UAT run by the FDE instead of business users
4. Launch gates based on claims, not evidence
5. Feedback with no owner → misses become noise
6. Adoption measured by "has access / entry exists" instead of "is used / is accepted"
7. No role-based training, no adoption plan
8. FDE exits before written accountability handover (no long-term owner)
9. No expansion seeds with baselines; no asset/feedback hand-back

## Pre-delivery checklist <!--a:checklist-->

- [ ] Pilot fence explicit on six axes (users/scenarios/data/actions/time/success), with breaker and daily review
- [ ] Every eval residual risk mapped to a fence constraint or review item
- [ ] Role-based training delivered (manager/expert/frontline/ops)
- [ ] Feedback loop with labels and routing in place, with response SLA
- [ ] Autonomy matches accumulated evidence; scope expansion resets levels; high-risk/low-confidence/boundary → human
- [ ] UAT run by business users covering normal/anomaly/refusal paths, signed in writing
- [ ] Evidence for all eight launch gates
- [ ] Four adoption metrics defined, baselined, and reported weekly as a snapshot
- [ ] Handover covers knowledge, operations, and written accountability; knowledge/system/escalation owners named
- [ ] Expansion seeds with baselines and asset/feedback hand-back recorded; four-exit decision recorded with evidence