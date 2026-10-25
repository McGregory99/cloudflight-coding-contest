"""Replay tournament-matches.json with the engine and classify how each game ended."""
import json, re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "env"))
from colony_one.env import ColonyOneEnv

LINE = re.compile(r"^\s*\d+\.\s+(CYAN|MAGENTA)\s+(\w\w)\s+([A-H][1-8])\s+->\s+([A-H][1-8])\s+(MOVE|SHOOT)\s*(x\w\w)?")
rows = []
for m in sorted(json.load(open(HERE / "data" / (sys.argv[1] if len(sys.argv) > 1 else "tournament-matches.json"))), key=lambda m: m["played_at"]):
    lines = [LINE.match(l) for l in m.get("protocol", "").splitlines()]
    lines = [x for x in lines if x]
    env = ColonyOneEnv(); ok = True; why = ""; last = ""
    for x in lines:
        team, piece, a, b = x.group(1), x.group(2), x.group(3), x.group(4)
        want = f"{a} -> {b}"
        cand = [ac for ac in env.legal_actions() if env.format_action(ac) == want]
        if env.terminated or env.current_team != team or len(cand) != 1:
            ok = False; why = "desync at %s %s" % (team, want); break
        last = "%s %s %s%s" % (team[:3], piece, want, (" " + x.group(6)) if x.group(6) else "")
        env.step(cand[0])
    r = env.render()
    end = "n/a" if not ok else ("kernel captured" if ("cK" not in r or "mK" not in r) else "firewall/endgame")
    rows.append((m["match_id"], m["you"][:3], m["score"], ok, len(lines), env.round_number, env.winner, end, last, why))
for r in rows: print(*r, sep=" | ")
ok = [r for r in rows if r[3]]
print("replayed %d/%d" % (len(ok), len(rows)))
from collections import Counter
c = Counter((r[1], r[2], r[7]) for r in ok)
for k, v in sorted(c.items()): print(k, v)
