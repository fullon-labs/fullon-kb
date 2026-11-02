---
title: Whitepaper integration: scope and source conflicts
status: active
updated: 2026-11-02
source: whitepaper v2.4.0 synthesis
---

# Whitepaper integration: scope and source conflicts

This page summarizes protocol design in whitepaper v2.4.0 (2026-10-22); it does not certify deployment on any network.

## Pinned sources

The English and Chinese main whitepapers and `rwid-design.md` were read from the same official repository revision. The main documents identify v2.4.0, 2026-10-22 and Core/CDT v0.8.7. The README's older v2.1 revision note mentions v0.8.5; it is not a universal deployment baseline.

[Resources](resource-model.md) · [Tokenomics](tokenomics.md) · [Interoperability](interoperability.md) · [Governance](governance.md) · [Roadmap](roadmap.md)

Four original FAQ pages contain only headings. That does not mean the wider official documentation lacks explanations. This update adds whitepaper design while retaining the FAQ retrieval record; source and on-chain inspection remain necessary to establish implementation and deployment.

## Differences retained explicitly

| Topic | Different source statements | Treatment |
| --- | --- | --- |
| Mining cap | BP section forbids mining beyond the 500-million budget; inflation section mentions later DAO-approved issuance | Do not interpret the latter as permission to extend mining; issuance scope and total-supply constraints need clarification |
| GAS and burning | Resource section retains reserve FLON after ELON consumption; deflation section uses one-way conversion/burn wording | Distinguish liability retirement, reserve locking and actual token burning |
| Block interval | Source has 500ms slots; whitepaper describes 0.5s active and up to 12s idle production | Separate slot duration from produced-block interval; verify deployed policy |
| Performance/finality | 10,000+ TPS and 1–1.5s finality claims | Whitepaper specifications, not measurements or SLAs verified here |
| EVM | Whitepaper claims 100% compatibility; existing verified path is native WASM/RPC | Retain attribution without inventing MetaMask or Ethereum RPC configuration |
| Allocation/unlocking | Foundation percentage denominator and cliff/vesting timing need clarification | Do not calculate current circulation, TGE date or investor unlock dates from ambiguous wording |
| RWID | Design proposes multiple social factors, thresholds and decentralized oracle recovery; inspected implementation uses auth/DAO/owner controls | Separate design goals from reviewed permissions; do not certify deployed trustless recovery |

The RWID design also says a contract generates a new keypair locally for a user. This is not treated as an implementation instruction. Verify where key generation occurs, who can access private keys and which public keys/permissions change on-chain; do not infer that an on-chain contract can generate and conceal a user's private key.

## Deployment checks still required

Network chain IDs/endpoints, fees, producer membership, registration terms, TGE/vesting status, supported proxy wallets/chains, EVM endpoints and RWID providers require separate verification.

No funds, permissions or nodes are changed by this documentation update; upstream whitepaper files are unchanged. See the [source hash manifest](../contributing/whitepaper-source-manifest.json).

## Sources

[English whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.md) · [Chinese whitepaper](https://github.com/fullon-labs/flon.whitepaper/blob/f49e5f0f821162a997260535be30767e3f147d8e/fullon.whitepaper.cn.md) · [Scope and source conflicts](whitepaper.md). Pinned revision `f49e5f0f821162a997260535be30767e3f147d8e`; retrieved 2026-11-02.
