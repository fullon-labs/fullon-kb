---
title: funod RPC Developer Guide
type: developer_guide
status: verified
updated: 2026-09-03
source: official
---

# funod RPC Developer Guide

## Scope and source baseline

This is the complete RPC catalog for the `funod` executable in the current
FullOn Core `v0.8.0-alpha` source. It covers:

- every HTTP route registered by plugins linked into `funod`;
- conditions that make a route available or unavailable;
- request fields, response purpose, and mutability;
- the State History WebSocket protocol, which is not a `/v1/*` JSON endpoint.

The catalog was verified against route registration code, not inferred from
Swagger alone. The checked source revision was `72cde15a3fb1` on 2026-09-03.
Some repository Swagger files do not yet include every current route.

`fuwal` wallet RPC belongs to a different executable and is intentionally not
included here.

## Discover the actual routes on a node

A route exists only when its API plugin is enabled and its API category is
exposed by the listener being called. Ask the node instead of assuming:

```bash
curl --fail --silent --show-error \
  'http://127.0.0.1:8888/v1/node/get_supported_apis' | jq
```

`get_supported_apis` returns the routes visible on that specific TCP or Unix
socket listener. It does not list routes assigned to a different category
listener. A missing route normally means one of these conditions is true:

1. its plugin is not enabled;
2. its category is not exposed on this listener;
3. an additional feature flag is disabled;
4. it is restricted to a Unix socket;
5. the running node is older than this guide.

## Calling conventions

The base form is:

```text
POST http://HOST:PORT/v1/<api>/<method>
Content-Type: application/json
```

Send `{}` to no-parameter methods. String-only Net API methods expect a JSON
string such as `"peer.example.org:9876"`, not an object. Unless a method says
otherwise, successful read calls return HTTP `200`; transaction submission
returns `202`; Net and most Producer APIs currently return `201`.

Minimal helper:

```bash
rpc=http://127.0.0.1:8888

curl --fail --silent --show-error \
  -X POST "$rpc/v1/chain/get_info" \
  -H 'Content-Type: application/json' \
  --data '{}' | jq
```

The HTTP dispatcher currently resolves a registered path without enforcing a
verb, but clients should use `POST` for stable compatibility. `OPTIONS` is
handled for CORS preflight. Treat CORS headers as node configuration, not a
protocol guarantee.

## Plugin and category matrix

| API group | Required API plugin | Category | Exposure guidance |
| --- | --- | --- | --- |
| Node discovery | `eosio::http_plugin` | `node` | Public or internal |
| Chain read | `eosio::chain_api_plugin` | `chain_ro` | Public with rate limits |
| Chain write | `eosio::chain_api_plugin` | `chain_rw` | Public transaction gateway or protected |
| Network read/write | `eosio::net_api_plugin` | `net_ro`, `net_rw` | Internal only; keep writes private |
| Producer read/write | `eosio::producer_api_plugin` | `producer_ro`, `producer_rw` | Internal only |
| Snapshot control | `eosio::producer_api_plugin` | `snapshot` | Internal only |
| Chain database size | `eosio::db_size_api_plugin` | `db_size` | Monitoring network only |
| Trace API | `eosio::trace_api_plugin` | `trace_api` | Indexed/read node; rate limit |
| Transaction history | `eosio::transaction_history_api_plugin` | `history_ro` | Indexed/read node; rate limit |
| Prometheus | `eosio::prometheus_plugin` | `prometheus` | Monitoring network only |
| Local signing gateway | `eosio::sign_transaction_api_plugin` | `sign_transaction` | Unix socket only |
| Test control | `eosio::test_control_api_plugin` | `test_control` | Test nodes only |

With a normal `http-server-address`, the listener exposes all enabled
categories. For production, category listeners allow read and privileged APIs
to be separated:

```ini
plugin = eosio::http_plugin
plugin = eosio::chain_api_plugin
plugin = eosio::net_api_plugin
plugin = eosio::producer_api_plugin

http-server-address = http-category-address
http-category-address = chain_ro,0.0.0.0:8888
http-category-address = chain_rw,0.0.0.0:8888
http-category-address = net_ro,127.0.0.1:8890
http-category-address = net_rw,./net-rw.sock
http-category-address = producer_ro,127.0.0.1:8891
http-category-address = producer_rw,./producer-rw.sock
http-category-address = snapshot,./snapshot.sock
```

Do not expose `net_rw`, `producer_rw`, `snapshot`, `test_control`, or signing
categories directly to the Internet.

