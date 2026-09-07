# Business Discovery — Find the Right Problem

**Goal:** Turn a vague ask ("we want a knowledge base / reconciliation bot") into a
business problem with a quantified baseline, supporting evidence, and a verdict on
whether AI is even needed. Deliver the *problem*, not the *solution*.

> **The client's request is not the problem.** The system or feature the client names
> is usually their *candidate solution* for a problem they haven't articulated. Your
> job is to find that problem. The output of discovery is the input to `02-scoping.md`.

## Inputs & outputs

| | |
|---|---|
| Inputs | Raw client ask, industry profile (`industry/`), interview list (business owner, frontline operators, IT/data owner…) |
| Outputs | `DSC-<client>-<YYYYMMDD>-NN` discovery interview notes; `STM-<client>-NN` stakeholder map; a one-sentence problem statement + quantified baseline + falsifiable hypothesis |
| Feeds into | `02-scoping.md` — turning the problem into a scope contract |

## Step 1: Record the raw ask <!--a:step1-->

Record the client's words verbatim before rewriting. The phrasing is your first clue
about what they think is wrong.

```text
Raw ask (verbatim): ...
Who said it:        <name, role>
Where it surfaced:  <meeting / ticket / "we've been meaning to...">
Presumed solution:  <the feature they think they want>
```

Do not rewrite yet. Do not promise any feature name.

## Step 2: Map stakeholders, find who is actually stuck <!--a:step2-->

Draw the stakeholder map first (`templates/stakeholder-map.md`), then interview along
it. **Batch 3–5 questions per interview**; talk to the people who do the work, not just
the manager who pays for it.

| Role | What you want from them |
|---|---|
| Business owner | Who owns outcome and risk; what "success" is worth |
| Frontline operator | Real workflow, workarounds, waiting and rework |
| Decision maker / budget | Priorities; what would kill the project |
| IT / data owner | Systems, permissions, data quality, change windows |
| Affected parties | Who gets replaced, audited, or escalates to them |

For every claimed pain point ask "who suffers, how often, what happens if we change
nothing" until you can name **one person** and **one moment of pain**:

| Question | Why it matters |
|---|---|
| Who does this today? | The real user, not the budget owner |
| When does it hurt? | A recurring moment, not a calendar slot |
| What do they fall back to? | Workarounds expose the real cost |
| What breaks if they err? | Error consequence → whether AI is allowed |

Record per interview: the current process, pain points **with frequency and cost**,
previous failed fix attempts, and the implicit constraints everyone assumes "everyone
knows." Produce `STM-<client>-NN`.

## Step 3: Reconstruct the As-Is workflow <!--a:step3-->

Record how work happens *today* before drawing any future feature. The bottleneck
lives at *handoffs and waits*, not the last step.

```
Trigger → step → handoff → wait → step → exception path → escalation → result

Per step, capture:
  Owner:       role (named person where possible)
  System:      which system the work actually happens in
  Time:        typical and P95 duration
  Defect:      error / rework / rejection rate
  Wait:        queue and approval delay
  Workaround:  spreadsheets, message nudges, personal notebooks (the truth off the happy path)
```

## Step 4: Cross-validate with multiple sources <!--a:step4-->

One smooth interview is a *clue*, not a fact. Corroborate with records, data, and observation.

| Source | What it can prove |
|---|---|
| Verbal process | What people *say* happens |
| System logs / records | What actually happens (frequency, volume) |
| Business data | Scale, errors, inconsistencies |
| Field observation | Waits, workarounds, exceptions nobody mentions |

A claim only becomes a **confirmed fact** when backed by **2+ independent sources**.

## Step 5: Quantify the business baseline <!--a:step5-->

Record the *before* state so the project can later prove it changed. A baseline is a
measurement, not a narrative. **No baseline, no claim of value.**

| Dimension | Baseline measure | Example |
|---|---|---|
| Volume | scale / frequency | 1,200 anomalous orders per month |
| Time | cycle / wait | 38 min average, 4 h P95; "complex questions 2–4 h" |
| Cost | labor / rework hours | 4.5 FTE on manual matching; "each escalation costs faculty 3 h" |
| Quality | error / rework rate | 11% rejection / rework; "1 in 8 answers wrong or stale" |
| Risk | exposure / incident rate | 3 compliance incidents per quarter; wrong answer triggers refund dispute |
| Behavior | adoption / throughput | sales prefer waiting over answering |

Every number carries a **source** (only a checkable "before" makes "after" checkable).
If a metric cannot be measured today, note it and define how the Pilot will instrument
it (see `05-pilot-adoption.md`).

## Step 6: Separate business problem, technical symptom, solution hypothesis <!--a:step6-->

Never collapse three different things into one sentence:

| Layer | Definition | Example |
|---|---|---|
| **Business problem** | What value the current process loses | Staff wait on materials; answers are inconsistent |
| **Technical symptom** | Observable anomaly in the tool/system | Retrieval recall is unstable; answers don't bind sources |
| **Solution hypothesis** | A change we can still falsify | Controlled retrieval + source-bound answers might cut wait time |

