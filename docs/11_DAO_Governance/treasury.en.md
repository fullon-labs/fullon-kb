---
title: Treasury assets, grants, and payments
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# Treasury assets, grants, and payments

Proposal approval, budget reservation, and payment are different outcomes. Check proposal, grant, token contract/precision, recipient, amount, payment count, and expiry before payment.

## Lifecycle and accounting

| Operation | Meaning | Accounting / asset change |
| --- | --- | --- |
| setasset | Governance-authorized asset configuration | Enables contract/full symbol; does not issue a token |
| Incoming transfer notification | Accept an enabled asset | liquid and total_received increase |
| reserve | Create a grant linked to proposal_id | reserved increases; liquid unchanged; no external payment |
| pay | Pay an installment | liquid/reserved decrease; paid/total_paid increase; transfer to recorded recipient |
| release | Release all unpaid remaining reservation | reserved decreases; liquid unchanged; grant becomes released; no external payment |
| closegrant | Close a still-open expired grant | Release remaining reservation and mark expired; not a generic close action for completed grants |

New reservable balance is `liquid - reserved`. Do not add liquid and reserved as total assets or interpret reserved as paid. Grant remaining amount is `total - paid - released`.

A grant proposal_id is a reference, not approval evidence by itself. Reviewed reserve only requires a positive ID and does not query proposal approval across contracts. Audit the originating governance execution transaction.

## Checks

1. Verify enabled Treasury assets by token contract and precision. Do not attempt deposits for an unenabled asset.
2. A budget proposal should specify beneficiary, purpose, total, maximum payments, expiry, and evidence hash.
3. After approved reserve execution, record grant_id. The beneficiary has not been paid yet.
4. Each pay needs valid governance authorization and must satisfy remaining budget, count, and expiry. Knowing grant_id does not permit arbitrary withdrawals.
5. Verify transfer traces, grant paid, payment records, balances, and irreversibility.
6. Release unused budget under governance authority. Anyone may close a still-open expired grant to release the remainder. Expired grants cannot pay.

The [mainnet snapshot](rules-and-parameters.md) has an empty Treasury asset table. Governance allowlisting of reserve/pay does not establish available assets or budgets. Re-read current state.

## Sources and scope

[Sources, snapshots, and discrepancies](sources.md). Implementation descriptions use the listed revisions; live configuration must be read from the target network.
