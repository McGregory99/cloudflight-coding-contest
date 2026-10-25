import json, re, sys
from pathlib import Path
import numpy as np
L4 = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(L4 / "env")); sys.path.insert(0, str(L4 / "plan_b"))
from colony_one.env import ColonyOneEnv
from colony_one.encoding import encode_board
from b_gen import can_kill, opp
LINE = re.compile(r"^\s*\d+\.\s+(CYAN|MAGENTA)\s+(\w\w)\s+([A-H][1-8])\s+->\s+([A-H][1-8])\s+(MOVE|SHOOT)\s*(x\w\w)?")
X, W, T, Z, K, G = [], [], [], [], [], []
for gi, m in enumerate(json.load(open(L4 / "data" / "tournament-matches.json"))):
    lines = [x for x in (LINE.match(l) for l in m.get("protocol", "").splitlines()) if x]
    env = ColonyOneEnv(); pos = []; ok = True
    for x in lines:
        want = "%s -> %s" % (x.group(3), x.group(4))
        cand = [a for a in env.legal_actions() if env.format_action(a) == want]
        if env.terminated or env.current_team != x.group(1) or len(cand) != 1: ok = False; break
        t, l, r = env.current_team, env.actions_left, env.round_number
        pos.append((encode_board(env.board, t, l, r), float(can_kill(env.board, t, l)), float(can_kill(env.board, opp(t), 2)), t, bool(x.group(6) and x.group(6) == "xKE")))
        env.step(cand[0])
    if not ok or not env.terminated: continue
    for o, w, t_, team, kill in pos:
        X.append(o); W.append(w); T.append(t_); Z.append(1.0 if team == env.winner else -1.0); K.append(kill); G.append(gi)
np.savez("b_real.npz", X=np.array(X), W=np.array(W, np.float32), T=np.array(T, np.float32), Z=np.array(Z, np.float32), K=np.array(K), G=np.array(G))
print(len(X), "pos; win_now", np.mean(W), "thr", np.mean(T), "xKE actions", sum(K), "games", len(set(G)))
