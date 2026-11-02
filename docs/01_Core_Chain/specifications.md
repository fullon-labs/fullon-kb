---
title: FullOn blockchain specifications｜技术规格
type: core_chain
status: active
updated: 2026-11-02
source: source review
---

# FullOn blockchain specifications｜技术规格

本页区分源码规格和运行网络参数。源码值不等于当前主网配置；性能指标需要测试环境、版本和测量方法支持。

| 项目 | 已确认内容 | 适用范围 |
| --- | --- | --- |
| 实现 | C++ 节点软件 `funod`，工具 `fucli`、`fuwal` | Core 源码与打包说明 |
| 合约 | C/C++ 工具链生成 WASM，ABI 描述动作与表 | 原生开发路径 |
| 共识 | Core 支持 Savanna | 是否启用及策略以目标链为准 |
| 区块间隔 | `block_interval_ms = 500`，即 0.5 秒 | 本次审阅的源码常量；不是最终性耗时承诺 |
| 连续生产 slot | `producer_repetitions = 12` | 源码调度常量，不等于当前 BP 数 |
| 最终性 | 通过 LIB 与最终性策略判断 | 交易成功后等待所在区块不可逆 |
| 账户权限 | owner、active 与 authority | 当前权限用 `get_account` 查询 |
| 资源计量 | 源码含 CPU、NET、RAM 对应 gas 转换参数 | 当前费率与资源状态以链上返回为准 |
| HTTP RPC | JSON 请求，`/v1/*` 路径 | 依赖插件、类别与版本 |
| P2P | 节点间同步和传播，独立于 HTTP RPC | 部署配置决定端口与 peers |
| 历史 | History、Trace、State History 分工 | 依赖 history 构建、插件与保留策略 |

## 白皮书公布的规格

以下来自 v2.5.0 的“技术规格”，与上表的源码核验层次不同：

| 项目 | 白皮书描述 | 应用时的边界 |
| --- | --- | --- |
| 动态产块间隔 | 活跃 0.5 秒，闲置最长 12 秒 | 与 500ms slot 常量分别理解，运行策略另核验 |
| 最终性 | 1–1.5 秒 | 白皮书声明，非本次实测；业务仍以 LIB 确认 |
| 吞吐量 | 10,000+ TPS，单线程 | 需负载与环境证据；并行/分片扩展另见路线图 |
| 共识 | DPoS + Savanna | 目标链的排班、策略及激活状态另核验 |
| VM | 原生 WASM + 声称 100% 兼容的 EVM | EVM 入口、部署和工具链未由本文验证 |
| 原生资产 | FLON；总量计划 100 亿 | 不等于当前发行量或流通量 |

来源与差异见[白皮书整合](whitepaper.md)。[资源模型](resource-model.md)、[代币经济](tokenomics.md)、[治理](governance.md)及[扩展路线](roadmap.md)补充详细解释。

## 如何获得目标网络的实际参数

- `get_info`：chain ID、节点版本、head、LIB，以及该版本提供的资源字段。
- `get_consensus_parameters`：链配置和可用的 WASM 参数。
- `get_producer_schedule`：活动、待定和拟议出块排班。
- `get_finalizer_info`：节点提供的 finalizer 策略与信息。
- `get_supported_apis`：确认上述接口在当前节点是否可用。

调用方法见[RPC 快速开始](../10_Developer_Guides/quickstart.md)。同一条链的多个节点也可能使用不同版本和索引配置。

## 尚未作为当前网络规格确认的内容

主网/测试网 chain ID、当前 BP 数、实时 gas 费率、实际最终性延迟、TPS、生产节点最低硬件配置和公共 P2P 种子列表，需要网络级核验。本文不把源码容量上限或注释中的估算当作性能实测。

## 来源

[源码常量](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/libraries/chain/include/eosio/chain/config.hpp)、[Core README](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/README.md)、[节点角色与打包](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/docs/node-build-profiles.md)。审阅日期：2026-11-02。
