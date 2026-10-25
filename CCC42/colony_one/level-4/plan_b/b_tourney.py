"""b_tourney.py A.onnx B.onnx [games] [offset] [procs] [sims] -> A's wins, per colour. Game g uses seeds 2(g+off), 2(g+off)+1."""
import sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path
L4 = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(L4 / "env")); sys.path.insert(0, str(L4 / "env" / "play"))


def one(args):
    a, b, g, off, sims = args
    from colony_one.env import ColonyOneEnv
    from model_vs_model import SearchAgent
    gg = g + off
    aa, bb = SearchAgent(Path(a), sims, seed=2 * gg), SearchAgent(Path(b), sims, seed=2 * gg + 1)
    swap = g % 2 == 1
    cyan, mag = (bb, aa) if swap else (aa, bb)
    env = ColonyOneEnv()
    while not env.terminated:
        env.step((cyan if env.current_team == "CYAN" else mag).select(env.board, env.current_team, env.actions_left, env.round_number))
    return (env.winner == "MAGENTA") if swap else (env.winner == "CYAN"), swap, env.round_number


def match(a, b, games=60, off=0, procs=3, sims=100):
    with Pool(procs) as p:
        res = p.map(one, [(str(a), str(b), g, off, sims) for g in range(games)], chunksize=1)
    return res


def summary(a, b, res, off):
    w = sum(r[0] for r in res); cy = [r for r in res if not r[1]]; mg = [r for r in res if r[1]]
    return "%s vs %s (off %d): %d/%d (%.1f%%) | A as CYAN %d/%d | A as MAGENTA %d/%d" % (
        Path(a).name, Path(b).name, off, w, len(res), 100 * w / len(res),
        sum(r[0] for r in cy), len(cy), sum(r[0] for r in mg), len(mg))


if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]
    games = int(sys.argv[3]) if len(sys.argv) > 3 else 60
    off = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    procs = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    sims = int(sys.argv[6]) if len(sys.argv) > 6 else 100
    print(summary(a, b, match(a, b, games, off, procs, sims), off), flush=True)
