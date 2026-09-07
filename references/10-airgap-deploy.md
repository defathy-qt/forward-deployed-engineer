# Air-Gapped & On-Prem Deployment

**Goal:** Deliver and operate in networks that are **offline by default** — typical for
state-owned enterprises, regulated finance, government, and 信创 (domestic-tech-stack)
environments. Everything a cloud deployment fetches at runtime must instead be
**shipped in the package, verified offline, and patched offline**.

> Air-gap is not "deployment without the internet as usual" — it is treating
> read-only external dependencies as entirely unavailable, and pre-programming every
> runtime fetch into the package. Confirm the isolation level in writing, never by
> assumption.

## Inputs & outputs

| | |
|---|---|
| Inputs | client network topology and isolation level (written confirmation from security/IT), 信创 stack version inventory, `arch-<client-slug>-<YYYYMMDD>.md` architecture, frozen Golden Set and eval results |
| Outputs | offline delivery kit (`kit-<client-slug>-v<N>.tar` with `SHA256SUMS` + signature), signed data-boundary diagram, offline upgrade/patch packages, written acceptance record |
| Feeds into | `06-deployment-runbook.md` (offline runbook variant), `04-evaluation.md` (Golden Set regression in the offline test environment), `07-client-debug.md` (triage process under constrained access) |

## Step 1: Confirm the isolation level <!--a:step1-->

**Never assume; confirm the level in writing with the client's security/IT team.**

| Level | Network reality | Design implication |
|---|---|---|
| Fully air-gapped | no internet at all; physical media / one-way data diode ferry | everything offline; eliminate any callback |
| One-way diode | outbound only through an audited gateway, no inbound | pre-approved outbound allowlist; artifacts signed before entry |
| Controlled egress | access to an allowlisted domain list via proxy | explicit allowlist; everything else blocked |
| Private cloud / VPC | internal cloud, no public endpoints | internal mirror registry, internal IdP, private model endpoint |

## Step 2: Inventory the 信创 stack <!--a:step2-->

Record exact versions; domestic CPUs, OSes, databases, and middleware each carry
compatibility and dialect risk.

| Layer | What to confirm |
|---|---|
| CPU architecture | x86 / ARM / Kunpeng / Hygon / LoongArch; every binary and wheel supported |
| OS | exact Kylin, UOS, openEuler versions and kernels |
| Database | SQL dialect and driver differences for Dameng, KingbaseES, GaussDB, OceanBase |
| Middleware | TongWeb, domestic message queues, internal image registry |
| Model serving | local weights vs VPC API proxy; GPU driver/CUDA compatibility |
| Identity | local LDAP/AD/SSO; no public OAuth |
| Crypto | SM2/SM3/SM4 or GM module certification required |

## Step 3: Build the offline delivery kit <!--a:step3-->

Assemble one immutable, checksummed delivery package; **the client site downloads
nothing**.

| Kit component | Contents |
|---|---|
| App package | app images/binaries, version-pinned |
| Dependency mirror | complete wheels/images/apt-yum sources for the target OS/arch |
| Model artifacts | LLM weights, embedding/rerank/ASR models, version-pinned |
| Runtime | language runtime, container runtime, internal base images |
| License | offline license file, machine-fingerprint binding flow |
| Install script | idempotent offline installer; never touches a network |
| Checksum & signature | SHA256 manifest + signature; verified before install |
| Documentation | offline manual, rollback, contact card (no external links) |

```text
kit-v1.2.0/
├── app/            # app images & binaries
├── mirror/         # complete dependency mirror for target OS+arch
├── models/         # version-pinned model weights
├── runtime/        # language & container runtimes
├── licenses/       # offline licenses
├── install.sh      # idempotent offline installer
├── SHA256SUMS      # checksum manifest
└── SHA256SUMS.sig  # detached signature
```

## Step 4: Design data-boundary controls <!--a:step4-->

Data never leaves the client domain without a signed, explicit path.

| Control | Requirement |
|---|---|
| Data-flow diagram | draw every byte's path; enumerate and remove or approve every external call |
| Callback audit | telemetry, update checks, fonts/CDN, analytics — all disabled or redirected inward |
| Log egress | approved channels only; sensitive fields masked first |
| Model boundary | prompts/embeddings stay local or reach only approved private endpoints |
| Retention & audit | who accessed what, retained per client policy; SM crypto where required |
| Media rules | no real data off-site via laptop/USB; all external use is synthetic data |

## Step 5: Operate under restricted access <!--a:step5-->

- **Bastion only:** all access through an approved jump host; no personal-device SSH; screen-recording audit where required.
- **Log-export process:** export → client-side masking/approval → signed package out; no screen-sharing of real production data in external meetings.
- **Remote-assist limits:** when live remote access is forbidden, work from exported artifacts and written reproduction steps, and state the limitation plainly (see `07-client-debug.md` — if you can't reproduce, say so, don't guess).
- **Time/DNS/CA:** internal NTP, internal DNS, internal CA trust — none may point at public infrastructure.

