---
title: What is a FullOn RWID account?
type: core_chain
status: active
updated: 2026-11-02
source: source review
translation_of: 01_Core_Chain/rwid-accounts.md
---

# What is a FullOn RWID account?

RWID is a contract-based account creation and permission-recovery scheme. In the reviewed implementation, a new account delegates its owner authority to the RWID owner contract's active permission, while user-supplied public keys form the new account's active authority.

## How it differs from self-managed owner authority

| Item | Self-managed owner | Reviewed RWID creation path |
| --- | --- | --- |
| Daily signing | Determined by active authority | User-supplied active keys and threshold |
| Root authority | Determined by account configuration | Initially points to the RWID owner contract's active permission |
| Changing active | Requires authority allowed to change permissions | RWID DAO authorizes the owner contract to update permissions |
| Recovery | Depends on prior configuration | Depends on authentication, recovery orders, and DAO/owner contract workflows |

Being able to sign daily operations does not mean a user solely controls every root permission. Recovery depends on contract permissions and authentication services; it is not an unconditional promise of recovery using only a phone number.

## Contract flow

`rwid.auth` exposes authentication-side account creation and recovery-related entry points. `rwid.dao` coordinates creation, active authority records, and recovery. `rwid.owner` calls the system `newaccount`, points owner at itself, and purchases the configured gas amount for the new account.

The reviewed owner implementation requires a positive active threshold, 1–10 keys, positive weights, no duplicate keys, and sufficient total weight to meet the threshold. It rejects account-permission entries and waits in active. These are restrictions of this RWID implementation, not of all ordinary FullOn authorities.

## Check before using it

1. Whether the current wallet offers RWID registration and which authentication methods it supports.
2. The actual contract accounts, code versions, and permission structure on the chosen network.
3. How authentication information is stored, who reviews recovery, and the applicable fees and waiting conditions.
4. Query owner and active with `get_account` after creation rather than relying on a product label.

This guide does not publish phone numbers, verification codes, or private authentication APIs. Use supported registration and recovery flows in the official application.

[Mobile wallet](../06_User_Guides/hufu-mobile.md) · [Developer account flow](../10_Developer_Guides/accounts.md)

## Sources and scope

[Source 1](https://github.com/fullon-labs/rwid.contracts/blob/d0fcb698711a0ea807515e76cf44e357d38787f3/contracts/rwid.owner/src/rwid.owner.cpp), [Source 2](https://github.com/fullon-labs/rwid.contracts/blob/d0fcb698711a0ea807515e76cf44e357d38787f3/contracts/rwid.auth/include/rwid.auth/rwid.auth.hpp), [Source 3](https://github.com/fullon-labs/rwid.contracts/blob/d0fcb698711a0ea807515e76cf44e357d38787f3/contracts/rwid.dao/src/rwid.dao.cpp). Source review: 2026-11-02. This does not verify the version deployed on every network.

## RWID design in the whitepaper repository

The [RWID design](https://github.com/fullon-labs/flon.whitepaper/blob/d695da53f4e453dd0e372e9dc5a605a0c56d455e/rwid-design.md) expands RWID as Real-World Identity. It proposes binding factors such as phone, email, Google, WhatsApp, and Telegram, with configurable recovery thresholds and decentralized oracle verification for key replacement.

These are design goals, not a verified list of available authentication services. Consider them separately from the reviewed auth/DAO/owner permission paths above. They do not establish that current recovery is fully decentralized or trustless. Key generation, factor storage, and recovery review require product-level verification; see [design and implementation differences](whitepaper.md).
