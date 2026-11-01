---
name: token-usage
description: Use when the user asks how many tokens this session has used, wants a token or cost meter, or asks where tokens are going. Reports real counts from the session transcript.
---

# Token Usage

Report real token counts for the current session. Do not estimate or guess numbers.

## Steps
1. Run `python3 scripts/usage.py` (path relative to this skill's folder). It reads the newest session transcript under `~/.claude/projects/` and prints totals.
2. If it prints "no transcript found", say so plainly and stop. Do not invent figures.
3. Reply with the script's output as a compact table: turns, input, output, cache read, cache write, and the last call's context size.
4. Add one line on the biggest cost driver (usually cache read or output) and one concrete way to reduce it.

## Notes
- Counts update on each run, so this is an on-demand meter, not a live display. Tell the user to ask again, or use `/token-usage`, to refresh.
- Never claim access to the user's account billing. Figures come only from this session's transcript.
