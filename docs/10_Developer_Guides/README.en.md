---
title: Developer guides
type: index
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/README.md
---

# Developer guides

## Integration basics

- [Comprehensive fucli command-line guide](fucli.md)
- [RPC quickstart](quickstart.md)
- [Retrieve ABI and code](get-abi-code.md)
- [Create / activate accounts](accounts.md)
- [Sign, broadcast, and confirm](transactions.md)
- [Troubleshooting](troubleshooting.md)

## Nodes and networking

- [Docker Compose deployment](docker-compose.md)
- [Run common nodes and BP nodes](nodes.md)
- [P2P configuration and synchronization](p2p.md)
- [Complete RPC reference](../03_Operators/funod-rpc.md)
- [History and pagination](../03_Operators/transaction-history-rpc.md)

## Contracts and tokens

- [Write and build a contract](build-contract.md)
- [Deploy and upgrade](deploy-contract.md)
- [Call contract actions](call-actions.md)
- [Issue tokens](issue-tokens.md)

## Mobile wallets

[Install HuFu and manage accounts](../06_User_Guides/hufu-mobile.md). Mobile use and wallet SDK integration are separate tasks; integration requires an officially confirmed protocol.

## Verification scope

New tutorials were reviewed against local Core, CDT, system-contract, and RWID source on 2026-11-02. Existing long-form RPC references retain their `72cde15a3fb1` (2026-09-03) baseline. Discover live node capabilities: source support does not establish deployment.

## Governance integration

[DAO contracts, tables, and actions](../11_DAO_Governance/developer-reference.md) · [Keeper and Standby operations](../11_DAO_Governance/operations.md).
