# project-workbench-skill

A skill for Claude that makes it work carefully on files, code, and study notes you attach or paste into a chat.

## What it does

- Checks which files are actually attached before assuming anything
- Works on a copy and never overwrites your originals
- Runs code when possible and reports real output
- Returns finished files with clear names and a short summary
- Teaches from basics to advanced with examples and self-check questions when you are studying

## Skills in this repo

| Skill | Location | Purpose |
|---|---|---|
| project-workbench | `SKILL.md` | Careful hands-on work on attached files, code, and study notes |
| token-optimizer | `token-optimizer/SKILL.md` | Lean, low-token workflow for long sessions, large files, and repeated tasks, without losing correctness |

### token-optimizer highlights

- Reads only the lines it needs and never re-reads files
- Batches tool calls and skips narration
- Leads with the answer and delivers long content as files
- Keeps a short running state in long sessions

## Install

1. Download the skill's `SKILL.md` (`SKILL.md` for project-workbench, `token-optimizer/SKILL.md` for token-optimizer).
2. Put it in a folder named after the skill (`project-workbench` or `token-optimizer`).
3. Zip that folder and upload it in Claude's Settings under Skills (the exact menu name can differ between web and mobile).

## Contributing

Issues and pull requests are welcome. Keep the skill focused on one job, and keep the `description` line specific about when it should trigger.

## License

No license has been chosen yet. Add one (for example MIT) before others reuse or redistribute this.
