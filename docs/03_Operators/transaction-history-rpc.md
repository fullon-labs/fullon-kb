---
title: funod 交易历史 RPC
type: developer_guide
status: verified
updated: 2026-09-03
source: official
translation_of: 03_Operators/transaction-history-rpc.md
translated: '2026-11-02'
---

# funod 交易历史 RPC

## 用途与范围

本页扩展[完整 RPC 参考](funod-rpc.md)中的交易历史部分，只讨论原生 `funod` RPC。Flonscan 源码和实际调用用作消费侧证据；浏览器私有应用 API 不属于原生 RPC 协议。

可查询账户动作、按交易 ID 获取交易及 trace、公钥到账户和控制关系索引、区块交易数，以及本地历史数据库健康。历史数据是节点维护的索引；当前账户、余额、权限和合约表应查询 `/v1/chain/*`。

## 启用与探测

```ini
plugin = eosio::transaction_history_plugin
plugin = eosio::transaction_history_api_plugin
```

两种前缀注册相同处理器：

```text
/v1/history/*
/v1/transaction_history/*
```

兼容旧节点优先 `/v1/history/*`。使用新方法或长别名前先检查能力：

```bash
rpc=http://127.0.0.1:8888

curl -sS "$rpc/v1/node/get_supported_apis" | jq \
  '.apis[] | select(test("^/v1/(history|transaction_history)/"))'
```

全部位于 `history_ro` 类别。共享准入控制的源码默认值：

```ini
http-max-history-requests-in-flight = 4
http-history-requests-per-second = 5
```

按容量调整，但两项都须大于零。

## 方法列表

| 方法 | 请求 | 主要结果 |
| --- | --- | --- |
| `get_transaction` | `id`，可选 `block_num_hint` | 索引交易、trace、资源/gas、区块与 LIB |
| `get_actions` | `account_name`，可选 `pos`、`offset` | 动作序列、LIB、分页标志 |
| `get_transaction_count` | 可选 `start_block`、`end_block` | 数量与实际范围 |
| `get_key_accounts` | `public_key` | `account_names` |
| `get_controlled_accounts` | `controlling_account` | `controlled_accounts` |
| `get_database_stats` | `{}` | `success`、数据库 `stats`、可选 `error` |
| `get_performance_metrics` | `{}` | `success`、性能 `metrics`、可选 `error` |

插件头文件声明的 `get_optimization_suggestions`、`get_cache_analysis`、`get_maintenance_needs`、`trigger_auto_optimize` 未注册为 HTTP RPC。

## 查询账户动作

```text
POST /v1/history/get_actions
```

| 字段 | 类型 | 必填 | 含义 |
| --- | --- | --- | --- |
| `account_name` | string | 是 | 查询该账户接收或授权的动作 |
| `pos` | 有符号整数 | 否 | 动作序列游标，`-1` 从最新开始 |
| `offset` | 有符号整数 | 否 | 负数向后、正数向前、零不返回行 |

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

| 结果字段 | 含义 |
| --- | --- |
| `actions` | 动作记录，含账户/全局序号、区块元数据和 `action_trace` |
| `last_irreversible_block` | 此响应观察到的 LIB |
| `more` | 是否还有匹配历史，旧节点可能缺失 |
| `time_limit_exceeded_error` | 扫描是否因时限停止，旧节点可能缺失 |

返回的是动作列表，不是唯一交易列表。一笔交易可产生多个顶层和内联动作；产品需要显示交易时才按 `action_trace.trx_id` 分组。

### 向后分页

1. 用 `pos: -1` 和负 `offset` 请求。
2. 找到返回的最小 `account_action_seq`。
3. 减一作为下一页 `pos`。
4. 保持负 `offset`。
5. 空页停止；当前节点还可按 `more: false` 停止。

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

旧实现可能包含 `pos` 边界并多返回一行；按实际序号推进，并以 `account_action_seq` 去重，不假设固定页长。若超时标志为 true，保留已有行，从序号继续并减小页大小。

### 不可逆判定

```ts
const irreversible = action.block_num <= response.last_irreversible_block;
```

高于 LIB 的动作仍可逆，分叉后可能消失。

