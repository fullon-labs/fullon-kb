---
title: What is a FullOn RWID account?｜RWID 账户
type: core_chain
status: active
updated: 2026-11-02
source: source review
---

# What is a FullOn RWID account?｜RWID 账户

RWID 是一套基于合约的账户创建与权限恢复方案。在本次审阅的实现中，新账户的 owner 委托给 RWID owner 合约的 active 权限，用户提供的公钥配置为新账户的 active 权限。

## 与自行管理 owner 的账户有何不同

| 项目 | 自行管理 owner 的账户 | 本次审阅的 RWID 创建路径 |
| --- | --- | --- |
| 日常签名 | 由 active authority 决定 | 由用户提供的 active 公钥与阈值决定 |
| 根权限 | 由账户配置决定 | 新建时指向 RWID owner 合约的 active |
| 修改 active | 经有权修改权限的主体授权 | RWID DAO 授权 owner 合约执行权限更新 |
| 恢复 | 取决于事先配置 | 依赖认证、恢复订单与 DAO/owner 合约流程 |

这意味着用户日常可签名，与用户独自控制所有根权限，是两个不同的问题。恢复能力依赖合约权限与认证服务，不承诺任何人仅凭手机号就能无条件恢复。

## 源码中的调用关系

`rwid.auth` 提供认证侧账户创建与恢复相关入口；`rwid.dao` 协调创建、active 权限记录和恢复；`rwid.owner` 调用系统 `newaccount`，将 owner 指向自身，并给新账户购买配置数量的 gas。

当前审阅的 owner 实现校验 active：阈值为正、公钥数量 1–10、权重为正、无重复公钥、总权重足以达到阈值，并且不接受 active 中的账户权限和 waits。此限制属于这份 RWID 合约实现，不能推广到所有普通 FullOn authority。

## 白皮书仓库中的 RWID 设计

[RWID 设计稿](https://github.com/fullon-labs/flon.whitepaper/blob/d695da53f4e453dd0e372e9dc5a605a0c56d455e/rwid-design.md)将 RWID 展开为 Real-World Identity，提出绑定手机号、邮箱、Google、WhatsApp、Telegram 等现实身份因素，并通过可配置恢复阈值与去中心化预言机验证实现密钥替换。

这些是设计目标，不是本文已确认的可用认证服务清单。它与上文实际审阅的 auth/DAO/owner 权限路径需分别看待；不能因此称当前恢复流程已完全去中心化或无信任。密钥生成、因子保存和恢复审核仍需产品级核验，详见[设计与实现差异](whitepaper.md)。

## 使用前确认

1. 当前钱包是否提供 RWID 注册入口，支持哪些认证方式。
2. 所选网络实际使用的合约账户、代码版本和权限结构。
3. 认证信息如何保存、恢复由谁审核、费用与等待条件是什么。
4. 创建后用 `get_account` 检查 owner 和 active，而不是只依赖产品标签。

本文不发布手机号、验证码或认证服务内部 API。注册和恢复应使用官方应用当前提供的受支持流程。

[手机钱包](../06_User_Guides/hufu-mobile.md) · [开发者账户流程](../10_Developer_Guides/accounts.md)

## 来源

[owner 实现](https://github.com/fullon-labs/rwid.contracts/blob/d0fcb698711a0ea807515e76cf44e357d38787f3/contracts/rwid.owner/src/rwid.owner.cpp)、[auth 接口](https://github.com/fullon-labs/rwid.contracts/blob/d0fcb698711a0ea807515e76cf44e357d38787f3/contracts/rwid.auth/include/rwid.auth/rwid.auth.hpp)、[DAO 实现](https://github.com/fullon-labs/rwid.contracts/blob/d0fcb698711a0ea807515e76cf44e357d38787f3/contracts/rwid.dao/src/rwid.dao.cpp)。源码审阅日期：2026-11-02；不代表已验证各网络部署。
