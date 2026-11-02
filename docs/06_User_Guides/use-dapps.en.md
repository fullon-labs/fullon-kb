---
title: 'Use DApps: connect, authorize, and confirm'
type: guide
status: active
updated: 2026-11-02
source: repository synthesis
translation_of: 06_User_Guides/use-dapps.md
---

# Use DApps: connect, authorize, and confirm

Goal: understand an application's purpose and verify the actual operation before signing.

## Choose an application

The following purposes and links come from existing draft pages. Current availability, supported assets, and terms were not reverified.

| Application | Recorded purpose | Details |
| --- | --- | --- |
| FullSwap | AMM asset swaps | [Project and official entry](../07_DApps/fullswap.md) |
| FullBridge | Cross-chain bridge | [Project and official entry](../07_DApps/fullbridge.md) |
| FullVest | Token locks and linear release | [Project and official entry](../07_DApps/fullvest.md) |
| RWAVerse | RWA application | [Project and official entry](../07_DApps/rwaverse.md) |

## General steps

1. Enter through the project's official link and verify domain, network, and wallet account.
2. Connect your wallet. Distinguish connecting an account from signing a transaction.
3. Check operation-specific parameters: input/output assets and minimum received for swaps; source/destination chain, recipient, and supported assets for bridges; beneficiary and release time for locks.
4. Review every action and authority shown by the wallet. If the application's description differs from the signing payload, stop and verify with the project.
5. Use a small test first, save the transaction ID, and [check the result](transaction-status.md).
6. For bridging, retain the source transaction, application order ID, and destination transaction. Source-chain success does not establish destination receipt.

Do not infer undisclosed rules. Current application disclosures govern swap fees, bridge timing, redemptions, and reward conditions.
