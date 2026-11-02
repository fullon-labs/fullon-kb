---
title: 'P2P: connect and synchronize nodes'
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/p2p.md
---

# P2P: connect and synchronize nodes

P2P propagates blocks, transactions, and consensus-related messages between nodes. RPC handles application requests. An HTTP RPC URL is not a P2P peer, and State History WebSocket is not P2P.

## Configuration {#net-plugin-configuration}

```ini
# 以下主机名是示例，启动前替换为可信网络配置。
p2p-listen-endpoint = 0.0.0.0:9876
p2p-server-address = node.example.org:9876
p2p-peer-address = seed-a.example.org:9876
p2p-peer-address = seed-b.example.org:9876
```

The hostnames are examples; replace them with trusted network configuration before starting.

- `p2p-listen-endpoint`: local listener; inbound traffic also needs firewall/routing access.
- `p2p-server-address`: advertised reachable address; NAT may require a mapping.
- `p2p-peer-address`: outbound peer; repeat it for multiple peers.

9876 is an example port, not a universal public network port. Use peers from trusted operator configuration; no unverified seeds are published here.

## Verify

1. Confirm expected chain IDs match and node/protocol-feature versions are compatible.
2. Check TCP reachability and handshake/disconnect logs.
3. Observe head and LIB progression. A connection does not prove synchronization.
4. If a private `net_api_plugin` is enabled, query `/v1/net/connections`. Management writes are for controlled operations only.

For sync failures, check network, DNS/firewall/NAT, version, snapshot compatibility, disk, and peers. Preserve logs and determine a recovery plan before deleting any data directory.

## Related documentation

- [Net Plugin configuration guide](#net-plugin-configuration): P2P examples and parameter descriptions on this page.
- [Net RPC API guide](../03_Operators/funod-rpc.md#net-api): request formats for inspecting, connecting, and disconnecting peers.

## Source reference

[Source reference: Net Plugin configuration definitions](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/plugins/net_plugin/net_plugin.cpp), for developers checking the implementation. Source review: 2026-11-02. This does not verify the version deployed on every network.
