---
title: 网络与入口
type: core_chain
status: active
updated: 2026-11-02
source: source review
---

# 网络与入口

接入任何服务前确认目标网络。主网与测试网资产、账户状态、合约部署和交易历史彼此独立。

| 入口 | 用途 | 核验要求 |
| --- | --- | --- |
| [HuFu](https://hufu.io) | 手机钱包入口 | 核对下载来源、发行方与钱包所选网络 |
| [Flonscan](https://flonscan.io) | 浏览账户与交易 | 确认页面所选网络 |
| [FullSwap](https://fullswap.flon.network) | 代币兑换入口 | 核对应用网络、代币合约和交易参数 |
| [Core releases](https://github.com/fullon-labs/flon-core/releases) | 节点和工具包 | 选择与目标网络兼容的版本 |

以上产品地址来自仓库资料；不能据此保证当前服务可用性。历史 RPC 指南记录的 `https://m.flonscan.io` 仅是历史核验入口，不应直接视作当前 SLA 或默认主网配置。

## 校验网络

开发者从运营方或官方配置取得预期 chain ID，再用 `get_info.chain_id` 比较。只读取同一未知节点的 chain ID 然后信任它，不能完成独立核验。

用户核对钱包网络、收款服务网络和浏览器网络。跨链时来源链与目标链要分别确认。

[RPC 接入](../10_Developer_Guides/quickstart.md) · [P2P](../10_Developer_Guides/p2p.md) · [技术规格](specifications.md)
