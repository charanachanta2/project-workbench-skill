---
name: project-workbench
description: Use when the user attaches or pastes files, code, or notes and wants them worked on, fixed, explained, or returned as finished files.
---

# Project Workbench

Use this when the user wants hands-on work on their own files, code, or study material, and Claude can only see what has been attached or pasted in the conversation.

## Step 1: Check what is actually available
- Look for attached files first (Glob with `*`, then Read by file name). Never assume a file exists because the user mentioned it.
- If something needed is missing, ask for it in one short message: attach the file, or paste the relevant part. Say exactly which file or section is needed.
- Do not claim access to the user's laptop, folders, or apps. Work only on what is in the conversation.

## Step 2: Work on a copy
- Treat uploaded files as originals. Make changes in a copy and return the result.
- For code, change only what the request needs. Keep the existing style, structure, and naming.
- For notes or study material, keep the user's wording where it is already clear.

## Step 3: Do the task
- Fix, build, refactor, explain, or summarize as asked. Run code when it can be run, and report real output rather than guessing.
- If the request is ambiguous and a wrong guess would be costly, ask one question first. Otherwise state the assumption briefly and continue.

## Step 4: Deliver
- Send finished work as files (SendUserFile), not as long pasted blocks.
- Reply with 1 to 3 sentences: what changed, anything that needs the user's attention, and one sensible next step.
- Name every file clearly (for example `app_fixed.py`, `module3_notes.md`) so the user can tell versions apart.

## Safety rules
- Never delete or overwrite the user's originals.
- Do not run destructive commands or install unknown packages without saying so.
- Ask before touching anything that looks like credentials, API keys, or personal data. Remove them from output instead of repeating them.

## Explanations
When the user is studying, teach in order from the basics to the advanced version, use a short worked example for each concept, and end with two or three self-check questions.