### Linked plugins without standalone JSON routes

`chain_plugin`, `net_plugin`, `producer_plugin`, `signature_provider_plugin`,
`transaction_history_plugin`, and `sign_transaction_plugin` provide node
functionality consumed by their matching API plugins; they do not independently
register `/v1/*` routes. `resource_monitor_plugin` monitors disk use and also
has no client RPC. `state_history_plugin` is the separate WebSocket service
documented below.

## Node discovery API

| Path | Body | Result |
| --- | --- | --- |
| `/v1/node/get_supported_apis` | none | Sorted paths visible on the listener |

This route is provided directly by `http_plugin`; it is not inserted into its
own returned `apis` array.

## Chain API

Enable:

```ini
plugin = eosio::chain_api_plugin
```

### Chain status, blocks, and finality

| Path | Request fields | Purpose and availability |
| --- | --- | --- |
| `/v1/chain/get_info` | `{}` | Node version, chain ID, head, LIB, resource limits, gas rates, and earliest available block |
| `/v1/chain/get_block` | `block_num_or_id` | ABI-decoded signed block |
| `/v1/chain/get_raw_block` | `block_num_or_id` | Raw signed-block representation |
| `/v1/chain/get_block_info` | `block_num` | Compact block metadata by number |
| `/v1/chain/get_block_header` | `block_num_or_id`, optional `include_extensions` | Signed header and optional extensions |
| `/v1/chain/get_block_header_state` | `block_num_or_id` | Legacy block-header state; may be unavailable for retained ranges |
| `/v1/chain/get_transaction_status` | `id` | Tracked transaction state and finality context; only registered when transaction finality status storage is enabled |
| `/v1/chain/get_finalizer_info` | `{}` | Active/pending finalizer policies and last tracked votes |
| `/v1/chain/get_consensus_parameters` | `{}` | Chain configuration and optional WASM configuration |

Although `get_info` is implemented by `chain_api_plugin`, it is tagged with the
universal `node` category and is visible on every configured HTTP listener.

Examples:

```bash
curl -sS -X POST "$rpc/v1/chain/get_block" \
  -H 'Content-Type: application/json' \
  --data '{"block_num_or_id":"14415393"}' | jq

curl -sS -X POST "$rpc/v1/chain/get_transaction_status" \
  -H 'Content-Type: application/json' \
  --data '{"id":"TRANSACTION_ID"}' | jq
```

Enable the conditional transaction-status route with a nonzero storage limit:

```ini
transaction-finality-status-max-storage-size-gb = 1
```

Its result is a bounded finality-tracking view, not permanent transaction
history.

### Accounts, code, and ABI

| Path | Request fields | Purpose |
| --- | --- | --- |
| `/v1/chain/get_account` | `account_name` | Account metadata, permissions, balances, gas and resource state |
| `/v1/chain/get_code` | `account_name`, optional `code_as_wasm` | Deployed code hash, WASM/WAST, and ABI |
| `/v1/chain/get_code_hash` | `account_name` | Deployed code hash only |
| `/v1/chain/get_abi` | `account_name` | Decoded ABI definition |
| `/v1/chain/get_raw_code_and_abi` | `account_name` | Raw WASM and ABI blobs |
| `/v1/chain/get_raw_abi` | `account_name`, optional `abi_hash` | ABI hash and ABI blob; hash supports cache validation |
| `/v1/chain/get_accounts_by_authorizers` | `accounts`, `keys` | Permissions satisfiable by specified permission levels or public keys; only registered with account queries enabled |

Account example:

```bash
curl -sS -X POST "$rpc/v1/chain/get_account" \
  -H 'Content-Type: application/json' \
  --data '{"account_name":"numguessgame"}' | jq
```

`get_accounts_by_authorizers` input example:

```json
{
  "accounts": ["alice", {"actor": "bob", "permission": "active"}],
  "keys": ["PUB_K1_..."]
}
```

Enable this conditional route with:

```ini
enable-account-queries = true
```

### Contract tables and token data

| Path | Request fields | Purpose |
| --- | --- | --- |
| `/v1/chain/get_table_rows` | `code`, `scope`, `table`, plus options below | Read rows from one primary or secondary table index |
| `/v1/chain/get_table_by_scope` | `code`, optional `table`, bounds/options | Enumerate scopes that contain a table |
| `/v1/chain/get_currency_balance` | `code`, `account`, optional `symbol` | Token balance rows for an account |
| `/v1/chain/get_currency_stats` | `code`, `symbol` | Token supply, max supply, and issuer |

