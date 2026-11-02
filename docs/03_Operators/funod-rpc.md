---
title: funod RPC 完整参考
type: developer_guide
status: verified
updated: 2026-09-03
source: official
translation_of: 03_Operators/funod-rpc.md
translated: '2026-11-02'
---

# funod RPC 完整参考

## 范围与源码基线

本目录覆盖核验时 FullOn Core `v0.8.0-alpha` 中链接到 `funod` 的插件所注册的全部 HTTP 路径，包括可用条件、请求字段、响应用途、读写属性，以及独立的 State History 二进制 WebSocket 协议。它不是 `/v1/*` JSON 接口。

基线为 2026-09-03 的 `72cde15a3fb1`，依据实际注册代码，不只依赖 Swagger。部分 Swagger 尚未列全接口。`fuwal` 是独立程序，其钱包 RPC 不在本页范围。翻译不改变原核验日期，也不代表当前部署全部符合此基线。

## 发现实际可用接口

```bash
curl --fail --silent --show-error \
  'http://127.0.0.1:8888/v1/node/get_supported_apis' | jq
```

`get_supported_apis` 只返回当前 TCP/Unix 监听器可见的路径。路径缺失可能因插件未启用、当前监听器未暴露类别、附加功能开关未开、仅允许 Unix socket，或节点版本较旧。

## 调用约定

```text
POST http://HOST:PORT/v1/<api>/<method>
Content-Type: application/json
```

无参数方法发送 `{}`。Net 的字符串参数须用 JSON 字符串，例如 `"peer.example.org:9876"`，不能改成对象。通常读接口返回 `200`，交易提交返回 `202`，Net 和多数 Producer 接口返回 `201`，各方法另有说明时除外。

```bash
rpc=http://127.0.0.1:8888

curl --fail --silent --show-error \
  -X POST "$rpc/v1/chain/get_info" \
  -H 'Content-Type: application/json' \
  --data '{}' | jq
```

核验版本的 HTTP 分发未强制请求动词；客户端应统一使用 `POST` 保持兼容。`OPTIONS` 处理 CORS 预检。CORS 头属于节点配置，不能视为协议保证。

## 插件与类别

| API 组 | 所需插件 | 类别 | 暴露建议 |
| --- | --- | --- | --- |
| Node discovery | `eosio::http_plugin` | `node` | 公开或内部 |
| Chain read | `eosio::chain_api_plugin` | `chain_ro` | 公开并限流 |
| Chain write | `eosio::chain_api_plugin` | `chain_rw` | 公开交易网关或受保护入口 |
| Network read/write | `eosio::net_api_plugin` | `net_ro`, `net_rw` | 仅内部，写接口保持私有 |
| Producer read/write | `eosio::producer_api_plugin` | `producer_ro`, `producer_rw` | 仅内部 |
| Snapshot control | `eosio::producer_api_plugin` | `snapshot` | 仅内部 |
| Chain database size | `eosio::db_size_api_plugin` | `db_size` | 仅监控网络 |
| Trace API | `eosio::trace_api_plugin` | `trace_api` | 索引/查询节点，并限流 |
| Transaction history | `eosio::transaction_history_api_plugin` | `history_ro` | 索引/查询节点，并限流 |
| Prometheus | `eosio::prometheus_plugin` | `prometheus` | 仅监控网络 |
| Local signing gateway | `eosio::sign_transaction_api_plugin` | `sign_transaction` | 仅 Unix socket |
| Test control | `eosio::test_control_api_plugin` | `test_control` | 仅测试节点 |

普通 `http-server-address` 会暴露所有已启用类别。生产部署应分离读取与特权控制监听器：

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

不要将 `net_rw`、`producer_rw`、`snapshot`、`test_control` 或签名类别直接暴露公网。

`chain_plugin`、`net_plugin`、`producer_plugin`、`signature_provider_plugin`、`transaction_history_plugin`、`sign_transaction_plugin` 为 API 插件提供功能，本身不独立注册 `/v1/*`。`resource_monitor_plugin` 监控磁盘，也没有客户端 RPC。`state_history_plugin` 提供独立 WebSocket。

