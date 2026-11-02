---
title: Resource model: FLON, GAS and ELON
status: active
updated: 2026-11-02
source: whitepaper v2.4.0 synthesis
---

# Resource model: FLON, GAS and ELON

This page summarizes protocol design in whitepaper v2.4.0 (2026-10-22); it does not certify deployment on any network.

## Resources and units

| Resource | Whitepaper measurement | Example |
| --- | --- | --- |
| CPU | Transaction execution time | Contract computation |
| NET | Transaction size | Signed transaction data |
| RAM | Allocated on-chain state storage | Contract table records |

GAS denotes resource usage rights; ELON is its smallest accounting unit. The design states `1 FLON = 100,000,000 ELON` and `1 ELON = 0.00000001 FLON`. This is an accounting relationship, not a market price or investment claim. Verify deployed symbols and precision.

## Payment and reserves

The resource-model section describes spending existing GAS first and converting account FLON when needed, rather than requiring every standard account to pre-buy GAS manually. CPU/NET spending consumes usage rights; releasing RAM may return or reclaim GAS under protocol rules. Automatic conversion, refunds and failure behavior still require version-specific confirmation. Do not infer fees or record retention for every failed request from the whitepaper alone.

Redeemable ELON liabilities are backed by FLON in `flon.gas`, one smallest FLON unit per new ELON. Reserves cannot be reused while they back redemption liabilities. Consuming GAS retires the corresponding liability; that section says reserve FLON remains locked by default. **GAS consumption therefore does not by itself prove FLON was burned.** The deflation section uses conflicting wording; see the [source conflict record](whitepaper.md).

## Reward and DAO ledgers

- `bp_reward_balance` accounts for BP and voter rewards.
- `dao_locked_balance` remains locked unless approved DAO proposals meet quorum, timelock and execution-allowlist requirements.
- The proposed initial split is 10% / 90%; this is a design recommendation, not a verified live parameter.
- Reconcile each epoch and maintain reserves, in smallest FLON units, at least equal to outstanding redeemable ELON. Backing reserves are not unrestricted spending balances.

## Practical use

Users should check displayed resources and fees before signing, separating system costs from proxy service charges. Developers should query supported resource fields using `get_info`, `get_account` and the target version's definitions. No fixed transfer fee, free registration or return is promised here.

The whitepaper also describes proxy fees, 1,000 free proxy uses and variable EVM-address fees. Availability requires product/network verification; these are not current promotional guarantees.

[Account funding](../10_Developer_Guides/accounts.md) · [RPC reference](../03_Operators/funod-rpc.md) · [Tokenomics](tokenomics.md)

## Sources

[English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.md) · [Chinese whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.cn.md) · [Scope and source conflicts](whitepaper.md). Pinned revision `f49e5f0f821162a997260535be30767e3f147d8e`; retrieved 2026-11-02.