Complete `get_table_rows` request fields:

| Field | Required | Default / meaning |
| --- | --- | --- |
| `code` | yes | Contract account |
| `scope` | yes | Table scope, encoded as a string |
| `table` | yes | Table name |
| `json` | no | `false`; use `true` for ABI-decoded rows |
| `table_key` | no | Legacy table-key hint |
| `lower_bound`, `upper_bound` | no | Index bounds |
| `limit` | no | `10` |
| `key_type` | no | Index type such as `i64`, `i128`, `i256`, `float64`, `float128`, `sha256`, or `ripemd160` |
| `index_position` | no | `1`/`primary`, `2`/`secondary`, and so on |
| `encode_type` | no | `dec`; may be `hex` where supported |
| `reverse` | no | Reverse index traversal |
| `show_payer` | no | Include each row's RAM payer |
| `time_limit_ms` | no | Per-query time limit, bounded by node configuration |

Pagination uses `more` and `next_key`; pass `next_key` as the next
`lower_bound`. Do not infer completion from `rows.length < limit` alone.

```bash
curl -sS -X POST "$rpc/v1/chain/get_table_rows" \
  -H 'Content-Type: application/json' \
  --data '{
    "json": true,
    "code": "flon.token",
    "scope": "numguessgame",
    "table": "accounts",
    "limit": 100
  }' | jq
```

### Producers, protocol features, and deferred transactions

| Path | Request fields | Purpose |
| --- | --- | --- |
| `/v1/chain/get_producers` | optional `json`, `lower_bound`, `limit`, `time_limit_ms` | Producer rows and total vote weight |
| `/v1/chain/get_producer_schedule` | `{}` | Active, pending, and proposed producer schedules |
| `/v1/chain/get_activated_protocol_features` | optional `lower_bound`, `upper_bound`, `limit`, `search_by_block_num`, `reverse`, `time_limit_ms` | Activated protocol-feature history |
| `/v1/chain/get_scheduled_transactions` | optional `json`, `lower_bound`, `limit`, `time_limit_ms` | Deferred transaction queue |

For `get_activated_protocol_features`, bounds represent activation ordinals by
default and block numbers when `search_by_block_num` is `true`.

### ABI conversion and authorization preparation

| Path | Request fields | Purpose |
| --- | --- | --- |
| `/v1/chain/abi_json_to_bin` | `code`, `action`, `args` | Serialize JSON action data with the current ABI |
| `/v1/chain/abi_bin_to_json` | `code`, `action`, `binargs` | Decode binary action data with the current ABI |
| `/v1/chain/get_required_keys` | `transaction`, `available_keys` | Determine which available public keys satisfy transaction authorization |
| `/v1/chain/get_transaction_id` | unpacked transaction object | Calculate the transaction ID without submitting it |

ABI conversion is tied to the ABI currently visible to the node. A client must
rebuild and re-sign a transaction if the serialized action data changes.

### Transaction simulation and submission

| Path | Request shape | Behavior |
| --- | --- | --- |
| `/v1/chain/compute_transaction` | `{ "transaction": <packed-or-unpacked-transaction> }` | Execute for computation/result inspection without normal submission |
| `/v1/chain/send_read_only_transaction` | `{ "transaction": <packed-or-unpacked-transaction> }` | Execute a read-only transaction; registered on all Chain API nodes |
| `/v1/chain/push_transaction` | packed transaction object | Legacy single transaction submission |
| `/v1/chain/push_transactions` | array of packed transaction objects | Legacy batch submission |
| `/v1/chain/send_transaction` | packed transaction object | Submit one transaction |
| `/v1/chain/send_transaction2` | wrapper described below | Submit with retry/failure-trace controls; preferred advanced endpoint |
| `/v1/chain/push_block` | signed block object | Inject a block; privileged operational use only |

`send_transaction2` body:

```json
{
  "return_failure_trace": true,
  "retry_trx": false,
  "transaction": {
    "signatures": ["SIG_K1_..."],
    "compression": 0,
    "packed_context_free_data": "",
    "packed_trx": "..."
  }
}
```

`retry_trx_num_blocks` is meaningful when `retry_trx` is true. Transaction
acceptance also requires `api-accept-transactions = true`. An HTTP `202`
response means the node accepted processing of the request; applications must
still confirm inclusion and then compare the block number with LIB.

Do not use `push_transactions` as an atomic batch: entries are processed as
individual transactions.

