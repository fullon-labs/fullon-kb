---
title: Get started with DAO governance and POWER
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# Get started with DAO governance and POWER

## Connect and check

1. Enter through [official DAO Gov](https://daogov.flon.network/). On mobile, use the DApp opened in HuFu where supported. In an ordinary browser, follow the current connection flow; QR/callback availability depends on the version.
2. Verify network and full chain ID, then connect the right account. Do not mix mainnet/testnet sessions; recheck after network/account changes.
3. Read governance power, locked node-voting principal, pending allocations, proposal phase, and current rules. Viewing data does not require sending private keys to the site.
4. Before signing, review contract, action, parameters, and authority. Save the transaction ID and wait for [irreversibility](../06_User_Guides/transaction-status.md).

## FLON versus POWER

FLON is the token used for locking and asset operations. POWER is the internal `dao.gov` governance ledger. `powers` stores account power, `global.total_power` aggregates it, and `checkpoints` records changes. POWER cannot be transferred, spent, or traded. Proposing, endorsing, and voting do not consume POWER, although transaction gas may still be required.

System source calls `setpower` when node-voting principal increases/decreases, recording power corresponding to the target principal. Pending BP allocation activation and the DAO snapshot taken by `activate` are different events. “Next epoch” does not describe every governance update.

Users cannot mint POWER for themselves. `setpower` requires the configured `power_source`. Newly acquired power does not retroactively increase power in an already activated proposal.

## Next steps

- Choose nodes: [BP voting and rewards](bp-voting-rewards.md).
- Participate in a proposal: [proposal lifecycle](proposals.md).
- Request community funding: [Treasury](treasury.md).
- Disabled controls or zero power: [troubleshoot](troubleshooting.md). Check network, current power, and snapshot first rather than paying again or broadening permissions.

## Sources and scope

[Sources, snapshots, and discrepancies](sources.md). Implementation descriptions use the listed revisions; live configuration must be read from the target network.
