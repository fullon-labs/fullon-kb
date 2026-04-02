# OpenClaw Agent Setup

This document describes how to wire the FullOn KB Assistant into an OpenClaw-compatible agent runtime.

## Goal
Create a dedicated agent that answers FullOn questions using the Markdown knowledge base in `/home/node/.openclaw/workspace-fullon-kb/`.

## Source files
Use these configuration files from `10_Agent_Config/`:
- `AGENTS.md`
- `AGENT-ROUTING.md`
- `agent-system-prompt.md`
- `agent-config-draft.md`
- `fullon-kb-agent.md`

## Minimal runtime contract
The agent runtime should:
1. Load the system prompt.
2. Load the routing rules.
3. Read the repository root at `/home/node/.openclaw/workspace-fullon-kb/`.
4. Search Markdown pages before answering.
5. Return grounded answers only.

## Recommended setup

### 1. Agent identity
- Name: `FullOn KB Assistant`
- Purpose: FullOn knowledge base Q&A

### 2. Knowledge root
- `/home/node/.openclaw/workspace-fullon-kb/`

### 3. Retrieval order
- `01_Core_Chain/`
- `02_Ecosystems/`
- `03_Operators/`
- `07_DApps/`
- `06_User_Guides/`
- `04_FAQ/`
- `05_Glossary/`
- `08_Policies/`
- `09_Release_Notes/`
- `99_Archive/`

### 4. Answer policy
- Answer directly.
- Use only knowledge base evidence.
- Say when information is missing.
- Do not invent details.

## Operational notes
- The agent should be treated as a retrieval-first assistant.
- Draft or internal pages may be used only as provisional context.
- Official or canonical pages take precedence over drafts.

## Integration checklist
- [ ] Load system prompt
- [ ] Load routing rules
- [ ] Attach `/home/node/.openclaw/workspace-fullon-kb/` as knowledge source
- [ ] Verify search over Markdown files
- [ ] Verify answer grounding
- [ ] Verify conflict handling
- [ ] Verify missing-info behavior

## Example behavior
User: `What is FullBridge?`

Expected behavior:
- Search `07_DApps/fullbridge.md`
- Search related FAQ or operator pages if needed
- Respond with a short, grounded answer

## Notes
This file is the practical handoff for implementing the agent in an OpenClaw-compatible runtime.
