---
title: 开发者帮助
type: index
status: active
updated: 2026-11-02
source: repository synthesis
---

# 开发者帮助

按从读取数据到提交交易的顺序接入：

1. [RPC 快速开始](quickstart.md)：确认网络与节点能力，读取账户和表数据。
2. [签名、广播与确认](transactions.md)：交易生命周期、幂等与不可逆状态。
3. [智能合约开发路径](contracts.md)：工具链、权限、测试和部署准备。
4. [接入排错](troubleshooting.md)：接口不存在、历史缺失、限流和签名失败。

## 深入参考

- [完整 funod RPC 参考](../03_Operators/funod-rpc.md)
- [交易历史与分页](../03_Operators/transaction-history-rpc.md)
- [节点与插件](../03_Operators/README.md)

现有 RPC 参考核验基线为 `72cde15a3fb1`（2026-09-03），不是对所有当前部署节点的保证。接入时记录 chain ID、节点版本和能力清单；本文不把历史公共节点地址当作当前服务承诺。
