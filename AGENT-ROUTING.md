# FullOn Agent Retrieval Routing

## Goal
Route each question to the most relevant part of the FullOn knowledge base before answering.

## Routing rules

### 1. Protocol / chain concepts
Use:
- `docs/01_Core_Chain/`
- `docs/05_Glossary/`
- `docs/04_FAQ/`

Examples:
- what is FullOn
- account types
- VM
- interoperability
- resource model
- tokenomics

### 2. Ecosystem / project questions
Use:
- `docs/02_Ecosystems/`
- `docs/07_DApps/`

Examples:
- HuFu Wallet
- Cisum AI
- Gnos AI
- FullSwap
- FullBridge
- FullVest
- RWAVerse

### 3. User, developer, and operator workflows

- Wallet setup, transfers, DApp usage, transaction status, and user support:
  `docs/06_User_Guides/`.
- RPC onboarding, transaction integration, contract development, and developer
  troubleshooting: `docs/10_Developer_Guides/`, then `docs/03_Operators/`
  for the detailed API reference.
- Node plugins, listeners, history indexing, and operational controls:
  `docs/03_Operators/`.

Do not route ordinary wallet users to node configuration or contract deployment.
Preserve source verification dates and distinguish documented interfaces from
currently deployed node capabilities.

### 4. Canonical short answers
Use:
- `docs/04_FAQ/`

Examples:
- quick explanation questions
- repeated user-facing questions

### 5. Policies and wording
Use:
- `docs/08_Policies/`

Examples:
- how to answer
- source attribution
- response style

### 6. Historical context only
Use:
- `docs/09_Release_Notes/`
- `docs/99_Archive/`

Only when the user asks about past changes or deprecated content.

## Retrieval sequence
1. Identify the question type.
2. Search the most relevant directory first.
3. If needed, search the next most relevant directory.
4. Answer using the smallest sufficient set of pages.
5. If information is missing, say what is missing.

## DAO governance

Route POWER, proposals, endorsement, voting, Timelock, Treasury, BP allocations, rewards, and Keeper questions to `docs/11_DAO_Governance/`. Treat the mainnet snapshot as dated evidence, not live configuration; check its source/discrepancy page before reusing historical DApp help.
