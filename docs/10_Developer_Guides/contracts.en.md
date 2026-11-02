---
title: Smart contract development path
type: index
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/contracts.md
---

# Smart contract development path

Node, CLI, and RPC examples target **FullOn Core v0.9.2**. Contracts, CDT, and wallets have independent versions; their stated verification scope does not automatically change with Core. See [version baseline and migration](../09_Release_Notes/v0.9.2.md).

Follow these executable tutorials in order:

1. [Write and compile](build-contract.md): minimal C++ contract and WASM/ABI artifacts.
2. [Retrieve ABI and code](get-abi-code.md): verify interfaces and deployed bytecode.
3. [Deploy and upgrade](deploy-contract.md): publish WASM/ABI and verify hashes/permissions.
4. [Call actions](call-actions.md): CLI calls, authorization, and integration.
5. [Issue tokens](issue-tokens.md): maximum supply, issuer, distribution, and balances.

Command parameters were checked against local source. The minimal contract was compiled separately. Chain-write commands were not run on production networks. Match toolchain, system contract, and network versions.