A hypothesis is **not** an established fact; it is exactly what `04-evaluation.md` exists
to test.

## Step 7: Write the problem statement <!--a:step7-->

One sentence, forced into a fixed pattern. If it doesn't fit, you haven't found the problem yet.

```text
<Who> in <what scenario> suffers <what observable loss>
because <what underlying cause>, today costing <baseline number>.
```

## Step 8: Decide whether AI is even needed <!--a:step8-->

A good FDE first proves *what* to do, then proves it needs an Agent.

| If the work is… | Then use… |
|---|---|
| Deterministic, enumerable rules | Rules / conventional software |
| Prediction from historical data | Predictive model |
| Retrieval around documents | RAG (before Agent) |
| Multi-step reasoning + tools + state | Agent workflow |
| High-risk, high-ambiguity, low-frequency | Keep human, add assistance |

If rules or RAG already suffice, forcing an Agent is scope creep, not progress.

## Templates / artifacts <!--a:template-->

- `templates/discovery-interview-guide.md` — batched interview questions and notes skeleton
- `templates/stakeholder-map.md` — stakeholder map
- Artifact IDs: `DSC-<client>-<YYYYMMDD>-NN` (discovery interview notes), `STM-<client>-NN` (stakeholder map)

**Gate note:** only proceed to `02-scoping.md` when the problem is falsifiable, the
baseline is measurable, and key claims have 2+ sources. If repeated interviews show
the problem is unformed or too small, **stop** and record why — cheaper than building
something nobody uses.

<correct_patterns>

### Good problem statement (manufacturing / logistics)

> "Anomalous order handling consumes 4.5 FTE, averages 38 minutes and an 11% reject
> rate, because triage staff manually check 6 systems and answers aren't source-bound.
> Hypothesis: source-bound assisted triage can cut time to under 10 minutes — exactly
> what the PoC must falsify."

**Why it's good:** names the workflow, quantifies the baseline, separates problem from
hypothesis, and states what would falsify the hypothesis.

### Good problem statement (sales / course content)

> "Sales loses deal windows in presales because every technical question waits 2–4
> hours for faculty, costing an estimated N downgrades/churn per month."

**Why it's good:** names who, scenario, observable loss, cause, and a baseline number.
It never says "knowledge base" — that is a solution, deferred to `02-scoping.md`.

### Good baseline

| Dimension | Before | Source |
|---|---|---|
| Time | 2–4 h for complex questions | sales interviews + chat logs |
| Quality | ~1 in 8 answers stale | 30-case faculty audit |

**Why it's good:** every number has a source; "before" is checkable, so "after" can be.

</correct_patterns>

<common_mistakes>

### Mistake: treating a features request as the problem

```
"The client wants a Q&A Agent, so build a Q&A Agent."
```

**Why it's bad:** you've recorded the client's proposed solution, not the problem. No
workflow, no baseline, no falsifiable hypothesis; when adoption fails nobody can
explain why. Discovery ended before it began.

### Mistake: one source treated as fact

> "We confirmed the process with the sales lead."

**Why it's bad:** one interview is a clue. Confident recall is not evidence; system
logs and observed work rarely match anyone's memory.

### Mistake: no baseline

> "It's slow right now; you'll know if it's fixed."

**Why it's bad:** no numbers means you can't price the value or prove the change.
"Faster" is unmeasurable, so delivery can never be accepted.

### Rationalizations to reject

- **"The client already said what they want; more interviews just slow us down."**
  → Reality: whoever requested it is usually not the person doing the work. One round
  with the frontline often overturns the original ask; discovery is the cheapest insurance.
- **"We can't measure the baseline now; estimate after launch."**
  → Reality: without a before-number you can't prove value, tell a renewal story, or
  detect regressions. Instrument no later than Pilot.

</common_mistakes>

## TOP errors <!--a:top-->

1. Treating the named feature ("knowledge base", "Q&A bot") as the problem
2. One interview treated as confirmation (single source = fact)
3. No quantified business baseline ("you'll know it when you see it")
4. Business problem / technical symptom / solution hypothesis collapsed into one sentence
5. Defaulting to "an Agent" before checking rules / RAG
6. Describing the ideal process instead of the as-is process

## Pre-delivery checklist <!--a:checklist-->

- [ ] Raw ask recorded verbatim, unrewritten
- [ ] Stakeholder map done; a real user and a recurring pain moment are named
- [ ] As-is workflow reconstructed with owner, time, defect, wait per step
- [ ] Every key claim supported by 2+ sources
- [ ] Baseline quantified, every number sourced (or Pilot instrumentation defined)
- [ ] Problem / symptom / hypothesis written as three separate statements
- [ ] Problem statement fits the one-sentence template
- [ ] "Should we use AI at all" decision and routing rationale recorded
- [ ] Gate decision (continue / revise / narrow / stop) recorded with rationale