Although `send_read_only_transaction` is registered whenever Chain API is
enabled, execution requires `read-only-threads > 0`; otherwise it returns an
unsupported-feature error.

## Transaction History API

Enable both plugins:

```ini
plugin = eosio::transaction_history_plugin
plugin = eosio::transaction_history_api_plugin
```

Every registered operation has two equivalent route prefixes:

```text
/v1/history/<method>
/v1/transaction_history/<method>
```

Use `/v1/history/*` when clients must also work with older deployed nodes.

The complete registered path set is:

```text
/v1/history/get_transaction
/v1/history/get_actions
/v1/history/get_transaction_count
/v1/history/get_key_accounts
/v1/history/get_controlled_accounts
/v1/history/get_database_stats
/v1/history/get_performance_metrics
/v1/transaction_history/get_transaction
/v1/transaction_history/get_actions
/v1/transaction_history/get_transaction_count
/v1/transaction_history/get_key_accounts
/v1/transaction_history/get_controlled_accounts
/v1/transaction_history/get_database_stats
/v1/transaction_history/get_performance_metrics
```

| Method | Request fields | Purpose |
| --- | --- | --- |
| `get_transaction` | `id`, optional `block_num_hint` | Indexed transaction, traces, resources, gas data, block and LIB |
| `get_actions` | `account_name`, optional `pos`, `offset` | Indexed account action sequence |
| `get_transaction_count` | optional `start_block`, `end_block` | Count indexed transactions in a block range |
| `get_key_accounts` | `public_key` | Accounts referenced by an indexed public key |
| `get_controlled_accounts` | `controlling_account` | Accounts controlled by an indexed account authority |
| `get_database_stats` | `{}` | History database statistics |
| `get_performance_metrics` | `{}` | History database/cache performance metrics |

The following methods are declared internally but are **not** HTTP RPC routes
in the checked version: `get_optimization_suggestions`, `get_cache_analysis`,
`get_maintenance_needs`, and `trigger_auto_optimize`.

See [[transaction-history-rpc|funod Transaction History RPC]] for pagination,
irreversibility, and examples verified through the Flonscan integration.

## Trace API

Enable:

```ini
plugin = eosio::trace_api_plugin
trace-dir = traces
trace-rpc-abi = CONTRACT=ABI_FILE
```

Alternatively configure `trace-no-abis` when decoded ABI data is not required.

| Path | Request fields | Result |
| --- | --- | --- |
| `/v1/trace_api/get_block` | `block_num` | Retired action traces and related metadata for a retained block |
| `/v1/trace_api/get_transaction_trace` | `id` | Trace for a transaction ID found in retained trace logs |

Missing retained data returns `404`; malformed input returns `400`. Trace
retention is local-node policy and can differ from block-log or history-plugin
retention.

## Net API

Enable:

```ini
plugin = eosio::net_api_plugin
```

| Path | JSON body | Mutability |
| --- | --- | --- |
| `/v1/net/connections` | `{}` | Read all peer connection states |
| `/v1/net/status` | `"host:port"` | Read one peer connection state |
| `/v1/net/connect` | `"host:port"` | Open a P2P connection |
| `/v1/net/disconnect` | `"host:port"` | Close a P2P connection |

Example:

```bash
curl -sS -X POST "$rpc/v1/net/connect" \
  -H 'Content-Type: application/json' \
  --data '"peer.example.org:9876"' | jq
```

`connect` and `disconnect` are node-control operations. Restrict `net_rw` to a
Unix socket or a protected management network.

## Producer and Snapshot API

Enable:

```ini
plugin = eosio::producer_api_plugin
```

The node also needs producer configuration appropriate to its role. Enabling
the API plugin does not by itself make the node an elected producer.

### Read operations

| Path | Request fields | Purpose |
| --- | --- | --- |
| `/v1/producer/paused` | `{}` | Whether local production is paused |
| `/v1/producer/get_runtime_options` | `{}` | Current subjective runtime options |
| `/v1/producer/get_whitelist_blacklist` | `{}` | Actor, contract, action, and key allow/deny configuration |
| `/v1/producer/get_scheduled_protocol_feature_activations` | `{}` | Feature digests scheduled for activation |
| `/v1/producer/get_supported_protocol_features` | optional `exclude_disabled`, `exclude_unactivatable` | Protocol features supported by this binary/configuration |
| `/v1/producer/get_account_ram_corrections` | optional `lower_bound`, `upper_bound`, `limit`, `reverse` | Accounts with RAM correction records |
| `/v1/producer/get_unapplied_transactions` | optional `lower_bound`, `limit`, `time_limit_ms` | Transactions waiting in local unapplied queues |
| `/v1/producer/get_snapshot_requests` | `{}` | Scheduled and pending snapshot requests |

