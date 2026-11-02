---
title: "Resource model: FLON, GAS and ELON"
status: active
updated: 2026-11-02
source: Core v0.9.2 source review and whitepaper v2.6.0 policy clarification draft
---

# Resource model: FLON, GAS and ELON

FullOn integrates resource calculation, balance checks and payment into transaction execution. Ordinary users keep sufficient spendable FLON in the actual payer account and approve their business transaction. They do not need a separate GAS purchase, conversion transaction or gas-price setting. Automatic payment reduces steps; it does not make transactions free or guarantee success with insufficient funds.

This explanation reviews Core v0.9.2 at `2188e4f94a1e9fe564a31c33e497b464556f3650`. Live network rates, contracts and wallet presentation require separate verification.

## Resources

| Resource | Whitepaper measurement | Example |
| --- | --- | --- |
| CPU | Transaction execution time | Contract computation |
| NET | Transaction size | Signed transaction data |
| RAM | Allocated on-chain state storage | Contract table records |

## GAS, ELON and FLON units

GAS represents execution and storage resources. ELON expresses their accounting relationship to the smallest core-token unit. The implementation converts one integer GAS unit to **one smallest core-token unit**, not one whole FLON. The official build uses FLON with eight decimal places:

- `1 FLON = 100,000,000 ELON`;
- `1 ELON = 0.00000001 FLON`;
- covering `N` GAS units automatically costs `N / 100,000,000 FLON`.

This is a protocol accounting conversion, not an exchange-market rate or a requirement to acquire another tradable token. Core accesses the core-token balance table and internal GAS allowance. An ELON reference in a comment does not establish a separate ELON token contract or exchange interface.

## Automatic payment inside a transaction {#auto-gas-payment}

1. **Identify the payer.** CPU/NET billing uses the transaction's first authorizer, which need not be the account currently displayed by a wallet or the transfer recipient. RAM changes are billed to their corresponding RAM payer, which a contract may assign to another account.
2. **Calculate resources.** Billed CPU time and NET bytes are converted to GAS using effective on-chain rates and rounding up. Positive RAM allocation is charged separately. Actual cost depends on usage and parameters.
3. **Use existing GAS first.** Core consumes internal `gas_reserved`; sufficient reserved allowance avoids an additional FLON charge for the same cost.
4. **Cover only the shortfall.** Core checks spendable core-token balances and directly moves the shortfall's smallest FLON units from the payer balance to the system `flon.gas` balance. This balance-table path needs no separately signed deposit, conversion or `transfer` action. Ordinary transfer history is therefore not a substitute for GAS details.
5. **Commit the outcome.** GAS checks and payment are part of transaction state changes. An ordinary transaction cannot commit successfully without meeting payment conditions. Special transaction paths, application fees and failed-history records should not all be assigned identical semantics from this alone.

Example: a charge of `3,000` GAS units with `1,000` reserved requires `2,000` additional units, or `0.00002000 FLON`. This illustrates conversion only, not a fixed transfer fee. RAM costs must be considered separately for their actual payer.

## How GAS is calculated per transaction {#gas-calculation}

For ordinary resource-billed accounts, v0.9.2 uses the following calculation. `ceil` rounds each component up separately; `payer` identifies each RAM-paying account. Resource-exempt accounts do not follow ordinary charging.

```text
P = 1000
G_cpu = ceil(cpu_usage_us * gas_per_cpu_ms / P)
G_net = ceil(net_usage_bytes * gas_per_net_kb / P)
G_ram_charge = sum(ceil(max(ram_delta_bytes[payer], 0) * gas_per_ram_kb / P))
G_consumed = G_cpu + G_net + G_ram_charge
G_ram_credit = sum(ceil(max(-ram_delta_bytes[payer], 0) * gas_per_ram_kb / P))
FLON_debited = sum(converted_gas[payer]) / 100000000
```

