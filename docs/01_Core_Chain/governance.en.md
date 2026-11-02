---
title: Governance power and BP eligibility
status: active
updated: 2026-11-02
source: whitepaper v2.5.0 clarification draft
---

# Governance power and BP eligibility

This page summarizes protocol design in the whitepaper v2.5.0 clarification draft (2026-11-02); it does not certify deployment on any network.

## DAO proposals and governance power

The lifecycle is draft → endorsement → voting → finalization → timelock → execution. Protocol parameters, treasury allocations and contract-control actions must be auditable; high-risk execution is allowlisted and subject to longer timelocks.

FLON locked for BP voting is recorded as equal governance power in the account’s internal contract ledger. Governance power is not a separately issued token: it cannot be transferred, spent or traded and does not create equity, dividend or fixed-return rights. Reducing or withdrawing voting principal updates available governance power; activated proposals retain their frozen power snapshots without issuing or burning another token.

BP elections and DAO proposals share locking infrastructure but use distinct actions, thresholds and execution paths. The whitepaper allows up to 30 BP selections per account, dividing power equally rather than multiplying total votes.

## Node roles

| Role | Responsibility / qualification | Reward design |
| --- | --- | --- |
| Ordinary sync/RPC node | Validation, synchronization or application service; no automatic production seat | No automatic BP reward |
| Active BP | Active schedule and production/performance eligibility | Qualified mining plus Active GAS rewards, with permitted voter sharing |
| Standby BP | Online proof and promotion readiness | Standby GAS availability rewards; no fixed mining share |

The target is 21 Active and 30 Standby BPs. Bootstrapping may expand Active membership within 3–21. Self-stake, public information, valid keys and performance determine eligibility alongside ranking. Running the program or ranking highly does not itself establish production eligibility.

## Epochs, performance and recovery

- Proposed reward epoch: six hours, or 43,200 half-second slots. This is slot accounting, not an assumption that every dynamically produced block takes half a second.
- Votes take effect for the next ranking epoch. Historical snapshots determine reward ownership; later claims do not change it.
- The whitepaper describes zero rewards and suspension below 90% availability, with network-wide incident protection considered before individual penalties.
- After cooldown, the BP must authorize `resumeprod` and enter probation; 12 consecutive assigned missed slots during probation can trigger suspension again.
- Repeated cooldowns are 1, 2, 4 and 8 epochs: 6, 12, 24 and 48 hours at the proposed epoch length.
- Ordinary downtime first affects rewards and eligibility. Principal slashing is reserved for objectively verifiable safety violations. Verify actual deployed rules and governance parameters.

No unverified registration amount, lock duration or production command is supplied here. Check current contracts, schedules, parameters and permissions before acting.

[Launching nodes](../10_Developer_Guides/nodes.md) · [Mining and GAS rewards](tokenomics.md)

## Sources

[English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/d695da53f4e453dd0e372e9dc5a605a0c56d455e/fullon.whitepaper.md) · [Chinese whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/d695da53f4e453dd0e372e9dc5a605a0c56d455e/fullon.whitepaper.cn.md) · [Scope and source conflicts](whitepaper.md). Pinned revision `d695da53f4e453dd0e372e9dc5a605a0c56d455e`; retrieved 2026-11-02. The clarification awaits upstream merge and is not a deployment certification.