## 节点发现 API

| 路径 | 请求体 | 结果 |
| --- | --- | --- |
| `/v1/node/get_supported_apis` | 无 | 监听器可见路径，按序排列 |

此路径由 `http_plugin` 直接提供，但不会把自身放入返回的 `apis` 数组。

## Chain API

```ini
plugin = eosio::chain_api_plugin
```

### 链状态、区块与最终性

| 路径 | 请求字段 | 用途与可用性 |
| --- | --- | --- |
| `/v1/chain/get_info` | `{}` | 节点版本、chain ID、head、LIB、资源限额、gas 费率和最早可用区块 |
| `/v1/chain/get_block` | `block_num_or_id` | ABI 解码后的签名区块 |
| `/v1/chain/get_raw_block` | `block_num_or_id` | 原始签名区块 |
| `/v1/chain/get_block_info` | `block_num` | 按区块号获取精简元数据 |
| `/v1/chain/get_block_header` | `block_num_or_id`, 可选 `include_extensions` | 签名区块头与可选扩展 |
| `/v1/chain/get_block_header_state` | `block_num_or_id` | 旧式区块头状态，部分保留范围可能不可用 |
| `/v1/chain/get_transaction_status` | `id` | 交易追踪状态与最终性，仅在启用最终性状态存储时注册 |
| `/v1/chain/get_finalizer_info` | `{}` | 活动/待定 finalizer 策略与最近追踪投票 |
| `/v1/chain/get_consensus_parameters` | `{}` | 链配置与可选 WASM 配置 |

`get_info` 虽由 Chain API 实现，却使用通用 `node` 类别，可在每个配置的 HTTP 监听器上访问。

```bash
curl -sS -X POST "$rpc/v1/chain/get_block" \
  -H 'Content-Type: application/json' \
  --data '{"block_num_or_id":"14415393"}' | jq

curl -sS -X POST "$rpc/v1/chain/get_transaction_status" \
  -H 'Content-Type: application/json' \
  --data '{"id":"TRANSACTION_ID"}' | jq
```

非零存储限制启用有条件的交易状态接口：

```ini
transaction-finality-status-max-storage-size-gb = 1
```

这是有界最终性追踪，不是永久历史记录。

### 账户、代码与 ABI

| 路径 | 请求字段 | 用途 |
| --- | --- | --- |
| `/v1/chain/get_account` | `account_name` | 账户元数据、权限、余额、gas 与资源状态 |
| `/v1/chain/get_code` | `account_name`, 可选 `code_as_wasm` | 已部署代码哈希、WASM/WAST 与 ABI |
| `/v1/chain/get_code_hash` | `account_name` | 仅已部署代码哈希 |
| `/v1/chain/get_abi` | `account_name` | 解码后的 ABI |
| `/v1/chain/get_raw_code_and_abi` | `account_name` | 原始 WASM 与 ABI 二进制数据 |
| `/v1/chain/get_raw_abi` | `account_name`, 可选 `abi_hash` | ABI 哈希与数据，可用于缓存校验 |
| `/v1/chain/get_accounts_by_authorizers` | `accounts`, `keys` | 按指定权限或公钥查询可满足的权限，仅开启账户查询时注册 |

```bash
curl -sS -X POST "$rpc/v1/chain/get_account" \
  -H 'Content-Type: application/json' \
  --data '{"account_name":"numguessgame"}' | jq
```

`get_accounts_by_authorizers` 输入示例：

```json
{
  "accounts": ["alice", {"actor": "bob", "permission": "active"}],
  "keys": ["PUB_K1_..."]
}
```

该接口需要开启账户查询：

```ini
enable-account-queries = true
```

### 合约表与代币数据

| 路径 | 请求字段 | 用途 |
| --- | --- | --- |
| `/v1/chain/get_table_rows` | `code`, `scope`, `table`, plus options below | 读取主索引或次索引的行 |
| `/v1/chain/get_table_by_scope` | `code`, 可选 `table`, bounds/options | 枚举包含某表的 scope |
| `/v1/chain/get_currency_balance` | `code`, `account`, 可选 `symbol` | 账户代币余额 |
| `/v1/chain/get_currency_stats` | `code`, `symbol` | 供应量、最大供应量与 issuer |