- `cpu_usage_us` is the transaction's **billed CPU microseconds**, not an action's `elapsed` or an HTTP request duration. Billing also follows rules such as the configured CPU minimum.
- `net_usage_bytes` is the transaction's **billed byte count**, including protocol billing rules and rounding up to an eight-byte multiple. Multiply receipt `net_usage_words` by `8`; do not substitute serialized JSON length.
- `ram_delta_bytes[payer]` is each account's aggregated RAM change. Allocation is charged and released storage credits internal GAS. Show `G_ram_credit` separately; subtracting it from cumulative consumption does not determine actual FLON debits.
- CPU/NET uses the transaction payer; RAM uses its respective payers. Reserved allowance, execution order and RAM credits affect automatic shortfalls. Use `gas_traces[].converted_gas` rather than treating balances across accounts as one pool.

The `ms` and `kb` field names describe nominal rate units. **When using raw integer rates, both CPU microseconds and NET/RAM bytes use the source divisor `P = 1000`. Do not divide by 1000 again or replace this divisor with 1024.**

### Observed rates

On 2026-11-02, read-only queries to `https://m.flonscan.io` reported Core `v0.9.2-2188e4f9` and the chain ID recorded in the documentation's mainnet snapshot. Both `get_info` and `get_consensus_parameters` returned these rates. This dated observation is not a fixed future price.

| Resource | Raw on-chain rate | Effective unit price |
| --- | --- | --- |
| CPU | `gas_per_cpu_ms = 10000` | `10 GAS` per billed microsecond |
| NET | `gas_per_net_kb = 50000` | `50 GAS` per billed byte |
| RAM | `gas_per_ram_kb = 50000` | `50 GAS` per newly allocated byte |

See the [rate observation](gas-rate-observation.json) for responses, chain ID and height. These match v0.9.2 source defaults; actual billing uses the parameters effective on the target network.

### Ordinary FLON transfer: individual and average examples

These are **hypothetical resource-usage examples, not a measured mainnet average**. Assume one ordinary FLON transfer per transaction, existing balance rows, no additional contract business, no new RAM, and `192 billed NET bytes` each, using the rates above:

| Example | Assumed billed CPU | CPU GAS | NET GAS | Total GAS | FLON equivalent |
| --- | --- | --- | --- | --- | --- |
| A | `100 μs` | `1,000` | `9,600` | `10,600` | `0.00010600` |
| B | `120 μs` | `1,200` | `9,600` | `10,800` | `0.00010800` |
| C | `200 μs` | `2,000` | `9,600` | `11,600` | `0.00011600` |
| Example mean | `140 μs` | `1,400` | `9,600` | **`11,000`** | **`0.00011000`** |

For C, `ceil(200 × 10000 / 1000) + ceil(192 × 50000 / 1000) = 11600 GAS`. With no reserved allowance, automatic payment debits `0.00011600 FLON`. With `1000 GAS` reserved, it debits only `0.00010600 FLON`. Existing GAS reduces the new FLON debit, not the transaction's `11600 GAS` consumption.

If a transfer also allocates `240 bytes` for a recipient balance row, add `12000 GAS`, or `0.00012000 FLON` equivalent, charged to the actual RAM payer. That byte count is also hypothetical; use actual RAM deltas. Memo length, signatures, authorization count, recipient-contract notifications and account state affect costs. GAS is not a percentage of the transfer amount.

### Measuring a real transfer average

For `n` successful, irreversible ordinary transfers on one network in a defined time window, deduplicate transaction IDs and aggregate consumption and automatic shortfalls from `gas_traces`:

```text
average_consumed_GAS = sum(G_consumed[i]) / n
average_FLON_equivalent = average_consumed_GAS / 100000000
average_new_FLON_debit = sum(sum(converted_gas[i][payer])) / n / 100000000
```

Publish the network/chain ID, time window, sample count, rates and RAM inclusion alongside the mean. Separate first-receipt allocations from existing balance rows. Do not mix swaps, bridges, inline transfers or failed transactions into ordinary-transfer samples, or count one transaction repeatedly for its actions.

This review did not obtain sufficient complete fee records for ordinary transfers: retrieved transfer actions primarily belonged to FullSwap and are not representative. The reproducible example mean is therefore provided here; **`0.00011000 FLON` is not reported as an observed average transaction fee**.

## Ensuring payment succeeds

