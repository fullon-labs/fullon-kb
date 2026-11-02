---
title: 'Run a node: common nodes and BP nodes'
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/nodes.md
---

# Run a node: common nodes and BP nodes

## Choose a role

| Role | Responsibilities | Package | Producer identity/key needed? |
| --- | --- | --- | --- |
| Common synchronization / seed | Validate, synchronize, and relay P2P | `flon-node` core | No |
| RPC | Current-state queries and transaction entry | `flon-node` core | No |
| History | History indexes, Trace / State History | `flon-node-history` | No |
| BP | Synchronize, validate, and produce when scheduled | `flon-node` core | Yes |

A common node also validates blocks and need not be a BP. Actual production requires configured identity/signing, fulfillment of network requirements, and inclusion in the active schedule.

## Installation and network preparation

1. Choose a version/platform compatible with the target network from [Core releases](https://github.com/fullon-labs/flon-core/releases). The development branch is not a production release.
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

Enable required plugins such as `eosio::chain_api_plugin` and expose only necessary chain read/write categories. Use category listeners to keep management on loopback or protected Unix sockets. Do not expose a generic preset containing management plugins directly to the Internet.

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

[Source 1](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/docs/node-build-profiles.md), [Source 2](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/README.md). Source review: 2026-11-02. This does not verify the version deployed on every network.
