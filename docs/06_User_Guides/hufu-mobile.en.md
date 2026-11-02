---
title: Manage FullOn on your phone with HuFu
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 06_User_Guides/hufu-mobile.md
---

# Manage FullOn on your phone with HuFu

Goal: install a mobile wallet, manage accounts, and connect to DApps.

## Download and install HuFu APP

1. Find the iOS or Android download on the [official HuFu website](https://hufu.io).
2. Check the publisher and official instructions. Stable App Store / Google Play direct links have not been confirmed in this repository, so no guessed store or package URLs are provided.
3. Set up the application's local protection and follow its account creation/import flow.
4. Select FullOn, verify the full account name, and confirm on-chain creation using the [account guide](create-account.md).
5. Back up recovery material. Before replacing or resetting your phone, verify you have a working recovery method.

## Daily use

- Receive: copy receiving information for the correct network and asset.
- Transfer: check account, token contract, amount, and memo; see [transfers](transfer-token.md).
- DApps: enter through official links and review signing requests; see [DApp use](use-dapps.md).
- Swap: see the [FullSwap guide](fullswap.md).
- Multiple accounts: check the active account before each operation.

A wallet password or phone biometrics generally protect local access. Understand these separately from on-chain signing permissions and RWID recovery conditions. The current HuFu screens were not verified step by step; specific button names, an in-app browser, or a connection protocol are not assumed.

## For developers

This page explains mobile wallet use. Application integration additionally requires an officially supported SDK, callback flow, and signing protocol. Do not label generic EOSIO wallet-connection code as the official HuFu API.

Source: [HuFu repository page](../02_Ecosystems/hufu-wallet.md).

[Desktop: download and use the HuFu Chrome extension](hufu-extension.md)
