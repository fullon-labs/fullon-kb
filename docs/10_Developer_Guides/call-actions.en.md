---
title: Call smart contract actions
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/call-actions.md
---

# Call smart contract actions

Node, CLI, and RPC examples target **FullOn Core v0.9.2**. Contracts, CDT, and wallets have independent versions; their stated verification scope does not automatically change with Core. See [version baseline and migration](../09_Release_Notes/v0.9.2.md).

## CLI calls

[Read the current ABI](get-abi-code.md) and verify action fields, types, and authorization. This calls the [hello example](build-contract.md) and requires a deployed contract and prepared signing wallet. It submits a write transaction.

```bash
export FULLON_RPC='http://127.0.0.1:8888'
fucli -u "$FULLON_RPC" push action contractacct hi   '{"user":"calleracct"}' -p calleracct@active
```

`contractacct` is the contract account; `calleracct` is the signing user. JSON fields come from the ABI, not interface labels. `-p` cannot grant authority the signer does not possess.

## Application flow

1. Obtain chain ID and ABI; construct action account, name, authorization, and data.
2. Serialize and sign with a confirmed compatible SDK or wallet protocol.
3. Broadcast the packed transaction, then check execution and irreversibility; see [transactions](transactions.md).

`abi_json_to_bin` converts arguments only; it does not sign or submit. Node RPC generally does not accept arbitrary plain action JSON as a complete signed transaction.

## Errors

For missing authority, inspect current permissions. For ABI mismatch, reserialize and sign again. For resource errors, follow current chain rules. Reconcile the original transaction after broadcast timeouts rather than duplicating the business operation.

## Sources and scope

[Source 1](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/programs/client/main.cpp), [Source 2](../03_Operators/funod-rpc.md). Source review: 2026-11-02. This does not verify the version deployed on every network.