- Retain spendable FLON in the actual payer account. An amount being transferred out in full cannot also fund the fee. Staked, locked or externally held assets are not automatically spendable core-token balances for this path.
- Use wallet estimates and retain a margin. Execution may change balances; an estimate does not reserve the final cost.
- For sponsored transactions, verify the application's actual authorization and payment arrangement. Core does not automatically charge a developer, recipient or arbitrary third party when the user lacks funds.
- The payer and system `flon.gas` core-token balance rows must exist and have matching symbol and precision. Missing required rows prevent construction of the conversion path; a displayed FLON number alone does not validate network setup.
- Errors such as `tx_gas_usage_exceeded` indicate resource payment failure. Fund the relevant payer or reduce usage before retrying.

Releasing RAM can credit internal GAS at the effective rate. This does not automatically return FLON to the user's core-token balance or guarantee an amount identical to the original expenditure.

## Simple operation with visible charges

Transparent payment means automatic execution with explainable charges. The following wallet/explorer presentation is recommended from Core fields, not asserted as implemented by every wallet:

- Before signing, show the actual payer, estimated cost and FLON equivalent, business transfer amount and insufficient-balance errors. Routine users should not need gas-price entry or separate CPU/NET/RAM purchases.
- After execution, explain `gas_traces`: `reserved_gas_before`, `reserved_gas_after`, `used_gas`, `converted_gas` and `ram_gas_delta`. Separate allowance consumption, automatic FLON payment and RAM changes.
- Use `get_account` fields `gas_reserved` and `gas_max` for resource availability. `gas_max` already includes convertible core-token balance; adding that balance again double counts capacity. It is not a network-wide flat fee or a final quote.
- If a node omits or has not retained complete traces, show details as unavailable rather than zero. List protocol GAS separately from proxy, cross-chain and application service charges.

Advanced CPU/NET limits remain available in transaction headers. Removing manual GAS configuration from routine user flows does not remove protocol execution limits or resource protection.

## Reserves and governance policy

The following reserve and reward policies describe the whitepaper design and its additional clarification draft. Core automatic payment alone does not establish deployed redemption rules, reward allocation, or DAO parameters.

Redeemable ELON liabilities are backed by FLON in `flon.gas`, one smallest FLON unit per new ELON. Reserves cannot be reused while they back redemption liabilities. Consuming GAS retires the corresponding liability; that section says reserve FLON remains locked by default. A portion rewards eligible Active and Standby BPs under effective rules; the remainder is DAO-locked by default. **Future FullOn DAO Gov proposals decide whether, when and how much of the remaining disposable balance is burned.** No amount is counted as burned before an approved burn is executed. Reserves needed for outstanding ELON redemption cannot fund rewards or burns. See the [governance clarification](whitepaper.md).

### Reward and DAO ledgers

- `bp_reward_balance` accounts for BP and voter rewards.
- `dao_locked_balance` remains locked unless approved DAO proposals meet quorum, timelock and execution-allowlist requirements.
- The proposed initial split is 10% / 90%; this is a design recommendation, not a verified live parameter.
- Reconcile each epoch and maintain reserves, in smallest FLON units, at least equal to outstanding redeemable ELON. Backing reserves are not unrestricted spending balances.

The whitepaper also describes proxy fees, 1,000 free proxy uses and variable EVM-address fees. Availability requires product/network verification; these are not current promotional guarantees.

[Account funding](../10_Developer_Guides/accounts.md) · [RPC reference](../03_Operators/funod-rpc.md) · [Tokenomics](tokenomics.md)

## Source evidence

All links pin the v0.9.2 commit:

- [Conversion precision and default rates](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/include/eosio/chain/config.hpp)
- [Core symbol and precision](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/chain_config.cmake)
- [Resource billing, automatic shortfall payment and RAM credit](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/resource_limits.cpp)
- [Payer selection and transaction GAS traces](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/transaction_context.cpp)
- [Balance access and symbol validation](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/contract_table_utils.cpp)
- [GAS trace fields](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/include/eosio/chain/trace.hpp)
- [get_account resource fields](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/plugins/chain_plugin/chain_plugin.cpp)


[English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.md) · [Chinese whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.cn.md) · [Scope and source conflicts](whitepaper.md). Pinned revision `5758318eba75d48afd1d543bf020255c1a998d26`; retrieved 2026-11-02. The Core v0.9.2 baseline is published; the additional future issuance/GAS policy clarification remains a separate draft, not a deployment certification.
