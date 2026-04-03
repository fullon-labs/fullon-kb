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

### 3. Operator / developer workflows
Use:
- `docs/03_Operators/`
- `docs/06_User_Guides/`

Examples:
- create wallet
- query account
- transfer token
- deploy contract
- read contract state
- query chain info
- CLI commands

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
