---
title: Retrieve a contract ABI and WASM code
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/get-abi-code.md
---

# Retrieve a contract ABI and WASM code

Node, CLI, and RPC examples target **FullOn Core v0.9.2**. Contracts, CDT, and wallets have independent versions; their stated verification scope does not automatically change with Core. See [version baseline and migration](../09_Release_Notes/v0.9.2.md).

The ABI describes actions and data structures. WASM is the deployed executable bytecode. Downloading WASM does not recover the original C++ source or prove which repository produced it.

## Prerequisites

Install `fucli` from `flon-tools` and verify the RPC network. Replace the placeholder `contractacct`. These examples are read-only.

```bash
export FULLON_RPC='http://127.0.0.1:8888'
fucli -u "$FULLON_RPC" get abi contractacct -f contract.abi
fucli -u "$FULLON_RPC" get code contractacct -c contract.wasm -a contract.abi
```

`get code` prints the code hash; `-c` saves WASM to a file. `get abi -f` saves the decoded ABI.

## HTTP RPC

```bash
curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_abi"   -H 'Content-Type: application/json'   --data '{"account_name":"contractacct"}' | jq '.abi'

curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_code_hash"   -H 'Content-Type: application/json'   --data '{"account_name":"contractacct"}' | jq
```

For raw data, use `get_raw_code_and_abi` or `get_raw_abi`; see the [RPC reference](../03_Operators/funod-rpc.md) for types and encodings. Do not save an encoded JSON string directly as binary WASM.

## Verify and cache

Confirm chain ID and account name; record the code hash, ABI, and retrieval time. Separate requests are not an atomic snapshot. Recheck hashes during upgrades. ABI changes require reserialization and signing. Accounts may have no deployed code or ABI; that is not necessarily a node failure.

## Sources and scope

[Source 1](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/programs/client/main.cpp). Source review: 2026-11-02. This does not verify the version deployed on every network.
