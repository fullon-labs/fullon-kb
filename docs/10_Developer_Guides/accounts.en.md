---
title: Create and activate an account
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/accounts.md
---

# Create and activate an account

## Prerequisites

You need an existing creator account, a local signing wallet satisfying its authority, the target RPC, owner/active public keys for the new account, and sufficient funding/resources. Users should generate and confirm their public keys; do not collect private keys.

This source-supported `fucli system newaccount` command submits a write transaction. Use an isolated development chain or verified testnet and replace example accounts, keys, and amounts.

```bash
export FULLON_RPC='http://127.0.0.1:8888'
export OWNER_PUBLIC_KEY='REPLACE_WITH_VALID_OWNER_PUBLIC_KEY'
export ACTIVE_PUBLIC_KEY='REPLACE_WITH_VALID_ACTIVE_PUBLIC_KEY'
fucli -u "$FULLON_RPC" system newaccount creatoracct newaccount11   "$OWNER_PUBLIC_KEY" "$ACTIVE_PUBLIC_KEY"   --fund-gas '1.0000 FLON' -p creatoracct@active
fucli -u "$FULLON_RPC" get account newaccount11
```

`1.0000 FLON` demonstrates syntax; it is **not a promised registration fee or minimum gas amount**. Verify the core symbol, precision, and current gas rules. The reviewed CLI requires at least one positive `--fund-gas` or `--fund-account`: the former buys gas, while the latter transfers core assets and does not necessarily buy gas.

`fucli create account` exposes basic native creation without the same funding steps. System-contract resource/naming restrictions still apply. The example uses a 12-character name; short names and dotted names have additional rules.

## What does activation mean?

Identify the missing step: no on-chain account, wallet not imported, insufficient resources, or incomplete application authentication. The general creation path is `newaccount`. `fucli system activate` activates protocol features; **it does not activate user accounts**.

## RWID creation

Do not bypass authentication services by copying ordinary account creation. The reference path calls auth → DAO → owner → system contract and sets a specific owner authority. Services must verify administrator permissions, authentication type, recovery policy, and deployed ABI. See [RWID accounts](../01_Core_Chain/rwid-accounts.md).

## Completion check

Keep the creation transaction ID, confirm successful irreversible execution, query owner/active and resources, then perform a controlled operation using the user's active authority.

## Sources and scope

[Source 1](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/programs/client/main.cpp), [Source 2](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.system/src/flon.system.cpp). Source review: 2026-11-02. This does not verify the version deployed on every network.
