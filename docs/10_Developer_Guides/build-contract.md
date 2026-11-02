---
title: How to build a smart contract｜编写与编译合约
type: guide
status: active
updated: 2026-11-02
source: source review
---

# How to build a smart contract｜编写与编译合约

## 准备工具

从官方 [CDT 仓库与 releases](https://github.com/fullon-labs/flon.cdt)选择与目标网络兼容的工具链。安装方式依平台和版本而异；本文核验本机 `cdt-cpp --version` 输出为 `0.9.0`，不代表推荐所有网络使用该版本。

## 最小 C++ 合约

创建 `hello.cpp`：

```cpp
#include <eosio/eosio.hpp>

class [eosio::contract("hello")](eosio::contract("hello").md) hello : public eosio::contract {
public:
    using eosio::contract::contract;

    [eosio::action](eosio::action.md)
    void hi(eosio::name user) {
        eosio::require_auth(user);
        eosio::print("Hello, ", user);
    }
};
```

`require_auth(user)` 要求调用者满足该账户授权。此示例只打印文本，不持久化数据，也不转移资产。

## 编译

```bash
cdt-cpp --version
mkdir -p build
cdt-cpp -abigen -contract hello -o build/hello.wasm hello.cpp
```

检查生成 `build/hello.wasm` 和 `build/hello.abi`，ABI 中应存在 `hi` 动作和 `user` 参数。保持编译器版本、源码提交和构建命令可追溯。

## 测试要点

在隔离链或测试网验证有效授权成功、缺少授权失败、ABI 参数正确。较复杂合约还应验证表迁移、整数边界、资源用量、重复调用和外部通知。仅编译通过不等于安全或可上线。

下一步：[部署合约](deploy-contract.md)、[调用动作](call-actions.md)。

来源：[CDT](https://github.com/fullon-labs/flon.cdt)、其 `examples/hello` 与本地工具链编译核验。
