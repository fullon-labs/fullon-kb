---
title: What is a FullOn account?
type: core_chain
status: active
updated: 2026-11-02
source: source review
translation_of: 01_Core_Chain/accounts.md
---

# What is a FullOn account?

A FullOn account is an on-chain identity. Its name identifies it; its permissions determine who can act for it. Token balances are generally stored in token contract tables, not inside a wallet installation.

## Accounts, keys, and wallets

| Concept | Purpose |
| --- | --- |
| Account name | Queryable on-chain identity used for transfers and action calls |
| Public key | Public information used in authorization rules |
| Private key | Creates signatures; protect it with its holder or a controlled signer |
| Wallet | Manages keys, displays accounts, and requests signatures |
| Authority | A threshold and weighted public keys, account permissions, or waits |

Accounts usually have `owner` and `active` permissions. `owner` is the root permission and `active` is used for daily operations. Dedicated child permissions and action links may also apply. Multiple keys or account permissions can jointly control an account; an account is not necessarily one private key.

## Official account categories

The official FAQ lists native & sovereign, proxy, social-recoverable, and simple address accounts, with WASM/EVM-managed variants for the latter. A category name alone does not establish current registration or recovery capabilities.

## Creation and use

Generating a key happens locally. An account must be created on-chain with `newaccount` before it can be queried or used. The creator needs an authorized existing account and must cover required resources. Naming rules depend on the deployed system contract; arbitrary short names are not necessarily available.

Self-managed accounts can configure owner and active. [RWID accounts](rwid-accounts.md) use a different owner-management and recovery path. Understand who can change daily signing permissions before choosing a model.

Query current permissions with `get_account`. A historical key index, wallet cache, or old screenshot is not a substitute.

[User registration](../06_User_Guides/create-account.md) · [Developer account creation](../10_Developer_Guides/accounts.md)

## Sources and scope

[Source 1](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/programs/client/main.cpp), [Source 2](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.system/src/flon.system.cpp). Source review: 2026-11-02. This does not verify the version deployed on every network.

## Whitepaper account classification

The whitepaper distinguishes canonical/sovereign accounts, EVM address accounts, and proxy accounts. Sovereign accounts use named identities and single-signature or multisignature permissions. EVM addresses have meaning within the EVM environment. Proxy accounts bind an external-chain identity and participate in FullOn applications through proxy submission signatures.

The FAQ also lists social-recoverable and simple-address accounts. These classifications have different scopes: RWID, proxy accounts, and EVM addresses are not interchangeable. A description of “12 alphanumeric characters” does not establish that every Latin letter or digit is accepted; consult the target chain's system contract.

See [interoperability and account distinctions](interoperability.md).

Source: [official account categories](https://docs.flon.network/fullon-faq/what_are_fullon_account_types), retrieved 2026-11-02.
