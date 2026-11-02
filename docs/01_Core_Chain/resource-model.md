---
title: 资源模型：FLON、GAS 与 ELON
status: active
updated: 2026-11-02
source: Core v0.9.2 source review and whitepaper v2.6.0 policy clarification draft
---

# 资源模型：FLON、GAS 与 ELON

FullOn 将资源费用的计算、可用余额检查和扣除集成在交易执行流程中。普通用户只需在实际付款账户中保留足够的可用 FLON，并确认钱包中的业务交易，无需先手动购买 GAS，也无需另外发起兑换交易或填写 gas price。自动支付减少操作步骤，但不代表交易免费，也不保证余额不足的交易能成功。

本文依据 Core v0.9.2，固定提交 `2188e4f94a1e9fe564a31c33e497b464556f3650`；网络实际费率、合约和钱包展示须另行核验。

## 三种资源

| 资源 | 白皮书的计量含义 | 用户可能遇到的操作 |
| --- | --- | --- |
| CPU | 交易执行时间 | 合约动作与计算 |
| NET | 交易大小 | 签名及交易数据传输 |
| RAM | 执行中分配的链上状态存储 | 创建/更新合约表记录 |

## GAS、ELON 和 FLON 的关系

GAS 表示链上执行和存储所需的资源额度；ELON 是说明该额度与主币最小单位对应关系的记账单位。v0.9.2 的实现把一个 GAS 整数单位按 **一个主币最小单位**换算，而不是将每个整数单位当作一整枚 FLON。官方构建配置的主币为 8 位精度的 FLON，因此：

- `1 FLON = 100,000,000 ELON`；
- `1 ELON = 0.00000001 FLON`；
- 自动补足 `N` 个 GAS 单位，需要扣除 `N / 100,000,000 FLON`。

这是协议记账换算，不是交易所浮动汇率，也不要求用户持有另一种可交易代币。Core 实际读取主币账户表和内部 GAS 额度；不应仅凭代码注释里的 ELON 字样推定存在独立的 ELON 代币合约或兑换界面。

## 交易内如何自动支付 {#auto-gas-payment}

1. **确定付款账户。** 普通交易的 CPU/NET 付款人为交易的第一个授权账户；并不总是钱包当前展示的账户或转账收款人。RAM 按状态变动对应的 RAM payer 记账，可能由应用合约指定给另一账户。
2. **计算资源用量。** CPU 按计费执行时间、NET 按计费字节数转换为 GAS；正向 RAM 分配单独计算。转换使用链上资源费率并向上取整，实际费用取决于用量和有效参数。
3. **优先使用已有 GAS。** Core 先扣除账户内部已有的 `gas_reserved`，有足够额度时不再为同一笔费用扣 FLON。
4. **自动补足差额。** 已有额度不足时，Core 检查付款账户主币余额，仅将不足部分对应的 FLON 最小单位直接从付款账户余额记入系统 `flon.gas` 账户。该路径直接更新余额表，不要求用户另外签署一笔充值、兑换或 `transfer` 动作；普通转账历史也不能替代 GAS 明细。
5. **提交结果。** GAS 检查和扣除属于交易执行的状态变更。若资源支付条件不满足，普通交易不能按成功交易提交；不要据此笼统推断所有特殊交易路径、应用服务费或失败记录都具有相同语义。

例：本次应付 `3,000` 个 GAS 单位，已有 `1,000`，则只需自动补足 `2,000`，扣除 `0.00002000 FLON`。该例只演示单位换算，不代表固定转账费；RAM 费用应按其实际付款账户另行计算。

## 每笔交易的 GAS 如何计算 {#gas-calculation}

对需要计费的普通账户，v0.9.2 使用下列计算。`ceil` 表示每一项分别向上取整，`payer` 表示各 RAM 付款账户；资源豁免账户不适用普通扣费公式。

