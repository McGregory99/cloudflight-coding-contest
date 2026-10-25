"""Parallel model-vs-model matches under referee MCTS on the Level 4 scene.

    tourney.py A.onnx B.onnx [games] [sims]    -> prints A's win rate (sides alternate) and how games end
"""
import sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "env")); sys.path.insert(0, str(HERE / "env" / "play"))

SIMS = 100


def one(args):
    a, b, g, sims = args
    from colony_one.env import ColonyOneEnv
    from model_vs_model import SearchAgent
    aa, bb = SearchAgent(Path(a), sims, seed=2 * g), SearchAgent(Path(b), sims, seed=2 * g + 1)
    swap = g % 2 == 1
    cyan, mag = (bb, aa) if swap else (aa, bb)
    env = ColonyOneEnv()
    while not env.terminated:
        ag = cyan if env.current_team == "CYAN" else mag
        env.step(ag.select(env.board, env.current_team, env.actions_left, env.round_number))
    a_won = (env.winner == "MAGENTA") if swap else (env.winner == "CYAN")
    return a_won, env.winner, env.round_number


def match(a, b, games=60, sims=SIMS):
    with Pool() as p:
        res = p.map(one, [(str(a), str(b), g, sims) for g in range(games)])
    return sum(r[0] for r in res), res


if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]
    games = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    sims = int(sys.argv[4]) if len(sys.argv) > 4 else SIMS
    w, res = match(a, b, games, sims)
    print("%s vs %s: %d/%d (%.0f%%)" % (Path(a).name, Path(b).name, w, games, 100 * w / games))
    print("end rounds (winner=A):", sorted(Counter(r[2] for r in res if r[0]).items()))
    print("end rounds (winner=B):", sorted(Counter(r[2] for r in res if not r[0]).items()))
