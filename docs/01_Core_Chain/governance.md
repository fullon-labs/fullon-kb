---
title: 治理权与 BP 资格
status: active
updated: 2026-11-02
source: whitepaper v2.6.0 Core v0.9.2 baseline and policy clarification draft
---

# 治理权与 BP 资格

本文整理白皮书 v2.6.0 澄清稿（2026-11-02）的协议设计，不代表本次已验证各网络部署。

## DAO 提案与治理权

白皮书描述的生命周期为：草稿 → 附议 → 投票 → 定案 → 时间锁 → 执行。协议参数、国库拨款和合约控制动作需可审计；高风险动作受执行白名单与较长时间锁约束。

锁定 FLON 参与 BP 投票时，合约在账户内部账本记录等额治理权。治理权不是另行发行的代币，不可转让、支付或交易，也不代表股权、分红或固定收益。减少或退出投票本金会调整账户可用治理权；已激活提案仍使用其冻结的治理权快照，不涉及另一种代币的发行或销毁。

BP 选举与 DAO 提案共用锁定基础，但动作、门槛和执行路径分开。白皮书允许每账户最多选 30 个 BP，并把票权平均分配给所选候选人，不因多选放大总票权。

## 普通节点、Active 和 Standby

| 角色 | 白皮书职责/资格 | 奖励设计 |
| --- | --- | --- |
| 普通同步或 RPC 节点 | 校验、同步或服务应用；不自动进入生产排班 | 不因运行节点而自动获得 BP 奖励 |
| Active BP | 进入活动排班并满足生产/绩效条件 | 合格生产挖矿 + Active GAS 池，可按规则分享给投票人 |
| Standby BP | 保持在线、完成 proof 并具备递补资格 | 独立的 Standby GAS 可用性奖励，无固定挖矿份额 |

白皮书目标为 21 个 Active 和 30 个 Standby；启动阶段 Active 数可在 3–21 范围逐步扩大。候选人的自有质押、公开资料、有效密钥和绩效都影响资格，不能只凭排名或运行程序判断已成为出块 BP。

## Epoch、表现与恢复

- 建议奖励 epoch 为 6 小时，即 43,200 个 0.5 秒 slot；这是 slot 计账设计，不可简单乘以动态实际产块间隔来推算。
- epoch 内投票从下一排名 epoch 生效；奖励按产生期间历史票权归属，延后领取不改变所有权。
- `get_producer_slot_stats_v2` 按 `expected = produced + missed` 统计；`idle_skipped` 不进入可用率分母，也不算漏块。
- 样本不足或全网事故先保护，再考虑个体停权与 Standby 递补。
- 冷却后的授权恢复、试运行、具体门槛及奖励池处理以生效系统合约和治理配置为准，不能由 Core 版本直接推断。
- 普通下线首先影响奖励和资格；本金罚没仅针对可客观验证的安全违规。具体门槛以目标链实现和治理配置核验。

本文不提供未验证的报名金额、质押锁定期或生产命令。参与前查询当前合约、排班、治理参数及权限，再按正式操作指南执行。

[节点启动](../10_Developer_Guides/nodes.md) · [挖矿与 GAS 奖励](tokenomics.md)

## 来源

[中文白皮书](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.cn.md) · [English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.md) · [核验范围与资料冲突](whitepaper.md)。固定提交 `5758318eba75d48afd1d543bf020255c1a998d26`；读取日期 2026-11-02。Core v0.9.2 基线已发布；未来发行/GAS 政策澄清仍在独立草稿中，不能标作已部署规则。
