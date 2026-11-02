---
title: How to deploy a smart contract｜部署与升级
type: guide
status: active
updated: 2026-11-02
source: source review
---

# How to deploy a smart contract｜部署与升级

本文的节点、CLI 与 RPC 目标版本为 **FullOn Core v0.9.2**。合约、CDT 和钱包各有独立版本；其已注明的核验范围不因 Core 升级自动改变。详见[版本基线与升级说明](../09_Release_Notes/v0.9.2.md)。

## 前提

已生成 WASM/ABI，有目标网络的合约账户、足够资源和可满足该账户部署权限的签名钱包。下例会修改链上代码；先在隔离开发链或测试网执行，`contractacct` 必须替换。

```bash
export FULLON_RPC='http://127.0.0.1:8888'
fucli -u "$FULLON_RPC" get account contractacct
fucli -u "$FULLON_RPC" set contract contractacct ./build   hello.wasm hello.abi -p contractacct@active
fucli -u "$FULLON_RPC" get code contractacct -c deployed.wasm -a deployed.abi
```

`set contract` 中 WASM/ABI 文件名相对于 `./build`。`active` 是否足够以该账户实际权限与动作绑定为准；不要为让示例通过而随意改 owner。

## 验收

保存部署交易 ID，确认执行成功与不可逆；将下载代码的哈希与本地 WASM 比较，检查 ABI 动作和表定义，再调用一次受控动作。合约名称 `hello` 与部署账户名可以不同。

## 升级

升级前保存旧 WASM、ABI、哈希、权限和业务数据迁移方案。升级代码不会自动重置已有表；代码回滚也不会自动回滚数据。

`eosio.code` 只应在确有合约内联授权需求时按最小范围设置。部署一个普通 hello 合约无需因为教程习惯而授予额外权限。

[获取 ABI / code](get-abi-code.md) · [调用动作](call-actions.md)

## 来源

[fucli set contract 参数](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/programs/client/main.cpp)，源码审阅：2026-11-02。
