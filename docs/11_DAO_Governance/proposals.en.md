---
title: Create, endorse, vote, and execute proposals
type: governance_guide
status: active
updated: '2026-11-02'
source: pinned source review; dated RPC evidence where stated
---

# Create, endorse, vote, and execute proposals

## Prepare a proposal

Discuss the goal, rationale, expected impact, and verifiable outcome first. The application may prefill a proposal from community discussion, but a post or forum reaction is not an on-chain endorsement/vote. Keep the content URI and SHA-256 and verify they match.

- **Signal proposal**: no actions; records community opinion. Passing does not call business contracts and cannot enter the execution queue. Source treats empty-action proposals as L1, so enabled risk requirements still apply.
- **Executable proposal**: freezes contract, action name, and parameter bytes. Each action needs enabled `actpolicies` and `allowlist` entries and must meet count/byte limits. Multiple actions use the highest risk level.

1. Check the proposer's current POWER, risk threshold, and network. A signal proposal is not a zero-threshold forum message.
2. Enter title, summary, content URI/hash, and discussion link. Review decoded actions, parameters, target authority, and recipients for executable proposals.
3. Sign `propose`, save transaction/proposal IDs, and confirm irreversibility before requesting endorsements.

## Endorsement and formal voting

Endorsement supports advancing to a vote, not executing the proposal. Each endorser must meet the individual threshold and may endorse once. Count and aggregate endorsement-power requirements must also pass.

`activate` requires the endorsement period to have ended; sufficient endorsements do not allow early activation. It checks network power/risk rules and freezes power sequence, total, voting window, and passing conditions. Wait until `vote_start` after activation.

`castvote` choices are Against `0`, For `1`, and Abstain `2`. Each account can vote once per proposal; the reviewed version has no vote-change action. Endorsers must separately vote and may vote Against or Abstain. Voting requires `now < vote_end`.

## Advance the lifecycle

| Phase | Operation | Verify afterwards |
| --- | --- | --- |
| Endorsement | endorse; proposer may cancel | Endorsement record/count or cancelled |
| Endorsement ended | activate | Snapshot sequence/total and vote_start / vote_end |
| Voting ended | finalize | succeeded only if all three tests pass; otherwise defeated |
| Executable proposal passed | queue | execute_after / execute_before |
| Timelock elapsed | execute | Execution, target state/recipient outcome, and irreversibility |
| Execution window exceeded | expire | expired; frozen actions not executed |

`activate`, `finalize`, `queue`, `execute`, and `expire` do not require proposer identity but remain transactions subject to phase, time, policy, and gas. Only the proposer can cancel during endorsement. The discussion link may also be updated only by the proposer during that phase; this does not allow editing the frozen content hash or actions.

## Timelock and execution

Timelock starts when `queue` succeeds. Voting is closed and parameters cannot be replaced. Execution is allowed at `execute_after <= now <= execute_before`; expiry requires strictly later than `execute_before`. Interface countdowns are advisory; chain time/checks determine success.

Queue and execute revalidate current allowlists, risk policy, and size limits. Passing does not guarantee later executability: disabled policy, changed target permissions/code, or unmet business conditions may prevent execution. Callers cannot arbitrarily replace frozen actions/recipients. Execution authority comes from the matching allowlist rule; see [developer reference](developer-reference.md).

See [rules and parameters](rules-and-parameters.md) for passing formulas, abstention, and snapshot limitations.

## Sources and scope

[Sources, snapshots, and discrepancies](sources.md). Implementation descriptions use the listed revisions; live configuration must be read from the target network.
