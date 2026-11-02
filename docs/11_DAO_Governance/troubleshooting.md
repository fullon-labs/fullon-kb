---
title: DAO 常见问题与排错
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# DAO 常见问题与排错

| 问题 | 检查与处理 |
| --- | --- |
| POWER 是可交易代币吗？ | 不是。不能通过转账 POWER 购买票权，也不会因投票被扣除。 |
| 钱包有 FLON，为什么不能提案？ | 液态余额不等于治理权；检查当前 powers、风险等级门槛及网络。 |
| 有当前 POWER 却不能投票？ | 必须在 vote_start / vote_end 窗口，并在 activate 快照有票权；每账户只投一次。 |
| 附议达到人数，为什么仍不能 activate？ | 附议期必须结束，还需全网总量、个人和累计 POWER 比例、风险规则均满足。 |
| 已附议还要再投票吗？ | 要。附议不是正式赞成票，正式投票期需单独操作。 |
| 能改票吗？ | 核验版本拒绝重复投票，没有改票入口；签名前确认选择。 |
| 100% 赞成为什么没通过？ | 还需 Quorum 和绝对支持率；决定票分母不包含弃权。 |
| 已通过为什么没有执行？ | 信号提案无自动执行；可执行提案还需 queue、Timelock、窗口与当前策略。 |
| 为什么不能选择某个 action？ | 它可能不在该网络启用的 actpolicies/allowlist 中；不能照搬测试网列表。 |
| BP 分配合计报错？ | 核验源码要求合计等于目标锁定本金，各项正数、唯一排序，最多 30 个。 |
| 改了 BP 投票，排名没变？ | 检查 pending、生效 Epoch、排班和节点资格，避免重复广播。 |
| 预算已 reserve，却没收到币？ | reserve 只是预留；只有合法 pay 会实际支付到记录受益人。 |
| closegrant 失败？ | 核验源码仅允许仍 open 且严格已过期的 grant；不是通用已完成项目关闭命令。 |
| 找不到 standbyproof？ | 本次主网 ABI 没有该动作；该运维流程依赖支持的版本。 |
| 钱包网络错误/签名不弹出？ | 核对 Chain ID、账户与会话；重连或在正确钱包环境重开，未确认链上结果前别重复提交。 |

## 求助资料

提供网络与 Chain ID、公开账户、提案/grant/Epoch ID、交易 ID、时间与时区、脱敏错误、预期结果。附上当时配置或快照来源。不要提交私钥、助记词、验证码、密码或带凭据的链接。

[提案流程](proposals.md) · [当前查询方式](developer-reference.md) · [参数与快照](rules-and-parameters.md)

## 来源与范围

[源码、查询快照与资料差异](sources.md)。实现说明基于所列提交；运行配置以目标网络当前状态为准。
