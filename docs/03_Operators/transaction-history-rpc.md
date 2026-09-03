---
title: funod Transaction History RPC
type: developer_guide
status: verified
updated: 2026-09-03
source: official
---

# funod Transaction History RPC

## Purpose

This page expands the Transaction History section of the
[funod RPC Developer Guide](funod-rpc.md). It covers only native `funod` RPC.
Flonscan is mentioned as integration evidence because its source and production
calls exercise these native routes; Flonscan's private application APIs are not
part of the `funod` RPC contract.

Use this API to retrieve:

- action history involving an account;
- a transaction and its action traces by transaction ID;
- indexed key-to-account and controlling-account relationships;
- transaction counts and local history-database health.

History is an index maintained by the node. Use `/v1/chain/*` for authoritative
current account, balance, permission, and contract-table state.

## Enable and detect the API

Enable both plugins:

```ini
plugin = eosio::transaction_history_plugin
plugin = eosio::transaction_history_api_plugin
```

The current source registers identical handlers under both prefixes:

```text
/v1/history/*
/v1/transaction_history/*
```

Use `/v1/history/*` when compatibility with older deployed nodes is required.
Feature-detect before using newer methods or the longer alias:

```bash
rpc=http://127.0.0.1:8888

curl -sS "$rpc/v1/node/get_supported_apis" | jq \
  '.apis[] | select(test("^/v1/(history|transaction_history)/"))'
```

All routes are in the `history_ro` HTTP category. FullOn Core also applies
shared History admission controls:

```ini
http-max-history-requests-in-flight = 4
http-history-requests-per-second = 5
```

Those are the checked source defaults. Tune them for node capacity; both must
remain greater than zero.

## Complete method list

Each method below is available under both route prefixes when the current API
plugin is enabled.

| Method | Request | Main result |
| --- | --- | --- |
| `get_transaction` | `id`, optional `block_num_hint` | Indexed transaction, traces, resource/gas data, block and LIB |
| `get_actions` | `account_name`, optional `pos`, `offset` | Account action sequence, LIB, pagination flags |
| `get_transaction_count` | optional `start_block`, `end_block` | Count and effective block range |
| `get_key_accounts` | `public_key` | `account_names` |
| `get_controlled_accounts` | `controlling_account` | `controlled_accounts` |
| `get_database_stats` | `{}` | `success`, database `stats`, optional `error` |
| `get_performance_metrics` | `{}` | `success`, performance `metrics`, optional `error` |

The plugin header also declares maintenance helpers named
`get_optimization_suggestions`, `get_cache_analysis`, `get_maintenance_needs`,
and `trigger_auto_optimize`. They are not registered by the current HTTP API
plugin and therefore are not RPC endpoints.

## Get account actions

Endpoint:

```text
POST /v1/history/get_actions
```

Request fields:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `account_name` | string | yes | Account whose received or authorized actions are queried |
| `pos` | signed integer | no | Account action sequence cursor; `-1` starts at the newest action |
| `offset` | signed integer | no | Negative reads backward, positive reads forward, zero returns no rows |

```bash
curl --fail --silent --show-error \
  -X POST "$rpc/v1/history/get_actions" \
  -H 'Content-Type: application/json' \
  --data '{
    "account_name": "numguessgame",
    "pos": -1,
    "offset": -20
  }' | jq
```

Result fields:

| Field | Meaning |
| --- | --- |
| `actions` | Action records with account/global sequence, block metadata, and `action_trace` |
| `last_irreversible_block` | LIB observed by the node for this response |
| `more` | Whether more matching history is available; optional on older nodes |
| `time_limit_exceeded_error` | Whether scanning stopped at its time limit; optional on older nodes |

An account history result is an action list, not a unique transaction list.
One transaction can produce multiple top-level and inline actions. Group by
`action_trace.trx_id` only when the product intends to display transactions
rather than actions.

### Backward pagination

1. Request `pos: -1` with a negative `offset`.
2. Find the smallest returned `account_action_seq`.
3. Use that value minus one as the next `pos`.
4. Keep the same negative `offset`.
5. Stop on an empty page; on current nodes also stop when `more` is `false`.

```ts
type HistoryAction = {
  account_action_seq: number;
  action_trace: { trx_id: string };
};

function olderCursor(actions: HistoryAction[]): number | null {
  if (actions.length === 0) return null;
  return Math.min(...actions.map((item) => item.account_action_seq)) - 1;
}
```

Older history implementations can include the explicit `pos` boundary and
return one extra row. Derive the next cursor from returned sequence values and
deduplicate by `account_action_seq`; do not assume an exact page length.

If `time_limit_exceeded_error` is true, retain the rows already returned and
continue from their sequence cursor with a smaller page.

### Determine irreversibility

```ts
const irreversible = action.block_num <= response.last_irreversible_block;
```

Actions above LIB remain reversible and can disappear after a fork.

