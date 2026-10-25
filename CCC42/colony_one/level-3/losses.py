import sys
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "env")); sys.path.insert(0, str(HERE / "env" / "play"))
from colony_one import constants
from colony_one.baselines import GreedyAgent
from colony_one.env import ColonyOneEnv
from model_vs_model import SearchAgent

model = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "model.onnx"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 60
c = Counter()
for g in range(N):
    env = ColonyOneEnv(); cy = SearchAgent(model, 60, seed=g); ma = GreedyAgent(seed=1000 + g)
    log = []
    while not env.terminated:
        ag = cy if env.current_team == "CYAN" else ma
        a = ag.select(env.board, env.current_team, env.actions_left, env.round_number)
        log.append((env.current_team, env.round_number, env.format_action(a)))
        env.step(a)
    k = [(r, t) for (t, r, _) in log][-1]
    c[(env.winner, "round<=8" if k[0] <= 8 else "late")] += 1
    if env.winner != "CYAN" and g < 4:
        print("LOSS game", g, "last 6:", log[-6:])
print(c)
