---
title: What is FullOn’s resource model?｜资源模型
status: active
updated: 2026-11-02
source: official FAQ synthesis
---

# What is FullOn’s resource model?｜资源模型

官方 FAQ 对应页面目前仅有标题，没有资源规则正文。不能从该页得出固定转账费、免费额度或资源单价。

当前 Core 源码包含 CPU、NET、RAM 对应的 gas 转换参数；应用应读取目标网络实际返回的账户资源和节点信息。源码默认值与运行网络费率要分开。

用户按钱包当前显示处理资源不足；开发者见[创建账户与 gas](../10_Developer_Guides/accounts.md)、[技术规格](../01_Core_Chain/specifications.md)和[RPC 参考](../03_Operators/funod-rpc.md)。

来源：[官方资源模型页面](https://docs.flon.network/fullon-faq/what_is_fullon_resource_model)，读取日期 2026-11-02；源码核验见技术规格页。