```text
P = 1000
G_cpu = ceil(cpu_usage_us * gas_per_cpu_ms / P)
G_net = ceil(net_usage_bytes * gas_per_net_kb / P)
G_ram_charge = sum(ceil(max(ram_delta_bytes[payer], 0) * gas_per_ram_kb / P))
G_consumed = G_cpu + G_net + G_ram_charge
G_ram_credit = sum(ceil(max(-ram_delta_bytes[payer], 0) * gas_per_ram_kb / P))
FLON_debited = sum(converted_gas[payer]) / 100000000
```

- `cpu_usage_us` 是整笔交易的**计费 CPU 微秒数**，不是某个 action 的 `elapsed` 或浏览器的请求耗时；计费也受链上最小 CPU 用量等规则影响。
- `net_usage_bytes` 是整笔交易的**计费字节数**，包含协议计费规则，并向上补齐为 8 字节的整数倍；若从 receipt 读取 `net_usage_words`，需乘以 `8`。不能直接把 JSON 文本长度代入。
- `ram_delta_bytes[payer]` 是交易汇总后的各账户 RAM 变化，新增存储计费，释放存储返还内部 GAS。`G_ram_credit` 单独列示，不能直接从累计消耗中减去后当作实际 FLON 扣款。
- CPU/NET 归交易付款人，RAM 归各自付款人。实际自动补差还受各账户已有 GAS、执行顺序和 RAM 返还影响；以交易的 `gas_traces[].converted_gas` 为准，不应把所有账户余额混为一个资金池。

字段名中的 `ms`、`kb` 是费率的名义单位。**代入原始整数费率时，CPU 微秒及 NET/RAM 字节都按源码的 `P = 1000` 计算，不能额外再除一次 1000，也不能把这里的 1000 换成 1024。**

### 费率快照

2026-11-02 只读查询 `https://m.flonscan.io`，节点报告 Core `v0.9.2-2188e4f9`，chain ID 与文档主网快照一致。`get_info` 与 `get_consensus_parameters` 均返回以下费率；这只是带日期的观察，不是未来固定价格。

| 项目 | 链上原始费率 | 换算后的单价 |
| --- | --- | --- |
| CPU | `gas_per_cpu_ms = 10000` | 每计费微秒 `10 GAS` |
| NET | `gas_per_net_kb = 50000` | 每计费字节 `50 GAS` |
| RAM | `gas_per_ram_kb = 50000` | 每新增字节 `50 GAS` |

对应读取结果、chain ID 与区块高度见[费率观察记录](gas-rate-observation.json)。这些费率也与 v0.9.2 源码默认值一致；实际计费应读取目标网络当时生效的参数。

### FLON 普通转账：单笔及平均开销示例

以下是**假设资源用量的计算示例，不是主网实测均值**。假设每笔只有一次普通 FLON 转账，双方已有余额行，无额外合约业务、无新增 RAM，计费 NET 均为 `192 bytes`，使用上述费率：

| 示例转账 | 假设计费 CPU | CPU GAS | NET GAS | 总 GAS | FLON 等值 |
| --- | --- | --- | --- | --- | --- |
| A | `100 μs` | `1,000` | `9,600` | `10,600` | `0.00010600` |
| B | `120 μs` | `1,200` | `9,600` | `10,800` | `0.00010800` |
| C | `200 μs` | `2,000` | `9,600` | `11,600` | `0.00011600` |
| 示例平均 | `140 μs` | `1,400` | `9,600` | **`11,000`** | **`0.00011000`** |

例如 C 的计算为 `ceil(200 × 10000 / 1000) + ceil(192 × 50000 / 1000) = 11600 GAS`。如无已有 GAS，则自动扣除 `0.00011600 FLON`；如已有 `1000 GAS`，则只补差扣除 `0.00010600 FLON`。已有 GAS 降低本次新增 FLON 扣款，不改变这笔交易消耗的 `11600 GAS`。

