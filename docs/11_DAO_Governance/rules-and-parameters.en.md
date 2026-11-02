---
title: Governance rules, risk thresholds, and mainnet snapshot
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# Governance rules, risk thresholds, and mainnet snapshot

## Three passing conditions

```text
S = snapshot_total_power
F = for_votes
N = against_votes
B = abstain_votes

(F + N + B) * 10000 >= S * quorum_bps
F + N > 0
F * 10000 >= (F + N) * approval_bps
F * 10000 >= S * min_support_bps
```

Quorum measures participation. Approval measures For votes among decisive votes. Absolute support measures For votes against total snapshot power. Abstention counts toward quorum but not the approval denominator. 100 basis points = 1%. Integer cross-multiplication, not rounded interface percentages, determines the result.

Illustrative example: S = 100,000, quorum 25%, approval 67%, absolute support 15%. For 20,000, Against 8,000, Abstain 2,000 passes all three. For 10,000, Against 0, Abstain 15,000 has 25% participation and 100% decisive approval but fails because absolute support is only 10%. This is not a live network configuration.

## Mainnet read-only snapshot, 2026-11-02

The application's published configuration and RPC both reported chain ID:

`d4019d7d8633a337973408c6c00e5c4888933ad1b6ce10edddea8145317d8d12`

Observed heads were **14,966,774 / 14,966,778**, with head times **09:19:31.500 / 09:20:13.500 UTC**. Calls were independent, not an atomic single-block snapshot or a node-liveness audit. Values can change after publication. Full responses and deployed code hashes are in the [snapshot JSON](mainnet-snapshot.json).

- Total power: 2,100,000 POWER at precision 8; `powers` had one row, `flonian`.
- Proposals were empty; bootstrap administration was enabled. One power-bearing account cannot satisfy the minimum of three distinct endorsers; enabled allowlists do not establish fully open community governance.
- L1–L4 risk rules were enabled, with five enabled action policies and five execution allowlist entries.
- Treasury assets were empty. Allowlisting is not proof of enabled assets or withdrawable funds.

### Risk thresholds

Amounts are POWER; counts are distinct endorser accounts, not verified distinct people.

| Level | Minimum network total | Proposer | Individual endorser | Minimum count | Aggregate endorsement | Quorum | Approval | Absolute support |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| L1 | 100,000 | 1,000 | 1,000 | 3 | 1% | 5% | 50.01% | 1% |
| L2 | 500,000 | 5,000 | 5,000 | 5 | 2% | 15% | 60% | 8% |
| L3 | 1,000,000 | 10,000 | 10,000 | 7 | 5% | 25% | 67% | 15% |
| L4 | 2,000,000 | 21,000 | 21,000 | 9 | 10% | 40% | 75% | 30% |

Minimum network power is not an amount the proposer must hold alone. Count and aggregate endorsement conditions must also pass. Multi-action proposals use the highest risk; activation uses the higher of creation-time and current risk.

### Phase duration in seconds

| Level | Endorsement | Voting delay | Voting | Timelock | Execution grace |
| --- | ---: | ---: | ---: | ---: | ---: |
| L1 | 86400 | 43200 | 259200 | 86400 | 604800 |
| L2 | 172800 | 86400 | 432000 | 172800 | 604800 |
| L3 | 259200 | 172800 | 604800 | 259200 | 864000 |
| L4 | 604800 | 259200 | 864000 | 604800 | 1209600 |

86,400 seconds = 1 day; 43,200 = 12 hours. Base config had proposer/individual endorsement thresholds of 1,000 POWER and a minimum of three endorsers. Limits were 10 actions, 4,096 bytes each, and 16,384 bytes total. Read risk rules and proposal snapshots as well as base config for effective requirements.

### Enabled execution scope

| Action | Risk | Authorization | Per-action byte limit |
| --- | --- | --- | ---: |
| `dao.treasury::reserve` | L3 | `dao.gov@active` | 128 |
| `dao.treasury::pay` | L3 | `dao.gov@active` | 320 |
| `dao.treasury::release` | L3 | `dao.gov@active` | 288 |
| `flon::setgasrwcfg` | L3 | `flon@dao` | 16 |
| `dao.treasury::closegrant` | L1 | `dao.gov@active` | 16 |

The snapshot did **not** allowlist `flon::setbpquorum`, `flon::setbpstake`, `dao.gov::setconfig`, `dao.gov::setallow`, or `dao.treasury::setasset`. Do not apply old testnet allowed-action lists to mainnet.

## Snapshot and implementation boundaries

- Formal votes use POWER checkpoints at activation; subsequent power changes do not alter those votes.
- Reviewed source accumulates power at endorsement time and does not recompute each existing endorser at activation. Aggregate endorsement power can differ from activation-time current balances; not all endorsements use the formal voting snapshot.
- Queue and execute revalidate allowlists; disabling an action can affect approved but unexecuted proposals.
- `setriskcfg` and `setactrisk` require `flon` and cannot be allowlisted for ordinary DAO execution. `setpower` requires power_source.
- Bootstrap `sealadmin` permanently closes administration, rather than pausing it. These guides explain it without execution instructions.

Some thresholds and the empty-allowlist statement in the historical mainnet draft differ from this snapshot and are not republished as current values.

## Sources and scope

[Sources, snapshots, and discrepancies](sources.md). Implementation descriptions use the listed revisions; live configuration must be read from the target network.
