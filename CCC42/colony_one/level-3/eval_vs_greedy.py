"""Play our ONNX (CYAN, referee MCTS, 60 sims) against GreedyAgent (MAGENTA); print the win rate."""
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "env"))
sys.path.insert(0, str(HERE / "env" / "play"))

from colony_one.baselines import GreedyAgent  # noqa: E402
from model_vs_model import SearchAgent, play_game  # noqa: E402

model = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "model.onnx"
games = int(sys.argv[2]) if len(sys.argv) > 2 else 10
wins = 0
for g in range(games):
    t = time.time()
    winner, actions = play_game(SearchAgent(model, 60, seed=g), GreedyAgent(seed=1000 + g))
    wins += winner == "CYAN"
    print("game %d: winner=%s actions=%d %.1fs" % (g, winner, actions, time.time() - t), flush=True)
print("cyan wins %d/%d" % (wins, games))
