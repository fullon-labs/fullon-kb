---
title: Receive and transfer assets
type: guide
status: active
updated: 2026-11-02
source: repository synthesis
translation_of: 06_User_Guides/transfer-token.md
---

# Receive and transfer assets

Goal: transfer the intended asset on the correct network and confirm the result.

## Receive

1. Select the network and asset in your wallet and copy the complete receiving account or provided receiving information.
2. Tell the sender the network, account, asset, and required memo. Exchanges or custodial services may require a memo; follow the receiving deposit page.
3. Start with a small test and verify it in the correct explorer before proceeding.

## Send

1. Verify network, recipient, token contract, and symbol. Identical symbols do not guarantee identical assets.
2. Enter the amount and required memo. Do not assume clipboard contents are correct.
3. On the signing screen, recheck recipient, amount, contract, actions, authorizing account, and displayed resources/fees. Follow current wallet instructions if funding is insufficient; this guide gives no fixed fee.
4. Sign when the details are correct and save the transaction ID. Do not click send repeatedly.
5. Use the [transaction-status guide](transaction-status.md) to check execution, recipient balance changes, and irreversibility.

## Completion check

Execution succeeded, transfer data is correct, and the containing block is irreversible. An exchange may still require its own deposit processing.

For errors or missing funds, check the original transaction before retrying; see [troubleshooting](troubleshooting.md).