若某笔转账还为收款方新增 `240 bytes` 的余额记录，则按示例费率另计 `12000 GAS`，即 `0.00012000 FLON` 等值，由实际 RAM payer 支付；`240 bytes` 同样是假设值，应以真实 RAM 变化为准。memo 长度、签名、授权数量、收款合约通知及账户状态都会改变成本，转账金额本身不是 GAS 费率的百分比基数。

### 怎样统计真实平均转账费

对同一网络、明确时间窗口内 `n` 笔成功且不可逆的普通转账，逐笔去重交易 ID，统计 `gas_traces` 的消耗及自动补差：

```text
average_consumed_GAS = sum(G_consumed[i]) / n
average_FLON_equivalent = average_consumed_GAS / 100000000
average_new_FLON_debit = sum(sum(converted_gas[i][payer])) / n / 100000000
```

发布均值时同时给出网络/chain ID、区间、样本量、费率及是否包含新增 RAM；将首次收款与已有余额行的转账分组。合约兑换、跨链、内联转账和失败交易不能混入普通转账样本；也不能把同一笔交易的多条动作重复计费。

本次未取得足够的普通转账完整费用样本：查询到的转账动作主要来自 FullSwap，不能代表普通 FLON 转账。因此这里只发布可复算的示例平均，**暂不将 `0.00011000 FLON` 标作实际平均手续费**。

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

## 储备与治理政策

以下储备与奖励口径来自白皮书设计及其独立澄清稿。Core 的自动扣费实现本身不能证明目标链已部署兑换规则、奖励分配或 DAO 参数。

ELON 的可兑回记账由 `flon.gas` 的 FLON 储备支持：每新增一个 ELON 对应一个 FLON 最小单位。可兑换负债存在时，储备不得重复使用；消耗 GAS 会注销对应 ELON 负债，储备 FLON 按该章节的描述默认保留。其中一部分按生效规则用于符合资格的 Active 与 Standby BP 奖励，其余默认进入 DAO 锁定账；**剩余可支配部分是否销毁、何时及销毁多少，由未来 FullOn DAO Gov 决定**。没有通过并执行的销毁提案，不能计为已销毁；仍需支持未偿 ELON 兑回的储备不得用于奖励或销毁。详见[治理口径](whitepaper.md)。

### 奖励账与 DAO 锁定账

- `bp_reward_balance`：BP 与其投票人的奖励记账。
- `dao_locked_balance`：默认锁定，后续用途需满足 DAO 提案、法定人数、时间锁与执行白名单。
- 初始建议新增 GAS 对应金额按 10% / 90% 分入上述两账；这是治理设计中的建议比例，不是当前链上参数声明。
- 按 epoch 对账，并维持储备最小单位不少于未偿可兑回 ELON；不能把需要支持兑换的储备当作可自由支付余额。

白皮书还描述代理账户额外服务费、1000 次免费体验及 EVM 地址的变动费用；这些需要产品和网络级确认，不能作为当前优惠或上线承诺。

[开户与 gas](../10_Developer_Guides/accounts.md) · [RPC 参考](../03_Operators/funod-rpc.md) · [代币经济](tokenomics.md)

## 源码依据

所有链接均固定至 v0.9.2 提交：

- [换算精度及默认费率](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/include/eosio/chain/config.hpp)
- [主币符号与精度](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/chain_config.cmake)
- [资源计费、自动补差及 RAM 额度返还](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/resource_limits.cpp)
- [付款账户选择及交易 GAS trace 汇总](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/transaction_context.cpp)
- [余额表访问与符号校验](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/contract_table_utils.cpp)
- [GAS trace 字段](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/include/eosio/chain/trace.hpp)
- [get_account 资源字段](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/plugins/chain_plugin/chain_plugin.cpp)


[中文白皮书](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.cn.md) · [English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.md) · [核验范围与资料冲突](whitepaper.md)。固定提交 `5758318eba75d48afd1d543bf020255c1a998d26`；读取日期 2026-11-02。Core v0.9.2 基线已发布；未来发行/GAS 政策澄清仍在独立草稿中，不能标作已部署规则。
