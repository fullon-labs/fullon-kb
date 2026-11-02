---
title: DAO 合约接入与状态查询
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# DAO 合约接入与状态查询

## 先确认网络与 ABI

目标账户通常为 `dao.gov`、`dao.treasury`、`flon`、`voter.reward`，仍应以所选网络配置和已部署 ABI 为准。读取 chain ID、代码哈希、ABI、global/config；未初始化或缺关键 action 时保持只读，不生成假数据或模拟成功。

下例仅查询本机节点。远程使用前替换 RPC 并独立核对 chain ID：

```bash
export FULLON_RPC='http://127.0.0.1:8888'
curl --fail --silent --show-error --max-time 15 \
  -X POST "$FULLON_RPC/v1/chain/get_info" \
  -H 'Content-Type: application/json' --data '{}' | jq
curl --fail --silent --show-error --max-time 15 \
  -X POST "$FULLON_RPC/v1/chain/get_table_rows" \
  -H 'Content-Type: application/json' \
  --data '{"json":true,"code":"dao.gov","scope":"dao.gov","table":"riskconfigs","limit":100}' | jq
```

## 表与 scope

| code | table | scope | 用途 |
| --- | --- | --- | --- |
| dao.gov | global / config | dao.gov | 管理、票权来源、总量、基础规则 |
| dao.gov | powers | dao.gov | 当前账户 POWER |
| dao.gov | checkpoints | voter 账户名 | 票权序列历史 |
| dao.gov | proposals / policysnaps | dao.gov | 提案与风险/规则快照 |
| dao.gov | riskconfigs / actpolicies / allowlist | dao.gov | 风险门槛、动作等级和执行授权 |
| dao.gov | endorsements / ballots | proposal_id 的十进制字符串 | 附议与投票记录 |
| dao.treasury | global / assets / grants | dao.treasury | 治理账户、资产账目与预算 |
| dao.treasury | payments | grant_id 的十进制字符串 | 分期付款记录 |

proposal_id=1 的查询示例，须换成实际 ID：

```bash
curl --fail --silent --show-error --max-time 15 \
  -X POST "$FULLON_RPC/v1/chain/get_table_rows" \
  -H 'Content-Type: application/json' \
  --data '{"json":true,"code":"dao.gov","scope":"1","table":"ballots","limit":100}' | jq
```

分页读取 `more` / `next_key`；不要将一次 limit=100 的结果当作全量。uint64、资产整数和 bps 运算避免 JavaScript 浮点精度损失。接口的时间字段按链上语义解释；当前 UI 阶段不能只看 status，还需比较窗口。

## 用户动作

| 方法 | 参数/约束 |
| --- | --- |
| propose | proposer、proposal_type、title、summary、content_hash、metadata_uri、discussion_uri、actions；详见 ABI |
| endorse | endorser、proposal_id；个人门槛与唯一记录 |
| castvote | voter、proposal_id、choice；0 反对、1 赞成、2 弃权，不能改票 |
| activate / finalize / queue / execute / expire | proposal_id；受阶段、时间和策略限制 |
| cancel / setforum | proposer 身份，且仅附议阶段 |

以下是**两种独立操作的语法示例**，不是需要连续执行的步骤；会产生写交易。只在隔离链或已核对的测试网替换账户、ID、权限并独立满足各自阶段后使用，不在主网试跑：

```bash
fucli -u "$FULLON_RPC" push action dao.gov endorse \
  '{"endorser":"voteracct","proposal_id":1}' -p voteracct@active
fucli -u "$FULLON_RPC" push action dao.gov castvote \
  '{"voter":"voteracct","proposal_id":1,"choice":2}' -p voteracct@active
```

## 冻结数据与实际授权

`proposal_action` 包含 contract、action_name、data，没有逐动作 authorization 字段；execution_hash 对打包后的 action 列表求哈希。执行时从 allowlist 读取 authorization_actor / authorization_permission。核验版本的 setallow 禁止修改既有规则的授权身份/权限，但 enabled 与大小限制可变；queue/execute 仍重新校验策略。

按目标 ABI 序列化 bytes，核对原始内容 SHA-256，不将 forum 内容或页面标题当作可执行指令。新 ABI/新参数应重新构造提案，不能在已冻结提案上替换。记录网络、提案 ID、快照、交易 ID 和目标状态；等 LIB 后再完成业务确认。

## 来源限制

源码描述不证明任意链部署相同实现。本次发布附有主网代码哈希，但没有进行源码到链上 WASM 的可复现构建比对。附议累计 POWER 的实现边界见[参数页](rules-and-parameters.md)。

## 来源与范围

[源码、查询快照与资料差异](sources.md)。实现说明基于所列提交；运行配置以目标网络当前状态为准。
