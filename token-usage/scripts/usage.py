#!/usr/bin/env python3
import glob, json, os, sys

files = sorted(glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")), key=os.path.getmtime, reverse=True)
if not files:
    print("no transcript found")
    sys.exit(0)

seen, tot, last = set(), dict(input=0, output=0, cache_read=0, cache_write=0), None
for line in open(files[0], errors="ignore"):
    try:
        d = json.loads(line)
    except Exception:
        continue
    m = d.get("message")
    if not isinstance(m, dict) or d.get("type") != "assistant":
        continue
    u = m.get("usage")
    if not u:
        continue
    key = m.get("id") or d.get("uuid")
    if key in seen:
        continue
    seen.add(key)
    tot["input"] += u.get("input_tokens", 0)
    tot["output"] += u.get("output_tokens", 0)
    tot["cache_read"] += u.get("cache_read_input_tokens", 0)
    tot["cache_write"] += u.get("cache_creation_input_tokens", 0)
    last = u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)

print(f"turns (model calls): {len(seen)}")
for k, v in tot.items():
    print(f"{k}: {v:,}")
print(f"last call context: {last:,}" if last is not None else "last call context: n/a")
