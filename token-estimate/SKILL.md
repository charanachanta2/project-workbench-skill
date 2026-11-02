---
name: token-estimate
description: Estimate token usage when real counts are unavailable, such as in claude.ai chat or any sandbox with no session transcript. Use whenever the user asks how many tokens a conversation, pasted text, or uploaded file uses, wants a rough token or cost meter, or asks where tokens are going and /token-usage reports "no transcript found". Always labels figures as estimates.
---

# Token Estimate

Sandboxed chats give Claude no access to real usage counts, so this skill produces a labelled **estimate** from text. It never claims billing accuracy.

## Be upfront
Say once, before the numbers: these are heuristic estimates (typically within about 20-30%), not exact counts and not billing data. For exact figures the user needs Claude Code (`/token-usage`), the API's `usage` field, or their account settings.

## Mode 1: count given text (default)
Use when the user pastes text, uploads a file, or exports a conversation.
1. Save pasted text to a file, or use the uploaded path.
2. Run `python3 scripts/estimate.py count <file> [<file> ...]` (path relative to this skill folder).
3. Report the table it prints.

## Mode 2: running ledger (opt-in)
Use only if the user wants a per-turn meter for this chat. Logging each turn means writing that turn's text again, which costs extra output, so offer it and say so.
1. At each turn: `python3 scripts/estimate.py add user <<'T' ... T` then `python3 scripts/estimate.py add assistant <<'T' ... T`.
2. On request: `python3 scripts/estimate.py report`.
3. Only the character and token estimates are stored, not the text. The ledger lives in `/tmp/token_ledger.json` and is lost when the sandbox resets.
4. The report shows input, output, and **context re-read**: every turn re-sends the earlier conversation, which is usually the biggest driver.

## Reply format
Compact table (turns, input, output, context re-read, total), the "estimate" label, one line naming the biggest driver, and one concrete saving (shorter replies, start a fresh chat for new topics, avoid re-uploading large files).