`get_table_rows` 字段：

| 字段 | 必填 | 默认值 / 含义 |
| --- | --- | --- |
| `code` | 是 | 合约账户 |
| `scope` | 是 | 以字符串表示的 scope |
| `table` | 是 | 表名 |
| `json` | 否 | 默认 `false`，用 `true` 获取 ABI 解码行 |
| `table_key` | 否 | 旧式表键提示 |
| `lower_bound`, `upper_bound` | 否 | 索引边界 |
| `limit` | 否 | 默认 `10` |
| `key_type` | 否 | 索引类型，如 `i64`、`i128`、`i256`、`float64`、`float128`、`sha256`、`ripemd160` |
| `index_position` | 否 | `1`/`primary`、`2`/`secondary` 等 |
| `encode_type` | 否 | 默认 `dec`，支持时可用 `hex` |
| `reverse` | 否 | 反向遍历索引 |
| `show_payer` | 否 | 包含各行 RAM 付款者 |
| `time_limit_ms` | 否 | 单次查询时限，受节点配置限制 |

分页检查 `more` 和 `next_key`，下一页将 `next_key` 作为 `lower_bound`。不能仅以 `rows.length < limit` 判断结束。

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

### 生产者、协议特性与延迟交易

| 路径 | 请求字段 | 用途 |
| --- | --- | --- |
| `/v1/chain/get_producers` | 可选 `json`, `lower_bound`, `limit`, `time_limit_ms` | 生产者记录与总投票权重 |
| `/v1/chain/get_producer_schedule` | `{}` | 活动、待定和拟议生产者排班 |
| `/v1/chain/get_activated_protocol_features` | 可选 `lower_bound`, `upper_bound`, `limit`, `search_by_block_num`, `reverse`, `time_limit_ms` | 已激活协议特性的历史 |
| `/v1/chain/get_scheduled_transactions` | 可选 `json`, `lower_bound`, `limit`, `time_limit_ms` | 延迟交易队列 |

`get_activated_protocol_features` 默认边界是激活序号；`search_by_block_num: true` 时按区块号。

### ABI 转换与授权准备

| 路径 | 请求字段 | 用途 |
| --- | --- | --- |
| `/v1/chain/abi_json_to_bin` | `code`, `action`, `args` | 按当前 ABI 序列化 JSON 动作数据 |
| `/v1/chain/abi_bin_to_json` | `code`, `action`, `binargs` | 按当前 ABI 解码动作二进制 |
| `/v1/chain/get_required_keys` | `transaction`, `available_keys` | 判断可用公钥中哪些满足交易授权 |
| `/v1/chain/get_transaction_id` | unpacked transaction object | 计算交易 ID，不提交 |

ABI 转换使用节点当前可见的 ABI。序列化动作数据变化后必须重建并重新签名。

### 模拟与提交交易

| 路径 | 请求结构 | 行为 |
| --- | --- | --- |
| `/v1/chain/compute_transaction` | `{ "transaction": <packed-or-unpacked-transaction> }` | 执行以检查计算/结果，不作常规提交 |
| `/v1/chain/send_read_only_transaction` | `{ "transaction": <packed-or-unpacked-transaction> }` | 执行只读交易，所有 Chain API 节点均注册 |
| `/v1/chain/push_transaction` | packed transaction object | 旧式单笔提交 |
| `/v1/chain/push_transactions` | array of packed transaction objects | 旧式批量提交 |
| `/v1/chain/send_transaction` | packed transaction object | 提交单笔交易 |
| `/v1/chain/send_transaction2` | wrapper described below | 支持重试/失败 trace 控制，适合高级接入 |
| `/v1/chain/push_block` | signed block object | 注入区块，仅特权运维使用 |

`send_transaction2` 请求包装：

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

