---
title: 智能合约开发路径
type: index
status: active
updated: 2026-11-02
source: source review
---

# 智能合约开发路径

本文的节点、CLI 与 RPC 目标版本为 **FullOn Core v0.9.2**。合约、CDT 和钱包各有独立版本；其已注明的核验范围不因 Core 升级自动改变。详见[版本基线与升级说明](../09_Release_Notes/v0.9.2.md)。

按可执行教程依次完成：

1. [编写与编译](build-contract.md)：最小 C++ 合约与 WASM/ABI 产物。
2. [读取 ABI 与 code](get-abi-code.md)：核对接口和链上代码。
3. [部署与升级](deploy-contract.md)：发布 WASM/ABI，核验哈希和权限。
4. [调用动作](call-actions.md)：CLI 调用、授权和应用集成。
5. [发行代币](issue-tokens.md)：最大供应量、issuer、分发与余额核对。

命令参数已对照本地源码。最小合约单独编译验证；链上写命令没有在生产网络执行。工具链、系统合约和网络版本须匹配。
