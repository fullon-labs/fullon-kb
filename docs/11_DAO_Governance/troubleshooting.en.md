---
title: DAO troubleshooting and FAQ
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# DAO troubleshooting and FAQ

| Question | Check / action |
| --- | --- |
| Is POWER tradable? | No. It is not purchased by transferring POWER and is not consumed by voting. |
| I have FLON but cannot propose | Liquid balance is not governance power. Check powers, risk threshold, and network. |
| Current POWER but cannot vote | Verify the vote window and activation snapshot power; one vote per account. |
| Enough endorsers but activation fails | The period must end; network total, individual/aggregate power, and risk checks must pass. |
| Must endorsers vote again? | Yes. Endorsement is not a formal For vote. |
| Can I change my vote? | Reviewed source rejects a second vote and has no vote-change entry. Confirm before signing. |
| Why did 100% approval fail? | Quorum and absolute support must also pass; abstention is excluded from decisive approval. |
| Approved but not executed | Signals have no automatic execution; actions still need queue, Timelock, window, and current policy. |
| Action unavailable | It may lack enabled policies/allowlist on this network. Testnet lists are not mainnet lists. |
| Allocation-total error | Reviewed source requires equality with target locked principal, positive unique/sorted allocations, at most 30 BPs. |
| Rankings unchanged after voting | Check pending state, activation epoch, schedule, and eligibility before resubmitting. |
| Grant reserved but no receipt | Reserve earmarks funds; only an authorized pay transfers to the recorded recipient. |
| closegrant fails | Reviewed source accepts only still-open, strictly expired grants, not arbitrary completed grants. |
| standbyproof missing | The observed mainnet ABI lacks it; the procedure requires a supporting version. |
| Wallet mismatch / signer does not open | Check chain ID, account, and session; reconnect/reopen in the proper wallet environment, reconciling before resubmission. |

## Support details

Provide network/chain ID, public account, proposal/grant/epoch ID, transaction ID, time/timezone, redacted error, and expected result. Include configuration/snapshot provenance. Never share private keys, recovery phrases, verification codes, passwords, or credential-bearing links.

[Proposal lifecycle](proposals.md) · [Queries](developer-reference.md) · [Rules and snapshot](rules-and-parameters.md)

## Sources and scope

[Sources, snapshots, and discrepancies](sources.md). Implementation descriptions use the listed revisions; live configuration must be read from the target network.
