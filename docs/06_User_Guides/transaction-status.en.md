---
title: Check transaction status and receipt
type: guide
status: active
updated: 2026-11-02
source: repository synthesis
translation_of: 06_User_Guides/transaction-status.md
---

# Check transaction status and receipt

Goal: distinguish wallet messages, on-chain execution, and recipient crediting.

1. Copy the complete transaction ID and query an explorer on the same network.
2. Check execution status, contract, actions, sender, recipient, amount, and memo. A transaction ID alone is not proof of a successful transfer.
3. Check the block and irreversibility. If it is only included, wait for confirmation. Developers can compare the block number with LIB; see [transaction integration](../10_Developer_Guides/transactions.md).
4. If the chain shows success but the wallet balance is stale, refresh and check network/token. For exchange deposits, check confirmations, minimum amounts, and memo rules.

| Observation | Meaning and next step |
| --- | --- |
| Wallet submitted | A request was sent; still check execution |
| Included but reversible | A fork can still affect it; wait |
| Execution failed | Read the error; this is not a successful payment |
| Not found | Wrong network, not yet included, or missing index coverage are possible; failure is not established |
| Successful and irreversible | On-chain execution is confirmed; the receiving service may have a separate crediting process |

Do not immediately resend an unlocated transaction. Keep its ID, submission time, and error details, then follow [troubleshooting](troubleshooting.md).
