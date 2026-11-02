---
title: DAO Gov governance help
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# DAO Gov governance help

[Open FullOn DAO Gov](https://daogov.flon.network/). Verify that the site, wallet, and RPC use the same network. These guides organize DApp help and contract rules around user, developer, and operator tasks.

## Users

1. [Getting started and governance power](getting-started.md): connect a wallet and distinguish FLON from POWER.
2. [Proposals, endorsement, voting, and execution](proposals.md): from discussion to execution.
3. [BP voting and rewards](bp-voting-rewards.md): locked principal, allocation, pending changes, and claims.
4. [Treasury and grants](treasury.md): reserve, pay, release, and expiry closure.
5. [Troubleshooting](troubleshooting.md).

## Rules and networks

[Thresholds and mainnet parameter snapshot](rules-and-parameters.md): L1–L4, the three passing conditions, timing, allowlists, and rollout boundaries. A snapshot is not live state, and testnet values are not mainnet rules.

## Developers and operators

- [DAO contract integration](developer-reference.md): tables, scopes, ABI, actions, and lifecycle.
- [Keeper and Standby operations](operations.md): automatic epoch closure, reward claims, and BP-authorized proofs.
- [Sources and verification](sources.md).

## Distinguish three operations

| Operation | Purpose | Directly executes proposal business actions? |
| --- | --- | --- |
| Allocate locked FLON to BPs | Node selection and reward attribution | No |
| DAO endorsement / formal voting | Decide community authorization | No |
| Execute an approved proposal | Run frozen actions still satisfying policy | Yes; may change parameters or transfer treasury funds |

POWER is not a tradable token. Endorsement is not a For vote, and approval is not immediate execution.
