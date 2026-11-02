---
title: 白皮书整合：来源、适用范围与差异
status: active
updated: 2026-11-02
source: whitepaper v2.4.0 synthesis
---

# 白皮书整合：来源、适用范围与差异

本文整理白皮书 v2.4.0（2026-10-22）的协议设计，不代表本次已验证各网络部署。

## 固定来源

本次从官方 `flon.whitepaper` 仓库读取中英文主白皮书及 `rwid-design.md`，固定到同一提交。主文档标注 v2.4.0、日期 2026-10-22、Core/CDT v0.8.7；仓库 README 的 v2.1 修订记录另提到 v0.8.5，不能将它当作所有章节或部署的版本号。

[资源模型](resource-model.md) · [代币经济](tokenomics.md) · [互操作性](interoperability.md) · [治理](governance.md) · [路线图](roadmap.md)

## 与现有文档的衔接

原 FAQ 有四页只有标题，并不代表整个官方资料库没有相关解释。本次用白皮书补足协议设计，保留原 FAQ 的读取记录；源码与链上状态用于进一步核验实现与部署。

## 必须保留的差异

| 主题 | 来源中的不同说法 | 本站处理 |
| --- | --- | --- |
| 挖矿上限 | BP 奖励节禁止 5 亿预算耗尽后新增挖矿发行；通膨节又提到储备耗尽后经 DAO 批准的后续发行 | 不将通膨段解释为可追加挖矿预算；后续发行范围与总量约束需维护者澄清 |
| GAS 与销毁 | 资源节说消费 ELON 后储备 FLON 默认保留；通缩节仍含单向转换、燃烧措辞 | 区分 ELON 负债消耗、储备锁定和真实 token burn；不声明储备已自动销毁 |
| 区块间隔 | 源码有 500ms slot 常量；白皮书描述活跃 0.5 秒、闲置最长 12 秒动态产块 | slot 长度和实际产块间隔分开，动态策略需目标网络验证 |
| 性能/最终性 | 白皮书写 10,000+ TPS、1–1.5 秒最终性 | 标为白皮书规格声明，不当作本次实测或服务保证 |
| EVM | 白皮书宣称 100% 兼容；现有核验只覆盖原生 WASM/RPC 路径 | 保留宣称出处，不据此给出未经核实的 MetaMask/Ethereum RPC 配置 |
| 分配/解锁 | 基金会行的两项 10% 基数不清；cliff/vesting 起算需结合条款 | 不据此算当前流通量、具体 TGE 日期或投资者解锁时间 |
| RWID | `rwid-design.md` 描述多社交因素、阈值与去中心化预言机恢复；现有审阅实现有 auth/DAO/owner 管理路径 | 将设计目标和已审阅权限结构分别说明，不称已部署无信任恢复 |

白皮书 RWID 流程中有“智能合约为用户本地生成新密钥”的表述；这里不作为可执行实现说明。实际恢复必须核实密钥在何处生成、谁能接触私钥、链上更新什么公钥/权限，不能推定链上合约安全地产生并保密用户私钥。

## 尚需网络/产品核验

主网与测试网 chain ID、节点地址、当前 gas 费率、实际生产者数量、报名金额/期限、TGE 与锁仓状态、代理钱包和链列表、EVM 合约与入口、RWID 因子和审核服务，都不能单靠设计文档确认。

本次不执行任何资金、权限或节点操作，也不修改上游白皮书。读取文件的哈希见[来源清单](../contributing/whitepaper-source-manifest.json)。

## 来源

[中文白皮书](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.cn.md) · [English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.md) · [核验范围与资料冲突](whitepaper.md)。固定提交 `f49e5f0f821162a997260535be30767e3f147d8e`；读取日期 2026-11-02。
