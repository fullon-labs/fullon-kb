---
title: Issue a new token
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 10_Developer_Guides/issue-tokens.md
---

# Issue a new token

Goal: deploy standard token logic to an account you control, create a symbol, issue to its issuer, and distribute to users.

## Three account roles

- **Token contract account**: hosts code/tables; example `tokenexample`.
- **Issuer**: allowed to increase supply; example `issueracct`.
- **Holder**: receives/transfers tokens; example `holderacct`.

You cannot freely create tokens in someone else's `flon.token`. The reference `create` requires the token contract's own authorization. First deploy reviewed token WASM/ABI to your controlled account; see [deployment](deploy-contract.md).

## Create, issue, and transfer

These commands submit transactions. Use an isolated development chain or testnet first. Replace example accounts and deploy a token contract matching the reviewed behavior.

```bash
export FULLON_RPC='http://127.0.0.1:8888'
fucli -u "$FULLON_RPC" push action tokenexample create   '{"issuer":"issueracct","maximum_supply":"1000000.0000 DEMO"}'   -p tokenexample@active

fucli -u "$FULLON_RPC" push action tokenexample issue   '{"to":"issueracct","quantity":"1000.0000 DEMO","memo":"initial issue"}'   -p issueracct@active

fucli -u "$FULLON_RPC" push action tokenexample transfer   '{"from":"issueracct","to":"holderacct","quantity":"10.0000 DEMO","memo":"distribution"}'   -p issueracct@active
```

`DEMO` and four decimal places are examples. `create` sets maximum supply and precision but does not issue tokens. The reference `issue` requires `to` to be the issuer, a positive amount, matching precision, and sufficient remaining supply. Issue to the issuer, then transfer to holders.

## Read and verify

```bash
curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_currency_stats"   -H 'Content-Type: application/json'   --data '{"code":"tokenexample","symbol":"DEMO"}' | jq

curl --fail --silent --show-error --max-time 15   -X POST "$FULLON_RPC/v1/chain/get_currency_balance"   -H 'Content-Type: application/json'   --data '{"code":"tokenexample","account":"holderacct","symbol":"DEMO"}' | jq
```

Check max_supply, supply, issuer, balances, and successful irreversible execution of each transaction. Network, contract, symbol, and precision together identify the asset.

## After issuance

Wallet display, explorer icons, FullSwap markets, and liquidity are separate processes. Issuance does not automatically list a token. Publish its contract, issuance/upgrade authority, and purpose, then follow each application's current integration process.

## Sources and scope

[Source 1](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.token/src/flon.token.cpp), [Source 2](https://github.com/fullon-labs/flon.contracts/blob/d34fc8f588e4bcc581e1377e729a248e0098f090/contracts/flon.token/include/flon.token/flon.token.hpp). Source review: 2026-11-02. This does not verify the version deployed on every network.
