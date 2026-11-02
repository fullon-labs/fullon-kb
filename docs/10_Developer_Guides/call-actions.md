---
title: How to call smart contract actions｜调用合约动作
type: guide
status: active
updated: 2026-11-02
source: source review
---

# How to call smart contract actions｜调用合约动作

本文的节点、CLI 与 RPC 目标版本为 **FullOn Core v0.9.2**。合约、CDT 和钱包各有独立版本；其已注明的核验范围不因 Core 升级自动改变。详见[版本基线与升级说明](../09_Release_Notes/v0.9.2.md)。

## 用 CLI 调用

先[读取当前 ABI](get-abi-code.md)，核对动作字段、类型与授权要求。下面调用[hello 示例](build-contract.md)；需要已部署合约和已准备好的签名钱包，命令将提交写交易。

```bash
export FULLON_RPC='http://127.0.0.1:8888'
fucli -u "$FULLON_RPC" push action contractacct hi   '{"user":"calleracct"}' -p calleracct@active
```

`contractacct` 是合约账户，`calleracct` 是需要签名的用户账户。JSON 对象字段来自 ABI，不是网页显示名称；权限 `-p` 也不能凭空赋予调用者授权。

## 从应用发起

1. 获取目标网络 chain ID 与合约 ABI，构建 action 的 account、name、authorization、data。
2. 使用已确认兼容的 SDK 或钱包协议序列化、签名。
3. 广播 packed transaction，再核对执行结果与不可逆状态，见[交易开发](transactions.md)。

HTTP `abi_json_to_bin` 只转换参数，不签名也不提交。节点 RPC 通常不接受随意拼接的明文 action JSON 作为完整已签名交易。

## 错误处理

缺少授权时读取当前权限；ABI 不匹配时重新序列化并重新签名；资源不足时按当前链规则处理。广播超时先查原交易，不能直接生成第二笔相同业务交易。

## 来源

[fucli 动作调用实现](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/programs/client/main.cpp)、[RPC 参考](../03_Operators/funod-rpc.md)。
