---
title: 开发者指南
type: index
status: active
updated: 2026-11-02
source: source review
---

# 开发者指南

## 接入基础

- [RPC 快速开始](quickstart.md)
- [获取 ABI 与 code](get-abi-code.md)
- [创建 / 激活账户](accounts.md)
- [签名、广播与确认](transactions.md)
- [接入排错](troubleshooting.md)

## 节点与网络

- [Docker Compose 部署节点](docker-compose.md)
- [启动普通节点与 BP 节点](nodes.md)
- [P2P 配置与同步](p2p.md)
- [完整 RPC 参考](../03_Operators/funod-rpc.md)
- [交易历史与分页](../03_Operators/transaction-history-rpc.md)

## 合约与代币

- [编写与编译合约](build-contract.md)
- [部署与升级合约](deploy-contract.md)
- [调用合约动作](call-actions.md)
- [发行新代币](issue-tokens.md)

## 手机钱包

[下载 HuFu 与管理账户](../06_User_Guides/hufu-mobile.md)。手机端操作与钱包 SDK 集成是不同任务；SDK 需使用官方确认的协议。

## 核验范围

新增教程对照 2026-11-02 本地 Core、CDT、系统合约与 RWID 源码；现有 RPC 长篇参考保留 `72cde15a3fb1`（2026-09-03）基线。节点能力需现场发现，源码支持不代表目标网络已经部署。
