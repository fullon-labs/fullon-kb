---
title: How to get ABI / code｜读取合约接口与 WASM
type: guide
status: active
updated: 2026-11-02
source: source review
---

# How to get ABI / code｜读取合约接口与 WASM

本文的节点、CLI 与 RPC 目标版本为 **FullOn Core v0.9.2**。合约、CDT 和钱包各有独立版本；其已注明的核验范围不因 Core 升级自动改变。详见[版本基线与升级说明](../09_Release_Notes/v0.9.2.md)。

ABI 是动作和数据结构的接口描述；WASM 是已部署的可执行字节码。获取 WASM 不能还原原始 C++ 源码，也不能证明某个 Git 仓库就是部署来源。

## 前提

安装 `flon-tools` 的 `fucli`，准备经核对的 RPC 地址。以下 `contractacct` 是占位账户名，需替换。所有示例为只读请求。

```bash
export FULLON_RPC='http://127.0.0.1:8888'
fucli -u "$FULLON_RPC" get abi contractacct -f contract.abi
fucli -u "$FULLON_RPC" get code contractacct -c contract.wasm -a contract.abi
```

`get code` 会输出 code hash；只有加 `-c` 才将 WASM 保存到文件。`get abi -f` 保存解码后的 ABI。

## 通过 HTTP RPC

```bash
curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_abi"   -H 'Content-Type: application/json'   --data '{"account_name":"contractacct"}' | jq '.abi'

curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_code_hash"   -H 'Content-Type: application/json'   --data '{"account_name":"contractacct"}' | jq
```

需要原始数据时使用 `get_raw_code_and_abi` 或 `get_raw_abi`，字段类型和编码见[RPC 参考](../03_Operators/funod-rpc.md)。不要把 JSON 中的编码字符串直接保存成二进制 WASM。

## 验证和缓存

核对 chain ID 与账户名，记录 code hash、ABI 和读取时间。不同请求不是同一状态的原子快照；升级期间应重新核对哈希。ABI 变化后需重新序列化并签名交易。账户可能尚无代码或 ABI，查询失败不一定是节点故障。

## 来源

[fucli get code / get abi 参数与实现](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/programs/client/main.cpp)，源码审阅：2026-11-02。
