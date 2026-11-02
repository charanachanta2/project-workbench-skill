#!/usr/bin/env python3
"""Heuristic token estimator for sandboxes with no real usage data. Estimates only."""
import json, os, sys

LEDGER = os.environ.get("TOKEN_LEDGER", "/tmp/token_ledger.json")

def estimate(text: str) -> int:
    """~4 chars/token for ASCII, ~1.5 chars/token for non-ASCII; floor at 1.3 tokens/word."""
    if not text:
        return 0
    ascii_chars = sum(1 for c in text if ord(c) < 128)
    other = len(text) - ascii_chars
    by_chars = ascii_chars / 4 + other / 1.5
    by_words = len(text.split()) * 1.3
    return int(round(max(by_chars, by_words)))

def load():
    try:
        with open(LEDGER) as f:
            return json.load(f)
    except (OSError, ValueError):
        return []

def table(rows, header):
    w = [max(len(str(r[i])) for r in [header] + rows) for i in range(len(header))]
    line = lambda r: "| " + " | ".join(str(c).ljust(w[i]) for i, c in enumerate(r)) + " |"
    print(line(header)); print("|" + "|".join("-" * (x + 2) for x in w) + "|")
    for r in rows: print(line(r))

def read_text(args):
    if args and args[0] != "-":
        return "\n".join(open(a, encoding="utf-8", errors="replace").read() for a in args)
    return sys.stdin.read()

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("count", "add", "report", "reset"):
        sys.exit("usage: estimate.py count <files...> | add <user|assistant> [file|-] | report | reset")
    cmd = sys.argv[1]
    if cmd == "count":
        if len(sys.argv) < 3: sys.exit("count needs at least one file")
        rows, total = [], 0
        for p in sys.argv[2:]:
            t = open(p, encoding="utf-8", errors="replace").read()
            n = estimate(t); total += n
            rows.append([os.path.basename(p), len(t), len(t.split()), n])
        table(rows, ["file", "chars", "words", "est. tokens"])
        print(f"\nTotal: ~{total:,} tokens (ESTIMATE, roughly +/-20-30%; not billing data)")
    elif cmd == "add":
        if len(sys.argv) < 3 or sys.argv[2] not in ("user", "assistant"):
            sys.exit("add needs role: user|assistant")
        t = read_text(sys.argv[3:])
        led = load()
        led.append({"role": sys.argv[2], "chars": len(t), "tokens": estimate(t)})
        json.dump(led, open(LEDGER, "w"))
        print(f"logged {sys.argv[2]}: ~{led[-1]['tokens']:,} tokens ({len(led)} entries)")
    elif cmd == "reset":
        if os.path.exists(LEDGER): os.remove(LEDGER)
        print("ledger cleared")
    else:
        led = load()
        if not led:
            print("ledger is empty: nothing logged yet (use `add`, or `count` for a file)"); return
        inp = sum(e["tokens"] for e in led if e["role"] == "user")
        out = sum(e["tokens"] for e in led if e["role"] == "assistant")
        # Each assistant reply is generated from everything before it, which is re-read as input.
        reread, ctx, turns = 0, 0, 0
        for e in led:
            if e["role"] == "assistant":
                reread += ctx; turns += 1
            ctx += e["tokens"]
        table([[turns, f"~{inp:,}", f"~{out:,}", f"~{reread:,}", f"~{inp+out+reread:,}", f"~{ctx:,}"]],
              ["turns", "new input", "output", "context re-read", "total processed", "current context"])
        drivers = {"new input": inp, "output": out, "context re-read": reread}
        top = max(drivers, key=drivers.get)
        print(f"\nBiggest driver: {top}. ESTIMATE only (roughly +/-20-30%); excludes system prompt and tool definitions.")

main()
