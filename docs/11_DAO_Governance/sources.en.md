---
title: Governance sources, verification, and discrepancies
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# Governance sources, verification, and discrepancies

## Integrated sources

- [DAO DApp README](https://github.com/fullon-labs/flon.daogov/blob/93aadcf3c8421cd4ae9228696c9501196dd8febb/README.md): wallets, BPs, proposals, and community entry points.
- [Governance user help](https://github.com/fullon-labs/flon.daogov/blob/93aadcf3c8421cd4ae9228696c9501196dd8febb/docs/governance-help.md): power, phases, risk, and rewards.
- [Operations guide](https://github.com/fullon-labs/flon.daogov/blob/93aadcf3c8421cd4ae9228696c9501196dd8febb/docs/operations-guide.md) and [Keeper README](https://github.com/fullon-labs/flon.daogov/blob/93aadcf3c8421cd4ae9228696c9501196dd8febb/keeper/README.md): newer role/operations boundaries.
- [Interface phase derivation](https://github.com/fullon-labs/flon.daogov/blob/93aadcf3c8421cd4ae9228696c9501196dd8febb/src/governance.js): explains the interface, not authoritative chain validation.
- [DAO implementation](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/dao.gov/src/dao.gov.cpp) and [interface/tables](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/dao.gov/include/dao.gov/dao.gov.hpp).
- [Treasury implementation](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/dao.treasury/src/dao.treasury.cpp), [BP voting](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.system/src/voting.cpp), and [reward claiming](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.system/src/producer_pay.cpp).
- [Mainnet read-only responses and code hashes, 2026-11-02](mainnet-snapshot.json), with [interpretation](rules-and-parameters.md).

A local mainnet operations draft dated 2026-11-01 was also reviewed. It was uncommitted in the DApp repository and partly outdated, so it was not directly published as current configuration.

## Resolving source differences

| Source statement | Verified behavior / treatment |
| --- | --- |
| Allocation sum must not exceed principal | Listed system source requires equality with target locked principal; the guide states that constraint. |
| reserve reduces liquid / release restores liquid | Source reserve increases reserved only; release decreases reserved only. Available balance is liquid - reserved. |
| closegrant closes completed/released grants | Listed source accepts only open, expired grants; completed/released are other terminal states. |
| Keeper drives external closeepoch | New operations documentation describes onblock closure and reward-claim assistance; verify the deployment version. |
| New guide includes standbyproof | Observed mainnet ABI lacks it; described conditionally, not as a live mainnet command. |
| November 1 mainnet allowlists empty, higher thresholds | November 2 reads show five enabled entries and changed thresholds; publish dated evidence instead of static current-state claims. |
| Endorsement and formal votes use one snapshot | Source accumulates endorsement-time power without per-account activation recomputation; formal votes read activation checkpoints. |
| Proposal stores full per-action authorization | proposal_action stores target/action/bytes; authorization comes from allowlist, is immutable for existing rules in the reviewed version, and is checked again at execution. |

## Verification limits

Read-only queries verify chain ID, tables, code hashes, and ABI action presence. They are not protocol audits, liveness audits, or reproducible source-to-WASM proofs. Independent reads are not an atomic single-block snapshot. Values change; mainnet and testnet need separate confirmation.
