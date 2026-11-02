---
title: Trade tokens on FullSwap
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 06_User_Guides/fullswap.md
---

# Trade tokens on FullSwap

FullSwap is an AMM swap application listed in this repository. The goal is to exchange one asset for another and verify actual receipt.

## Prepare

Have a wallet account on the target network, the input asset, and sufficient operation resources. Enter through the [official site](https://fullswap.flon.network). Supported networks, pairs, fees, and screens depend on the current application.

## Swap steps

1. Connect your wallet and verify network/account.
2. Select input and output tokens. Check complete contracts and symbols rather than names or icons alone.
3. Enter the input amount and review the quote, route, fees, price impact, and minimum received where displayed.
4. Understand slippage: execution prices may change after quoting. Increasing tolerance lowers the minimum acceptable result; do not raise it blindly to bypass an error.
5. Review asset, amount, receiving contract, and actions in the wallet. The FullSwap implementation can trigger swaps through token `transfer` notifications and a memo; an action named `transfer` is not necessarily a simple payment.
6. Sign, save the transaction ID, and check successful execution and [irreversibility](transaction-status.md).
7. Verify the output-token balance. A transaction may contain multiple inline actions; inspect the full transaction and balance changes.

## Common issues

| Issue | Action |
| --- | --- |
| Token or pair missing | Check network, contract, and supported markets; avoid same-name substitutes |
| Quote changed / slippage failure | Refresh the quote and assess size and price impact before signing |
| Insufficient liquidity | Assess size; a displayed quote does not guarantee execution |
| Submitted but balance unchanged | Check the original transaction and contract before another swap |
| Unclear memo or contract | Stop signing and verify with official support |

Token issuance does not automatically create a FullSwap listing or liquidity. Developers: see [issuing tokens](../10_Developer_Guides/issue-tokens.md).

## Evidence and scope

The [FullSwap project page](../07_DApps/fullswap.md) provides its official entry. Local contract revision `582fcccb469098f78532b502803db137b3c00c58`, `flon.swap.hpp`, documents transfer-memo swap notifications. The live interface and deployed code were not reverified; no production swap memo template is provided.
