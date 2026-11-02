---
title: "Whitepaper integration: scope and source conflicts"
status: active
updated: 2026-11-02
source: whitepaper v2.6.0 Core v0.9.2 baseline and policy clarification draft
---

# Whitepaper integration: scope and source conflicts

This page summarizes protocol design in the whitepaper v2.6.0 clarification draft (2026-11-02); it does not certify deployment on any network.

## Pinned sources

Published baseline: [English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/c1b5ed6cc8572fc79c9eacd964b04d4ca60e8d9a/fullon.whitepaper.md) · [Chinese whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/c1b5ed6cc8572fc79c9eacd964b04d4ca60e8d9a/fullon.whitepaper.cn.md) · [Implementation source manifest](https://github.com/fullon-labs/flon.whitepaper/blob/c1b5ed6cc8572fc79c9eacd964b04d4ca60e8d9a/v0.9.2-source-manifest.json).

Whitepaper v2.6.0 (2026-11-02) is published with Core v0.9.2 as its implementation baseline and CDT v0.9.0 as an independently versioned contract API reference. The pinned revision includes that baseline plus a separate pending future issuance/GAS policy clarification; the extra draft policy is not presented as effective rules. `rwid-design.md` is pinned at the same revision. Historical README entries are not deployment evidence.

[Resources](resource-model.md) · [Tokenomics](tokenomics.md) · [Interoperability](interoperability.md) · [Governance](governance.md) · [Roadmap](roadmap.md)

Four original FAQ pages contain only headings. That does not mean the wider official documentation lacks explanations. This update adds whitepaper design while retaining the FAQ retrieval record; source and on-chain inspection remain necessary to establish implementation and deployment.

## Core v0.9.2 new and cumulative capabilities

- **Elastic production statistics:** `get_producer_slot_stats_v2` separates produced, genuinely missed, and `idle_skipped` slots. `expected = produced + missed`; idle skips do not reduce availability. The v0.9.1 actual-producer attribution fix is included.
- **GAS metering:** `get_gas_fee_totals` exposes cumulative consumption and corresponding FLON value for checkpoint-difference accounting. Counters do not transfer funds, authorize issuance, or change reserve rules.
- **Roles and history:** core/history builds and a tools package; optional RocksDB history with backpressure, fork rollback, and coverage/gap diagnostics. A missing result is not proof that a transaction never occurred.
- **Operations and recovery:** management listeners default to loopback or Unix sockets; signing remains Unix-only. Offline physical checkpoints, restore continuation, and operation locks provide explicit recovery paths, not automatic crash recovery or BP failover.
- **v0.9.2-specific fix:** preserve the legacy activated `ACTION_DATA_TO_JSON` digest for replay compatibility, without activating a replacement feature.

New intrinsics require compatible validators, feature activation, matching CDT interfaces, and system contracts. QSA-V1 remains a design draft; two-dimensional sharding, DSR, and universal cross-chain deployment are not established release capabilities. See [release and migration notes](../09_Release_Notes/v0.9.2.md) and the whitepaper repository's implementation source manifest.

## Confirmed governance clarification

- The current 500-million-FLON mining budget stops at exhaustion. FullOn DAO Gov separately decides whether and how to authorize future issuance, with implementation upgrades when required.
- Part of GAS-linked value rewards eligible Active and Standby BPs. The remainder is locked by default; DAO Gov decides future burns, without touching required ELON redemption backing.

Resource, reward, inflation and deflation wording is aligned in both whitepaper languages in the same proposed revision.

## Governance power terminology

Governance power is recorded in the internal account ledger, not issued, transferred or burned as a separate governance token. Changes in locked principal update available power; activated proposals retain their frozen snapshots.

## Remaining source differences and verification boundaries

| Topic | Different source statements | Treatment |
| --- | --- | --- |
| Block interval | Source has 500ms slots; the revised whitepaper identifies a 12s reference heartbeat rather than a hard maximum | Separate slot duration from produced-block interval; verify deployed policy |
| Performance/finality | The revised whitepaper labels 10,000+ TPS and 1–1.5s finality as conditional design targets | Whitepaper specifications, not measurements or SLAs verified here |
| EVM | The revised whitepaper identifies native WASM and a separate EVM integration | Do not infer a second VM in the Core package or invent MetaMask/Ethereum RPC configuration |
| Allocation/unlocking | Foundation percentage denominator and cliff/vesting timing need clarification | Do not calculate current circulation, TGE date or investor unlock dates from ambiguous wording |
| RWID | Design proposes multiple social factors, thresholds and decentralized oracle recovery; inspected implementation uses auth/DAO/owner controls | Separate design goals from reviewed permissions; do not certify deployed trustless recovery |

The RWID design also says a contract generates a new keypair locally for a user. This is not treated as an implementation instruction. Verify where key generation occurs, who can access private keys and which public keys/permissions change on-chain; do not infer that an on-chain contract can generate and conceal a user's private key.

## Deployment checks still required

Network chain IDs/endpoints, fees, producer membership, registration terms, TGE/vesting status, supported proxy wallets/chains, EVM endpoints and RWID providers require separate verification.

No funds, permissions or nodes are changed by this documentation update. Upstream whitepaper changes are submitted separately; proposed policy text is not deployment evidence. See the [source hash manifest](../contributing/whitepaper-source-manifest.json).

## Sources

[English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.md) · [Chinese whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/5758318eba75d48afd1d543bf020255c1a998d26/fullon.whitepaper.cn.md) · [Scope and source conflicts](whitepaper.md). Pinned revision `5758318eba75d48afd1d543bf020255c1a998d26`; retrieved 2026-11-02. The Core v0.9.2 baseline is published; the additional future issuance/GAS policy clarification remains a separate draft, not a deployment certification.
