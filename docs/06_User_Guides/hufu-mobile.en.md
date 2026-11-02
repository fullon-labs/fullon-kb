---
title: Manage FullOn on your phone with HuFu
type: guide
status: active
updated: 2026-11-02
source: source review; user-confirmed Wallet Connect flow
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

A wallet password or phone biometrics generally protect local access. Understand these separately from on-chain signing permissions and RWID recovery conditions. Exact button labels and locations depend on the installed HuFu version and the current DApp interface.

## Connect HuFu to a PC DApp with Wallet Connect

Open a DApp that supports this feature in your PC browser, then use Wallet Connect and scan its QR code with HuFu App to connect a FullOn account from your mobile wallet.

### Connection steps

1. **On PC**: open the official DApp website, choose Connect Wallet, and select **Wallet Connect** to display a QR code.
2. **On your phone**: open HuFu App and use its scanner to scan the QR code on the PC screen.
3. **Choose an account**: select the FullOn account in HuFu and verify that its network matches the DApp, particularly mainnet versus testnet.
4. **Approve the connection**: review the DApp information and account shown by HuFu, then confirm the connection request.
5. **Return to PC**: verify that the page displays the correct FullOn account before continuing.

### After connecting

When you initiate a swap, vote, or another operation on PC, review the signing request in HuFu App, including contract, action, amount, and permission, before confirming. Connecting a wallet does not approve every subsequent transaction. Check the transaction result on the PC page or explorer after the operation.

Disconnect from the DApp when finished, especially on a public or shared computer.

### Common issues

| Issue | Action |
| --- | --- |
| QR code expired or connection timed out | Generate a fresh QR code on PC and scan it again with HuFu. |
| Wrong account or network connected | Disconnect, select the correct FullOn account/network in HuFu, and reconnect. |
| No signing request after a PC operation | Open HuFu and check requests, connection status, and network. Reconcile the original operation before submitting again. |
| No Wallet Connect option | This flow applies to DApps offering the feature; use the connection methods currently supported by that application. |

## For developers

This page explains mobile wallet use. Application integration additionally requires an officially supported SDK, callback flow, and signing protocol. Do not label generic EOSIO wallet-connection code as the official HuFu API.

Source: [HuFu repository page](../02_Ecosystems/hufu-wallet.md).
