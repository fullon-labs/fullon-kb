---
title: Scalability roadmap and unverified capabilities
status: active
updated: 2026-11-02
source: whitepaper v2.4.0 synthesis
---

# Scalability roadmap and unverified capabilities

This page summarizes protocol design in whitepaper v2.4.0 (2026-10-22); it does not certify deployment on any network.

Architecture and roadmap descriptions must be read separately from currently available products.

| Direction | Whitepaper description | Interpretation |
| --- | --- | --- |
| Single-thread execution | 10,000+ TPS | Performance claim requiring workload, version and environment evidence |
| Parallel execution | Example scaling to 100,000 TPS with ten threads | Roadmap direction, not a deployment verified here |
| Multi-sharding | State sharding toward one million TPS | Roadmap direction, not a current throughput guarantee |
| L2/sidechains | Specialized applications and ecosystem connections | Architecture possibility, not proof of live networks |
| Synchronous WASM inline calls | Improved composability | Future research feature in the whitepaper |
| BP clusters | Availability and resilience | Operational direction, not permission for uncoordinated duplicate signing |
| Infrastructure/markets | Identity, credit, storage, DNS/CDN, asset and AI markets | Product-specific plans requiring availability checks |

These plans do not establish hardware minima, deployed shard counts, EVM services, wallet protocols or public RPC SLAs. Start integration with the documented [RPC](../10_Developer_Guides/quickstart.md) and [WASM contract path](../10_Developer_Guides/contracts.md).

[Specifications](specifications.md) · [Whitepaper scope and conflicts](whitepaper.md)

## Sources

[English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.md) · [Chinese whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.cn.md) · [Scope and source conflicts](whitepaper.md). Pinned revision `f49e5f0f821162a997260535be30767e3f147d8e`; retrieved 2026-11-02.
