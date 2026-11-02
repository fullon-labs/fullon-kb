---
title: FullOn blockchain specifications
type: core_chain
status: active
updated: 2026-11-02
source: source review
translation_of: 01_Core_Chain/specifications.md
---

# FullOn blockchain specifications

Node source specifications target **v0.9.2**, `2188e4f94a1e9fe564a31c33e497b464556f3650`, reviewed 2026-11-02. See [release guidance](../09_Release_Notes/v0.9.2.md).

Source specifications and running-network parameters are different. A source value is not necessarily a current mainnet setting. Performance claims require a test environment, version, and measurement method.

| Item | Confirmed information | Scope |
| --- | --- | --- |
| Implementation | C++ node `funod`, tools `fucli` and `fuwal` | Core source and packaging documentation |
| Contracts | C/C++ compiled to WASM; ABI describes actions and tables | Native development path |
| Consensus | Core supports Savanna | Activation and policy depend on the target chain |
| Block interval | `block_interval_ms = 500`, or 0.5 seconds | Reviewed source constant; not a finality-latency promise |
| Consecutive production slots | `producer_repetitions = 12` | Scheduling constant, not the current BP count |
| Finality | Check LIB and finality policy | Wait for the successful transaction's block to become irreversible |
| Account permissions | owner, active, and authority | Query current permissions with `get_account` |
| Resource accounting | Source includes CPU, NET, and RAM gas-conversion parameters | Read current rates and resource state from the target chain |
| HTTP RPC | JSON requests under `/v1/*` | Depends on plugins, categories, and version |
| P2P | Node synchronization and propagation, separate from HTTP RPC | Ports and peers depend on configuration |
| History | History, Trace, and State History have distinct roles | Depends on the history build, plugins, and retention |

## Read the target network's parameters

- `get_info`: chain ID, node version, head, LIB, and resource fields exposed by that version.
- `get_consensus_parameters`: chain configuration and available WASM parameters.
- `get_producer_schedule`: active, pending, and proposed producer schedules.
- `get_finalizer_info`: available finalizer policy and information.
- `get_supported_apis`: discover which of these endpoints the node actually exposes.

See the [RPC quickstart](../10_Developer_Guides/quickstart.md). Nodes on the same chain may use different versions and indexing configurations.

## Not confirmed as current network specifications

Mainnet/testnet chain IDs, current BP count, live gas rates, measured finality latency, TPS, minimum production hardware, and public P2P seeds need network-level verification. Source capacity limits and estimates in comments are not performance measurements.

## Sources and scope

[Source 1](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/libraries/chain/include/eosio/chain/config.hpp), [Source 2](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/README.md), [Source 3](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/docs/node-build-profiles.md). Source review: 2026-11-02. This does not verify the version deployed on every network.

## Specifications stated by the whitepaper

The v2.5.0 technical specifications describe a different evidence layer from the source review above.

| Item | Whitepaper description | Scope |
| --- | --- | --- |
| Dynamic block interval | 0.5 seconds when active; up to 12 seconds when idle | Distinguish this from the 500 ms slot constant; verify runtime policy separately |
| Finality | 1–1.5 seconds | Whitepaper claim, not measured here; applications should still confirm LIB |
| Throughput | 10,000+ TPS, single-threaded | Requires workload and environment evidence; see the roadmap for parallelism/sharding |
| Consensus | DPoS + Savanna | Verify the target chain's schedule, policy, and activation |
| VM | Native WASM + claimed 100% compatible EVM | EVM endpoints, deployment, and tooling are not verified here |
| Native asset | FLON; planned total of 10 billion | Does not establish current issued or circulating supply |

See [whitepaper integration](whitepaper.md), [resources](resource-model.md), [tokenomics](tokenomics.md), [governance](governance.md), and [roadmap](roadmap.md).
