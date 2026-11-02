---
title: DAO Gov 治理帮助
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# DAO Gov 治理帮助

[打开 FullOn DAO Gov](https://daogov.flon.network/)。先确认站点、钱包和 RPC 属于同一网络。本文按用户、开发者与运营人员的任务组织 DApp 帮助和合约规则。

## 普通用户

1. [入门与治理权](getting-started.md)：连接钱包、区分 FLON 与 POWER。
2. [提案、附议、投票与执行](proposals.md)：从讨论到最终执行。
3. [BP 投票与奖励](bp-voting-rewards.md)：锁定本金、分配、pending 与领取。
4. [Treasury 与预算](treasury.md)：预留、付款、释放与到期关闭。
5. [常见问题](troubleshooting.md)。

## 规则与网络

[治理门槛和主网参数快照](rules-and-parameters.md)：L1–L4、三项通过条件、时长、白名单及上线边界。快照不是实时状态，测试网数值不能当作主网规则。

## 开发者与节点运营人员

- [DAO 合约接入](developer-reference.md)：表、scope、ABI、动作和状态机。
- [Keeper 与 Standby 运维](operations.md)：自动封存、代领奖励与节点本人在线证明。
- [资料来源与核验](sources.md)。

## 先分清这三件事

| 行为 | 目的 | 是否直接执行提案业务动作 |
| --- | --- | --- |
| 给 BP 分配 FLON 投票本金 | 节点选择与奖励归属 | 否 |
| DAO 附议/正式投票 | 决定提案能否获授权 | 否 |
| 已通过提案的 execute | 执行冻结且仍符合策略的动作 | 是，可能改变参数或转移 Treasury 资产 |

POWER 不是用于交易的 Token；附议不是赞成票；通过不是立即执行。
