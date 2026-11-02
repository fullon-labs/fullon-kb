---
title: FLON tokenomics and BP rewards
status: active
updated: 2026-11-02
source: whitepaper v2.4.0 synthesis
---

# FLON tokenomics and BP rewards

This page summarizes protocol design in whitepaper v2.4.0 (2026-10-22); it does not certify deployment on any network.

## Supply and allocation

The whitepaper sets total FLON supply at **10 billion (10,000,000,000)**. These are allocation plans, not measurements of current issuance, unlocking or circulation.

| Category | Share | Planned FLON | Vesting description |
| --- | ---: | ---: | --- |
| Team and contributors | 20% | 2,000,000,000 | 18-month cliff, 5-year linear vesting; confirm the contractual start/overlap rules |
| Community airdrop | 12% | 1,200,000,000 | 1.2% × 10 years; individual releases involve designated DID and one-year vesting |
| Seed investors | 10% | 1,000,000,000 | 18-month cliff, 5-year linear vesting |
| Private sale | 15% | 1,500,000,000 | 18-month cliff and 4-year vesting after investment |
| BP mining | 5% | 500,000,000 | Fixed budget and reward-block halving curve |
| Strategic partners | 18% | 1,800,000,000 | Conditional, agreement-specific releases |
| Foundation | 20% | 2,000,000,000 | Table lists TGE and later 10-year vesting portions; percentage denominator needs clarification |
| Total | 100% | 10,000,000,000 | Not all necessarily circulating |

The foundation row lists “10%” at TGE and “10%” later, without clearly identifying the denominator. Do not convert these into unlocked token amounts without clarification. Confirm the TGE date, cliff/vesting overlap, deployed vesting contracts and recipient accounts separately; mainnet launch does not establish the TGE date.

## Fixed mining budget

- Budget: `500,000,000 FLON`. Only producing, performance-qualified Active BPs qualify for mining; Standby BPs have no fixed mining allocation.
- Each period contains `315,360,000` eligible reward blocks. The first three period budgets are 250,000,000, 125,000,000 and 62,500,000 FLON.
- The first period's theoretical average is approximately `0.7927447996 FLON` per reward block. Integer-unit remainders are distributed deterministically and constrained by the remaining budget.
- Downtime does not advance the reward-block counter. A period is not a guaranteed number of calendar years.
- The mining section prohibits DAO increases to the cap, counter resets and new mining issuance after exhaustion. Its wording conflicts with the later inflation paragraph; see [source conflicts](whitepaper.md).

## GAS rewards are separate

The proposed initial GAS-linked split is 10% for BP rewards and 90% DAO-locked. The BP GAS pool is split 80% Active / 20% eligible Standby, equivalent to 8% / 2% of the total. These are not verified live ratios.

Active allocation follows qualified actual production; Standby eligibility requires online proofs and readiness. Unallocated shares and integer remainders move to the DAO ledger. This pool does not increase or replace the 500-million-FLON mining budget; ELON reserve obligations still apply.

BP reward sharing may benefit voters under permitted ratios, historical epoch snapshots and performance rules. Delaying claims does not change settled ownership. Rewards can be zero and are not fixed returns.

## FLON, ELON and GLON

FLON is the native asset; ELON is the smallest GAS/reserve accounting unit; GLON is non-transferable governance power associated with FLON locked for BP voting. GLON is not a tradable investment or dividend claim.

Use `get_currency_stats` for deployed supply, max_supply and issuer, and inspect vesting contracts for unlock status. Allocation, maximum supply, issued supply, circulation and protocol-locked balances are distinct.

[Resources](resource-model.md) · [Governance](governance.md) · [Issuing a token](../10_Developer_Guides/issue-tokens.md)

## Sources

[English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.md) · [Chinese whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.cn.md) · [Scope and source conflicts](whitepaper.md). Pinned revision `f49e5f0f821162a997260535be30767e3f147d8e`; retrieved 2026-11-02.
