---
title: BP 投票、本金与奖励
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# BP 投票、本金与奖励

DAO 提案投票与 BP 投票是两个流程。BP 分配用于节点选择及奖励归属；正式 DAO 票权由提案快照决定。

## 锁定与分配

1. 核对账户、网络、可用 FLON、已锁定本金和待生效投票。
2. 增加本金会涉及 `flon::addvote` 等实际资产动作，先确认金额、权限及当前规则。钱包液态余额不会因显示在页面上就自动变成已锁定票。
3. 选择最多 30 个 BP，分别指定份额。源码 `votealloc` 要求每项为正、BP 唯一且排序，合计**等于**该账户当前目标锁定本金；DApp 应负责构造合法列表。
4. 确认签名后查询 pending 与生效 Epoch，不要因当前排名未立刻更新而反复提交。
5. 在目标 Epoch 后核对实际分配与奖励归属。节点 active 注册资格、界面 Active/Standby 排名和实际出块排班不能仅凭名称等同。

## 减少本金与退出

减少节点投票本金、调整 BP 分配、取回投票退款以及 BP 自质押退出是不同操作。源码的 `subvote` 建立退款记录，并受选举状态、已有退款等限制；`voterefund` 需等待退款成熟。不要把“取消选择 BP”理解成立即到账退款。

具体退款时长与 BP 自质押 `unstake_delay_sec` 不应混用，以目标合约和当前记录为准。已有提案的正式投票权仍按激活快照，不随之后减少本金追溯变化。

## 奖励领取

| 对象 | 动作 | 谁授权 / 收款 |
| --- | --- | --- |
| 投票人 | `voter.reward::claimrewards` | 受益账户本人授权，核对当前 ABI |
| BP | `flon::claimrewards(caller, producer, max_steps)` | BP 或第三方触发；款项固定给 producer |

奖励先形成链上待领取记录，并非自动空投；可跨 Epoch 累积，不代表固定收益。领取后确认交易不可逆，并核对待领取记录与余额。页面“无数据”或 RPC 失败不能解释成奖励一定为零。

公共 Keeper 只帮助代领 BP 奖励，不能替未授权的 Standby BP 提交在线证明。更多见[运维指南](operations.md)。

## 来源与范围

[源码、查询快照与资料差异](sources.md)。实现说明基于所列提交；运行配置以目标网络当前状态为准。
