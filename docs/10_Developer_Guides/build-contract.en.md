---
title: Write and build a smart contract
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/build-contract.md
---

# Write and build a smart contract

Node, CLI, and RPC examples target **FullOn Core v0.9.2**. Contracts, CDT, and wallets have independent versions; their stated verification scope does not automatically change with Core. See [version baseline and migration](../09_Release_Notes/v0.9.2.md).

## Toolchain

Choose a compatible toolchain from the official [CDT repository and releases](https://github.com/fullon-labs/flon.cdt). Installation varies by platform/version. The installed `cdt-cpp --version` returned `0.9.0` during verification; this is not a recommendation for every network.

## Minimal C++ contract

Create `hello.cpp`:

```cpp
#include <eosio/eosio.hpp>

class [[eosio::contract("hello")]] hello : public eosio::contract {
public:
    using eosio::contract::contract;

    [[eosio::action]]
    void hi(eosio::name user) {
        eosio::require_auth(user);
        eosio::print("Hello, ", user);
    }
};
```

`require_auth(user)` requires authorization from that account. This example prints text only; it does not persist data or transfer assets.

## Compile

```bash
cdt-cpp --version
mkdir -p build
cdt-cpp -abigen -contract hello -o build/hello.wasm hello.cpp
```

Confirm `build/hello.wasm` and `build/hello.abi` exist. The ABI should contain action `hi` with parameter `user`. Record compiler version, source commit, and build command for reproducibility.

## Test

On an isolated chain or testnet, verify valid authorization succeeds, missing authorization fails, and ABI parameters are correct. More complex contracts also need table migrations, integer boundaries, resource usage, repeated calls, and external notifications checked. Compilation alone does not establish safety or production readiness.

Next: [deploy](deploy-contract.md) and [call actions](call-actions.md).

Sources: [CDT](https://github.com/fullon-labs/flon.cdt), its `examples/hello`, and the local compilation check.
