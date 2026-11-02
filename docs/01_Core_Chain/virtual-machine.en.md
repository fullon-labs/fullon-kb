---
title: What is FullOn’s VM?
status: active
updated: 2026-11-02
source: official FAQ synthesis
translation_of: 01_Core_Chain/virtual-machine.md
---

# What is FullOn’s VM?

The official FAQ describes native WASM support and EVM-like execution through WASM.

The verified native development path is C/C++ → CDT → WASM + ABI. That short compatibility statement does not establish which EVM services are deployed, whether Ethereum JSON-RPC is exposed, or whether Solidity/MetaMask can be used directly.

Start with the [contract build tutorial](../10_Developer_Guides/build-contract.md). For EVM requirements, obtain the target network's implementation, addresses, interfaces, and toolchain documentation first.

Source: [official VM page](https://docs.flon.network/fullon-faq/what_are_fullon_virtual_machines), retrieved 2026-11-02.

## Whitepaper supplement

Whitepaper v2.6.0 identifies native WASM and a separate EVM integration, rather than a second VM verified in the Core v0.9.2 package. Target-network EVM endpoints and tooling require verification. See [specifications and differences](../01_Core_Chain/whitepaper.md).
