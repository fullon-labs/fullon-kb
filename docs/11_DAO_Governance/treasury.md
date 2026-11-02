---
title: Treasury 资产、预算与付款
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# Treasury 资产、预算与付款

Treasury 的“提案通过”“预算已预留”和“已付款”是三个不同结果。付款前要核对对应提案、grant、代币合约、精度、收款人、金额、次数和到期时间。

## 生命周期与账目

| 动作 | 含义 | 账目/资产变化 |
| --- | --- | --- |
| setasset | 治理授权资产配置 | 按合约与完整符号启用资产；不是发行 Token |
| 入金 transfer 通知 | 接收已启用的资产 | liquid 与 total_received 增加 |
| reserve | 创建绑定 proposal_id 的 grant | reserved 增加，liquid 不减少，不发生外部付款 |
| pay | 从 grant 分期支付 | liquid 与 reserved 同时减少，paid / total_paid 增加，实际转给记录中的 recipient |
| release | 释放全部剩余未支付预留 | reserved 减少，liquid 不变，grant 记为 released；无外部付款 |
| closegrant | 关闭仍 open 且已过期的 grant | 释放剩余 reserved，记为 expired；不是任意关闭任何已完成 grant 的通用动作 |

可新预留金额为 `liquid - reserved`，不能把 liquid 与 reserved 相加当总资产，也不能把 reserved 当已付款。grant 剩余金额为 `total - paid - released`。

grant 的 proposal_id 是引用标识，不能仅凭编号认定预算已获得批准。核验源码的 reserve 只要求编号为正，不会跨合约查询该提案是否通过；审计时需关联真实治理执行交易。

## 用户核对步骤

1. 查看 Treasury 资产白名单是否启用目标合约与精度；未启用时不要尝试直接充值。
2. 预算提案说明受益人、用途、总量、最多付款次数、到期时间及凭证哈希。
3. 通过并执行 reserve 后，记录 grant_id；此时尚未到账给受益人。
4. 每次 pay 都需合法治理授权，受剩余预算、次数和到期限制。普通用户不能通过知道 grant_id 任意提款。
5. 付款后核对代币转账 trace、grant paid、支付记录和余额；等待不可逆。
6. 不再使用的预算按授权 release；过期仍 open 的 grant 可由任何账户调用 closegrant 释放余量。已过期 grant 不能继续 pay。

[主网快照](rules-and-parameters.md)中 Treasury 资产表为空；即使 reserve/pay 已有治理白名单，也不代表已有可用资产或预算。白名单状态随时可能变化，应重读。

## 来源与范围

[源码、查询快照与资料差异](sources.md)。实现说明基于所列提交；运行配置以目标网络当前状态为准。
