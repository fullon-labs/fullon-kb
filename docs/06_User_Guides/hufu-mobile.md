---
title: 手机管理 FullOn 钱包：下载与使用 HuFu
type: guide
status: active
updated: 2026-11-02
source: source review; user-confirmed Wallet Connect flow
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

钱包密码或手机生物识别通常保护本地访问；它们与链上签名权限、RWID 恢复条件应分别理解。具体按钮文字与位置以当前安装的 HuFu 版本和 DApp 界面为准。

## PC 网页通过 Wallet Connect 连接 HuFu

在 PC 浏览器打开支持该功能的 DApp 后，可以使用 Wallet Connect，通过 HuFu App 扫描二维码，连接手机钱包中的 FullOn 账户。

### 连接步骤

1. **PC 端**：打开 DApp 官方网页，点击连接钱包，选择 **Wallet Connect**，显示连接二维码。
2. **手机端**：打开 HuFu App，使用扫码功能扫描 PC 页面上的二维码。
3. **选择账户**：在 HuFu 中选择要连接的 FullOn 账户，确认网络与 DApp 一致，尤其注意主网与测试网。
4. **确认连接**：核对 HuFu 显示的 DApp 信息与账户，确认连接请求。
5. **返回 PC**：检查页面已显示正确的 FullOn 账户，再继续操作。

### 连接后如何操作

在 PC 页面发起兑换、投票或其他操作后，按 HuFu App 中收到的签名请求核对合约、动作、金额和权限，再决定是否确认。连接钱包本身不代表已批准之后的每笔交易；操作完成后仍需在 PC 页面或浏览器查询交易结果。

使用完毕可在 DApp 断开连接，尤其是在公共或共用电脑上。

### 常见问题

| 问题 | 处理 |
| --- | --- |
| 二维码失效或连接超时 | 在 PC 重新生成二维码，再用 HuFu 扫描。 |
| 连接了错误账户或网络 | 断开当前连接，在 HuFu 选择正确的 FullOn 账户和网络后重新连接。 |
| PC 发起操作后未看到签名请求 | 打开 HuFu 检查请求，核对连接状态和网络；先查原操作结果，避免重复提交。 |
| DApp 没有 Wallet Connect 入口 | 该流程适用于提供此功能的 DApp；按该应用当前支持的连接方式操作。 |

## 开发者注意

本页说明终端用户如何安装和使用手机钱包；应用集成需另外取得官方支持的 SDK、回调与签名协议。不要把通用 EOSIO 钱包连接代码直接标为 HuFu 官方 API。

来源：[仓库 HuFu 介绍](../02_Ecosystems/hufu-wallet.md)。
