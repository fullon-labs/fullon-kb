---
title: "Interoperability: proxy accounts and cross-chain flows"
status: active
updated: 2026-11-02
source: whitepaper v2.6.0 Core v0.9.2 baseline and policy clarification draft
---

# Interoperability: proxy accounts and cross-chain flows

This page summarizes protocol design in the whitepaper v2.6.0 clarification draft (2026-11-02); it does not certify deployment on any network.

## Whitepaper design

The design lets external-chain users retain familiar wallet signing and interact with DApps deployed on FullOn through proxy accounts, rather than requiring each DApp to redeploy everywhere.

1. A user initiates binding using an external-chain address and key in a supporting application.
2. Binding associates the external public key/address with an allocated FullOn proxy account.
3. A supported bridge flow moves assets to the FullOn side.
4. The user signs an interaction message; a proxy miner separately signs and submits the FullOn transaction. The whitepaper describes validating both signatures while accounting for chain-specific hashes, signature schemes and serialization.
5. Assets may be returned to the originating chain while the proxy account remains valid.

A proxy miner is a transaction-submission service role; it is not automatically an [Active or Standby BP](governance.md).

## Verify identity and asset layers separately

| Layer | Confirm |
| --- | --- |
| Identity binding | Deployed contract, signing domain, supported wallets/chains, bind/unbind rules |
| Proxy submission | Availability, nonce/expiry handling, fees and deduplication |
| Asset bridge | Token contracts, proof/custody model, confirmations, pause/refund and destination-credit rules |
| DApp | Network, authorization, asset identity, execution result and irreversibility |

Two-signature validation is not a complete bridge proof protocol or security audit. It does not establish support for every chain, wallet or token. L2/sidechain architecture descriptions are not a list of verified deployments.

## Account distinctions

- Canonical/sovereign: named FullOn accounts and permissions.
- EVM-address: addresses meaningful within the EVM environment, requiring an asset bridge to native accounts in the design.
- Proxy: external-chain identity binding for FullOn interaction.
- RWID: real-world identity factors and recovery; distinct from cross-chain proxy interaction.

[Accounts](accounts.md) · [RWID](rwid-accounts.md) · [DApp and bridge use](../06_User_Guides/use-dapps.md)

## Sources

[English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.md) · [Chinese whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.cn.md) · [Scope and source conflicts](whitepaper.md). Pinned revision `5758318eba75d48afd1d543bf020255c1a998d26`; retrieved 2026-11-02. The Core v0.9.2 baseline is published; the additional future issuance/GAS policy clarification remains a separate draft, not a deployment certification.
