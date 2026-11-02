---
title: Official FullOn FAQ integration
status: active
updated: 2026-11-02
source: official FAQ synthesis
translation_of: contributing/faq-integration.md
---

# Official FullOn FAQ integration

All eight official FAQ topics have been integrated into this site. Follow the local pages below to read their content without leaving GitHub Pages. The source pages were retrieved on 2026-11-02; historical or aspirational statements are not deployment guarantees.

| Official topic | Retrieved content | Integrated page |
| --- | --- | --- |
| [What is FullOn](../01_Core_Chain/chain-overview.md) | L1, scalability, low latency, fast finality, interoperability positioning | [Definition](../01_Core_Chain/chain-overview.md) |
| [Basic properties](../01_Core_Chain/specifications.md) | Heading only | [Source specifications and unknowns](../01_Core_Chain/specifications.md) |
| [Account types](../01_Core_Chain/accounts.md) | Native & sovereign, proxy, social-recoverable, simple address; WASM/EVM-managed variants | [Categories](../01_Core_Chain/accounts.md) and [account basics](../01_Core_Chain/accounts.md) |
| [Resources](../01_Core_Chain/resource-model.md) | Heading only | [Resources](../01_Core_Chain/resource-model.md), supplemented with source/query paths |
| [Tokenomics](../01_Core_Chain/tokenomics.md) | Heading only | [Tokenomics](../01_Core_Chain/tokenomics.md), with the evidence gap stated |
| [VM](../01_Core_Chain/virtual-machine.md) | Native WASM and EVM-like execution through WASM | [VM](../01_Core_Chain/virtual-machine.md), with compatibility limits |
| [Interoperability](../01_Core_Chain/interoperability.md) | Heading only | [Interoperability](../01_Core_Chain/interoperability.md), separate from bridge applications |
| [Ecosystems](../02_Ecosystems/README.md) | Web3, AI, and Social directions | [Ecosystems](../02_Ecosystems/README.md) |

## Differences and boundaries

- The original “fast finality” statement gives no numerical latency. The source's 0.5-second block interval is not a finality claim.
- Account categories do not fully explain registration or recovery. RWID is reviewed separately and is not assumed equivalent to all social-recovery systems.
- EVM-like execution does not prove live compatibility with Ethereum JSON-RPC, MetaMask, or Solidity tools.
- Heading-only resource, tokenomics, and interoperability pages do not establish fees, supply, returns, or bridge protocols.
- Ecosystem plans and partnerships do not establish that every service is live.

Source URLs, SHA-256 hashes, and retrieval status are recorded in the [source manifest](https://fullon-labs.github.io/fullon-kb/contributing/faq-source-manifest.json) for later comparison.

## Source attribution

[Original official FAQ](https://docs.flon.network/fullon-faq) · [Retrieval records](https://fullon-labs.github.io/fullon-kb/contributing/faq-source-manifest.json). These links document provenance; the reading pages above are hosted on this site.

## Whitepaper supplement (2026-11-02)

The table above records the FAQ itself. The v2.5.0 whitepaper supplements [specifications](../01_Core_Chain/specifications.md), [resources](../01_Core_Chain/resource-model.md), [tokenomics](../01_Core_Chain/tokenomics.md), and [interoperability](../01_Core_Chain/interoperability.md), with additional [governance](../01_Core_Chain/governance.md) and [roadmap](../01_Core_Chain/roadmap.md) topics.

An empty FAQ source page therefore does not mean this site lacks a topic guide. The clarification draft places future issuance and burning of remaining GAS reserves under future FullOn DAO Gov decisions. The [verification record](../01_Core_Chain/whitepaper.md) retains revision status, source limitations, and deployment questions.
