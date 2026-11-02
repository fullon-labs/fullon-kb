---
title: Developer troubleshooting
type: guide
status: active
updated: 2026-11-02
source: repository synthesis
translation_of: 10_Developer_Guides/troubleshooting.md
---

# Developer troubleshooting

Node, CLI, and RPC examples target **FullOn Core v0.9.2**. Contracts, CDT, and wallets have independent versions; their stated verification scope does not automatically change with Core. See [version baseline and migration](../09_Release_Notes/v0.9.2.md).

| Symptom | Check | Action |
| --- | --- | --- |
| Connection failure / timeout | URL, TLS, proxy, node health | Set timeouts and bounded retries; query read-only state first |
| 404 / Unknown Endpoint | Supported APIs, plugins, categories, version | Use available routes rather than assuming reference availability |
| 400 | JSON, field types, account, ABI, permission | Read `error.name`, `what`, and `details`; correct deterministic errors |
| 503 / proxy 429 | Concurrency, rate, capacity | Exponential backoff with bounded attempts/concurrency |
| Empty history / transaction missing | Chain ID, full ID, index retention/sync | Use a known block hint; ask operators about coverage if necessary |
| Balance/history disagree | Network/sync, index lag, contract/scope | Cross-check current state with Chain API |
| Permission/signature failure | Account, permission, current keys, signing network | Reload permissions/ABI; do not bypass with broader permissions |
| Broadcast timeout | Original transaction, inclusion, business deduplication | Reconcile before rebuilding/signing again |

The `/v1/history/*` prefix is often more compatible, but still discover capabilities. Do not publicly expose Net, Producer, Snapshot, or signing management APIs just to resolve a 404.

## Reproducible reports

Record node version, chain ID, endpoint, redacted request, HTTP status, error, time/timezone, and transaction ID if relevant. Remove private keys, authorization headers, passwords, and access tokens.

[RPC error model](../03_Operators/funod-rpc.md) · [History operational notes](../03_Operators/transaction-history-rpc.md)
