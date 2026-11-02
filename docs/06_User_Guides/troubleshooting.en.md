---
title: User troubleshooting and support
type: guide
status: active
updated: 2026-11-02
source: repository synthesis
translation_of: 06_User_Guides/troubleshooting.md
---

# User troubleshooting and support

| Issue | Check first | Next step |
| --- | --- | --- |
| Account or balance missing | Network, full account name, asset contract | Cross-check in the same network's explorer; avoid importing keys into unfamiliar tools |
| Insufficient resources/fees | Displayed resource category and available balance | Follow current wallet instructions, not a fixed fee inferred from old docs |
| Signing canceled / insufficient authority | Selected account, required permission, cancellation | Verify permissions; do not arbitrarily expand authority |
| Transfer not found | Transaction ID, network, time, explorer index | Keep evidence and query the original before paying again |
| Chain success but exchange not credited | Memo, asset, minimum amount, confirmations | Give the receiving service the transaction ID and public details |
| Bridge not received | Source status, order, destination address | Ask official bridge support to reconcile the order before repeating |

## Include in a support request

- Wallet/application name, version, and network.
- Public account name, transaction ID, time, and timezone.
- Steps, expected outcome, actual error, or redacted screenshots.
- Source/destination chain and order ID for bridge issues.

Never provide private keys, recovery phrases, passwords, verification codes, or credential-bearing URLs. No unified support channel has been verified in this repository; find support through the wallet or project's official website.
