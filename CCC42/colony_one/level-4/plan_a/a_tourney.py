"""Model-vs-model under referee MCTS. usage: a_tourney.py A.onnx B.onnx [games] [offset] [procs] [sims]
Game g uses seeds 2(g+off), 2(g+off)+1; A is CYAN on even g, MAGENTA on odd g."""
import sys
from multiprocessing import Pool
from pathlib import Path

L4 = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(L4 / "env")); sys.path.insert(0, str(L4 / "env" / "play"))


def one(args):
    a, b, g, off, sims = args
    from colony_one.env import ColonyOneEnv
    from model_vs_model import SearchAgent
    aa, bb = SearchAgent(Path(a), sims, seed=2 * (g + off)), SearchAgent(Path(b), sims, seed=2 * (g + off) + 1)
    swap = g % 2 == 1
    cyan, mag = (bb, aa) if swap else (aa, bb)
    env = ColonyOneEnv()
    while not env.terminated:
        ag = cyan if env.current_team == "CYAN" else mag
        env.step(ag.select(env.board, env.current_team, env.actions_left, env.round_number))
    return (env.winner == "MAGENTA") if swap else (env.winner == "CYAN"), swap


def match(a, b, games=100, off=0, procs=3, sims=100):
    """-> (wins, wins_as_cyan, wins_as_magenta, games)"""
    with Pool(procs) as p:
        res = p.map(one, [(str(a), str(b), g, off, sims) for g in range(games)], chunksize=1)
    wc = sum(w for w, s in res if not s); wm = sum(w for w, s in res if s)
    return wc + wm, wc, wm, games


def fmt(name, r):
    w, wc, wm, n = r
    return "%s: %d/%d (%.1f%%) as CYAN %d/%d, as MAGENTA %d/%d" % (name, w, n, 100 * w / n, wc, (n + 1) // 2, wm, n // 2)


if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]
    games = int(sys.argv[3]) if len(sys.argv) > 3 else 100
    off = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    procs = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    sims = int(sys.argv[6]) if len(sys.argv) > 6 else 100
    print(fmt("%s vs %s off=%d" % (Path(a).name, Path(b).name, off), match(a, b, games, off, procs, sims)), flush=True)
