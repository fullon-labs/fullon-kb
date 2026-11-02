---
title: Deploy FullOn nodes with Docker Compose
type: developer_guide
status: active
updated: 2026-11-02
source: flon-docker deploy source review
translation_of: 10_Developer_Guides/docker-compose.md
---

# Deploy FullOn nodes with Docker Compose

Use the official `flon-docker/deploy` templates to start a common, BP, or History node through `docker-compose.yaml`, then verify its network and synchronization.

Reviewed baseline: `flon-docker` commit `8cba498ac0982382b8094f64ad8606ff25fb6658`, 2026-11-02. This is configuration/script verification, not a mainnet deployment or image compatibility certification. Read [node roles](nodes.md) first.

## 1. Prepare and choose a role

Install Docker Engine / Docker Desktop and Compose v2, then verify the commands:

```bash
docker --version
docker compose version
git clone https://github.com/fullon-labs/flon-docker.git
cd flon-docker
# 固定到本文核验的模板版本；采用其他版本时重新检查配置和发布说明。
git checkout 8cba498ac0982382b8094f64ad8606ff25fb6658
cd deploy
```

The templates declare `platform: linux/amd64`. ARM hosts may require emulation; production performance and compatibility are not established. Plan sufficient disk/memory and trusted P2P access. Node storage grows over time.

| Role | Official Compose file | Image | Template features |
| --- | --- | --- | --- |
| Common | `compose.common.yaml` | `ghcr.io/fullon-labs/floncore/flon-node` | Synchronization, chain/net APIs, no producer identity |
| BP | `compose.bp.yaml` | Same as above | Producer plugins and separate signing configuration |
| History | `compose.history.yaml` | `ghcr.io/fullon-labs/floncore/flon-node-history` | State History WebSocket, no BP keys |

All three use service name `funod`. Their default image tag `v0.9.0` **does not establish current mainnet compatibility**. Check the target network's release/upgrade requirements and pin `FLON_VERSION` before starting. Do not infer compatibility from `latest`.

## 2. Select mainnet or testnet explicitly

This example selects testnet. For mainnet, select `.env.mainnet.example` and use a separate working directory and data.

```bash
cp .env.testnet.example .env
# 编辑 .env，核对网络、版本、Chain ID、端口和 P2P peer。
set -a
. ./.env
set +a
mkdir -p "data/${FLON_NETWORK}" "snapshots/${FLON_NETWORK}"   "wallet/${FLON_NETWORK}" workspace
```

| Setting | Mainnet template | Testnet template |
| --- | --- | --- |
| `FLON_NETWORK` | `mainnet` | `testnet` |
| Host `RPC_PORT` | `8888` | `18888` |
| Host `P2P_PORT` | `9876` | `19876` |
| `HISTORY_WS_PORT` | `9555` | `19555` |
| Genesis | `networks/mainnet/genesis.json` | `networks/testnet/genesis.json` |
| Data root | `data/mainnet/` | `data/testnet/` |

Expected chain IDs recorded in the templates:

```text
mainnet: d4019d7d8633a337973408c6c00e5c4888933ad1b6ce10edddea8145317d8d12
testnet: 18b4d5837d83a8f7203ea57cb7ab37b9cef59547ea307e70b1bf1103cb06043f
```

These values come from the pinned official configuration; still verify the network when connecting. Never interchange `.env`, genesis, snapshots, wallets, or data between networks. For multiple roles/networks on one host, use separate working directories and nonconflicting host ports. Do not overwrite another running instance's `.env`.

Check these variables:

- `FLON_NETWORK`, `EXPECTED_CHAIN_ID`: use the chosen network's template.
- `FLON_VERSION`: pin a version supported by that network.
- `P2P_PEER`: a reachable peer for that network, not an HTTP RPC URL. Default peers are not availability guarantees.
- `RPC_PORT`, `P2P_PORT`, `HISTORY_WS_PORT`: published host ports.
- `SNAPSHOT_FILE`: optional snapshot filename, described below.
- `RPC_URL`: used by CLI. The template URL is a placeholder and must be replaced.

## 3. Save the selected template as docker-compose.yaml

Choose one in `deploy/`. Preserve relative mounts; copying a single YAML file into an empty directory omits required configuration, scripts, and genesis.

```bash
# 普通节点：
cp compose.common.yaml docker-compose.yaml
# BP 节点改用：cp compose.bp.yaml docker-compose.yaml
# History 节点改用：cp compose.history.yaml docker-compose.yaml
```

This creates your local `docker-compose.yaml`. Upstream names remain `compose.common.yaml`, `compose.bp.yaml`, and `compose.history.yaml`. Replacing an instance's template is not a stateless role switch.

### Additional BP configuration

For the BP role only:

```bash
cp "config/bp/${FLON_NETWORK}/config.ini.example"   "config/bp/${FLON_NETWORK}/config.ini"
chmod 600 "config/bp/${FLON_NETWORK}/config.ini"
```

Replace `producer-name` and `signature-provider` in the selected network's file. The account and production key must match on-chain configuration. Keep private keys in controlled configuration; never commit real keys or include them in support requests.

The BP RPC host mapping defaults to `127.0.0.1`. Common/History RPC and History WebSocket mappings do not restrict the host interface; narrow them to the required exposure. Common and BP configuration includes `net_api_plugin`; management listeners must also satisfy the node version's access restrictions. A host-port binding alone is insufficient. See the [RPC reference](../03_Operators/funod-rpc.md).