## 查询交易

```text
POST /v1/history/get_transaction
```

为保持兼容，发送完整 64 位十六进制 ID：

```bash
curl --fail --silent --show-error \
  -X POST "$rpc/v1/history/get_transaction" \
  -H 'Content-Type: application/json' \
  --data '{"id":"TRANSACTION_ID"}' | jq
```

已知所在区块时可提供提示以减少查找工作：

```json
{
  "id": "TRANSACTION_ID",
  "block_num_hint": 14415393
}
```

| 字段 | 含义 |
| --- | --- |
| `id` | 交易 ID |
| `trx` | 索引的回执与交易数据 |
| `block_time` | 区块时间戳 |
| `block_num` | 所在区块号 |
| `last_irreversible_block` | 查询时节点 LIB |
| `traces` | 顶层与内联动作 trace |
| `res_usage` | 记录的资源使用量 |
| `gas_traces` | 记录的 gas trace |

当前实现接受至少八位且无歧义的十六进制前缀，但公开客户端应继续使用完整 ID。

## 按区块范围计数

```text
POST /v1/history/get_transaction_count
```

```bash
curl -sS -X POST "$rpc/v1/history/get_transaction_count" \
  -H 'Content-Type: application/json' \
  --data '{"start_block":14415000,"end_block":14416000}' | jq
```

两个边界均可选；返回 `count`、`start_block`、`end_block`，包含实现选择的有效范围。旧节点即使支持动作/交易查询，也可能没有计数方法。

## 权限关系索引

按公钥查询：

```bash
curl -sS -X POST "$rpc/v1/history/get_key_accounts" \
  -H 'Content-Type: application/json' \
  --data '{"public_key":"PUB_K1_..."}' | jq
```

按控制账户查询：

```bash
curl -sS -X POST "$rpc/v1/history/get_controlled_accounts" \
  -H 'Content-Type: application/json' \
  --data '{"controlling_account":"alice"}' | jq
```

这些是历史索引结果。授权或签名前仍需用 `/v1/chain/get_account` 核对当前权限。

## 数据库健康

```bash
curl -sS -X POST "$rpc/v1/history/get_database_stats" \
  -H 'Content-Type: application/json' --data '{}' | jq

curl -sS -X POST "$rpc/v1/history/get_performance_metrics" \
  -H 'Content-Type: application/json' --data '{}' | jq
```

两方法返回 `success`、插件定义数据对象和可选 `error`。嵌套指标属于运维诊断，不是稳定 DApp 业务 schema；监控应容忍字段增加。

## TypeScript 客户端

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

不向历史服务发送钱包凭据、私钥或签名材料。示例公共地址属于下述历史核验记录，不是当前服务承诺。

## Flonscan 消费证据

核验时检查了 Flonscan：旧账户动作入口代理 `get_actions`，交易查询代理 `get_transaction`；当前浏览器页面也可使用自己的索引 API，后者不是 `funod` RPC 结构。

2026-09-03 曾通过 `https://m.flonscan.io` 验证主网动作/交易查询，该节点当时报告 `v0.6.6`，未提供长前缀别名和 `get_transaction_count`。此记录不是当前部署状态。始终探测能力，不将源码支持等同于上线。

## 运维说明

- `404 Unknown Endpoint`：当前监听器/版本不支持插件、别名、类别或方法。
- 空历史：检查网络、本地索引/保留和账户过滤。
- 交易不存在：使用完整 ID，已知区块时提供 `block_num_hint`。
- `503`：历史并发或令牌桶限流饱和，使用有界指数退避。
- 区块不可逆后缓存不可变交易详情。
- 历史索引可落后于 head；结算与授权应读取 Chain API 当前状态。

## 核验依据

原核验针对 `72cde15a3fb1` 的历史路径注册和请求反射、HTTP 准入控制、Flonscan 消费代码及 2026-09-03 主网响应。翻译保留此范围和日期。

[完整 RPC](funod-rpc.md) · [参考入口](README.md) · [最终性](../05_Glossary/finality.md) · [Core](https://github.com/fullon-labs/flon-core) · [Flonscan](https://flonscan.io)
