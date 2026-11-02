---
title: 'Run a node: common nodes and BP nodes'
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/nodes.md
---

# Run a node: common nodes and BP nodes

Node, CLI, and RPC examples target **FullOn Core v0.9.2**. Contracts, CDT, and wallets have independent versions; their stated verification scope does not automatically change with Core. See [version baseline and migration](../09_Release_Notes/v0.9.2.md).

For official container deployment, follow the [Docker Compose tutorial](docker-compose.md), including `docker-compose.yaml`, network isolation, role selection, and health checks.

## Choose a role

| Role | Responsibilities | Package | Producer identity/key needed? |
| --- | --- | --- | --- |
| Common synchronization / seed | Validate, synchronize, and relay P2P | `flon-node` core | No |
| RPC | Current-state queries and transaction entry | `flon-node` core | No |
| History | History indexes, Trace / State History | `flon-node-history` | No |
| BP | Synchronize, validate, and produce when scheduled | `flon-node` core | Yes |

A common node also validates blocks and need not be a BP. Actual production requires configured identity/signing, fulfillment of network requirements, and inclusion in the active schedule.

## Installation and network preparation

1. Choose a version/platform compatible with the target network from [Core releases](https://github.com/fullon-labs/flon-core/releases/tag/v0.9.2). The development branch is not a production release.
2. Verify release checksums and extract the node package. CLI/wallet tools come separately in `flon-tools`.
3. Obtain trusted genesis or a compatible snapshot, expected chain ID, P2P peers, and upgrade requirements from network operators.
4. Give each process separate configuration/data directories; plan disk, logging, and monitoring. Snapshot format must match the version. A snapshot need not include history indexes.

Mainnet/testnet genesis, snapshot download URLs, and minimum hardware were not verified here; no guessed parameters are provided.

## Start a common synchronization node

The archive includes `config/seed.ini`. Copy it into your own configuration and add network peers.

```bash
mkdir -p ./node-config ./node-data
cp ./config/seed.ini ./node-config/config.ini
# 启动前编辑 node-config/config.ini，补齐目标网络的 P2P 配置。
./bin/funod --config-dir ./node-config --config config.ini   --data-dir ./node-data --genesis-json /path/to/verified-genesis.json
```

Replace `/path/to/verified-genesis.json`. This example initializes a new data directory. Follow version-specific rules when restarting existing state, and never mix another network's genesis into it. For snapshot recovery, consult that version's `funod --help` and release notes.

## RPC node

The v0.9.2 `config/rpc.ini` preset enables `net_api_plugin` while binding ordinary HTTP to `0.0.0.0`; default management validation rejects that combination. Do not simply disable protection. Remove unneeded management plugins or separate `chain_ro`/`chain_rw` from `net_rw` and monitoring categories with category listeners, keeping management on loopback or Unix sockets. See the [RPC reference](../03_Operators/funod-rpc.md).

## Additional BP steps

1. Apply/register under current network governance and prepare separate production signing capability.
2. Set `producer-name = yourbpaccount` and configure the production public key through a protected signature provider. Keep private keys out of repositories, packages, and screenshots.
3. If the chain uses Savanna, complete its finalizer identity/key requirements. Verify production signing and finalizer duties separately.
4. Synchronize to head and check the active producer schedule and finalizer policy. Registration does not guarantee active scheduling.
5. Monitor actual production, missed blocks, LIB progression, and signer health. Do not run uncoordinated simultaneous signing instances for one production identity.

Bind BP HTTP locally and use separate RPC/History nodes for public queries. `producer-name` alone does not establish BP eligibility.

## Acceptance and troubleshooting

Check expected chain ID, advancing head/LIB, P2P connections, resources/disk, errors, and required APIs. A `core` binary cannot enable history plugins omitted at build time.

[P2P](p2p.md) · [RPC quickstart](quickstart.md)

## Sources and scope

[Source 1](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/docs/node-build-profiles.md), [Source 2](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/README.md). Source review: 2026-11-02. This does not verify the version deployed on every network.
