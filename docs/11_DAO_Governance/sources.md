---
title: 治理帮助来源、核验与资料差异
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# 治理帮助来源、核验与资料差异

## 已整合的资料

- [DAO DApp README](https://github.com/fullon-labs/flon.daogov/blob/93aadcf3c8421cd4ae9228696c9501196dd8febb/README.md)：钱包、BP、提案和讨论入口。
- [治理用户帮助](https://github.com/fullon-labs/flon.daogov/blob/93aadcf3c8421cd4ae9228696c9501196dd8febb/docs/governance-help.md)：治理权、阶段、风险和奖励。
- [日常运维指南](https://github.com/fullon-labs/flon.daogov/blob/93aadcf3c8421cd4ae9228696c9501196dd8febb/docs/operations-guide.md)与[Keeper 说明](https://github.com/fullon-labs/flon.daogov/blob/93aadcf3c8421cd4ae9228696c9501196dd8febb/keeper/README.md)：新版本角色和运维边界。
- [前端阶段推导](https://github.com/fullon-labs/flon.daogov/blob/93aadcf3c8421cd4ae9228696c9501196dd8febb/src/governance.js)：用于解释界面，不代替链上校验。
- [DAO 源码](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/dao.gov/src/dao.gov.cpp)与[接口/表结构](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/dao.gov/include/dao.gov/dao.gov.hpp)。
- [Treasury 源码](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/dao.treasury/src/dao.treasury.cpp)、[BP 投票实现](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.system/src/voting.cpp)、[奖励领取](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.system/src/producer_pay.cpp)。
- [2026-11-02 主网只读响应与代码哈希](mainnet-snapshot.json)，及[对应解释](rules-and-parameters.md)。

本地还阅读了 2026-11-01 的主网运行草稿；它尚未在 DApp 仓库提交，且部分数值已过时，所以没有作为当前配置直接发布。

## 如何处理差异

| 资料表述 | 核验结果与本文处理 |
| --- | --- |
| 旧帮助：投票分配合计不超过本金 | 所列 system 源码要求合计等于目标锁定本金，指南明确这一约束。 |
| 旧帮助：reserve 减少 liquid / release 恢复 liquid | Treasury 源码中 reserve 只增加 reserved，release 只减少 reserved；可用余额是 liquid - reserved。 |
| closegrant 可关闭已完成或已释放 grant | 所列源码只接收 open 且已过期 grant；完成/释放已是其他终态。 |
| Keeper 推动外部 closeepoch | 新运维指南描述 onblock 自动封存，Keeper 只代领奖励；按部署版本核验。 |
| 新运维指南存在 standbyproof | 本次主网 ABI 无此动作；条件化说明，不能当成已上线命令。 |
| 11 月 1 日主网白名单为空、门槛较高 | 11 月 2 日查询已有 5 条启用规则，门槛已变化；发布带日期快照而非静态“当前值”。 |
| 附议 POWER 与正式投票都取同一快照 | 源码附议时累加当时票权；activate 未逐账户重算，正式票权才读取激活检查点。 |
| 创建提案时保存完整逐动作授权 | proposal_action 只保存目标/动作/bytes；授权来自 allowlist，既有规则授权在核验版本中不可修改，并在执行时重新检查。 |

## 核验边界

本次只读查询验证网络 ID、表状态、代码哈希和 ABI 中的动作存在性。它不是协议审计、节点活性审计或源码到部署 WASM 的可复现构建证明。分开读取不保证同一区块原子一致，快照数值随时间变化；主网与测试网必须独立确认。
