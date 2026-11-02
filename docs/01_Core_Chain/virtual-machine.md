---
title: What is FullOn’s VM?｜虚拟机
status: active
updated: 2026-11-02
source: official FAQ synthesis
---

# What is FullOn’s VM?｜虚拟机

官方 FAQ 描述原生 WASM 与通过 WASM 提供 EVM 类执行；白皮书 v2.6.0 已明确原生 WASM，EVM 相容属于独立整合，不是本次已核实的 Core v0.9.2 套件内第二套 VM。目标网络 EVM 入口与工具链仍需核验，见[规格与差异](../01_Core_Chain/whitepaper.md)。

本站已核验的原生合约开发路径是 C/C++ → CDT → WASM + ABI。官方 FAQ 的一句兼容性描述不足以确认当前网络部署了哪些 EVM 服务、是否开放 Ethereum JSON-RPC 或能否直接使用 Solidity/MetaMask。

开发者请按[合约编译教程](../10_Developer_Guides/build-contract.md)开始；若项目需要 EVM，应先取得目标网络对应实现、地址、接口与工具链说明。

来源：[官方 VM 说明](https://docs.flon.network/fullon-faq/what_are_fullon_virtual_machines)，读取日期 2026-11-02。