### Write and control operations

| Path | Request fields | Effect |
| --- | --- | --- |
| `/v1/producer/pause` | `{}` | Pause local block production |
| `/v1/producer/resume` | `{}` | Resume local block production |
| `/v1/producer/update_runtime_options` | optional `max_transaction_time`, `max_irreversible_block_age`, `produce_block_offset_ms`, `subjective_cpu_leeway_us` | Change subjective producer runtime limits |
| `/v1/producer/set_whitelist_blacklist` | optional actor/contract/action/key allow/deny arrays | Replace supplied subjective allow/deny settings |
| `/v1/producer/create_snapshot` | `{}` | Create a snapshot asynchronously |
| `/v1/producer/schedule_snapshot` | optional `block_spacing`, `start_block_num`, `end_block_num`, `snapshot_description` | Schedule snapshots |
| `/v1/producer/unschedule_snapshot` | `snapshot_request_id` | Delete a scheduled snapshot request |
| `/v1/producer/get_integrity_hash` | `{}` | Calculate integrity hash at the current head; operationally expensive/control category |
| `/v1/producer/schedule_protocol_feature_activations` | `protocol_features_to_activate` array | Schedule protocol-feature digests for activation |

Snapshot scheduling example:

```json
{
  "block_spacing": 1200,
  "start_block_num": 15000000,
  "end_block_num": 16000000,
  "snapshot_description": "scheduled operational snapshot"
}
```

Protocol-feature activation changes chain behavior once the feature is included
in a produced block. Coordinate binary readiness across producers before using
that endpoint.

### Compile-time greylist routes

These routes exist only when the binary is compiled with
`ENABLE_GREYLIST_LIMIT`; the standard checked build does not define it:

| Path | Request fields | Purpose |
| --- | --- | --- |
| `/v1/producer/get_greylist` | `{}` | Get greylisted accounts |
| `/v1/producer/add_greylist_accounts` | `accounts` array | Add accounts |
| `/v1/producer/remove_greylist_accounts` | `accounts` array | Remove accounts |

Feature-detect them with `get_supported_apis`.

## DB Size API

Enable:

```ini
plugin = eosio::db_size_api_plugin
```

| Path | Body | Result |
| --- | --- | --- |
| `/v1/db_size/get` | `{}` | `free_bytes`, `used_bytes`, total `size`, `reclaimable_bytes`, and row count per index |

This exposes internal database sizing and schema/index names. Keep it on the
monitoring network rather than a public application endpoint.

## Prometheus API

Enable:

```ini
plugin = eosio::prometheus_plugin
```

| Path | Body | Content type |
| --- | --- | --- |
| `/v1/prometheus/metrics` | `{}` | `text/plain` Prometheus exposition format |

Example:

```bash
curl --fail --silent --show-error \
  -X POST "$rpc/v1/prometheus/metrics" \
  -H 'Content-Type: application/json' \
  --data '{}'
```

## Sign Transaction API

Enable both plugins and configure signature providers:

```ini
plugin = eosio::sign_transaction_plugin
plugin = eosio::sign_transaction_api_plugin
```

The following four paths have the same request/response shapes as their Chain
API counterparts:

| Path | Body |
| --- | --- |
| `/v1/sign_transaction/push_transaction` | packed transaction object |
| `/v1/sign_transaction/push_transactions` | array of packed transaction objects |
| `/v1/sign_transaction/send_transaction` | packed transaction object |
| `/v1/sign_transaction/send_transaction2` | `send_transaction2` wrapper |

All four are marked **Unix-socket-only in code**. They are unavailable over TCP
even if the TCP listener exposes the `sign_transaction` category. Configure a
Unix category listener and protect its filesystem permissions:

```ini
http-server-address = http-category-address
http-category-address = chain_ro,127.0.0.1:8888
http-category-address = sign_transaction,./sign-transaction.sock
```

This is a node-integrated signature-provider path, not `fuwal` wallet RPC.

## Test Control API

Enable only on disposable test nodes:

```ini
plugin = eosio::test_control_plugin
plugin = eosio::test_control_api_plugin
```

