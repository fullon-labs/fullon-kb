---
title: Keeper、BP 奖励与 Standby 运维
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# Keeper、BP 奖励与 Standby 运维

## 先确认版本，不能照抄运维动作

DApp 的新版运维指南描述：Epoch 封存和内部结算由 `onblock` 有界推进，公共 Keeper 负责辅助拉取 BP 奖励，不再通过外部 closeepoch/beginsettle/settlenext/finalizeepoch 驱动结算。这是该指南对应版本的职责划分，不能据此认定任何节点已升级。

**本次主网 ABI 查询结果：** `flon::claimrewards` 存在；`standbyproof`、`closeepoch`、`beginsettle`、`settlenext`、`finalizeepoch` 均不存在。不要向该主网部署提交这些缺失动作。ABI 存在也不独自证明运行配置已启用，或证明合约内部算法完全相同。

## BP 奖励代领

1. 读当前网络 chain ID、链头和 LIB；准备独立的专用 Keeper 调用账户。
2. 查询 BP `unclaimed_rewards` 与以 producer 为 scope 的 `prodclaims` / `gasclaims`，仅对确有待领取记录的 BP 构造交易。
3. `caller` 满足自身授权；资金固定支付给 `producer`，不能因第三方代领而改变受益人。
4. `max_steps` 控制有界处理；核验源码范围为 1–48，服务默认示例 24，不是任意网络永远固定的限制。
5. 每笔等不可逆后重读领取记录与余额。广播结果不明确时先对账，不盲目重复。

下面会广播写交易，仅供隔离链/已确认测试网，在 ABI、账户、专用权限与可领取状态都核对后使用；不是部署 Keeper 或在主网自动开播的命令：

```bash
export FULLON_RPC='http://127.0.0.1:8888'
fucli -u "$FULLON_RPC" get abi flon -f flon.abi
fucli -u "$FULLON_RPC" push action flon claimrewards \
  '{"caller":"keeperacct","producer":"produceracct","max_steps":24}' \
  -p keeperacct@claimer
```

服务的 `claimer` 权限须事先仅 link 到所需动作。先 dry-run，用受保护的签名文件/服务，不把密钥放入仓库。网络、配置、数据目录和告警分开；避免多个未经协调的 broadcaster。

## Standby 在线证明：仅适用于支持的部署

新版操作指南将 standbyproof 定义为 BP 本人或授权机器人提交的证明；它不能由公共奖励 Keeper 无授权代交。若目标网络当前 ABI 不支持，应停止此流程并查该版本运维说明，而不是绕过校验。

支持该机制的部署还需检查：当前 GAS Epoch、该节点快照角色是否 Standby、最小间隔、证明次数、区块有效窗口与 canonical block ID。文档示例参数为 43,200 slots、12 次证明和最近 240 块窗口，**不是本次主网已核实的配置**。必须读取该部署的当前配置并对照实现。

不要连续补交来绕过间隔或跨 Epoch 补旧证明。保留 Epoch、引用区块、交易 ID、不可逆结果；效果以支持该机制的合约规则为准。在线证明与奖励领取互不替代，不要把 gas奖励资格、BP 注册、自质押和排班资格混为一谈。

## 管理权限边界

Keeper 不应持有 BP 生产私钥或 owner/active 私钥，不托管奖励。`setpower`、风险配置、白名单、Treasury 资产配置及 `sealadmin` 属于单独的授权与上线流程，不是奖励维护任务。

## 来源与范围

[源码、查询快照与资料差异](sources.md)。实现说明基于所列提交；运行配置以目标网络当前状态为准。