Starting a BP container does not establish production eligibility. Complete registration/governance, production keys, and any finalizer requirements, and enter the active schedule; see [BP nodes](nodes.md).

### History scope

The template enables `state_history_plugin`, `trace-history`, and `chain-state-history`, using container WebSocket port `9555`. **It does not enable `transaction_history_api_plugin` or `trace_api_plugin`**. A history image alone does not expose `/v1/history/*` or `/v1/trace_api/*` HTTP endpoints.

State History is a binary indexing stream, not a wallet history HTTP service. Expose it only to intended indexers and configure HTTP history plugins/retention separately if required.

## 4. Validate and start

```bash
# 仅校验，不打印展开后的完整配置。
docker compose --env-file .env -f docker-compose.yaml config --quiet
docker compose --env-file .env -f docker-compose.yaml pull
docker compose --env-file .env -f docker-compose.yaml up -d
docker compose --env-file .env -f docker-compose.yaml ps
```

If image pulling or GHCR access fails, check the tag, architecture, and repository access. Do not substitute another product's or network's image to bypass an error.

The startup script accepts only `mainnet` / `testnet` and checks the mounted genesis SHA-256 on every start. If it fails, stop and investigate; do not edit the expected checksum to accept an unrelated genesis.

## 5. Check network, health, and synchronization

```bash
docker compose --env-file .env -f docker-compose.yaml ps
docker compose --env-file .env -f docker-compose.yaml logs --tail 100 funod

# .env 更新后重新加载，以免查询旧端口。
set -a
. ./.env
set +a
curl --fail --silent --show-error --max-time 15   -X POST "http://127.0.0.1:${RPC_PORT}/v1/chain/get_info"   -H 'Content-Type: application/json' --data '{}'
```

- `chain_id` must match the target network's `EXPECTED_CHAIN_ID`.
- Observe `head_block_num`, `head_block_time`, and `last_irreversible_block_num` over time to establish progress and catch-up.
- The template healthcheck verifies `get_info` returns the expected chain ID. **It does not check catch-up or BP production**. Healthy does not mean fully synchronized.
- An unhealthy status does not automatically trigger `restart: unless-stopped`; the restart policy primarily handles process exits. Inspect logs/network instead of repeatedly restarting.

## 6. Restore from a snapshot

Place a verified snapshot compatible with the target network/binary in `snapshots/${FLON_NETWORK}/`. Set its filename in `.env`, for example `SNAPSHOT_FILE=snapshot.bin`, and start as above.

The reviewed startup script chooses initialization only when `data/${FLON_NETWORK}/<role>/state/shared_memory.bin` **does not exist**. A nonempty `SNAPSHOT_FILE` selects `/snapshots/<filename>`; otherwise it uses genesis. An existing state file causes the snapshot setting to be ignored.

Changing `SNAPSHOT_FILE` and restarting therefore does not overwrite existing state. Stop and back up the instance first, then use a separate new data directory or the target version's explicit recovery procedure. Do not delete original data as an experiment. Consensus snapshots do not necessarily include History indexes.

## 7. Stop, upgrade, and roll back

```bash
# 停止容器；数据仍在宿主机绑定目录。
docker compose --env-file .env -f docker-compose.yaml down
```

This stops containers while retaining host bind-mounted data. Before upgrading, save configuration, old image identifiers, and compatible snapshots/backups. Confirm the network upgrade plan, then change the pinned version in `.env`:

```bash
docker compose --env-file .env -f docker-compose.yaml pull
docker compose --env-file .env -f docker-compose.yaml up -d --force-recreate
```

`pull` downloads images but does not replace running containers. After recreation, verify runtime version, chain ID, head/LIB, and role functions before removing old images. Rollback needs compatible old binaries and matching data backups; do not assume an older image can read newer state.

## Optional: CLI and contract compilation

Node images provide `funod`; do not assume `fucli` / `fuwal` are installed inside them.

```bash
# 从 deploy/ 进入 CLI 目录；使用当前网络的 ../.env。
cd cli
docker compose --env-file ../.env build wallet
docker compose --env-file ../.env up -d wallet cli
docker compose --env-file ../.env exec cli   fucli --wallet-url unix:///wallet/fuwal.sock version client
```

`deploy/cli/compose.yaml` uses a Unix wallet socket and persists wallets under `deploy/wallet/<network>/`. Set a real `RPC_URL` before querying/submitting transactions. Container `127.0.0.1` refers to that container, not the host's node. At the reviewed revision, the CLI Dockerfile pins tools `0.9.0` and its checksum. Changing only base-image `FLON_VERSION` does not update the tools version; review both when upgrading.

The CDT container mounts your source through `CONTRACTS_DIR`:

```bash
# 从 deploy/ 执行。
cd cdt
CONTRACTS_DIR=/absolute/path/to/contracts   docker compose --env-file ../.env run --rm cdt cdt-cpp --version
```

See the [contract build tutorial](build-contract.md) for compilation. This guide validates Compose rendering and example syntax only. No node was started, synchronized, or upgraded.

## Sources

- [Official source 1](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/README.md)
- [Official source 2](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/compose.common.yaml)
- [Official source 3](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/compose.bp.yaml)
- [Official source 4](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/compose.history.yaml)
- [Official source 5](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/bin/start-node.sh)
- [Official source 6](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/bin/healthcheck.sh)
- [Official source 7](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/cli/compose.yaml)
- [Official source 8](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/cli/Dockerfile)
- [Official source 9](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/cdt/compose.yaml)
- [Official source 10](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/.env.mainnet.example)
- [Official source 11](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/.env.testnet.example)
