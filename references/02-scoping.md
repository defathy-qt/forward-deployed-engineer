# Scoping — Define the Result, Boundaries & Responsibility

**Goal:** Turn a validated problem into an executable, acceptable one-phase contract:
who uses it, what changes, by how much, what is explicitly not done, who owns what,
and when to stop. Vague scope is the root cause of most AI delivery failures.

> Input: the problem statement and baseline from `01-discovery.md`. Feeds into:
> `03-integration-architecture.md` and the acceptance criteria of `04-evaluation.md`.

## Inputs & outputs

| | |
|---|---|
| Inputs | Problem statement, quantified baseline, stakeholder map from `01-discovery` |
| Outputs | `SCP-<client>-vN` scope contract (changes after freeze re-open this file); opportunity-scoring record |
| Feeds into | `03-integration-architecture.md`; acceptance criteria for `04-evaluation.md` |

## Step 1: Score the opportunity on three dimensions <!--a:step1-->

Before contracting anything, confirm this opportunity is *worth* contracting. Score
each candidate 1–5 on three dimensions; **multiply, don't add** — a zero on any axis
is a veto.

| Dimension | Question to answer |
|---|---|
| **Business value** | Is the baseline big enough? Is it in the executive top-5? Does it touch revenue, risk, or compliance? |
| **Technical feasibility** | Is data available and clean today? Can the thinnest end-to-end slice work in 1–2 weeks? |
| **Responsibility risk** | Is there a named owner? Who answers if AI errs? Are actions reversible? |

| Decision | Condition |
|---|---|
| **Do now** | high value, feasible, owner named |
| **Fix then do** | value exists but data / owner / condition missing |
| **Don't pursue** | value too small, conditions fail, or no one accepts the risk |

## Step 2: Name the first user and the real entry point <!--a:step2-->

The system must land where work already happens — not a back office nobody opens. Write
the **first user** and **existing entry point** in one line.

```text
First user:   <who actually does the task>
Entry point:  <the IM / dashboard / system they already use>
```

## Step 3: Write the business result (baseline → target) <!--a:step3-->

Replace "improve efficiency" with a measurable delta over the `01-discovery` baseline.

```text
Before: <baseline number from discovery>
Target: <measurable after-state>
Proof:  <how the after-state will be observed, not asserted>
```

A target you can't measure is a wish, not a result.

## Step 4: Draw the boundaries and the fence <!--a:step4-->

| Boundary | Meaning | Example |
|---|---|---|
| **In (this round)** | what this phase must deliver | "answer course-fact questions in Feishu" |
| **Not now** | real but deferred, not this phase | "image replies, other courses" |
| **Never auto-commit** | what the system may never decide alone | "price, refunds, entitlements, authorization" |
| **Fenced actions** | write-backs / scheduling / purchasing / external promises — all forbidden unless re-authorized | "no ERP write-back, no purchasing, no promises to customers (human only)" |

"Never auto-commit" items go to a human *by design*, not as an exception path.

## Step 5: Assign responsibility and risk <!--a:step5-->

| Role | Responsibility |
|---|---|
| Business / knowledge owner | keep source facts current and correct |
| Engineering / system owner | run the system, fix faults |
| Frontline manager / users | use, flag wrong or overstepping answers |
| Decision / sponsor | approve scope expansion and residual risk |

A task may have many R/A/C/I — but the **Accountable** role must always be unambiguous.
The contract also names: **business owner** (owns the outcome, by name), **technical
owner** (owns running, by name), **risk acceptor**, **stop conditions** (numeric
triggers), **escalation path** (who, with what SLA). "IT leads; business knows about
it" is not ownership.

## Step 6: Define acceptance criteria <!--a:step6-->

| Acceptance axis | Question |
|---|---|
| Input | which real questions / data count as the test set |
| Output | what a correct answer must contain |
| Boundary | what must route to a human / never auto-commit |
| User | which real users accept (not the developers themselves) |

## Step 7: Lock stop, narrow and revert conditions <!--a:step7-->

Decide in advance when to stop, narrow, or revert — so you can stop without a fight later.

```text
Stop if:   <value not confirmed / data not obtainable / risk not acceptable>
Narrow if: <a key assumption fails but direction still holds>
Revert if: <the problem itself is gone or reshaped>
```

## Step 8: Cut the minimal end-to-end loop <!--a:step8-->

Scope can be narrow, but it must run one real chain from entry to result — not a row
of side-by-side demos.

```text
First user:   <only these participants>
Entry point:  <only this existing workflow position>
Data:         <only these sources>
Actions:      <only these permitted moves>
Cycle:        <how long it runs to earn a verdict>
```

## Step 9: Price the ROI as a hypothesis <!--a:step9-->

Expected benefit is a claim to be validated, not money already banked.

| Side | Content |
|---|---|
| Expected benefit | baseline→target delta, valued |
| Full cost | build + run + migration / change cost |
| Conclusion | worth doing / adjust scope / don't start |

## Step 10: Freeze the scope contract <!--a:step10-->

