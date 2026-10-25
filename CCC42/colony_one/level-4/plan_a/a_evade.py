"""For real lost games (Kernel captured): from the start of the loser's last turn, let model play its 2 actions
(referee MCTS 100 sims, 4 seeds) and test with the exact oracle whether the opponent can still kill. usage: a_evade.py m1.onnx m2.onnx ..."""
import json, re, sys
from multiprocessing import Pool
from pathlib import Path
H = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(H / "env")); sys.path.insert(0, str(H / "env/play")); sys.path.insert(0, str(H / "plan_a"))
LINE = re.compile(r"^\s*\d+\.\s+(CYAN|MAGENTA)\s+(\w\w)\s+([A-H][1-8])\s+->\s+([A-H][1-8])\s+(MOVE|SHOOT)\s*(x\w\w)?")

def positions():
    out = []
    for m in json.load(open(H / "data" / "tournament-matches.json")):
        lines = [x for x in (LINE.match(l) for l in m.get("protocol", "").splitlines()) if x]
        if not lines or (m["you"] == "CYAN") == (m["score"] == 1) or lines[-1].group(6) != "xKE": continue
        loser = "CYAN" if lines[-1].group(1) == "MAGENTA" else "MAGENTA"
        # first action index of loser's last turn
        k = len(lines) - 1
        while k > 0 and lines[k - 1].group(1) != lines[-1].group(1): k -= 1   # start of killer's turn
        st = k
        while st > 0 and lines[st - 1].group(1) == loser: st -= 1
        import os
        for _ in range(int(os.environ.get('BACK', 0))):
            st = max(0, st - 2)
            while st > 0 and lines[st - 1].group(1) == loser: st -= 1
        out.append((m["match_id"], [(x.group(3), x.group(4)) for x in lines[:st]], loser))
    return out

def run(a):
    path, mid, acts, loser, seed = a
    from colony_one.env import ColonyOneEnv
    from model_vs_model import SearchAgent
    from a_test import can_kill
    env = ColonyOneEnv()
    for f, t in acts:
        c = [x for x in env.legal_actions() if env.format_action(x) == "%s -> %s" % (f, t)]
        env.step(c[0])
    ag = SearchAgent(Path(path), 100, seed=seed)
    while env.current_team == loser and not env.terminated:
        env.step(ag.select(env.board, env.current_team, env.actions_left, env.round_number))
    return (not env.terminated) and not can_kill(env.board, env.current_team, 2)

if __name__ == "__main__":
    P = positions(); print(len(P), "positions")
    with Pool(6) as p:
        for path in sys.argv[1:]:
            r = p.map(run, [(path, m, a, l, s) for m, a, l in P for s in range(4)])
            print(Path(path).name, "safe after own turn: %d/%d" % (sum(r), len(r)), flush=True)