## Get a transaction

Endpoint:

```text
POST /v1/history/get_transaction
```

Use the full 64-character hexadecimal ID for compatibility:

```bash
curl --fail --silent --show-error \
  -X POST "$rpc/v1/history/get_transaction" \
  -H 'Content-Type: application/json' \
  --data '{"id":"TRANSACTION_ID"}' | jq
```

Optional `block_num_hint` can reduce lookup work when the containing block is
known:

```json
{
  "id": "TRANSACTION_ID",
  "block_num_hint": 14415393
}
```

Result fields:

| Field | Meaning |
| --- | --- |
| `id` | Transaction ID |
| `trx` | Indexed receipt and transaction data |
| `block_time` | Block timestamp |
| `block_num` | Containing block number |
| `last_irreversible_block` | Node LIB at query time |
| `traces` | Top-level and inline action traces |
| `res_usage` | Recorded resource usage |
| `gas_traces` | Recorded gas-related traces |

The current implementation accepts an unambiguous hexadecimal prefix of at
least eight characters, but public clients should continue to send full IDs.

## Count transactions by block range

Endpoint:

```text
POST /v1/history/get_transaction_count
```

```bash
curl -sS -X POST "$rpc/v1/history/get_transaction_count" \
  -H 'Content-Type: application/json' \
  --data '{"start_block":14415000,"end_block":14416000}' | jq
```

Both bounds are optional. The response returns `count`, `start_block`, and
`end_block`, including the effective range selected by the implementation.
Older deployed nodes may not expose this method even when `get_actions` and
`get_transaction` are available.

## Query authority indexes

Public-key lookup:

```bash
curl -sS -X POST "$rpc/v1/history/get_key_accounts" \
  -H 'Content-Type: application/json' \
  --data '{"public_key":"PUB_K1_..."}' | jq
```

Controlling-account lookup:

```bash
curl -sS -X POST "$rpc/v1/history/get_controlled_accounts" \
  -H 'Content-Type: application/json' \
  --data '{"controlling_account":"alice"}' | jq
```

These results reflect the history index. Before authorizing or signing an
operation, confirm current permissions with `/v1/chain/get_account`.

## Inspect history database health

```bash
curl -sS -X POST "$rpc/v1/history/get_database_stats" \
  -H 'Content-Type: application/json' --data '{}' | jq

curl -sS -X POST "$rpc/v1/history/get_performance_metrics" \
  -H 'Content-Type: application/json' --data '{}' | jq
```

Both methods return a `success` flag, a plugin-defined data object, and an
optional `error`. Their nested metrics are operational diagnostics rather than
a stable DApp data schema; monitoring clients should tolerate added fields.

## TypeScript client

```ts
async function postRpc<T>(rpcBase: string, path: string, body: unknown): Promise<T> {
  const response = await fetch(`${rpcBase}${path}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`FullOn RPC ${response.status}: ${await response.text()}`);
  }
  return response.json() as Promise<T>;
}

const actionPage = await postRpc("https://m.flonscan.io", "/v1/history/get_actions", {
  account_name: "numguessgame",
  pos: -1,
  offset: -20,
});
```

Never send wallet credentials, private keys, or signing material to a History
endpoint.

## Flonscan integration evidence

Flonscan source was inspected to confirm how a production application consumes
native history RPC:

- its legacy account-action route proxies native `get_actions`;
- its transaction lookup proxies native `get_transaction`;
- current explorer pages can also use Flonscan-owned indexed APIs, whose schema
  is not a `funod` RPC contract.

Live verification on 2026-09-03 confirmed `get_actions` and `get_transaction`
through the mainnet node at `https://m.flonscan.io`. That node reported an older
`v0.6.6` version and did not yet expose the longer
`/v1/transaction_history/*` alias or `get_transaction_count`. Applications
must feature-detect rather than equating source availability with deployment.

## Operational notes

- `404 Unknown Endpoint`: plugin, alias, category, or method is unavailable on
  the selected listener/version.
- Empty history: verify network, local retention/indexing, and account filters.
- Transaction not found: use the full ID and supply `block_num_hint` when known.
- `503`: history concurrency or token-bucket admission is saturated; retry with
  bounded exponential backoff.
- Cache immutable transaction details after their block is irreversible.
- History indexes can lag head state. Use Chain API for settlement and
  authorization decisions.

## Verification basis

This guide was checked against:

- FullOn Core transaction-history route registration and reflected request
  structures at source revision `72cde15a3fb1`;
- HTTP history admission-control implementation;
- Flonscan source as a consumer of native History RPC;
- live mainnet responses on 2026-09-03.

## Related pages

- [funod RPC Developer Guide](funod-rpc.md)
- [Operator and Developer Guides](README.md)
- [Finality](../05_Glossary/finality.md)
- [FullOn Core source](https://github.com/fullon-labs/flon-core)
- [Flonscan](https://flonscan.io)