| Path | Request fields | Effect |
| --- | --- | --- |
| `/v1/test_control/kill_node_on_producer` | `producer`, `where_in_sequence`, `based_on_lib` | Terminate the node at a selected producer sequence for tests |

The actual current route is `kill_node_on_producer`. An older Swagger file
calls it `kill_node_or_producer`; do not use that stale path.

Never expose this category on a production node.

## State History WebSocket API

State History is a binary WebSocket streaming protocol, not HTTP JSON RPC and
does not appear under `/v1/node/get_supported_apis`.

Enable it separately:

```ini
plugin = eosio::state_history_plugin
state-history-endpoint = 127.0.0.1:8080
trace-history = true
chain-state-history = true
finality-data-history = true
```

On connection the server first sends its ABI as text, then switches to binary
messages serialized with that ABI. The current request variants are:

| Request | Important fields / behavior |
| --- | --- |
| `get_status_request_v0` | Get head, LIB, trace/state ranges, and chain ID |
| `get_status_request_v1` | Also reports finality-data range |
| `get_blocks_request_v0` | `start_block_num`, `end_block_num`, `max_messages_in_flight`, `have_positions`, `irreversible_only`, and fetch flags for block/traces/deltas |
| `get_blocks_request_v1` | v0 fields plus `fetch_finality_data` |
| `get_blocks_ack_request_v0` | Return `num_messages` flow-control credits |

The corresponding results are `get_status_result_v0/v1` and
`get_blocks_result_v0/v1`. `end_block_num` is exclusive. Consumers must honor
`max_messages_in_flight`, send acknowledgements, preserve block positions for
fork recovery, and decode binary payloads with the ABI supplied by the server.

Keep the endpoint on an internal network; source configuration explicitly
warns against public exposure.

## Error model and client behavior

Standard JSON errors have this general form:

```json
{
  "code": 400,
  "message": "Invalid Request",
  "error": {
    "code": 0,
    "name": "exception_name",
    "what": "error summary",
    "details": []
  }
}
```

Important statuses:

| HTTP status | Typical meaning |
| --- | --- |
| `200` | Read or simulation completed |
| `201` | Net/Producer operation completed |
| `202` | Transaction, block, or test-control request accepted for processing |
| `400` | Bad JSON, missing field, unknown block, authorization failure, or invalid request |
| `404` | Route/category absent or retained trace/history item unavailable |
| `500` | Chain/plugin exception |
| `503` | HTTP bytes, requests, connections, or history admission limit exceeded |

Client rules:

1. Discover optional routes at startup and cache the capability set briefly.
2. Set request timeouts and bounded concurrency.
3. Retry only transport failures, `429` if introduced by a proxy, and transient
   `503` responses with backoff; do not blindly retry deterministic `400`s.
4. Treat transaction submission as provisional until inclusion is observed.
5. Treat a block as final only when `block_num <= last_irreversible_block_num`.
6. Cache immutable blocks and irreversible transaction details.
7. Never send private keys to Chain, History, Trace, or Flonscan endpoints.

## Coverage summary

The checked source can expose up to 73 logical HTTP operations without the
compile-time greylist feature. The actual node exposes only the enabled and
listener-visible subset:

- 1 Node discovery operation;
- 35 Chain operations, including two conditionally registered routes and one
  always-registered read-only transaction route whose execution requires read
  threads;
- 17 standard Producer/Snapshot operations;
- 7 Transaction History operations, each exposed under two prefixes;
- 4 Net operations;
- 4 Unix-only Sign Transaction operations;
- 2 Trace operations;
- 1 DB Size operation;
- 1 Prometheus operation;
- 1 Test Control operation.

The three compile-time greylist operations raise the maximum logical total to
76 in a custom `ENABLE_GREYLIST_LIMIT` build. The duplicated History aliases
mean the maximum route-path count is 80, or 83 with those greylist routes.

## Verification basis

This guide was checked against:

- `programs/node/CMakeLists.txt` for plugins linked into `funod`;
- each API plugin's route-registration implementation;
- reflected request structures in Chain, Producer, History, State History, and
  Test Control headers;
- HTTP category routing and Unix-socket enforcement;
- the repository Swagger files as a secondary, non-authoritative cross-check.

## Related pages

- [[transaction-history-rpc|funod Transaction History RPC]]
- [[README|Operator and Developer Guides]]
- [[../01_Core_Chain/chain-overview|Chain Overview]]
- [[../05_Glossary/finality|Finality]]
- [FullOn Core source](https://github.com/fullon-labs/flon-core)