`retry_trx_num_blocks` 只在 `retry_trx` 为 true 时有意义。提交还要求 `api-accept-transactions = true`。HTTP `202` 只代表接受处理，需继续核对执行、包含区块和 LIB。

`push_transactions` 逐笔处理，不是原子批次。`send_read_only_transaction` 虽始终注册，执行仍要求 `read-only-threads > 0`，否则返回不支持错误。

## Transaction History API

```ini
plugin = eosio::transaction_history_plugin
plugin = eosio::transaction_history_api_plugin
```

每个方法都有两个等价前缀：

```text
/v1/history/<method>
/v1/transaction_history/<method>
```

兼容旧节点优先 `/v1/history/*`。完整注册路径：

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

| 方法 | 请求字段 | 用途 |
| --- | --- | --- |
| `get_transaction` | `id`, 可选 `block_num_hint` | 索引交易、trace、资源、gas、所在区块与 LIB |
| `get_actions` | `account_name`, 可选 `pos`, `offset` | 账户动作索引序列 |
| `get_transaction_count` | 可选 `start_block`, `end_block` | 统计区块范围内索引交易数 |
| `get_key_accounts` | `public_key` | 索引公钥关联账户 |
| `get_controlled_accounts` | `controlling_account` | 索引账户权限控制的账户 |
| `get_database_stats` | `{}` | 历史数据库统计 |
| `get_performance_metrics` | `{}` | 历史数据库/缓存性能指标 |

头文件内部声明的 `get_optimization_suggestions`、`get_cache_analysis`、`get_maintenance_needs`、`trigger_auto_optimize` 没有注册为 HTTP RPC。

分页、不可逆状态与 Flonscan 消费示例见[交易历史参考](transaction-history-rpc.md)。

## Trace API

```ini
plugin = eosio::trace_api_plugin
trace-dir = traces
trace-rpc-abi = CONTRACT=ABI_FILE
```

不需要 ABI 解码时可配置 `trace-no-abis`。

| 路径 | 请求字段 | 结果 |
| --- | --- | --- |
| `/v1/trace_api/get_block` | `block_num` | 保留区块中已处理动作的 trace 与元数据 |
| `/v1/trace_api/get_transaction_trace` | `id` | 按交易 ID 查保留 trace 日志 |

保留数据不存在返回 `404`，格式错误返回 `400`。Trace 保留策略独立于 block log 与 History 索引策略。

## Net API

```ini
plugin = eosio::net_api_plugin
```

| 路径 | JSON 请求体 | 读写行为 |
| --- | --- | --- |
| `/v1/net/connections` | `{}` | 读取所有 peer 连接状态 |
| `/v1/net/status` | `"host:port"` | 读取单个 peer 状态 |
| `/v1/net/connect` | `"host:port"` | 建立 P2P 连接 |
| `/v1/net/disconnect` | `"host:port"` | 关闭 P2P 连接 |

```bash
curl -sS -X POST "$rpc/v1/net/connect" \
  -H 'Content-Type: application/json' \
  --data '"peer.example.org:9876"' | jq
```

`connect`、`disconnect` 会控制节点；将 `net_rw` 限制在 Unix socket 或受保护的管理网络。

## Producer 与 Snapshot API

```ini
plugin = eosio::producer_api_plugin
```

节点还需符合角色要求的生产配置。启用 API 插件不代表成为已入选生产者。

### 读取

| 路径 | 请求字段 | 用途 |
| --- | --- | --- |
| `/v1/producer/paused` | `{}` | 本地是否暂停生产 |
| `/v1/producer/get_runtime_options` | `{}` | 当前主观运行选项 |
| `/v1/producer/get_whitelist_blacklist` | `{}` | actor、合约、动作、公钥的允许/拒绝配置 |
| `/v1/producer/get_scheduled_protocol_feature_activations` | `{}` | 已安排激活的特性摘要 |
| `/v1/producer/get_supported_protocol_features` | 可选 `exclude_disabled`, `exclude_unactivatable` | 此二进制/配置支持的特性 |
| `/v1/producer/get_account_ram_corrections` | 可选 `lower_bound`, `upper_bound`, `limit`, `reverse` | 包含 RAM 修正记录的账户 |
| `/v1/producer/get_unapplied_transactions` | 可选 `lower_bound`, `limit`, `time_limit_ms` | 本地未应用队列中的交易 |
| `/v1/producer/get_snapshot_requests` | `{}` | 已安排与待处理的快照请求 |