Land steps 1–9 into `SCP-<client>-vN` (fields in `templates/scope-contract.md`):
outcome boundary, scope boundary (including the explicit out-list), responsibility
boundary, and open assumptions for the PoC. Business and technical owners sign. **When
new facts appear after freeze, re-open this file and state what changed — never widen
silently.**

## Templates / artifacts <!--a:template-->

- `templates/scope-contract.md` — scope contract (outcome / scope / responsibility boundaries)
- Artifact ID: `SCP-<client>-vN`

**Gate note:** every open assumption must be explicitly falsified or confirmed in
`04-evaluation.md`. Signing a contract without scoring the opportunity, or leaving
acceptance in the developers' hands, means scope is not yet frozen.

<correct_patterns>

### Good result + closed loop

```text
Before:  sales wait 2–4 h per technical question (discovery baseline)
Target:  <1 h end-to-end, 7×24 available, in the existing Feishu entry
Proof:   median time-to-answer over 4 weeks, from chat logs
Slice:   one course, text answers only, 3 sales users, 2-week pilot
```

**Why it's good:** every line is measurable; the loop is one real chain, not stacked
demos; "never auto-commit" (price/refunds) is a designed-in human branch.

### Good scope contract (excerpt)

```
Result: in-fence order-type handling time 38 min → under 10 min
Baseline: 1,200 orders/month from 2026-06 ticket export; Owner: ops manager Li
Not this phase: auto re-scheduling, supplier messaging, finance orders
Fenced: no ERP write-back, no purchasing, no promises to customers (human only)
Stop: 2 consecutive eval rounds with error rate >5% → pause
Business owner: Wang (Ops); Technical owner: Zhao (IT); Risk acceptor: Ops Director
```

**Why it's good:** exclusions and fence are explicit, stop condition is numeric, every
responsibility is a named person — the next module can design inside a clear fence.

### Good boundaries

> "In: course-fact Q&A in Feishu. Not now: image replies, marketing KB. Never
> auto-commit: price, refunds, entitlements, authorization."

**Why it's good:** three clear boundaries mean future scope creep is a negotiation
against a written contract, not a surprise.

</correct_patterns>

<common_mistakes>

### Mistake: vague result

```text
Target: "make sales more efficient"
```

**Why it's bad:** unmeasurable, therefore unacceptable, therefore unfundable. Replace
with a baseline→target delta and one evidence source.

### Mistake: no non-goals

> "Scope: build a knowledge base."

**Why it's bad:** without "not now" and "never auto-commit", the project absorbs every
adjacent feature — and eventually auto-answers a commercial commitment it had no
business making.

### Mistake: demo-shaped "MVP"

> "MVP: deliver knowledge base + reports + image replies + multi-course support."

**Why it's bad:** that's a row of disconnected horizontal demos. A real MVP is one
vertical chain: one user, one entry, one data source, one result.

### Mistake: scope without exclusions or stop conditions

```
"Phase 1 covers order processing; edge cases come later."
```

**Why it's bad:** a scope that never says "not doing" expands without limit; a phase
without a stop condition can't be terminated on evidence. Write the out-list and a
numeric stop threshold.

### Mistake: no business owner

```
"IT leads; the business side knows about it."
```

**Why it's bad:** "knowing" is not owning. Without a business owner who accepts
residual risk and pushes the team to change how they work, nobody uses the system
after launch.

### Rationalizations to reject

- **"Cast the scope wider so the client feels more value."**
  → Reality: over-wide scope is what kills AI projects. A complete minimal loop beats
  a wide broken coverage; hold the fence, then expand.
- **"The client is a big institution; just let the system execute freely."**
  → Reality: a model's "reasonable answer" is not authorization. "Never auto-commit"
  and fence go to humans by design; an ungated auto-action is one business incident.

</common_mistakes>

## TOP errors <!--a:top-->

1. Result written as a feeling ("more efficient") instead of baseline→target
2. "MVP" = several demos with no closed loop
3. No "never auto-commit" boundary, no fence → the system makes commercial promises or dangerous write-backs
4. Acceptance decided by developers, not business users
5. No named business owner / risk acceptor
6. ROI treated as realized gain rather than hypothesis
7. Signing a contract without the three-dimensional opportunity score
8. Entering design without recording the gate decision

## Pre-delivery checklist <!--a:checklist-->

- [ ] Opportunity scored on value × feasibility × responsibility, decision recorded
- [ ] One first user + one existing entry point named
- [ ] Result is a measurable baseline→target with an evidence source
- [ ] Three boundaries written (in / not now / never auto-commit) + fenced actions listed
- [ ] Accountable unambiguous for every task; business owner and risk acceptor named
- [ ] Acceptance criteria owned by business users
- [ ] Stop + narrow + revert conditions defined (numeric)
- [ ] One real end-to-end loop cut (not stacked demos)
- [ ] ROI priced as hypothesis (benefit vs full cost)
- [ ] Scope contract frozen and signed, open assumptions listed