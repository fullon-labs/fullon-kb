---
title: How to create / activate an account｜创建与启用账户
type: guide
status: active
updated: 2026-11-02
source: source review
---

# How to create / activate an account｜创建与启用账户

本文的节点、CLI 与 RPC 目标版本为 **FullOn Core v0.9.2**。合约、CDT 和钱包各有独立版本；其已注明的核验范围不因 Core 升级自动改变。详见[版本基线与升级说明](../09_Release_Notes/v0.9.2.md)。

## 前提

需要已有创建者账户、可满足其权限的本地签名钱包、目标网络 RPC、新账户 owner/active 公钥，以及足够的资金/资源。公钥由用户生成并确认；不要收集用户私钥。

下例使用源码已实现的 `fucli system newaccount`。这会提交写交易；请在隔离开发链或已确认的测试网执行，替换所有示例账户、公钥和金额。

```bash
export FULLON_RPC='http://127.0.0.1:8888'
export OWNER_PUBLIC_KEY='REPLACE_WITH_VALID_OWNER_PUBLIC_KEY'
export ACTIVE_PUBLIC_KEY='REPLACE_WITH_VALID_ACTIVE_PUBLIC_KEY'
fucli -u "$FULLON_RPC" system newaccount creatoracct newaccount11   "$OWNER_PUBLIC_KEY" "$ACTIVE_PUBLIC_KEY"   --fund-gas '1.0000 FLON' -p creatoracct@active
fucli -u "$FULLON_RPC" get account newaccount11
```

`1.0000 FLON` 仅用于演示参数格式，**不是开户费或最低 gas 的承诺**。先确认目标链核心资产符号、精度和当前 gas 规则。当前 CLI 要求 `--fund-gas` 或 `--fund-account` 至少一项为正；前者追加买 gas，后者追加核心资产转账，后者不等于一定已购买 gas。

若仅需要原生创建动作，可研究 `fucli create account`，但它不自动完成同样的资金准备，且系统合约可能限制资源和命名。示例使用 12 字符名称；短名、带点名称等有独立规则。

## “激活”是什么意思

先判断实际缺哪一步：链上账户不存在、已创建但钱包未导入、资源不足，还是产品认证尚未完成。当前通用创建路径为 `newaccount`；`fucli system activate` 用于协议特性激活，**不是用户账户激活命令**。

## RWID 创建路径

RWID 不应绕过认证服务直接照抄普通账户创建。参考实现经 auth → DAO → owner → 系统合约调用，并设置特定 owner。服务端需确认管理者权限、认证类型、恢复策略及部署 ABI；见[RWID 账户](../01_Core_Chain/rwid-accounts.md)。

## 完成验证

保存创建交易 ID，确认成功且不可逆，查询账户 owner/active 与资源，然后用用户 active 权限执行一笔受控操作。

## 来源

[CLI 创建参数](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/programs/client/main.cpp)、[命名与资源限制](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.system/src/flon.system.cpp)。
