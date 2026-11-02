---
title: GAS 与 ELON：交易内自动支付
status: verified
updated: 2026-11-02
source: Core v0.9.2 source review
---

# GAS 与 ELON：交易内自动支付

FullOn 将资源费用的计算、可用余额检查和扣除集成在交易执行流程中。普通用户只需在实际付款账户中保留足够的可用 FLON，并确认钱包中的业务交易，无需先手动购买 GAS，也无需另外发起兑换交易或填写 gas price。自动支付减少操作步骤，但不代表交易免费，也不保证余额不足的交易能成功。

本文依据 Core v0.9.2，固定提交 `2188e4f94a1e9fe564a31c33e497b464556f3650`；网络实际费率、合约和钱包展示须另行核验。

## GAS、ELON 和 FLON 的关系

GAS 表示链上执行和存储所需的资源额度；ELON 是说明该额度与主币最小单位对应关系的记账单位。v0.9.2 的实现把一个 GAS 整数单位按 **一个主币最小单位**换算，而不是将每个整数单位当作一整枚 FLON。官方构建配置的主币为 8 位精度的 FLON，因此：

- `1 FLON = 100,000,000 ELON`；
- `1 ELON = 0.00000001 FLON`；
- 自动补足 `N` 个 GAS 单位，需要扣除 `N / 100,000,000 FLON`。

这是协议记账换算，不是交易所浮动汇率，也不要求用户持有另一种可交易代币。Core 实际读取主币账户表和内部 GAS 额度；不应仅凭代码注释里的 ELON 字样推定存在独立的 ELON 代币合约或兑换界面。

## 交易内如何自动支付

1. **确定付款账户。** 普通交易的 CPU/NET 付款人为交易的第一个授权账户；并不总是钱包当前展示的账户或转账收款人。RAM 按状态变动对应的 RAM payer 记账，可能由应用合约指定给另一账户。
2. **计算资源用量。** CPU 按计费执行时间、NET 按计费字节数转换为 GAS；正向 RAM 分配单独计算。转换使用链上资源费率并向上取整，实际费用取决于用量和有效参数。
3. **优先使用已有 GAS。** Core 先扣除账户内部已有的 `gas_reserved`，有足够额度时不再为同一笔费用扣 FLON。
4. **自动补足差额。** 已有额度不足时，Core 检查付款账户主币余额，仅将不足部分对应的 FLON 最小单位直接从付款账户余额记入系统 `flon.gas` 账户。该路径直接更新余额表，不要求用户另外签署一笔充值、兑换或 `transfer` 动作；普通转账历史也不能替代 GAS 明细。
5. **提交结果。** GAS 检查和扣除属于交易执行的状态变更。若资源支付条件不满足，普通交易不能按成功交易提交；不要据此笼统推断所有特殊交易路径、应用服务费或失败记录都具有相同语义。

例：本次应付 `3,000` 个 GAS 单位，已有 `1,000`，则只需自动补足 `2,000`，扣除 `0.00002000 FLON`。该例只演示单位换算，不代表固定转账费；RAM 费用应按其实际付款账户另行计算。

## 用户如何确保能够支付

- 在实际付款账户中留出可用 FLON，不能把计划全部转出的金额同时当作手续费余额。已质押、锁定或不在该账户余额表中的资产，不能直接当作该路径的可用主币余额。
- 使用钱包的费用估算，保留一定余量；交易执行可能改变余额，预估并不锁定最终费用。
- 若由应用代付，确认应用实际提供授权和付款安排；Core 不会因为用户余额不足而自动让开发者、收款人或任意第三方承担费用。
- 保证付款账户和系统 `flon.gas` 的主币余额表已正确初始化，符号及精度匹配。代码在缺少所需余额表时不能建立自动转换付款路径；仅有一个 FLON 显示数字并不足以证明目标网络配置正确。
- 不足时会出现 `tx_gas_usage_exceeded` 等资源错误，应补足相应付款账户的余额或减少资源用量后重试。

释放 RAM 时，Core 可按当时有效费率将相应 GAS 额度加回内部余额；这不是自动向用户主币余额转回 FLON，也不保证与最初支出完全相等。

## 如何做到操作简单、费用可见

“对用户透明”应指自动完成资源支付，同时能够解释扣费。以下是基于 Core 字段的钱包／浏览器展示建议，不代表每款钱包都已实现：

- 签名前显示实际付款账户、预估费用及折合 FLON、业务转账金额和余额不足提示；默认不要求用户设置 gas price 或分别购买 CPU/NET/RAM。
- 签名后根据交易 trace 显示 `gas_traces`：`reserved_gas_before`、`reserved_gas_after`、`used_gas`、`converted_gas` 和 `ram_gas_delta`，分别解释已有额度消耗、自动扣除 FLON 及 RAM 变动。
- 使用 `get_account` 的 `gas_reserved` 与 `gas_max` 展示可用资源概况；`gas_max` 包含可自动转换的主币额度，不应再次与该主币余额简单相加。该值也不是全网固定手续费或最终报价。
- 如果节点未保留或未返回完整 trace，明确说明明细不可用，不把缺失字段显示为零费用。系统 GAS 费用与代理、跨链或应用自行收取的服务费分别列示。

开发者仍可使用交易头的 CPU/NET 用量上限等高级控制。免除日常用户填写 GAS 参数的负担，不等于协议没有执行上限或资源保护。

## 源码依据

所有链接均固定至 v0.9.2 提交：

- [主币符号与精度](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/chain_config.cmake)
- [资源计费、自动补差及 RAM 额度返还](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/resource_limits.cpp)
- [付款账户选择及交易 GAS trace 汇总](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/transaction_context.cpp)
- [余额表访问与符号校验](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/contract_table_utils.cpp)
- [GAS trace 字段](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/include/eosio/chain/trace.hpp)
- [get_account 资源字段](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/plugins/chain_plugin/chain_plugin.cpp)

[资源模型](resource-model.md) · [RPC 参考](../03_Operators/funod-rpc.md)
