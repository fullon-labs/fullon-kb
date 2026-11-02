---
title: 扩展路线与尚待验证的能力
status: active
updated: 2026-11-02
source: whitepaper v2.4.0 synthesis
---

# 扩展路线与尚待验证的能力

本文整理白皮书 v2.4.0（2026-10-22）的协议设计，不代表本次已验证各网络部署。

白皮书的架构与路线图需要与当前可用产品分开阅读。

| 方向 | 白皮书描述 | 如何理解 |
| --- | --- | --- |
| 单线程执行 | 10,000+ TPS | 性能声明，仍需测试环境、版本与负载证据 |
| 并行执行 | 以 10 线程举例扩展至 100,000 TPS | 路线图方向，非本次验证的部署能力 |
| 多分片 | 状态分片进一步扩展至百万 TPS | 路线图方向，非当前吞吐保证 |
| L2/侧链 | 面向特定应用或与其他生态连接 | 架构可能性，不等于对应网络已上线 |
| 同步 WASM 内联调用 | 增强可组合性 | 白皮书列为后续研究功能 |
| BP 集群 | 提升可用性与韧性 | 运维方向，不构成多实例同时签名授权 |
| 基础设施与市场 | 身份信用、存储、DNS/CDN、资产与 AI 市场 | 生态规划，需要逐产品确认可用性 |

节点硬件最低值、已部署分片数、具体 EVM 服务、钱包协议以及公共节点 SLA 没有由这些愿景自动确定。开发接入应从已核验的[RPC](../10_Developer_Guides/quickstart.md)和[WASM 合约路径](../10_Developer_Guides/contracts.md)开始。

[技术规格](specifications.md) · [白皮书整合与差异](whitepaper.md)

## 来源

[中文白皮书](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.cn.md) · [English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.md) · [核验范围与资料冲突](whitepaper.md)。固定提交 `f49e5f0f821162a997260535be30767e3f147d8e`；读取日期 2026-11-02。
