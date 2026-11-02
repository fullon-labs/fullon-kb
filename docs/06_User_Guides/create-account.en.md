---
title: Create a FullOn account
type: guide
status: active
updated: 2026-11-02
source: source review
translation_of: 06_User_Guides/create-account.md
---

# Create a FullOn account

Goal: obtain an account that can be queried and used to sign on your chosen network.

## Choose a creation method

- **Ordinary wallet creation or import**: for users managing their own keys. Check how owner and active are configured.
- **RWID registration in a wallet or application**: for users of that product's authentication/recovery service. Read [RWID accounts](../01_Core_Chain/rwid-accounts.md) first. Availability, authentication methods, and fees depend on the application.
- **Creation by an existing account**: a team or developer submits the on-chain creation. Users should generate and keep their own keys and provide only public keys to the creator.

## Create on a phone

1. Install the official wallet using the [HuFu guide](hufu-mobile.md) and choose the FullOn network.
2. Select the account method offered by the current application. Importing an existing key is not new account creation.
3. Complete the name, backup, or authentication steps and review displayed fees and terms.
4. Wait for on-chain creation and save the account name and creation transaction ID, if provided.
5. Query the account in the same network's explorer, then try a small wallet operation.

## What counts as activation?

Application registration, wallet generation, on-chain account creation, and sufficient gas are different states. Confirm existence using an explorer or `get_account`. Follow wallet instructions if resources are insufficient. No universal `activate account` action has been verified for all account types.

If creation fails, check name availability/restrictions, network, creation-service health, and fees. Do not pay repeatedly for the same creation request.

[Transfers](transfer-token.md) · [Developer commands](../10_Developer_Guides/accounts.md)