### 写入与控制

| 路径 | 请求字段 | 效果 |
| --- | --- | --- |
| `/v1/producer/pause` | `{}` | 暂停本地产块 |
| `/v1/producer/resume` | `{}` | 恢复本地产块 |
| `/v1/producer/update_runtime_options` | 可选 `max_transaction_time`, `max_irreversible_block_age`, `produce_block_offset_ms`, `subjective_cpu_leeway_us` | 修改生产者主观运行限制 |
| `/v1/producer/set_whitelist_blacklist` | 可选 actor/contract/action/key allow/deny arrays | 替换所提供的主观允许/拒绝设置 |
| `/v1/producer/create_snapshot` | `{}` | 异步创建快照 |
| `/v1/producer/schedule_snapshot` | 可选 `block_spacing`, `start_block_num`, `end_block_num`, `snapshot_description` | 安排快照 |
| `/v1/producer/unschedule_snapshot` | `snapshot_request_id` | 取消已安排的快照请求 |
| `/v1/producer/get_integrity_hash` | `{}` | 计算当前 head 完整性哈希，开销较大，属于控制类别 |
| `/v1/producer/schedule_protocol_feature_activations` | `protocol_features_to_activate` array | 安排协议特性摘要激活 |

快照安排示例：

```json
{
  "block_spacing": 1200,
  "start_block_num": 15000000,
  "end_block_num": 16000000,
  "snapshot_description": "scheduled operational snapshot"
}
```

协议特性包含进生产区块后会改变链行为；激活前需协调各生产者二进制的支持情况。

### 编译期开关的灰名单接口

下列接口只在定义 `ENABLE_GREYLIST_LIMIT` 的自定义构建中存在；核验标准构建未定义它。

| 路径 | 请求字段 | 用途 |
| --- | --- | --- |
| `/v1/producer/get_greylist` | `{}` | 查询灰名单账户 |
| `/v1/producer/add_greylist_accounts` | `accounts` array | 添加账户 |
| `/v1/producer/remove_greylist_accounts` | `accounts` array | 移除账户 |

用 `get_supported_apis` 探测。

## 数据库大小

```ini
plugin = eosio::db_size_api_plugin
```

| 路径 | 请求体 | 结果 |
| --- | --- | --- |
| `/v1/db_size/get` | `{}` | `free_bytes`、`used_bytes`、总 `size`、`reclaimable_bytes` 与各索引行数 |

会暴露内部数据库大小和索引/模式信息，应仅供监控网络访问。

## Prometheus

```ini
plugin = eosio::prometheus_plugin
```

| 路径 | 请求体 | Content type |
| --- | --- | --- |
| `/v1/prometheus/metrics` | `{}` | `text/plain` Prometheus 格式 |

```bash
curl --fail --silent --show-error \
  -X POST "$rpc/v1/prometheus/metrics" \
  -H 'Content-Type: application/json' \
  --data '{}'
```

## 本地签名网关

```ini
plugin = eosio::sign_transaction_plugin
plugin = eosio::sign_transaction_api_plugin
```

需配置签名提供者。请求/响应结构对应 Chain API 同名方法：

| 路径 | 请求体 |
| --- | --- |
| `/v1/sign_transaction/push_transaction` | packed transaction 对象 |
| `/v1/sign_transaction/push_transactions` | packed transaction 对象数组 |
| `/v1/sign_transaction/send_transaction` | packed transaction 对象 |
| `/v1/sign_transaction/send_transaction2` | `send_transaction2` 包装对象 |

四个路径在代码中均仅允许 Unix socket，即使 TCP 暴露签名类别也不能访问。保护 socket 文件权限：

```ini
http-server-address = http-category-address
http-category-address = chain_ro,127.0.0.1:8888
http-category-address = sign_transaction,./sign-transaction.sock
```

