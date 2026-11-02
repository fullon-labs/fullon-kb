---
title: HuFu Wallet Chrome extension: download and use
type: guide
status: active
updated: 2026-11-02
source: official website entry and Chrome documentation
---

# HuFu Wallet Chrome extension: download and use

This guide is for desktop Chrome. For phones, see the [HuFu App guide](hufu-mobile.md). Installing an extension, creating a local wallet, having an on-chain account, and connecting a DApp are separate steps.

## Official download entry points

- [HuFu website](https://hufu.io): start with its Chrome download entry.
- [Search HuFu Wallet in the Chrome Web Store](https://chromewebstore.google.com/search/HuFu%20Wallet): the current official-site destination is a search page, **not a verified fixed extension-detail listing**.

The website's published assets were checked on 2026-11-02. No fixed extension ID, publisher identity, or particular store version was independently verified. If results are ambiguous or their connection to HuFu cannot be established, confirm through official support rather than relying on a name, icon, or ranking.

## Install and pin

1. Open the official entry in a normal desktop Chrome window. Check the listing's publisher, website association, permissions, and update information.
2. Once the official extension is confirmed, choose Add to Chrome, review the requested permissions, and confirm Add extension.
3. Open HuFu from Chrome's extensions menu. Pin its icon if useful.
4. Follow the current initialization flow. Organization-managed browsers may restrict installation; check those policies first.

A file offered by a website is not automatically a Chrome Web Store installation. No unverified CRX, ZIP, or unpacked-extension package is supplied here.

## Create or import a wallet and account

1. Use the creation/import methods supported by the current version. Handle recovery material only in the confirmed official extension interface.
2. Configure its local access protection and make a secure backup. Never give DApps wallet passwords, private keys, or recovery phrases.
3. When importing, verify public keys/permissions, full account name, and network. Importing a key does not create an on-chain account.
4. For a new account, complete [on-chain creation](create-account.md), then verify its existence in the correct explorer.

A local extension password is not on-chain owner authority or a recovery guarantee. Chrome sign-in/browser synchronization is not proof that wallet keys are backed up. Verify recovery before removing the extension or changing browser profiles.

## Select FullOn and receive assets

Select the application's required FullOn network if supported by the extension. If it is absent, confirm support with HuFu rather than guessing RPC or chain-ID settings. Mainnet and testnet are separate.

Verify account, token contract, symbol, and precision before copying receiving information. Start small; see [transfers and memos](transfer-token.md).

## Connect to a DApp and sign

1. Open an official application entry, such as [DAO Gov](https://daogov.flon.network/) or [FullSwap](https://fullswap.flon.network).
2. Unlock the extension and check account/network. Select HuFu browser extension if the application offers it. QR connection to a phone wallet is a separate method and is not inherently required for extension use.
3. Review the requesting origin and account in the extension before approving connection. Refresh an already-open DApp after installation if necessary for detection.
4. Account connection does not approve subsequent transactions. Review network, contract, actions, parameters, authority, amounts, and actual recipients before every signature.
5. Retain the transaction ID and verify successful execution and [irreversibility](transaction-status.md). Reconcile the original before retrying after timeouts or stale balances.

Reconnect and recheck after changing accounts/networks. Disconnect DApp sessions and lock the extension when finished. Disconnecting does not reverse executed transactions or alter on-chain permissions.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| No listing or multiple similar names | Start from the official site and verify publisher/website association; ask official support if uncertain. |
| Icon missing | Check installation/enabled status in the current Chrome profile. Pinning is not installation. |
| DApp cannot detect the extension | Check enabled/unlocked state and site access, then refresh. Do not grant all-sites access blindly. |
| Signing window absent | Check pending requests, browser profile, and site access; reconcile any broadcast before retrying. |
| Wrong connected account/network | Switch in the extension, disconnect/reconnect, and verify full account name and chain ID. |
| FLON balance but zero governance power | Liquid balance and internal DAO POWER differ; balance alone does not establish voting eligibility. |

## Sources and verification scope

- [HuFu website](https://hufu.io): published Chrome store-search destination checked on 2026-11-02.
- [Chrome installation and management help](https://support.google.com/chrome_webstore/answer/2664769?hl=en).

No extension installation, wallet inspection, or real signing was performed. Screens, supported networks, and connection methods depend on the current official version.
