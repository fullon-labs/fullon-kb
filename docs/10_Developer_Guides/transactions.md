---
title: 交易开发：签名、广播与确认
type: guide
status: active
updated: 2026-11-02
source: repository synthesis
---

# 交易开发：签名、广播与确认

目标：使应用能可靠显示交易状态，并避免重复执行业务操作。

## 推荐流程

1. 从可信配置取得预期 chain ID，用 `get_info` 校验所连网络。
2. 从目标合约当前 ABI 构建 action，明确账户、权限、参数、资产精度及 memo。ABI 转换可用 `abi_json_to_bin`；签名前再次检查授权。
3. 使用与你的网络及交易格式兼容的 SDK/钱包构造包含过期时间和参考区块的交易。当前知识库未核验通用钱包 SDK 的安装版本或 HuFu 签名 API，因此本文不提供猜测性的 SDK 调用。
4. 将签名交给钱包或受控签名器完成。私钥不发送给 Chain、History、Trace 或浏览器服务。
5. 按所选接口要求广播 packed transaction，保存交易 ID、业务请求 ID、网络与提交时间。具体字段见[RPC 参考](../03_Operators/funod-rpc.md)。
6. 查询执行结果和包含区块；确认成功执行后，再等待 `block_num <= last_irreversible_block_num`，将业务状态更新为不可逆。

## 状态与重试

| 状态 | 应用处理 |
| --- | --- |
| 等待用户签名 | 允许取消，不显示付款成功 |
| 请求已接受（例如 HTTP 202） | 表示节点接受处理，继续追踪执行结果 |
| 已执行并打包 | 核对执行状态和业务结果，继续等待 LIB |
| 成功且不可逆 | 可按业务策略完成结算 |
| 超时或暂时查不到 | 状态未知；先对账原交易与业务记录 |
| 确定失败 | 展示可操作原因，修正后重新构建并签名 |

业务请求 ID 应持久化并建立去重约束。重新构建交易可能产生新交易 ID；传输重试不能代替业务幂等。不要把批量 `push_transactions` 当成原子事务。

## 查询能力的边界

- `get_transaction_status` 为有条件接口，数据保留有限；先发现能力。
- History 与 Trace 依赖本地索引及保留策略；查询不到不等于链上没有执行。
- 当前余额、权限、表数据从 Chain API 读取；交易历史用于追踪和展示。
- 分叉期间先前的可逆记录可能变化；不可逆前允许业务状态回退。

参考：[历史 API 与最终性](../03_Operators/transaction-history-rpc.md)、[接入排错](troubleshooting.md)。
