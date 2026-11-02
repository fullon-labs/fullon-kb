---
title: 使用 Docker Compose 部署 FullOn 节点
type: developer_guide
status: active
updated: 2026-11-02
source: flon-docker deploy source review
---

# 使用 Docker Compose 部署 FullOn 节点

目标：使用官方 `flon-docker/deploy` 模板，通过 `docker-compose.yaml` 启动普通、BP 或 History 节点，并验证其网络和同步状态。

本文核验基线为 `flon-docker` 提交 `8cba498ac0982382b8094f64ad8606ff25fb6658`（2026-11-02）；这是配置与脚本核验，不是主网部署或镜像兼容性验收。先阅读[普通节点与 BP 的区别](nodes.md)。

## 1. 准备环境并选择角色

安装 Docker Engine / Docker Desktop 与 Compose v2，确认命令可用：

```bash
docker --version
docker compose version
git clone https://github.com/fullon-labs/flon-docker.git
cd flon-docker
# 固定到本文核验的模板版本；采用其他版本时重新检查配置和发布说明。
git checkout 8cba498ac0982382b8094f64ad8606ff25fb6658
cd deploy
```

模板声明 `platform: linux/amd64`。ARM 主机可能需要仿真；不能据此假设其生产性能或兼容性。准备足够磁盘、内存和可信 P2P 入口；节点数据会持续增长。

| 角色 | 官方 Compose 文件 | 镜像 | 模板功能 |
| --- | --- | --- | --- |
| 普通节点 | `compose.common.yaml` | `ghcr.io/fullon-labs/floncore/flon-node` | 同步、chain/net API，不配置出块身份 |
| BP 节点 | `compose.bp.yaml` | 同上 | producer 插件与独立生产身份配置 |
| History 节点 | `compose.history.yaml` | `ghcr.io/fullon-labs/floncore/flon-node-history` | State History WebSocket，不配置 BP 私钥 |

本文目标为 **Core v0.9.2**，三个服务都叫 `funod`。固定模板仍默认 `v0.9.0`，下面显式覆盖为 `FLON_VERSION=v0.9.2`；这是文档目标版本，不是对每条网络或镜像可用性的保证。启动前确认节点镜像标签和摘要，以及目标网络升级要求。

## 2. 显式选择主网或测试网

以下以测试网为例；主网应选择 `.env.mainnet.example`，并采用独立工作目录和数据。

```bash
cp .env.testnet.example .env
# Explicit Core target; keep the reviewed template default out of the running node.
printf '\nFLON_VERSION=v0.9.2\n' >> .env
# 编辑 .env，核对网络、版本、Chain ID、端口和 P2P peer。
set -a
. ./.env
set +a
mkdir -p "data/${FLON_NETWORK}" "snapshots/${FLON_NETWORK}"   "wallet/${FLON_NETWORK}" workspace
```

| 配置 | 主网模板 | 测试网模板 |
| --- | --- | --- |
| `FLON_NETWORK` | `mainnet` | `testnet` |
| 宿主机 `RPC_PORT` | `8888` | `18888` |
| 宿主机 `P2P_PORT` | `9876` | `19876` |
| `HISTORY_WS_PORT` | `9555` | `19555` |
| genesis | `networks/mainnet/genesis.json` | `networks/testnet/genesis.json` |
| 数据根目录 | `data/mainnet/` | `data/testnet/` |

模板记录的预期 Chain ID：

```text
mainnet: d4019d7d8633a337973408c6c00e5c4888933ad1b6ce10edddea8145317d8d12
testnet: 18b4d5837d83a8f7203ea57cb7ab37b9cef59547ea307e70b1bf1103cb06043f
```

这些值来自固定提交的官方配置；连接时仍需核对目标网络。不要互换 `.env`、genesis、快照、钱包或数据目录。多角色/多网络同机运行时，使用各自工作目录，分配不冲突的宿主机端口；不要在运行中覆盖另一实例的 `.env`。

必须检查的变量：

- `FLON_NETWORK`、`EXPECTED_CHAIN_ID`：来自所选网络模板。
- `FLON_VERSION`：目标网络允许的固定版本。
- `P2P_PEER`：该网络可用的 P2P peer，不能填 HTTP RPC 地址；默认 peer 不是可用性保证。
- `RPC_PORT`、`P2P_PORT`、`HISTORY_WS_PORT`：宿主机映射端口。
- `SNAPSHOT_FILE`：可选快照文件名，见下文。
- `RPC_URL`：供 CLI 使用；模板值是占位地址，必须替换。

