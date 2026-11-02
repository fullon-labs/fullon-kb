---
title: 资源模型：FLON、GAS 与 ELON
status: active
updated: 2026-11-02
source: whitepaper v2.6.0 Core v0.9.2 baseline and policy clarification draft
---

# 资源模型：FLON、GAS 与 ELON

本文整理白皮书 v2.6.0 澄清稿（2026-11-02）的协议设计，不代表本次已验证各网络部署。

## 三种资源

| 资源 | 白皮书的计量含义 | 用户可能遇到的操作 |
| --- | --- | --- |
| CPU | 交易执行时间 | 合约动作与计算 |
| NET | 交易大小 | 签名及交易数据传输 |
| RAM | 执行中分配的链上状态存储 | 创建/更新合约表记录 |

白皮书用 GAS 表示资源使用额度，最小记账单位为 ELON；`1 FLON = 100,000,000 ELON`，即 `1 ELON = 0.00000001 FLON`。这是设计中的单位关系，不是交易所报价或独立代币投资承诺；目标链实际符号和精度仍需查询。

## 支付与储备

按“资源模型”章节，交易先使用已有 GAS，也可将账户 FLON 转换为 GAS 支付资源成本，不要求标准账户总是提前手动购买。CPU/NET 消耗对应使用额度；RAM 归还时可按规则返还或回收 GAS。具体自动转换、退款条件及交易失败的处理需以运行版本为准，不能只凭白皮书认定某一报错不收费或未留痕。

ELON 的可兑回记账由 `flon.gas` 的 FLON 储备支持：每新增一个 ELON 对应一个 FLON 最小单位。可兑换负债存在时，储备不得重复使用；消耗 GAS 会注销对应 ELON 负债，储备 FLON 按该章节的描述默认保留。其中一部分按生效规则用于符合资格的 Active 与 Standby BP 奖励，其余默认进入 DAO 锁定账；**剩余可支配部分是否销毁、何时及销毁多少，由未来 FullOn DAO Gov 决定**。没有通过并执行的销毁提案，不能计为已销毁；仍需支持未偿 ELON 兑回的储备不得用于奖励或销毁。详见[治理口径](whitepaper.md)。

## 奖励账与 DAO 锁定账

- `bp_reward_balance`：BP 与其投票人的奖励记账。
- `dao_locked_balance`：默认锁定，后续用途需满足 DAO 提案、法定人数、时间锁与执行白名单。
- 初始建议新增 GAS 对应金额按 10% / 90% 分入上述两账；这是治理设计中的建议比例，不是当前链上参数声明。
- 按 epoch 对账，并维持储备最小单位不少于未偿可兑回 ELON；不能把需要支持兑换的储备当作可自由支付余额。

## 用户与开发者如何使用这些信息

用户在签名前检查钱包显示的资源与费用；标准账户的系统资源成本和代理服务费应分别查看。开发者从 `get_info`、`get_account` 等读取运行节点支持的资源字段，并按目标链版本解释。本文不提供固定转账费、免费开户或收益保证。

白皮书还描述代理账户额外服务费、1000 次免费体验及 EVM 地址的变动费用；这些需要产品和网络级确认，不能作为当前优惠或上线承诺。

[开户与 gas](../10_Developer_Guides/accounts.md) · [RPC 参考](../03_Operators/funod-rpc.md) · [代币经济](tokenomics.md)

## 来源

[中文白皮书](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.cn.md) · [English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.md) · [核验范围与资料冲突](whitepaper.md)。固定提交 `5758318eba75d48afd1d543bf020255c1a998d26`；读取日期 2026-11-02。Core v0.9.2 基线已发布；未来发行/GAS 政策澄清仍在独立草稿中，不能标作已部署规则。
