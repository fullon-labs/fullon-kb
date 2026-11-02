---
title: Deploy and upgrade a smart contract
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/deploy-contract.md
---

# Deploy and upgrade a smart contract

Node, CLI, and RPC examples target **FullOn Core v0.9.2**. Contracts, CDT, and wallets have independent versions; their stated verification scope does not automatically change with Core. See [version baseline and migration](../09_Release_Notes/v0.9.2.md).

## Prerequisites

You need compiled WASM/ABI, a contract account on the target network, sufficient resources, and a signing wallet satisfying its deployment authority. The example modifies on-chain code. Run it on an isolated chain or testnet first and replace `contractacct`.

```bash
export FULLON_RPC='http://127.0.0.1:8888'
fucli -u "$FULLON_RPC" get account contractacct
fucli -u "$FULLON_RPC" set contract contractacct ./build   hello.wasm hello.abi -p contractacct@active
fucli -u "$FULLON_RPC" get code contractacct -c deployed.wasm -a deployed.abi
```

WASM/ABI filenames in `set contract` are relative to `./build`. Whether active suffices depends on current permissions and action links. Do not change owner arbitrarily to make an example work.

## Verify

Keep the deployment transaction ID and confirm successful irreversible execution. Compare downloaded code hashes with the local WASM, check ABI actions/tables, and call a controlled action. The contract's declared name `hello` can differ from the deployment account.

## Upgrade

Save prior WASM, ABI, hashes, permissions, and a data-migration plan. Replacing code does not reset tables. Rolling code back does not roll data back.

Configure `eosio.code` only when inline authorization actually requires it, using minimum scope. Deploying a basic hello contract does not by itself require additional authority.

[Retrieve ABI / code](get-abi-code.md) · [Call actions](call-actions.md)

## Sources and scope

[Source 1](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/programs/client/main.cpp). Source review: 2026-11-02. This does not verify the version deployed on every network.