## Step 6: Offline upgrades, patches & acceptance <!--a:step6-->

1. Assemble the upgrade package exactly as in Step 3, with a version-to-version diff.
2. Land it in the client's **offline test environment** first and run the frozen Golden Set there (see `04-evaluation.md`).
3. Rehearse rollback, covering **model versions and database-dialect migration**.
4. Security patches travel the same signed-package path — **never install by temporarily connecting**.
5. Written acceptance: baseline version, checksums, test results, rollback results.

## Templates / artifacts <!--a:template-->

- Kit structure per Step 3; offline runbook reuses the `06-deployment-runbook.md` skeleton with any online command removed
- Checksum & signature: `SHA256SUMS` + `SHA256SUMS.sig`
- Artifact IDs: `kit-<client-slug>-v<N>.tar`, signed data-boundary diagram

**Gate note:** isolation level not confirmed in writing, 信创 stack not inventoried, kit
not proven on a clean homogeneous VM, callbacks not enumerated, real data potentially
leaving site → no on-site deployment. In an air-gap, "there should be internet" is not a
deployment plan.

<correct_patterns>

### Good offline kit manifest

```
kit-v1.2.0, target Kylin V10 SP3 / Kunpeng ARM64
- app images: 4, all multi-arch, digests recorded
- dependency mirror: 312 wheels, install verified on a clean same-version OS VM
- models: llm-qwen2.5-14b-int4 (sha256 9f3c…), bge-m3, rerank-v3
- install.sh run twice on a clean VM: second run idempotent, zero external packages
  (tcpdump during install saw loopback traffic only)
- SHA256SUMS signed; client security verified the signature before handover
```

**Why it's good:** target OS/arch named; integrity proven on a clean homogeneous VM;
"zero internet" proven by packet capture, not claimed; signature verified client-side.

### Good data-boundary design

> "All inference stays on the GPU cluster in VPC-A; embeddings don't cross VPCs;
> telemetry is redirected inward to the internal monitoring stack with client
> IPs/names masked; the only egress is a signed daily health summary through the
> one-way diode, with fields pre-approved by security. USB exports of production data
> are forbidden; external debugging uses synthetic copies only."

**Why it's good:** every flow has an explicit path; callbacks are redirected inward
rather than "theoretically disabled"; the single egress is named and pre-approved;
external debugging explicitly uses synthetic data only.

</correct_patterns>

<common_mistakes>

### Mistake: assuming `pip install` will work

```
"Run pip install -r requirements.txt on the client server."
```

**Why it's bad:** fails immediately in a full air-gap; worse, partially succeeds under
controlled egress, producing a non-reproducible mixture of vendor and online packages.
The complete mirror must ship with the package and be verified on a clean VM.

### Mistake: taking real client data off-site to debug

```
"I'll copy a few rows of real data to my machine, it reporodences faster."
```

**Why it's bad:** a data-boundary violation whatever the intent, and likely a
contract/compliance breach. Reproduce on-site, or use a synthetic copy generated
against the schema contract (see `09-retro-assets.md`).

### Rationalizations to reject

- **"The client network probably has internet; handle offline later."**
  → Reality: "probably" is not a deployment plan. Confirm the isolation level in
  writing during discovery; the offline kit is not removable scoped-down work.
- **"Telemetry data is small; one external call won't matter."**
  → Reality: in an air-gap audit, one unexplained external connection fails the whole
  acceptance. Redirect telemetry inward and enumerate every call.
- **"Dameng is basically Oracle; the SQL just works."**
  → Reality: dialect and driver differences (pagination, reserved words, boolean
  handling) surface late and break UAT. Every SQL statement must be verified on the
  real database in the offline test environment.

</common_mistakes>

## TOP errors <!--a:top-->

1. Isolation level assumed, not confirmed in writing
2. Runtime still depends on online downloads (pip/npm/image pull) at the client site
3. Domestic CPU/OS/DB compatibility not verified in a homogeneous environment
4. Callback/telemetry/CDN calls not fully enumerated and redirected
5. Real client data exported for external debugging
6. Patches installed via a temporary internet connection instead of the signed offline path
7. Rollback not rehearsed for model versions and database-dialect migration

## Pre-delivery checklist <!--a:checklist-->

- [ ] Isolation level confirmed in writing; outbound paths enumerated
- [ ] 信创 stack versions inventoried (CPU/OS/DB/middleware/crypto)
- [ ] Offline kit complete with checksum and signature, proven on a clean homogeneous VM
- [ ] Install idempotent; packet capture proves zero external packages
- [ ] Data-flow diagram signed; callbacks redirected inward; single egress approved
- [ ] No real data off-site; external debugging uses synthetic copies only
- [ ] Bastion-only access; masked log-export flow defined
- [ ] Upgrade/patch path and rollback rehearsed offline; written acceptance produced