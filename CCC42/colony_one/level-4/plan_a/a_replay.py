import json, re, sys
from pathlib import Path
H = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(H / "env")); sys.path.insert(0, str(H / "plan_a"))
import onnxruntime as ort
from colony_one.env import ColonyOneEnv
import a_build
a_build.build(H / "plan_a/a_test.onnx", debug=True)
s = ort.InferenceSession(str(H / "plan_a/a_test.onnx"), providers=["CPUExecutionProvider"])
LINE = re.compile(r"^\s*\d+\.\s+(CYAN|MAGENTA)\s+(\w\w)\s+([A-H][1-8])\s+->\s+([A-H][1-8])\s+(MOVE|SHOOT)\s*(x\w\w)?")
tot = dict(n=0, win_before_kill=0, thr_goyo=0, kills=0)
for m in json.load(open(H / "data" / "tournament-matches.json")):
    lines = [x for x in (LINE.match(l) for l in m.get("protocol", "").splitlines()) if x]
    if not lines: continue
    env = ColonyOneEnv(); rec = []
    for x in lines:
        want = "%s -> %s" % (x.group(3), x.group(4))
        cand = [a for a in env.legal_actions() if env.format_action(a) == want]
        o = s.run(["dbg_win", "dbg_thr"], {"observation": env.observation()[None]})
        rec.append((env.current_team, float(o[0][0]), float(o[1][0]), x.group(6), want, env.actions_left))
        env.step(cand[0])
    goyo_won = (m["you"] == "CYAN") == (m["score"] == 1)
    if goyo_won or not rec[-1][3] or rec[-1][3] != "xKE": continue
    tot["n"] += 1
    last = rec[-1]; tot["win_before_kill"] += last[1] > 0.5
    # Goyo's last positions: thr flag for Goyo (side != killer) at his turn start / mid-turn
    g = [r for r in rec if r[0] != last[0]][-2:]
    flag = any(r[2] > 0.5 for r in g); tot["thr_goyo"] += flag
    print(m["match_id"], m["you"], "kill", last[4], "win_now(killer pre-kill)=%.0f" % last[1], "| Goyo last 2 actions thr:", [(r[4], r[5], r[2]) for r in g])
print(tot)
