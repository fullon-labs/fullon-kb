---
title: RPC 快速开始：读取链上数据
type: guide
status: active
updated: 2026-11-02
source: repository synthesis
---

# RPC 快速开始：读取链上数据

目标：用只读请求确认网络、账户、资产与合约状态。

## 准备

需要 `curl` 和 `jq`，以及由网络运营方提供的 RPC 地址和可信的预期 chain ID。仓库尚未维护经当前核验的主网/测试网配置表，不要通过域名猜测网络。

下例默认访问本机节点；接入远程网络前替换 `FULLON_RPC`，并通过独立可信来源取得该网络的 chain ID。

```bash
export FULLON_RPC='http://127.0.0.1:8888'
curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_info"   -H 'Content-Type: application/json' --data '{}' | jq
```

核对 `chain_id`、节点版本、head 与 `last_irreversible_block_num`。单次响应只能说明当前状态；持续观察区块推进和节点延迟后再用于业务。

## 发现节点能力

```bash
curl --fail --silent --show-error --max-time 15   "$FULLON_RPC/v1/node/get_supported_apis" | jq '.apis'
```

可用接口取决于节点版本、插件和监听器类别；历史接口不属于每个节点的必备能力。

## 读取账户

将 `YOUR_ACCOUNT` 替换为目标网络存在的账户。

```bash
curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_account"   -H 'Content-Type: application/json'   --data '{"account_name":"YOUR_ACCOUNT"}' | jq
```

读取权限用账户接口；不要把历史公钥索引当作当前授权依据。

## 读取资产与合约表

以下全大写字符串均为占位符，必须依据目标网络合约 ABI 和实际部署替换。

```bash
curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_currency_balance"   -H 'Content-Type: application/json'   --data '{"code":"TOKEN_CONTRACT","account":"YOUR_ACCOUNT","symbol":"TOKEN_SYMBOL"}' | jq

curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_table_rows"   -H 'Content-Type: application/json'   --data '{"json":true,"code":"CONTRACT","scope":"SCOPE","table":"TABLE","limit":20}' | jq
```

资产身份包括网络、合约、符号和精度。表的 `scope`、索引和字段由合约定义；分页检查 `more` 和 `next_key`，不要仅用返回行数判断结束。

## 下一步

查询历史使用[历史 API](../03_Operators/transaction-history-rpc.md)；提交交易先阅读[交易生命周期](transactions.md)。完整参数与条件见[RPC 参考](../03_Operators/funod-rpc.md)。
