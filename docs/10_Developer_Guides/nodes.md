---
title: How to launch a node｜普通节点与 BP 节点
type: guide
status: active
updated: 2026-11-02
source: source review
---

# How to launch a node｜普通节点与 BP 节点

## 先选择角色

| 角色 | 职责 | 构建包 | 是否需要生产身份/密钥 |
| --- | --- | --- | --- |
| 普通同步 / Seed | 校验、同步与 P2P 传播 | `flon-node` core | 否 |
| RPC | 当前状态查询与交易入口 | `flon-node` core | 否 |
| History | 历史索引、Trace / State History | `flon-node-history` | 否 |
| BP | 同步、校验并在排班允许时生产区块 | `flon-node` core | 是 |

运行相同链的节点不要求成为 BP。普通节点也会验证区块；只有配置身份和签名、完成目标链要求并进入活动排班的 BP 才能实际出块。

## 安装与网络准备

1. 从 [Core releases](https://github.com/fullon-labs/flon-core/releases)选择与目标网络兼容的版本和平台；不要把开发分支直接当生产版本。
2. 验证发布包校验和，解压对应 node 包；CLI/钱包工具另取 `flon-tools`。
3. 从网络运营方取得可信 genesis 或兼容快照、预期 chain ID、P2P peers、升级要求。
4. 为每个进程使用独立配置和数据目录，规划磁盘、日志和监控。快照格式与版本必须兼容，快照不保证包含历史索引。

当前知识库未核验主网/测试网 genesis、快照下载地址及硬件最低值，因此不提供猜测性参数。

## 启动普通同步节点

发布包包含 `config/seed.ini`；复制到自己的配置目录后补充网络 peers。

```bash
mkdir -p ./node-config ./node-data
cp ./config/seed.ini ./node-config/config.ini
# 启动前编辑 node-config/config.ini，补齐目标网络的 P2P 配置。
./bin/funod --config-dir ./node-config --config config.ini   --data-dir ./node-data --genesis-json /path/to/verified-genesis.json
```

`/path/to/verified-genesis.json` 是必替换路径；此命令用于新的数据目录。已有链状态的重启按对应版本要求处理，不要混入另一网络 genesis。若用快照恢复，请按照该版本 `funod --help` 和发布说明选择恢复方式。

## RPC 节点

开启需要的 `eosio::chain_api_plugin`，对外只暴露必要的 chain read/write。若启用管理 API，须使用分类监听器将管理类别限制在回环或受保护的 Unix socket。不要原样将包含管理插件的通用 preset 放到公网。

## BP 节点额外步骤

1. 按当前网络治理要求申请/注册 BP，准备独立的生产签名能力。
2. 在 BP 配置中使用 `producer-name = yourbpaccount`，通过受保护的签名提供者配置对应生产公钥；不要把私钥写入仓库、发布包或截图。
3. 如目标链启用 Savanna，按其要求完成 finalizer 身份与密钥配置。生产签名与 finalizer 职责需分别核实。
4. 同步到链头，核对活动 producer schedule 和 finalizer 策略。注册成功不等于进入活动排班。
5. 观察实际生产、漏块、LIB 推进和签名服务健康。不要让同一生产身份在多个未协调实例上同时签名。

BP 应将 HTTP 绑定本地，公开查询交给独立 RPC/History 节点。不要仅靠配置 `producer-name` 判断已具备 BP 资格。

## 验收与排错

检查预期 chain ID、head/LIB 持续推进、P2P 连接、资源与磁盘余量、日志错误和角色需要的 API。`core` 包不能通过配置开启编译时排除的 History 插件。

[配置 P2P](p2p.md) · [RPC 接入](quickstart.md)

## 来源

[打包与节点角色](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/docs/node-build-profiles.md)、[Core 安装说明](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/README.md)。配置与命令基于源码审阅，未在生产网络启动新节点。