## 3. 选择模板并保存为 docker-compose.yaml

在 `deploy/` 目录执行以下一项。保留该文件中的相对挂载路径，不要只复制单个 YAML 到缺少配置、脚本和 genesis 的空目录。

```bash
# 普通节点：
cp compose.common.yaml docker-compose.yaml
# BP 节点改用：cp compose.bp.yaml docker-compose.yaml
# History 节点改用：cp compose.history.yaml docker-compose.yaml
```

此步骤生成你本地的 `docker-compose.yaml`，上游官方文件名仍是 `compose.common.yaml` / `compose.bp.yaml` / `compose.history.yaml`。不要将同一实例的模板替换当成无状态的角色切换。

### BP 额外配置

仅 BP 角色执行：

```bash
cp "config/bp/${FLON_NETWORK}/config.ini.example"   "config/bp/${FLON_NETWORK}/config.ini"
chmod 600 "config/bp/${FLON_NETWORK}/config.ini"
```

在该网络的文件中替换 `producer-name` 和 `signature-provider` 占位值。账户与生产公钥须匹配链上配置，私钥只能保存在受控配置中。不要把真实私钥提交到 Git 或粘贴到求助信息。

BP 的宿主机 RPC 映射默认为 `127.0.0.1`；普通/History 的 RPC 和 History WebSocket 映射未限制宿主机接口，按使用场景收紧。普通和 BP 配置含 `net_api_plugin`；含管理接口的监听器还须满足相应节点版本的访问限制，不能仅依赖宿主机端口映射。生产暴露方式见[RPC 参考](../03_Operators/funod-rpc.md)。

启动 BP 容器不等于已具备出块资格。仍需完成注册/治理、生产密钥及目标链要求的 finalizer 配置，并进入活动出块排班，见[BP 节点说明](nodes.md)。

### History 的范围

模板开启 `state_history_plugin`、`trace-history` 与 `chain-state-history`，容器内 WebSocket 端口为 `9555`。**它没有开启 `transaction_history_api_plugin` 或 `trace_api_plugin`**；使用 history 镜像本身不代表已经提供 `/v1/history/*` 或 `/v1/trace_api/*` HTTP 接口。

State History 是二进制索引流，不是钱包交易历史 HTTP 服务。只向需要的索引器开放，并按业务单独配置 HTTP 历史插件与保留策略。

## 4. 校验并启动

```bash
# 仅校验，不打印展开后的完整配置。
docker compose --env-file .env -f docker-compose.yaml config --quiet
docker compose --env-file .env -f docker-compose.yaml pull
docker compose --env-file .env -f docker-compose.yaml up -d
docker compose --env-file .env -f docker-compose.yaml ps
```

若出现镜像拉取或 GHCR 访问错误，先确认标签、架构与仓库访问权限；不要改成其他产品或其他网络的镜像来绕过错误。

启动脚本只接受 `mainnet` / `testnet`，每次校验挂载 genesis 的 SHA-256。校验不通过时停止处理，不要修改校验值来迁就不匹配的 genesis。

## 5. 检查网络、健康和同步

```bash
docker compose --env-file .env -f docker-compose.yaml ps
docker compose --env-file .env -f docker-compose.yaml logs --tail 100 funod

# .env 更新后重新加载，以免查询旧端口。
set -a
. ./.env
set +a
curl --fail --silent --show-error --max-time 15   -X POST "http://127.0.0.1:${RPC_PORT}/v1/chain/get_info"   -H 'Content-Type: application/json' --data '{}'
```

- `chain_id` 必须等于目标网络的 `EXPECTED_CHAIN_ID`。
- 持续观察 `head_block_num`、`head_block_time` 和 `last_irreversible_block_num`，判断是否推进、是否追上网络。
- 模板 healthcheck 检查 `get_info` 是否返回预期 Chain ID，**不检查已追上链头或 BP 正常出块**。`healthy` 不等于同步完成。
- `unhealthy` 不自动触发 `restart: unless-stopped`；重启策略主要处理进程退出。先检查日志和网络，而不是反复重启。

## 6. 从快照恢复

将已验证且与目标网络/二进制兼容的文件放到 `snapshots/${FLON_NETWORK}/`，在 `.env` 设置文件名，例如 `SNAPSHOT_FILE=snapshot.bin`，再按前文启动。

