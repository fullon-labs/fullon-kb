---
title: Comprehensive fucli command-line guide
status: active
updated: 2026-11-02
source: source review
---

# Comprehensive fucli command-line guide

## Installation and command discovery

Install a network-compatible flon-tools release from FullOn Core releases. fucli is the client, funod the node, and fuwal the local wallet service. Replace example accounts, paths, public keys and amounts. Test writes on an isolated chain or testnet first.

```bash
fucli --help
fucli --help-all
fucli version client
fucli get --help
fucli system --help
```

## Network and wallet endpoints

Node RPC and wallet RPC are separate services. Independently obtain the expected chain ID and compare get info. Never give a public node private keys. Global -u precedes subcommands; transaction-level -u can mean unpack-action-data.

```bash
export FULLON_RPC=http://127.0.0.1:8888
fucli -u "$FULLON_RPC" get info
fucli --help
```

## Create, unlock and lock a wallet

Creating a wallet does not create an on-chain account. Protect and back up both wallet and password files. umask affects newly created files in this shell; do not overwrite an existing password file. Enter secrets interactively for unlock/import rather than in command arguments. keys lists public keys; private_keys exposes secrets and is not routine diagnostics.

```bash
umask 077
fucli wallet create -n tutorial -f ./tutorial-wallet-password.txt
fucli wallet open -n tutorial
fucli wallet unlock -n tutorial
fucli wallet create_key -n tutorial K1
fucli wallet keys
fucli wallet import -n tutorial
fucli wallet list
fucli wallet lock -n tutorial
fucli wallet lock_all
```

## Query and create accounts

owner is the root permission; active commonly handles daily actions. Creation requires an authorized existing creator. Funding and naming rules depend on the network. The example 1 FLON is not a minimum fee. system activate activates protocol features, not user accounts.

```bash
fucli -u "$FULLON_RPC" get account accountname1
fucli -u "$FULLON_RPC" system newaccount creatoracct newaccount11 OWNER_PUBLIC_KEY ACTIVE_PUBLIC_KEY --fund-gas "1.0000 FLON" -p creatoracct@active
```

## Balances, supply and transfers

Matching symbols do not establish identical assets. Verify network, contract, symbol and precision. Transfers move real assets. Follow the recipient memo requirements and test with a small amount.

```bash
fucli -u "$FULLON_RPC" get currency balance flon.token accountname1 FLON
fucli -u "$FULLON_RPC" get currency stats flon.token FLON
fucli -u "$FULLON_RPC" transfer senderacct recipientacc "0.1000 FLON" "test" -c flon.token -p senderacct@active
```

## Blocks, transactions and finality

A transaction ID or accepted submission does not prove execution. Check the receipt and containing block, then wait until its block number is at or below LIB. History and Trace depend on plugins and retention; not found does not establish non-execution.

```bash
fucli -u "$FULLON_RPC" get block 12345
fucli -u "$FULLON_RPC" get transaction TRANSACTION_ID
fucli -u "$FULLON_RPC" get transaction-status TRANSACTION_ID
fucli -u "$FULLON_RPC" get actions --help
fucli -u "$FULLON_RPC" get transaction_trace --help
```

## Tables, scopes and pagination

code identifies the contract, scope the data scope, and table the table name. Verify fields and indexes against ABI/source. Paginate using more and next_key rather than row counts alone.

```bash
fucli -u "$FULLON_RPC" get table flon.token accountname1 accounts
fucli -u "$FULLON_RPC" get scope --help
fucli -u "$FULLON_RPC" get table --help
```

## Download ABI and code

ABI describes encoding/interfaces; WASM is bytecode, not C++ source. Record network, account and code hash. Avoid mixing ABI/code from different upgrade states.

```bash
fucli -u "$FULLON_RPC" get abi contractacct -f contract.abi
fucli -u "$FULLON_RPC" get code contractacct -c contract.wasm -a contract.abi
```

## Deploy and call contracts

Compile WASM/ABI and deploy to an account you control. set contract filenames are relative to its directory. Upgrades do not clear tables and code rollback does not roll back data. push action arguments must match the current ABI.

```bash
fucli -u "$FULLON_RPC" set contract contractacct ./build hello.wasm hello.abi -p contractacct@active
fucli -u "$FULLON_RPC" push action contractacct hi '{"user":"calleracct"}' -p calleracct@active
```

## Preview, sign and broadcast

-s skips signing and -d prevents broadcast. This is not execution simulation or a guarantee of success. Preparation may still need an ABI/reference block from the node. Before offline signing, verify chain ID, TAPOS, expiration, actions and authority. Rebuilding may produce another transaction ID.

```bash
fucli -u "$FULLON_RPC" push action contractacct hi '{"user":"calleracct"}' -p calleracct@active -s -d -j
fucli sign --help
fucli push transaction --help
fucli convert --help
fucli validate --help
```

## Transaction options

Options include -p for authority, -x for expiration seconds, -r for a reference block, -j for JSON, --json-file for saved JSON, and --return-packed with no-broadcast for packed data. --force-unique weakens duplicate protection and is not a timeout-retry strategy. push transactions is not atomic.

## Permissions and action links

Permission changes can lock an account out. Save current authority JSON and prepare recovery first. Understand threshold, keys, accounts and waits. Restrict automation with dedicated child permissions. Do not arbitrarily add code authority or change owner to bypass an error.

```bash
fucli set account permission --help
fucli set action permission --help
```

## Multisig workflow

The flow is proposal, independent review, approvals and execution, with unapproval/cancellation when needed. Multisig is distinct from DAO POWER snapshot voting. Execution does not grant authority to replace the transaction. Verify the deployed multisig contract and permissions.

```bash
fucli multisig propose_trx --help
fucli multisig review --help
fucli multisig approve --help
fucli multisig unapprove --help
fucli multisig exec --help
fucli multisig cancel --help
```

## Node and system commands

net peers/status/connect/disconnect manage nodes and require Net API; a public RPC is not a management endpoint. Match system commands to the deployed system ABI; old CPU/NET/RAM tutorials do not automatically apply to the current gas model. wrap exec is privileged authorization-bypass administration, not an ordinary contract call.

```bash
fucli -u "$FULLON_RPC" net peers
fucli net status --help
fucli system newaccount --help
fucli system regproducer --help
```

## Errors and automation

For wallet connection failures check local fuwal. Unknown Endpoint indicates plugin/category availability. Verify authority on authorization errors; refresh ABI and serialize again on ABI errors. Check head/expiration for expired transactions and current gas rules for resource errors. Reconcile the original after broadcast timeout. Automate with JSON, exit codes, timeouts and bounded retries; record IDs, network, time and final outcomes without secrets.

## Related reading

[RPC](../03_Operators/funod-rpc.md) · [Contracts](contracts.md) · [Tokens](issue-tokens.md) · [Transactions](transactions.md)

Source: [FullOn Core CLI](https://github.com/fullon-labs/flon-core/blob/49256d6bdb989b935e114de2b00b748f3f8b4911/programs/client/main.cpp). Commands were reviewed against source, without executing chain writes. Installed --help and target-network ABI take precedence.
