---
title: 'RPC quickstart: read on-chain data'
type: guide
status: active
updated: 2026-11-02
source: repository synthesis
translation_of: 10_Developer_Guides/quickstart.md
---

# RPC quickstart: read on-chain data

Node, CLI, and RPC examples target **FullOn Core v0.9.2**. Contracts, CDT, and wallets have independent versions; their stated verification scope does not automatically change with Core. See [version baseline and migration](../09_Release_Notes/v0.9.2.md).

Goal: verify network, accounts, assets, and contract state with read-only requests.

## Prerequisites

You need `curl`, `jq`, an operator-provided RPC URL, and a trusted expected chain ID. This repository does not maintain a currently verified mainnet/testnet configuration table. Do not infer the network from a domain name.

The example uses a local node. Replace `FULLON_RPC` for remote access and obtain the expected chain ID from an independent trusted source.

```bash
export FULLON_RPC='http://127.0.0.1:8888'
curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_info"   -H 'Content-Type: application/json' --data '{}' | jq
```

Check `chain_id`, node version, head, and `last_irreversible_block_num`. One response is only a snapshot; observe block progression and node lag before business use.

## Discover capabilities

```bash
curl --fail --silent --show-error --max-time 15   "$FULLON_RPC/v1/node/get_supported_apis" | jq '.apis'
```

Endpoints depend on node version, plugins, and listener categories. Not every node provides history.

## Read an account

Replace `YOUR_ACCOUNT` with an existing account on the target network.

```bash
curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_account"   -H 'Content-Type: application/json'   --data '{"account_name":"YOUR_ACCOUNT"}' | jq
```

Read permissions using the account endpoint. Historical public-key indexes are not current authorization evidence.

## Read balances and contract tables

All uppercase strings below are placeholders. Replace them using the target deployment and its ABI.

```bash
curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_currency_balance"   -H 'Content-Type: application/json'   --data '{"code":"TOKEN_CONTRACT","account":"YOUR_ACCOUNT","symbol":"TOKEN_SYMBOL"}' | jq

curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_table_rows"   -H 'Content-Type: application/json'   --data '{"json":true,"code":"CONTRACT","scope":"SCOPE","table":"TABLE","limit":20}' | jq
```

Asset identity includes network, contract, symbol, and precision. The contract defines table scope, indexes, and fields. Check `more` and `next_key` for pagination rather than inferring completion from row count.

## Next steps

Use the [History API](../03_Operators/transaction-history-rpc.md) for history. Read the [transaction lifecycle](transactions.md) before submitting transactions. See the [RPC reference](../03_Operators/funod-rpc.md) for complete parameters and conditions.
