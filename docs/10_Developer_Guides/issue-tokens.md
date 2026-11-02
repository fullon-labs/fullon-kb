---
title: How to issue new tokens｜发行代币
type: guide
status: active
updated: 2026-11-02
source: source review
---

# How to issue new tokens｜发行代币

本文的节点、CLI 与 RPC 目标版本为 **FullOn Core v0.9.2**。合约、CDT 和钱包各有独立版本；其已注明的核验范围不因 Core 升级自动改变。详见[版本基线与升级说明](../09_Release_Notes/v0.9.2.md)。

目标：在你控制的合约账户部署标准代币逻辑，创建符号、发行到 issuer，再分发给用户。

## 先区分三个账户

- **代币合约账户**：托管代码和代币表；示例 `tokenexample`。
- **issuer**：被允许增发该符号的账户；示例 `issueracct`。
- **持有人**：接收/转移代币的账户；示例 `holderacct`。

不能随意使用他人的 `flon.token` 创建新币。参考实现的 `create` 要求代币合约自身授权。先在你控制的账户部署已审查的 token WASM/ABI，见[部署教程](deploy-contract.md)。

## 创建、发行与转账

下列命令均会提交交易，应先在隔离开发链或测试网执行。账户均为占位符，且假定已部署与下述源码行为一致的 token 合约。

```bash
export FULLON_RPC='http://127.0.0.1:8888'
fucli -u "$FULLON_RPC" push action tokenexample create   '{"issuer":"issueracct","maximum_supply":"1000000.0000 DEMO"}'   -p tokenexample@active

fucli -u "$FULLON_RPC" push action tokenexample issue   '{"to":"issueracct","quantity":"1000.0000 DEMO","memo":"initial issue"}'   -p issueracct@active

fucli -u "$FULLON_RPC" push action tokenexample transfer   '{"from":"issueracct","to":"holderacct","quantity":"10.0000 DEMO","memo":"distribution"}'   -p issueracct@active
```

`DEMO` 与四位小数是示例。`create` 设置最大供应量和精度，不等于已增发。当前参考 `issue` 要求 `to` 是 issuer，金额为正、精度一致且不超过剩余可发行量，因此发行给 issuer 后再转出。

## 读取并核对

```bash
curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_currency_stats"   -H 'Content-Type: application/json'   --data '{"code":"tokenexample","symbol":"DEMO"}' | jq

curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_currency_balance"   -H 'Content-Type: application/json'   --data '{"code":"tokenexample","account":"holderacct","symbol":"DEMO"}' | jq
```

确认 max_supply、supply、issuer 和余额，以及每笔交易成功且不可逆。资产身份由网络、合约、符号和精度共同确定。

## 发行之后

钱包展示、浏览器图标、FullSwap 交易对和流动性都是独立流程，发行不等于自动上架。先公开代币合约、发行/升级权限和用途，再按相关应用的当前流程申请集成。

## 来源

[token create / issue / transfer 实现](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.token/src/flon.token.cpp)、[接口定义](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.token/include/flon.token/flon.token.hpp)。源码审阅：2026-11-02；不代表在任何生产网络发行了代币。
