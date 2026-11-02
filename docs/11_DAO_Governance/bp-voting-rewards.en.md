---
title: BP voting, principal, and rewards
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# BP voting, principal, and rewards

DAO proposal votes and BP votes are separate. BP allocation determines node selection and reward attribution; formal DAO weight comes from a proposal snapshot.

## Lock and allocate

1. Check account, network, available FLON, locked principal, and pending votes.
2. Increasing principal involves real asset operations such as `flon::addvote`. Confirm amount, authority, and current rules. Displayed liquid balance is not automatically locked voting principal.
3. Choose up to 30 BPs and assign amounts. Source `votealloc` requires positive allocations, unique/sorted BPs, and a total **equal to** the account's current target locked principal. The DApp should construct a valid list.
4. After signing, check pending state and activation epoch rather than repeatedly submitting because rankings have not updated immediately.
5. After the target epoch, verify effective allocation and reward attribution. Registered active eligibility, interface Active/Standby rankings, and the actual production schedule are distinct.

## Reduce principal and exit

Reducing voting principal, changing BP allocation, collecting a vote refund, and withdrawing BP self-stake are different operations. Source `subvote` creates a refund subject to election/existing-refund restrictions. `voterefund` waits for maturity. Deselecting a BP does not imply an immediate refund.

Do not confuse vote-refund timing with BP self-stake `unstake_delay_sec`. Read the target contract/current record. An activated proposal's formal voting power remains its snapshot despite later principal reductions.

## Claim rewards

| Beneficiary | Action | Authorization / recipient |
| --- | --- | --- |
| Voter | `voter.reward::claimrewards` | Beneficiary authorizes; check current ABI |
| BP | `flon::claimrewards(caller, producer, max_steps)` | BP or third party triggers; payment stays with producer |

Rewards become on-chain claim records rather than automatic airdrops and may accumulate across epochs. This is not a fixed-return promise. Confirm irreversible claims and verify claim rows/balances. Missing data or RPC failure is not evidence of zero rewards.

A public Keeper assists BP reward claims; it cannot submit a Standby proof without BP authorization. See [operations](operations.md).

## Sources and scope

[Sources, snapshots, and discrepancies](sources.md). Implementation descriptions use the listed revisions; live configuration must be read from the target network.
