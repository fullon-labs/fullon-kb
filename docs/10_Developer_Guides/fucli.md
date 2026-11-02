---
title: fucli 命令行全面使用指南
status: active
updated: 2026-11-02
source: source review
---

# fucli 命令行全面使用指南

## 安装与命令发现

从 FullOn Core 发布页取得与网络兼容的 flon-tools；fucli 是客户端，funod 是节点，fuwal 是本地钱包服务。以下占位账户、路径、公钥与金额均须替换；写命令先在隔离链或测试网验证。

```bash
fucli --help
fucli --help-all
fucli version client
fucli get --help
fucli system --help
```

## 网络与钱包服务

节点 RPC 与钱包 RPC 是不同服务。先独立取得可信 chain ID，再核对 get info；不要将私钥交给公共节点。全局 -u 放在子命令前；交易子命令中的 -u 可表示 unpack-action-data，不能混用。

```bash
export FULLON_RPC=http://127.0.0.1:8888
fucli -u "$FULLON_RPC" get info
fucli --help
```

## 钱包创建、解锁与锁定

创建钱包不是创建链上账户。密码文件与钱包文件都需备份并保护。umask 仅作用于当前 shell 新文件；不要覆盖已有密码文件。unlock/import 不在命令行填写秘密，按交互提示输入，避免 shell 历史记录。keys 输出公钥；private_keys 会暴露私钥，不用于常规排错。

```bash
umask 077
fucli wallet create -n tutorial -f ./tutorial-wallet-password.txt
fucli wallet open -n tutorial
fucli wallet unlock -n tutorial
fucli wallet create_key -n tutorial K1
fucli wallet keys
fucli wallet import -n tutorial
fucli wallet list
fucli wallet lock -n tutorial
fucli wallet lock_all
```

## 账户查询与创建

owner 是根权限，active 常用于日常操作。新账户需已有创建者授权；资金和命名限制由目标网络决定。示例 1 FLON 不是最低开户费。system activate 用于协议特性，不是账户激活。

```bash
fucli -u "$FULLON_RPC" get account accountname1
fucli -u "$FULLON_RPC" system newaccount creatoracct newaccount11 OWNER_PUBLIC_KEY ACTIVE_PUBLIC_KEY --fund-gas "1.0000 FLON" -p creatoracct@active
```

## 余额、供应量与转账

同名符号不等于同一资产，必须核对网络、合约、符号与精度。转账会真实移动资产；memo 按收款方要求填写，先小额测试。

```bash
fucli -u "$FULLON_RPC" get currency balance flon.token accountname1 FLON
fucli -u "$FULLON_RPC" get currency stats flon.token FLON
fucli -u "$FULLON_RPC" transfer senderacct recipientacc "0.1000 FLON" "test" -c flon.token -p senderacct@active
```

## 区块、交易与最终性

交易 ID 或提交成功不代表执行成功。检查执行回执和所在区块，再等待区块号不高于 LIB。历史与 Trace 接口依赖插件和保留策略；查询不到不等于未执行。

```bash
fucli -u "$FULLON_RPC" get block 12345
fucli -u "$FULLON_RPC" get transaction TRANSACTION_ID
fucli -u "$FULLON_RPC" get transaction-status TRANSACTION_ID
fucli -u "$FULLON_RPC" get actions --help
fucli -u "$FULLON_RPC" get transaction_trace --help
```

## 合约表、scope 与分页

code 是合约，scope 是数据作用域，table 是表名。字段与索引按 ABI 及合约实现确定。分页用返回的 more 和 next_key 推进，不能只按行数推断结束。

```bash
fucli -u "$FULLON_RPC" get table flon.token accountname1 accounts
fucli -u "$FULLON_RPC" get scope --help
fucli -u "$FULLON_RPC" get table --help
```

## 下载 ABI 与代码

ABI 描述编码与接口，WASM 是字节码，不是 C++ 源码。记录网络、账户和 code hash；升级时避免把不同时刻的 ABI 与代码混用。

```bash
fucli -u "$FULLON_RPC" get abi contractacct -f contract.abi
fucli -u "$FULLON_RPC" get code contractacct -c contract.wasm -a contract.abi
```

## 部署与调用合约

先编译 WASM/ABI，再部署到你控制的账户。set contract 文件名相对目录；升级不会清空旧表，回滚代码也不会回滚数据。push action 参数应与当前 ABI 一致。

```bash
fucli -u "$FULLON_RPC" set contract contractacct ./build hello.wasm hello.abi -p contractacct@active
fucli -u "$FULLON_RPC" push action contractacct hi '{"user":"calleracct"}' -p calleracct@active
```

## 预览、签名与广播

-s 跳过签名，-d 不广播；这不是执行模拟，也不保证交易能成功。预览仍可能需要节点 ABI/参考区块。离线签名前核对 chain ID、TAPOS、有效期、动作和权限。重建可能产生新交易 ID。

```bash
fucli -u "$FULLON_RPC" push action contractacct hi '{"user":"calleracct"}' -p calleracct@active -s -d -j
fucli sign --help
fucli push transaction --help
fucli convert --help
fucli validate --help
```

## 交易选项

常用选项：-p 指定授权；-x 指定过期秒数；-r 指定参考区块；-j 输出 JSON；--json-file 保存 JSON；--return-packed 与不广播组合输出 packed 数据。--force-unique 会削弱重复交易保护，不应作为超时重试手段。批量 push transactions 不是原子操作。

## 权限与动作绑定

权限变更可能锁死账户，先备份权限 JSON 并准备恢复方案。以 threshold、keys、accounts、waits 理解 authority；用专用子权限限制自动化操作。不要为解决普通授权报错随意添加合约代码权限或改 owner。

```bash
fucli set account permission --help
fucli set action permission --help
```

## 多签流程

流程是提出交易、逐方审阅、收集批准、执行，必要时撤销批准或取消。多签不是 DAO 的 POWER 快照投票，也不是谁执行就能替换交易。先确认目标网络多签合约与权限。

```bash
fucli multisig propose_trx --help
fucli multisig review --help
fucli multisig approve --help
fucli multisig unapprove --help
fucli multisig exec --help
fucli multisig cancel --help
```

## 节点与系统命令

net peers/status/connect/disconnect 是节点管理，需要 Net API，不能把公共 RPC 当作管理入口。system 子命令必须与已部署系统合约 ABI 匹配；旧版 CPU/NET/RAM 教程不能自动套用到当前 gas 模型。wrap exec 是特权绕过授权的管理能力，不是普通调用入口。

```bash
fucli -u "$FULLON_RPC" net peers
fucli net status --help
fucli system newaccount --help
fucli system regproducer --help
```

## 常见错误与脚本化

钱包连接失败先检查本地 fuwal；Unknown Endpoint 检查插件/类别；权限错误核对当前 authority；ABI 错误重新获取接口并序列化；过期错误核对链头和有效期；资源不足按当前 gas 规则处理。广播超时先对账原交易，不能直接重发。脚本用 JSON、退出码、超时和有界重试，保留交易 ID、网络、时间与最终结果，不记录秘密。

## 延伸阅读

[RPC](../03_Operators/funod-rpc.md) · [Contracts](contracts.md) · [Tokens](issue-tokens.md) · [Transactions](transactions.md)

来源：[FullOn Core CLI](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/programs/client/main.cpp). 命令按源码核对，未执行链上写交易；以安装版本的 --help 和目标网络 ABI 为准。
