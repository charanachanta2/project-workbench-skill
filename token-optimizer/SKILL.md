---
name: token-optimizer
description: Use when the user wants a lean, low-token workflow: long sessions, large files or repos, repeated tasks, or any request to be concise and cost-efficient without losing correctness.
---

# Token Optimizer

Goal: spend the fewest tokens that still produce a correct, complete result. Correctness always beats brevity.

## 1. Input: read less
- Locate before reading: use Glob and Grep to find the exact file and lines, then Read only that range (offset and limit).
- Never re-read a file you already have in context or just edited. Never re-run a search whose answer you hold.
- For large logs, data, or PDFs, extract what is needed with a script (head, filters, summary stats) instead of loading everything.
- Wide sweeps across many files go to a subagent, so only its conclusion enters the main context.

## 2. Process: act in fewer steps
- Batch independent tool calls in one turn.
- Plan once, briefly, then execute. Do not narrate each step or summarize each tool result.
- If a request is clear, start immediately. Ask at most one question, and only when a wrong guess would be costly.
- Run code to get real output rather than reasoning at length about what it would print.
- Stop when the task is done. No extra variants, alternatives, or unrequested features.

## 3. Output: say less, deliver as files
- Lead with the answer or result. No preamble, no restating the question, no closing recap.
- Default to short prose. Use lists or tables only when they cut words or aid scanning.
- Deliver code, documents, and long content as files (SendUserFile), not pasted blocks. The reply is 1 to 3 sentences: what changed, what needs attention, one next step.
- For edits, change only the affected lines (Edit). Do not rewrite whole files.
- Do not repeat code or text the user already has.

## 4. Context hygiene in long sessions
- Keep a short running state (decisions made, files touched, open items) and refer to it instead of re-deriving.
- Do not paste large tool outputs back into replies; quote only the relevant line.
- When the conversation gets heavy, offer to summarize progress into a notes file so a fresh session can continue from it.

## 5. Writing skills and prompts cheaply
- Keep SKILL.md under about 100 lines. Put the trigger in the description so the body loads only when needed.
- Move rarely used detail into separate reference files, linked from SKILL.md and read on demand.
- Use imperative, one-line rules. Cut examples that repeat a rule.

## Guardrails
- Never shorten by skipping verification, dropping requested content, or truncating code the user asked for.
- If the user asks for detail, depth, or a full explanation, give it. This skill sets defaults, not limits.
- Safety and honesty rules still apply: report real outputs, flag uncertainty, never fabricate.