核验脚本只有在 `data/${FLON_NETWORK}/<role>/state/shared_memory.bin` **不存在**时才选择初始化方式：`SNAPSHOT_FILE` 非空则使用 `/snapshots/<文件名>`，否则使用 genesis。已有状态文件时会忽略该快照设置。

因此，仅修改 `SNAPSHOT_FILE` 并重启不会覆盖已有状态。需要恢复时，先停止实例并备份，使用新的独立数据目录，或按目标版本明确的恢复步骤操作。不要直接删除原数据来试错；共识状态快照也不保证包含 History 索引。

## 7. 停止、升级与回滚

```bash
# 停止容器；数据仍在宿主机绑定目录。
docker compose --env-file .env -f docker-compose.yaml down
```

升级前保存配置、旧镜像标识及兼容快照/备份，确认目标网络升级安排，然后修改 `.env` 的固定版本：

```bash
docker compose --env-file .env -f docker-compose.yaml pull
docker compose --env-file .env -f docker-compose.yaml up -d --force-recreate
```

`pull` 只下载镜像，不会替换已经运行的容器。重建后核对运行版本、Chain ID、head/LIB 和角色功能，再决定是否清理旧镜像。回滚需要兼容的旧二进制与对应数据备份，不能假设降级镜像即可读取新版本状态。

## 可选：CLI 与合约编译容器

节点镜像只提供 `funod`，不要假设节点内包含 `fucli` / `fuwal`。

```bash
# 从 deploy/ 进入 CLI 目录；使用当前网络的 ../.env。
cd cli
# Confirm CDT_IMAGE_TAG independently; it is not the Core/tools version.
TOOLS_SHA256=e06858f051ed7c3fc5e2276258520993fbf07ba5e4636b8c20d1899172cde2a3
docker compose --env-file ../.env build \
  --build-arg "FLON_VERSION=${CDT_IMAGE_TAG:?set a verified floncdt base-image tag}" \
  --build-arg TOOLS_VERSION=0.9.2 \
  --build-arg "TOOLS_SHA256=$TOOLS_SHA256" wallet
docker compose --env-file ../.env up -d wallet cli
docker compose --env-file ../.env exec cli   fucli --wallet-url unix:///wallet/fuwal.sock version client
```

`deploy/cli/compose.yaml` 的钱包使用 Unix socket，并按网络持久化到 `deploy/wallet/<network>/`。填写实际 `RPC_URL` 后再查询/提交交易；容器里的 `127.0.0.1` 指向该容器自身，不能直接当成宿主机节点。固定 CLI Dockerfile 默认安装 tools `0.9.0`；上例使用官方 v0.9.2 tools 包摘要覆盖为 `TOOLS_VERSION=0.9.2`。`CDT_IMAGE_TAG` 是须单独确认的编译环境镜像版本，不能假定存在 `floncdt:v0.9.2`。上例的摘要来自官方 release asset 元数据，构建时仍校验下载字节；构建后检查 `fucli version client` 和 `fuwal --version`。节点版本与 CDT/基础镜像版本不是同一个变量。

编译容器通过 `CONTRACTS_DIR` 挂载你的源码目录：

```bash
# 从 deploy/ 执行。
cd cdt
FLON_VERSION="${CDT_IMAGE_TAG:?set a verified floncdt tag}" \
  CONTRACTS_DIR=/absolute/path/to/contracts \
  docker compose --env-file ../.env run --rm cdt cdt-cpp --version
```

实际编译命令见[合约编译教程](build-contract.md)。本文仅校验 Compose 展开与文档示例语法，没有实际启动、同步或升级任何链上节点。

## 来源

- [官方部署说明](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/README.md)
- [普通节点模板](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/compose.common.yaml)
- [BP 模板](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/compose.bp.yaml)
- [History 模板](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/compose.history.yaml)
- [启动脚本](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/bin/start-node.sh)
- [健康检查](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/bin/healthcheck.sh)
- [CLI Compose](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/cli/compose.yaml)
- [CLI Dockerfile](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/cli/Dockerfile)
- [CDT Compose](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/cdt/compose.yaml)
- [主网环境模板](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/.env.mainnet.example)
- [测试网环境模板](https://github.com/fullon-labs/flon-docker/blob/8cba498ac0982382b8094f64ad8606ff25fb6658/deploy/.env.testnet.example)
