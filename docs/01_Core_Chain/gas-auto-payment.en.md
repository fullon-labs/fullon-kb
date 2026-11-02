---
title: GAS and ELON automatic payment
status: verified
updated: 2026-11-02
source: Core v0.9.2 source review
---

# GAS and ELON automatic payment

FullOn integrates resource calculation, balance checks and payment into transaction execution. Ordinary users keep sufficient spendable FLON in the actual payer account and approve their business transaction. They do not need a separate GAS purchase, conversion transaction or gas-price setting. Automatic payment reduces steps; it does not make transactions free or guarantee success with insufficient funds.

This explanation reviews Core v0.9.2 at `2188e4f94a1e9fe564a31c33e497b464556f3650`. Live network rates, contracts and wallet presentation require separate verification.

## GAS, ELON and FLON units

GAS represents execution and storage resources. ELON expresses their accounting relationship to the smallest core-token unit. The implementation converts one integer GAS unit to **one smallest core-token unit**, not one whole FLON. The official build uses FLON with eight decimal places:

- `1 FLON = 100,000,000 ELON`;
- `1 ELON = 0.00000001 FLON`;
- covering `N` GAS units automatically costs `N / 100,000,000 FLON`.

This is a protocol accounting conversion, not an exchange-market rate or a requirement to acquire another tradable token. Core accesses the core-token balance table and internal GAS allowance. An ELON reference in a comment does not establish a separate ELON token contract or exchange interface.

## Automatic payment inside a transaction

1. **Identify the payer.** CPU/NET billing uses the transaction's first authorizer, which need not be the account currently displayed by a wallet or the transfer recipient. RAM changes are billed to their corresponding RAM payer, which a contract may assign to another account.
2. **Calculate resources.** Billed CPU time and NET bytes are converted to GAS using effective on-chain rates and rounding up. Positive RAM allocation is charged separately. Actual cost depends on usage and parameters.
3. **Use existing GAS first.** Core consumes internal `gas_reserved`; sufficient reserved allowance avoids an additional FLON charge for the same cost.
4. **Cover only the shortfall.** Core checks spendable core-token balances and directly moves the shortfall's smallest FLON units from the payer balance to the system `flon.gas` balance. This balance-table path needs no separately signed deposit, conversion or `transfer` action. Ordinary transfer history is therefore not a substitute for GAS details.
5. **Commit the outcome.** GAS checks and payment are part of transaction state changes. An ordinary transaction cannot commit successfully without meeting payment conditions. Special transaction paths, application fees and failed-history records should not all be assigned identical semantics from this alone.

Example: a charge of `3,000` GAS units with `1,000` reserved requires `2,000` additional units, or `0.00002000 FLON`. This illustrates conversion only, not a fixed transfer fee. RAM costs must be considered separately for their actual payer.

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

## Source evidence

All links pin the v0.9.2 commit:

- [Core symbol and precision](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/chain_config.cmake)
- [Resource billing, automatic shortfall payment and RAM credit](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/resource_limits.cpp)
- [Payer selection and transaction GAS traces](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/transaction_context.cpp)
- [Balance access and symbol validation](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/contract_table_utils.cpp)
- [GAS trace fields](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/include/eosio/chain/trace.hpp)
- [get_account resource fields](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/plugins/chain_plugin/chain_plugin.cpp)

[Resource model](resource-model.md) · [RPC reference](../03_Operators/funod-rpc.md)
