---
title: 白皮书整合：来源、适用范围与差异
status: active
updated: 2026-11-02
source: whitepaper v2.6.0 Core v0.9.2 baseline and policy clarification draft
---

# 白皮书整合：来源、适用范围与差异

本文整理白皮书 v2.6.0 澄清稿（2026-11-02）的协议设计，不代表本次已验证各网络部署。

## 固定来源

已发布的基线：[中文白皮书](https://github.com/fullon-labs/flon.whitepaper/blob/c1b5ed6cc8572fc79c9eacd964b04d4ca60e8d9a/fullon.whitepaper.cn.md) · [English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/c1b5ed6cc8572fc79c9eacd964b04d4ca60e8d9a/fullon.whitepaper.md) · [实现来源清单](https://github.com/fullon-labs/flon.whitepaper/blob/c1b5ed6cc8572fc79c9eacd964b04d4ca60e8d9a/v0.9.2-source-manifest.json)。

中英文白皮书已发布 v2.6.0（2026-11-02），实现基线为 Core v0.9.2，合约 API 独立参考 CDT v0.9.0。本文引用包含该基线的同一上游修订；其中未来发行/GAS 政策仍作为独立草稿保留，不将草稿政策写成已生效规则。`rwid-design.md` 也固定在同一来源提交；历史 README 版本记录不作为当前部署证明。

[资源模型](resource-model.md) · [代币经济](tokenomics.md) · [互操作性](interoperability.md) · [治理](governance.md) · [路线图](roadmap.md)

## Core v0.9.2 新增与累积能力

- **弹性出块统计**：`get_producer_slot_stats_v2` 区分实出、真实漏块和 `idle_skipped`；`expected = produced + missed`，空闲跳过不降低可用率。v0.9.1 的实际生产者归属修复已包含在本基线。
- **GAS 计量**：`get_gas_fee_totals` 提供累积消耗与 FLON 对应值，合约可按检查点差值计量；计数器本身不转账、增发或改变储备规则。
- **角色与历史**：core/history 构建与 tools 分包；可选 RocksDB 历史索引具备反压、分叉回滚和覆盖/缺口诊断。查询不到不能直接推断链上没有交易。
- **运维与恢复**：管理入口默认限制在回环或 Unix socket；签名入口仅限 Unix。离线物理检查点、恢复续作与操作锁提供明确恢复路径，不等于自动崩溃恢复或自动 BP 切换。
- **v0.9.2 专项修复**：保留已激活 `ACTION_DATA_TO_JSON` 特性的旧摘要，维持重放兼容性；不要求激活替代特性。

新的 intrinsic 需要相容验证节点、对应协议特性激活、匹配 CDT 和系统合约。QSA-V1 是设计草稿；二维分片、DSR 和通用跨链能力不能据此标作本版本已交付。详见[版本与升级说明](../09_Release_Notes/v0.9.2.md)及白皮书仓库的实现来源清单。

## 与现有文档的衔接

原 FAQ 有四页只有标题，并不代表整个官方资料库没有相关解释。本次用白皮书补足协议设计，保留原 FAQ 的读取记录；源码与链上状态用于进一步核验实现与部署。

## 已明确的治理口径

治理权是合约内部账户账本中的数值，不是另行发行、转让或销毁的治理代币。锁定本金变化影响可用治理权，已激活提案按其冻结快照处理。

- 当前 5 亿 FLON 挖矿预算耗尽后不自动继续发行；未来是否发行及其规则由 FullOn DAO Gov 另行决定，需要时配套实施升级。
- GAS 对应金额的一部分奖励符合资格的 Active 与 Standby BP；其余默认锁定，未来是否销毁由 DAO Gov 决定，不能动用仍支持 ELON 兑回的储备。

中英文白皮书的资源、奖励、通膨与通缩章节已在同一修订稿中统一以上口径。

## 仍需保留的差异与核验边界

| 主题 | 来源中的不同说法 | 本站处理 |
| --- | --- | --- |
| 区块间隔 | 源码有 500ms slot 常量；新版白皮书以 12 秒作为心跳参考配置，而非硬性最大间隔 | slot 长度和实际产块间隔分开，动态策略需目标网络验证 |
| 性能/最终性 | 新版白皮书将 10,000+ TPS、1–1.5 秒最终性标为有条件设计目标 | 标为白皮书规格声明，不当作本次实测或服务保证 |
| EVM | 新版白皮书明确原生 WASM，EVM 为独立整合 | 不把 Core 包当作已包含第二套 VM，不推断 MetaMask/Ethereum RPC 配置 |
| 分配/解锁 | 基金会行的两项 10% 基数不清；cliff/vesting 起算需结合条款 | 不据此算当前流通量、具体 TGE 日期或投资者解锁时间 |
| RWID | `rwid-design.md` 描述多社交因素、阈值与去中心化预言机恢复；现有审阅实现有 auth/DAO/owner 管理路径 | 将设计目标和已审阅权限结构分别说明，不称已部署无信任恢复 |

白皮书 RWID 流程中有“智能合约为用户本地生成新密钥”的表述；这里不作为可执行实现说明。实际恢复必须核实密钥在何处生成、谁能接触私钥、链上更新什么公钥/权限，不能推定链上合约安全地产生并保密用户私钥。

## 尚需网络/产品核验

主网与测试网 chain ID、节点地址、当前 gas 费率、实际生产者数量、报名金额/期限、TGE 与锁仓状态、代理钱包和链列表、EVM 合约与入口、RWID 因子和审核服务，都不能单靠设计文档确认。

本次不执行任何资金、权限或节点操作。上游白皮书另以独立修订分支提交，修订稿状态与当前部署明确分开。读取文件的哈希见[来源清单](../contributing/whitepaper-source-manifest.json)。

## 来源

[中文白皮书](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.cn.md) · [English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.md) · [核验范围与资料冲突](whitepaper.md)。固定提交 `5758318eba75d48afd1d543bf020255c1a998d26`；读取日期 2026-11-02。Core v0.9.2 基线已发布；未来发行/GAS 政策澄清仍在独立草稿中，不能标作已部署规则。
