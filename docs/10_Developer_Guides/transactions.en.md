---
title: 'Transactions: signing, broadcast, and confirmation'
type: guide
status: active
updated: 2026-11-02
source: repository synthesis
translation_of: 10_Developer_Guides/transactions.md
---

# Transactions: signing, broadcast, and confirmation

Node, CLI, and RPC examples target **FullOn Core v0.9.2**. Contracts, CDT, and wallets have independent versions; their stated verification scope does not automatically change with Core. See [version baseline and migration](../09_Release_Notes/v0.9.2.md).

Goal: display reliable transaction states and prevent duplicate business operations.

## Recommended flow

1. Obtain the expected chain ID from trusted configuration and verify it with `get_info`.
2. Build actions using the current deployed ABI. Specify account, permission, parameters, asset precision, and memo. Use `abi_json_to_bin` for conversion where appropriate and recheck authorization before signing.
3. Construct a transaction with expiration and a reference block using a compatible SDK/wallet. No general wallet SDK version or HuFu signing API has been verified here; guessed SDK calls are not supplied.
4. Sign with a wallet or controlled signer. Never send private keys to Chain, History, Trace, or explorer services.
5. Broadcast the packed transaction in the selected endpoint's format. Retain transaction ID, business request ID, network, and submission time; see the [RPC reference](../03_Operators/funod-rpc.md).
6. Check execution and the containing block. After successful execution, wait for `block_num <= last_irreversible_block_num` before marking it irreversible.

## States and retries

| State | Application behavior |
| --- | --- |
| Awaiting user signature | Allow cancellation; do not show successful payment |
| Request accepted, e.g. HTTP 202 | Node accepted processing; continue tracking execution |
| Executed and included | Verify execution/business outcome and wait for LIB |
| Successful and irreversible | Complete settlement under the business policy |
| Timeout or temporarily missing | Unknown state; reconcile the original transaction and business record |
| Definite failure | Explain an actionable reason, then rebuild and sign after correction |

Persist business request IDs with deduplication constraints. Rebuilding can create a new transaction ID; transport retries are not business idempotency. Batch `push_transactions` is not an atomic transaction.

## Query limitations

- `get_transaction_status` is conditional and has bounded retention; discover capability first.
- History/Trace depend on local indexes and retention. Not found does not establish non-execution.
- Read current balances, permissions, and tables from Chain API; history supports tracking/display.
- Forks can change reversible records. Allow state rollback before irreversibility.

[History and finality](../03_Operators/transaction-history-rpc.md) · [Troubleshooting](troubleshooting.md)
