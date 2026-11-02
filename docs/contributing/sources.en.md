---
title: Sources and verification
translation_of: contributing/sources.md
---

# Sources and verification

## Source hierarchy

1. Current target-network state: chain ID, ABI, code hash, permissions, gas, and schedules.
2. Pinned official source: implementation and command parameters.
3. Official product documentation/FAQ: retain provenance and distinguish goals or historical values from current state.
4. Internal notes/drafts: verification leads only.

Reviewed baselines: Core `2188e4f94a1e9fe564a31c33e497b464556f3650`; system contracts `d34fc8f588e4bcc581e1377e729a248e0098f090`; RWID `d0fcb698711a0ea807515e76cf44e357d38787f3`; CDT `5c4b07b077b8bc9378c7e7adcf52b474fbf63c74`. Local review does not verify remote branches, release packages, or deployed code.

## Maintenance rules

State audience, task, prerequisites, steps, completion checks, troubleshooting, and sources. Record network, source, and date for live parameters. Check commands against source or actual CLI. Never include real private keys, authentication tokens, or personal authentication information.

RPC documentation was rechecked against v0.9.2 on 2026-11-02. Historical live observations retain their own dates and are not evidence of a new deployment. The [audit manifest](v0.9.2-audit.json) records the pinned source, file hashes, and route catalog. Explain conflicts instead of hiding provenance or changing observation dates.

## Publication boundary

Build only `docs/`. Root agent configuration and internal `docs_CisuMusiC_App/` materials are outside the site. Unfilled historical templates are outside primary navigation. Public pages must be suitable for external readers.

## Whitepaper sources

The v2.5.0 clarification draft (2026-11-02, pending upstream merge) is pinned to `d695da53f4e453dd0e372e9dc5a605a0c56d455e`. This integration uses the main Markdown files and does not assume repository PDFs are synchronized. New topics have Chinese and English text. The [source and conflict record](../01_Core_Chain/whitepaper.md) separates protocol design, source review, and network deployment; file hashes are in the [manifest](whitepaper-source-manifest.json).

The upstream license for adapted content is retained in the [whitepaper MIT license](whitepaper-license.txt).
