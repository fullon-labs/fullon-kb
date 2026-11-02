---
title: What is a FullOn account?｜FullOn 账户
type: core_chain
status: active
updated: 2026-11-02
source: source review
---

# What is a FullOn account?｜FullOn 账户

FullOn 账户是链上身份：账户名用于定位身份，权限用于决定谁能执行操作。代币余额通常保存在代币合约的表中，而不是由钱包安装包保存。

## 账户、密钥与钱包

| 概念 | 作用 |
| --- | --- |
| 账户名 | 链上可查询的身份，收款和调用动作时使用 |
| 公钥 | 可公开，用于链上授权配置 |
| 私钥 | 生成签名，应由持有人或受控签名器保护 |
| 钱包 | 管理密钥、展示账户并请求签名的应用 |
| 权限 authority | threshold 与带权公钥、账户权限或等待项组成的授权规则 |

账户通常具有 `owner` 和 `active` 权限。`owner` 是根权限，`active` 用于日常操作；实际授权还可能包含专用子权限和动作绑定。一个账户可以由多个公钥或账户权限共同控制，不应把账户等同于单个私钥。

## 官方账户分类

白皮书将 canonical/主权账户、EVM 地址账户与代理账户分开：主权账户使用命名身份与单签/多签权限；EVM 地址在 EVM 环境内有意义；代理账户绑定外部链身份，通过代理签名提交参与 FullOn 应用。

原 FAQ 另列 social-recoverable 和 simple address 分类。两份资料的分类范围不完全相同；不能把 RWID、代理账户和 EVM 地址互相等同，也不能从“12 字元英数字”文字推断所有拉丁字母/数字均可作为账户名。实际命名规则仍看目标链系统合约。

[互操作性及账户区别](interoperability.md)。

## 创建与使用

生成密钥只发生在本地；账户必须经链上 `newaccount` 创建后才能查询和使用。创建者需拥有可授权账户并承担所需资源。具体命名规则与目标网络部署的系统合约有关，不能假设任意短名都可注册。

普通账户可自行配置 owner 与 active；[RWID 账户](rwid-accounts.md)采用不同的 owner 管理和恢复路径。选择前应先了解谁有能力修改你的日常签名权限。

查询当前权限：`get_account`。历史公钥索引、钱包缓存或旧截图不能代替当前链上权限。

[用户开户](../06_User_Guides/create-account.md) · [开发者创建账户](../10_Developer_Guides/accounts.md)

## 来源

[CLI 账户创建与权限参数](https://github.com/fullon-labs/flon-core/blob/2188e4f94a1e9fe564a31c33e497b464556f3650/programs/client/main.cpp)、[系统合约命名检查](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.system/src/flon.system.cpp)。源码审阅日期：2026-11-02。

来源：[官方账户分类](https://docs.flon.network/fullon-faq/what_are_fullon_account_types)，读取日期 2026-11-02。
