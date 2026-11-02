---
title: Official FullOn FAQ integration
status: active
updated: 2026-11-02
source: official FAQ synthesis
translation_of: 04_FAQ/official-faq.md
---

# Official FullOn FAQ integration

All eight official FAQ topics have been integrated into this site. Follow the local pages below to read their content without leaving GitHub Pages. The source pages were retrieved on 2026-11-02; historical or aspirational statements are not deployment guarantees.

| Official topic | Retrieved content | Integrated page |
| --- | --- | --- |
| [What is FullOn](what-is-fullon.md) | L1, scalability, low latency, fast finality, interoperability positioning | [Definition](what-is-fullon.md) |
| [Basic properties](../01_Core_Chain/specifications.md) | Heading only | [Source specifications and unknowns](../01_Core_Chain/specifications.md) |
| [Account types](account-types.md) | Native & sovereign, proxy, social-recoverable, simple address; WASM/EVM-managed variants | [Categories](account-types.md) and [account basics](../01_Core_Chain/accounts.md) |
| [Resources](resource-model.md) | Heading only | [Resources](resource-model.md), supplemented with source/query paths |
| [Tokenomics](tokenomics.md) | Heading only | [Tokenomics](tokenomics.md), with the evidence gap stated |
| [VM](vm.md) | Native WASM and EVM-like execution through WASM | [VM](vm.md), with compatibility limits |
| [Interoperability](interoperability.md) | Heading only | [Interoperability](interoperability.md), separate from bridge applications |
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
