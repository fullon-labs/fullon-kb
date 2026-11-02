---
title: DAO contract integration and state queries
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# DAO contract integration and state queries

## Verify network and ABI

Typical accounts are `dao.gov`, `dao.treasury`, `flon`, and `voter.reward`; confirm target configuration/deployed ABI. Read chain ID, code hashes, ABI, global/config. Stay read-only if uninitialized or missing required actions; do not fabricate data or simulated success.

These read-only examples use a local node. Replace RPC and independently verify chain ID before remote use:

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

## Tables and scopes

| code | table | scope | Purpose |
| --- | --- | --- | --- |
| dao.gov | global / config | dao.gov | Administration, power source/total, base rules |
| dao.gov | powers | dao.gov | Current account POWER |
| dao.gov | checkpoints | Voter account name | Power sequence history |
| dao.gov | proposals / policysnaps | dao.gov | Proposal and policy snapshots |
| dao.gov | riskconfigs / actpolicies / allowlist | dao.gov | Risk thresholds, action classification, execution authority |
| dao.gov | endorsements / ballots | Decimal proposal_id string | Endorsement/vote records |
| dao.treasury | global / assets / grants | dao.treasury | Governance account, asset accounting, grants |
| dao.treasury | payments | Decimal grant_id string | Installment records |

Example for proposal_id=1; replace it with a real ID:

```bash
curl --fail --silent --show-error --max-time 15 \
  -X POST "$FULLON_RPC/v1/chain/get_table_rows" \
  -H 'Content-Type: application/json' \
  --data '{"json":true,"code":"dao.gov","scope":"1","table":"ballots","limit":100}' | jq
```

Follow `more` / `next_key`; limit=100 is not a completeness guarantee. Avoid JavaScript floating-point precision loss for uint64, asset integers, and bps calculations. Respect chain timestamp semantics; derive phase from time windows as well as status.

## User actions

| Method | Parameters / constraints |
| --- | --- |
| propose | proposer, proposal_type, title, summary, content_hash, metadata_uri, discussion_uri, actions; see ABI |
| endorse | endorser, proposal_id; individual threshold and uniqueness |
| castvote | voter, proposal_id, choice; 0 Against, 1 For, 2 Abstain; no changes |
| activate / finalize / queue / execute / expire | proposal_id; phase, time, and policy constraints |
| cancel / setforum | Proposer only, during endorsement |

These are **two independent syntax examples**, not consecutive workflow steps. They write on-chain. Use only on an isolated chain or verified testnet, replace account/ID/permission, and separately satisfy each action's phase. Do not test them on mainnet:

```bash
fucli -u "$FULLON_RPC" push action dao.gov endorse \
  '{"endorser":"voteracct","proposal_id":1}' -p voteracct@active
fucli -u "$FULLON_RPC" push action dao.gov castvote \
  '{"voter":"voteracct","proposal_id":1,"choice":2}' -p voteracct@active
```

## Frozen payload and execution authority

`proposal_action` contains contract, action_name, and data, not per-action authorization. execution_hash hashes the packed action list. Execution reads authorization_actor / authorization_permission from allowlist. Reviewed setallow forbids changing an existing rule's actor/permission, but enabled/size limits may change. Queue/execute revalidate policy.

Serialize against the target ABI and verify the content SHA-256. Forum text/page titles are not executable instructions. New ABI/parameters require a new proposal, not edits to frozen payloads. Record network, proposal ID, snapshot, transaction ID, and resulting state; wait for LIB before business confirmation.

## Source limits

Source review does not establish deployment on every chain. Published mainnet code hashes were not compared with a reproducible source-to-WASM build. See the [parameter page](rules-and-parameters.md) for endorsement-power limitations.

## Sources and scope

[Sources, snapshots, and discrepancies](sources.md). Implementation descriptions use the listed revisions; live configuration must be read from the target network.
