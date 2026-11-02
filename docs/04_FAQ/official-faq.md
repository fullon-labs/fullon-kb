---
title: 官方 FullOn FAQ 内容整合
status: active
updated: 2026-11-02
source: official FAQ synthesis
---

# 官方 FullOn FAQ 内容整合

官方 FAQ 的 8 个主题已整合为本站正文。点击下表即可在 GitHub Pages 内阅读，无需跳转原站。原始内容读取于 2026-11-02；历史或目标性描述不作为当前部署保证。

| 官方条目 | 读取到的内容 | 本站整合位置 |
| --- | --- | --- |
| [What is FullOn](what-is-fullon.md) | L1、扩展性、低延迟、快速最终性、互操作性定位 | [FullOn 是什么](what-is-fullon.md) |
| [Basic properties](../01_Core_Chain/specifications.md) | 只有标题，无规格正文 | [源码规格与待确认项](../01_Core_Chain/specifications.md) |
| [Account types](account-types.md) | native & sovereign、proxy、social-recoverable、simple address；简单地址分 WASM/EVM 管理 | [账户类型](account-types.md)与[账户基础](../01_Core_Chain/accounts.md) |
| [Resource model](resource-model.md) | 只有标题 | [资源模型](resource-model.md)，补充源码与查询路径 |
| [Tokenomics](tokenomics.md) | 只有标题 | [代币经济](tokenomics.md)，明确数据缺口 |
| [VM](vm.md) | 原生 WASM，以及通过 WASM 支持 EVM 类执行的描述 | [虚拟机](vm.md)，注明兼容性边界 |
| [Interoperability](interoperability.md) | 只有标题 | [互操作性](interoperability.md)，与具体跨链应用分开 |
| [Ecosystems](../02_Ecosystems/README.md) | Web3、AI、Social 三方向的愿景与应用场景 | [生态概览](../02_Ecosystems/README.md) |

## 差异与保留

- 原 FAQ 的“快速最终性”没有给出数值；本站 0.5 秒来自源码区块间隔，不能当作最终性延迟。
- 原 FAQ 的账户分类没有提供完整操作或所有实现细节；RWID 权限机制另外根据合约源码说明，不假设它与所有社交恢复方案相同。
- 原 FAQ 的 EVM 类执行描述不足以证明当前公共节点兼容 Ethereum JSON-RPC、MetaMask 或 Solidity 工具链。
- 原 FAQ 的资源、代币经济和互操作性页面当前无正文；本站不捏造固定费用、供应量、收益或桥协议。
- 生态页中的未来方向与合作愿景不等于每项产品均已上线。

源文件的 URL、内容 SHA-256 和读取状态保存在[核验记录](../contributing/faq-source-manifest.json)，便于后续判断来源是否变化。

## 来源引用

[原始官方 FAQ](https://docs.flon.network/fullon-faq) · [读取核验记录](../contributing/faq-source-manifest.json)。这些链接仅用于追溯来源；上方阅读入口均为本站页面。
