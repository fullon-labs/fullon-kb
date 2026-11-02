---
title: DAO 入门与 POWER 治理权
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# DAO 入门与 POWER 治理权

## 连接与检查

1. 从[官方 DAO Gov 入口](https://daogov.flon.network/)进入。手机可使用 HuFu 内打开的 DApp；普通浏览器按页面提供的连接方式操作，二维码或钱包回调是否可用以当前版本为准。
2. 确认网络和完整 Chain ID，连接正确账户。主网与测试网会话不能混用；切换网络/账户后重新核对。
3. 在页面读取账户治理权、节点投票本金、待生效分配、提案阶段及当前规则。仅查看数据无需把私钥交给网站。
4. 首次签名前核对合约、action、参数和权限；保存交易 ID 并等待[不可逆确认](../06_User_Guides/transaction-status.md)。

## FLON 与 POWER

FLON 是参与锁定和资产操作的代币；POWER 是 `dao.gov` 内部治理账本。`powers` 保存账户票权，`global.total_power` 为总量，`checkpoints` 记录变更。POWER 不可转账、支付或交易，创建提案、附议和正式投票不会扣除 POWER；提交交易仍可能需要 gas。

系统源码在增加/减少节点投票本金时调用 `setpower` 写入目标本金对应的治理权。节点分配的 pending 生效时间与 DAO 提案 `activate` 冻结票权的时刻是不同概念，不能把“下个 Epoch 生效”套用到所有治理状态。

普通用户不能直接给自己增发 POWER；`setpower` 只接受配置的 `power_source` 授权。新锁定或新取得的 POWER 不能追溯增加已激活提案的快照票权。

## 选择下一步

- 想参与节点选择：[BP 投票与奖励](bp-voting-rewards.md)。
- 想参与某个提案：[提案流程](proposals.md)。
- 想申请社区预算：[Treasury](treasury.md)。
- 按钮不可用或显示零票权：[排错](troubleshooting.md)，先查网络、当前 POWER 和提案快照，不要重复支付或提高权限。

## 来源与范围

[源码、查询快照与资料差异](sources.md)。实现说明基于所列提交；运行配置以目标网络当前状态为准。
