---
title: 创建提案、附议、正式投票与执行
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# 创建提案、附议、正式投票与执行

## 创建前准备

先讨论目标、理由、预期影响和可核验的执行结果。页面可把社区讨论预填为提案，但讨论或论坛点赞不是链上附议/投票。记录正文 URI 与 SHA-256，核对正文与链上哈希一致。

- **信号提案**：不携带 actions，表达社区意见；即使通过也不会自动调用业务合约，不能进入执行队列。源码将空 action 提案按 L1 检查，仍需满足已启用风险规则。
- **可执行提案**：包含冻结的目标合约、动作名和参数 bytes。每个动作需在启用的 `actpolicies` 与 `allowlist` 中，且满足数量/字节上限。多动作按最高风险等级处理。

1. 检查提案人当前 POWER、风险门槛与网络。信号提案也不是零门槛留言。
2. 填写标题、摘要、正文 URI、内容哈希及讨论链接。可执行提案逐项检查 ABI 解码后的动作、参数、目标权限和实际收款人。
3. 签署 `propose`，保存交易与提案 ID，确认不可逆后再邀请附议。

## 附议与正式投票

附议只表示值得进入正式投票，不等于赞成执行。附议账户需满足个人门槛，且只能附议一次；提案还需满足独立账户数量和累计附议 POWER 比例。

附议期结束后才能 `activate`；达到人数不代表能提前激活。激活时检查全网 POWER 和风险规则，并冻结票权序号、总量、投票窗口及通过条件。激活后先等待 `vote_start`。

正式投票用 `castvote`：反对 `0`、赞成 `1`、弃权 `2`。每个账户每个提案只能投一次，核验版本没有改票动作。附议人仍需在正式投票期单独投票，也可以投反对或弃权。截止时间为 `now < vote_end`。

## 状态推进

| 阶段 | 操作 | 完成后应核对 |
| --- | --- | --- |
| 附议期 | endorse；提案人可 cancel | 附议记录/人数或 cancelled |
| 附议结束 | activate | 快照序号、总 POWER、vote_start / vote_end |
| 投票截止 | finalize | 三项门槛均满足才 succeeded，否则 defeated |
| 可执行提案通过 | queue | execute_after / execute_before |
| Timelock 到期 | execute | 执行交易、目标表/收款结果与不可逆状态 |
| 执行窗口已过 | expire | expired；未执行冻结动作 |

`activate`、`finalize`、`queue`、`execute`、`expire` 不要求提案人身份，但仍是交易，须符合阶段、时间、策略和 gas 要求。提案人仅在附议阶段可取消；讨论链接也仅可在该阶段由提案人更新，不能把此能力当成可修改冻结的正文哈希或 action。

## Timelock 与最终执行

Timelock 从成功 `queue` 时起算，不能继续投票或替换参数。合约允许在 `execute_after <= now <= execute_before` 执行；严格超过 `execute_before` 才能过期。前端倒计时是提示，链上时间与校验才决定交易可否成功。

queue 与 execute 会再次校验当前白名单、风险策略和大小限制。投票通过不保证之后一定可执行；禁用策略、目标权限/代码变化或业务条件不满足都可能阻止执行。调用者不能任意替换冻结动作或收款人。实际执行授权来自对应 allowlist 规则，详见[开发参考](developer-reference.md)。

通过比例、弃权的计算和快照注意事项见[规则与参数](rules-and-parameters.md)。

## 来源与范围

[源码、查询快照与资料差异](sources.md)。实现说明基于所列提交；运行配置以目标网络当前状态为准。
