---
title: Keeper, BP reward claims, and Standby operations
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# Keeper, BP reward claims, and Standby operations

## Verify the deployment before copying operations

The newer DApp operations guide describes bounded `onblock` epoch closure/settlement, with the public Keeper assisting BP reward pull claims rather than driving closeepoch/beginsettle/settlenext/finalizeepoch externally. This is a version-specific responsibility model, not proof that every deployment has upgraded.

**Observed mainnet ABI:** `flon::claimrewards` exists; `standbyproof`, `closeepoch`, `beginsettle`, `settlenext`, and `finalizeepoch` do not. Do not submit absent actions to that deployment. ABI presence alone also does not establish enabled configuration or identical internal algorithms.

## BP reward assistance

1. Read chain ID, head, and LIB; prepare a separate dedicated Keeper caller account.
2. Query BP `unclaimed_rewards` and producer-scoped `prodclaims` / `gasclaims`. Only construct claims for actual pending records.
3. `caller` supplies its authorization; funds remain payable to `producer`, not the third-party trigger.
4. `max_steps` bounds processing. Reviewed source accepts 1–48 and service examples default to 24; these are not permanent universal network limits.
5. Confirm irreversibility and re-read claims/balances. Reconcile ambiguous broadcasts before retrying.

This example broadcasts a write transaction. Use only on an isolated chain or verified testnet after confirming ABI, accounts, dedicated permission, and claimability. It does not deploy a Keeper or enable mainnet broadcasting:

```bash
export FULLON_RPC='http://127.0.0.1:8888'
fucli -u "$FULLON_RPC" get abi flon -f flon.abi
fucli -u "$FULLON_RPC" push action flon claimrewards \
  '{"caller":"keeperacct","producer":"produceracct","max_steps":24}' \
  -p keeperacct@claimer
```

Preconfigure `claimer` linked only to the required action. Start dry-run with protected signing files/services, not repository keys. Separate networks, configuration, data directories, and alerts; avoid uncoordinated broadcasters.

## Standby proofs: supported deployments only

The newer operations guide defines standbyproof as a BP- or explicitly authorized bot-submitted proof. A public reward Keeper cannot submit it without BP authorization. Stop if the target ABI lacks the action and consult that deployment's versioned instructions.

Supported deployments also require checking current GAS epoch, Standby snapshot role, minimum interval, proof count, recent-block window, and canonical block ID. Guide examples use 43,200 slots, 12 proofs, and a 240-block window; **these were not verified as current mainnet settings**. Read that deployment's configuration and implementation.

Do not bypass intervals by sending consecutive proofs or backfill old epochs. Record epoch, referenced block, transaction ID, and irreversibility; outcomes follow the supporting contract. Proof submission and claiming are different tasks. GAS eligibility, BP registration, self-stake, and scheduling are distinct.

## Administrative boundaries

A Keeper should not hold BP production keys or owner/active keys and does not custody rewards. `setpower`, risk/allowlist/asset configuration, and `sealadmin` belong to separate authorization/rollout processes, not routine reward maintenance.

## Sources and scope

[Sources, snapshots, and discrepancies](sources.md). Implementation descriptions use the listed revisions; live configuration must be read from the target network.
