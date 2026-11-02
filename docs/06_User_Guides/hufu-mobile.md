---
title: 手机管理 FullOn 钱包：下载与使用 HuFu
type: guide
status: active
updated: 2026-11-02
source: source review
---

# 手机管理 FullOn 钱包：下载与使用 HuFu

目标：在手机安装钱包，管理账户并连接 DApp。

## Download and install HuFu APP

1. 从 [HuFu 官网](https://hufu.io)查找适合 iOS 或 Android 的下载入口。
2. 核对下载页面发行方和官方说明。仓库尚未确认可长期使用的 App Store / Google Play 直链，因此不提供猜测的商店链接或安装包地址。
3. 安装后设置应用提供的本地保护方式，并按提示创建或导入账户。
4. 选择 FullOn 网络，核对完整账户名，按[开户指南](create-account.md)确认账户已在链上创建。
5. 按钱包提示备份恢复材料；更换或重置手机前先验证你具备可用的恢复方式。

## 日常操作

- 收款：复制正确网络和资产对应的收款信息。
- 转账：核对账户、资产合约、数量和 memo，见[转账指南](transfer-token.md)。
- 参与 DApp：从官方入口进入并确认签名内容，见[DApp 指南](use-dapps.md)。
- 兑换：见[FullSwap 操作指南](fullswap.md)。
- 多账户：每次操作前检查当前账户，避免从错误账户签名。

钱包密码或手机生物识别通常保护本地访问；它们与链上签名权限、RWID 恢复条件应分别理解。本文未对当前 HuFu 界面逐屏核验，因此不假设按钮名称、内置浏览器或连接协议一定存在。

## 开发者注意

本页说明终端用户如何安装和使用手机钱包；应用集成需另外取得官方支持的 SDK、回调与签名协议。不要把通用 EOSIO 钱包连接代码直接标为 HuFu 官方 API。

来源：[仓库 HuFu 介绍](../02_Ecosystems/hufu-wallet.md)。
