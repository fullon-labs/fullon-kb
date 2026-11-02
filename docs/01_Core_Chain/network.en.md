---
title: Networks and entry points
type: core_chain
status: active
updated: 2026-11-02
source: source review
translation_of: 01_Core_Chain/network.md
---

# Networks and entry points

Confirm the target network before using any service. Mainnet and testnet assets, account state, contract deployments, and transaction histories are separate.

| Entry point | Purpose | Verify |
| --- | --- | --- |
| [HuFu](https://hufu.io) | Mobile wallet | Download source, publisher, and selected network |
| [Flonscan](https://flonscan.io) | Account and transaction explorer | Network selected in the interface |
| [FullSwap](https://fullswap.flon.network) | Token swaps | Application network, token contracts, and transaction parameters |
| [Core releases](https://github.com/fullon-labs/flon-core/releases/tag/v0.9.2) | Node and tools packages | Version compatible with the target network |

These product URLs come from repository records and do not guarantee current availability. The RPC reference's historical `https://m.flonscan.io` address is historical verification evidence, not a current SLA or default mainnet configuration.

## Verify a network

Developers should obtain an expected chain ID from a trusted operator or official configuration, then compare it with `get_info.chain_id`. Reading and trusting the ID from the same unknown endpoint does not independently verify it.

Users should check the network in their wallet, receiving service, and explorer. Verify source and destination networks separately for bridging.

[RPC integration](../10_Developer_Guides/quickstart.md) · [P2P](../10_Developer_Guides/p2p.md) · [Specifications](specifications.md)
