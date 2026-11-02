---
title: P2P：连接和同步节点
type: guide
status: active
updated: 2026-11-02
source: source review
---

# P2P：连接和同步节点

P2P 用于节点间区块、交易及共识相关消息传播；RPC 用于应用请求。HTTP RPC 地址不能直接当 P2P peer，State History WebSocket 也不是 P2P。

## 配置含义

```ini
# 以下主机名是示例，启动前替换为可信网络配置。
p2p-listen-endpoint = 0.0.0.0:9876
p2p-server-address = node.example.org:9876
p2p-peer-address = seed-a.example.org:9876
p2p-peer-address = seed-b.example.org:9876
```

- `p2p-listen-endpoint`：本机监听地址；入站连接还需防火墙与路由允许。
- `p2p-server-address`：对外宣告的可达地址；NAT 后通常需要映射。
- `p2p-peer-address`：主动连接的 peer，可重复配置多个。

9876 是示例端口，不是每条网络的固定公共端口。peer 应来自可信网络维护配置；本文不发布未经验证的种子列表。

## 验证

1. 确认双方预期 chain ID 一致，节点版本和协议特性兼容。
2. 检查 TCP 可达性与日志中的握手/断连原因。
3. 连通后持续观察 head 和 LIB；有连接不代表已经追上链头。
4. 若启用私有 `net_api_plugin`，可用 `/v1/net/connections` 查看连接。管理写接口仅用于受控运维。

无法同步时依次检查网络选择、DNS/防火墙/NAT、版本、快照兼容性、磁盘和 peer 状态。不要通过删除数据目录来试错，先保存日志并确定恢复方案。

## 来源

[Net Plugin 配置定义](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/plugins/net_plugin/net_plugin.cpp)、[Net RPC 参考](../03_Operators/funod-rpc.md)。
