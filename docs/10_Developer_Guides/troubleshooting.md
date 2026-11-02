---
title: 开发接入排错
type: guide
status: active
updated: 2026-11-02
source: repository synthesis
---

# 开发接入排错

| 现象 | 检查顺序 | 处理 |
| --- | --- | --- |
| 连接失败或超时 | 地址、TLS、代理、节点状态 | 设置超时和有限重试；先查询只读状态 |
| 404 / Unknown Endpoint | `get_supported_apis`、插件、类别、版本 | 使用实际支持的路径；不要仅依据参考目录判断可用 |
| 400 | 请求 JSON、字段类型、账户、ABI、权限 | 读取 `error.name`、`what` 和 `details`，修正确定性错误 |
| 503 或代理 429 | 并发、速率和服务容量 | 指数退避并限制重试次数与并发 |
| 历史为空或找不到交易 | chain ID、完整 ID、索引保留与同步 | 查询含区块提示的历史记录；必要时从节点运营方核查覆盖范围 |
| 余额与历史不一致 | 节点网络与同步、索引延迟、合约和 scope | 当前状态从 Chain API 交叉核对 |
| 权限或签名失败 | 授权账户、权限、当前公钥、签名网络 | 重新读取权限与 ABI；不要通过扩大权限绕过问题 |
| 广播超时 | 原交易 ID、是否打包、业务去重记录 | 先对账，避免重新签名产生重复业务操作 |

历史 API 可尝试兼容性较好的 `/v1/history/*` 前缀，但仍需检查节点能力。生产环境不要为解决 404 而直接公开 Net、Producer、Snapshot 或签名管理接口。

## 提交可复现问题

记录节点版本、chain ID、接口路径、脱敏请求、HTTP 状态、错误响应、时间与时区、交易 ID（如有）。删除私钥、鉴权头、密码和访问令牌。

参考：[RPC 参考的错误模型](../03_Operators/funod-rpc.md)、[历史 API 运维说明](../03_Operators/transaction-history-rpc.md)。