这是节点集成签名提供者入口，不是 `fuwal` 钱包 RPC。

## Test Control API

只在可丢弃测试节点启用：

```ini
plugin = eosio::test_control_plugin
plugin = eosio::test_control_api_plugin
```

| 路径 | 请求字段 | 效果 |
| --- | --- | --- |
| `/v1/test_control/kill_node_on_producer` | `producer`, `where_in_sequence`, `based_on_lib` | 在指定生产者序列处终止节点，仅用于测试 |

正确路径是 `kill_node_on_producer`。旧 Swagger 的 `kill_node_or_producer` 已过时。不能将此类别暴露生产网络。

## State History WebSocket

State History 为二进制 WebSocket 协议，不会列入 `get_supported_apis`。

```ini
plugin = eosio::state_history_plugin
state-history-endpoint = 127.0.0.1:8080
trace-history = true
chain-state-history = true
finality-data-history = true
```

连接后服务先发送文本 ABI，再按该 ABI 序列化二进制消息。

| 请求 | 重要字段 / 行为 |
| --- | --- |
| `get_status_request_v0` | 查询 head、LIB、trace/state 范围与 chain ID |
| `get_status_request_v1` | 额外报告最终性数据范围 |
| `get_blocks_request_v0` | `start_block_num`、`end_block_num`、`max_messages_in_flight`、`have_positions`、`irreversible_only` 与 block/trace/delta 获取开关 |
| `get_blocks_request_v1` | v0 字段加 `fetch_finality_data` |
| `get_blocks_ack_request_v0` | 返还 `num_messages` 流控额度 |

响应变体为 `get_status_result_v0/v1` 和 `get_blocks_result_v0/v1`。`end_block_num` 为不包含的上界。消费者需遵守 `max_messages_in_flight`、发送确认、保存位置用于分叉恢复，并使用服务端 ABI 解码。该服务应限制在内部网络，源码也明确警告不要公开暴露。

## 错误与客户端行为

标准错误结构：

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

| HTTP 状态 | 常见含义 |
| --- | --- |
| `200` | 读取或模拟完成 |
| `201` | Net/Producer 操作完成 |
| `202` | 交易、区块或测试控制请求已接受处理 |
| `400` | JSON 错误、缺字段、未知区块、授权失败或无效请求 |
| `404` | 路径/类别不存在，或保留 trace/history 数据不可用 |
| `500` | 链或插件异常 |
| `503` | HTTP 字节、请求、连接或历史准入限额超限 |

1. 启动时发现可选接口，短暂缓存能力清单。
2. 使用超时与有界并发。
3. 仅对传输失败、代理可能引入的 `429`、临时 `503` 退避重试，不盲目重试确定性 `400`。
4. 提交后先确认包含和执行结果。
5. `block_num <= last_irreversible_block_num` 才视为不可逆。
6. 缓存不再变化的区块与不可逆交易。
7. 不向 Chain、History、Trace、Flonscan 发送私钥。

## 覆盖统计

不含编译期灰名单时最多 73 个逻辑 HTTP 操作：发现 1、Chain 35、Producer/Snapshot 17、History 7（各两个前缀）、Net 4、Unix 签名 4、Trace 2、DB Size 1、Prometheus 1、Test Control 1。Chain 包含两个条件注册接口和一个注册但需只读线程才能执行的接口。

灰名单另加 3 个操作，总计最多 76。计入 History 别名后，路径数最多 80，含灰名单为 83。实际节点只暴露启用且当前监听器可见的子集。

## 核验依据

`programs/node/CMakeLists.txt` 的插件链接、API 路径注册、Chain/Producer/History/State History/Test Control 请求反射结构、HTTP 类别与 Unix 限制，及作为次要交叉核对的 Swagger。均以原始 `72cde15a3fb1` 基线为准。

[交易历史](transaction-history-rpc.md) · [参考入口](README.md) · [链概览](../01_Core_Chain/chain-overview.md) · [最终性](../05_Glossary/finality.md) · [Core 源码](https://github.com/fullon-labs/flon-core)
