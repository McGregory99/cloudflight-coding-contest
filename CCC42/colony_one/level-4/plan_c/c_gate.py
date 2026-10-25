"""Gate match, copy of tourney.py with seed offset, procs and per-colour wins.
usage: c_gate.py A.onnx B.onnx GAMES OFFSET [PROCS] [SIMS]  -> game g (global index g+offset) uses seeds 2(g+off), 2(g+off)+1; A is cyan on even g+off"""
import sys
from collections import Counter
from multiprocessing import Pool
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "env")); sys.path.insert(0, str(HERE / "env" / "play"))


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
    return a_won, swap, env.round_number


def match(a, b, games, off=0, procs=2, sims=100):
    with Pool(procs) as p:
        res = p.map(one, [(str(a), str(b), g + off, sims) for g in range(games)], chunksize=2)
    return res


if __name__ == "__main__":
    a, b, games, off = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    procs = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    sims = int(sys.argv[6]) if len(sys.argv) > 6 else 100
    res = match(a, b, games, off, procs, sims)
    w = sum(r[0] for r in res)
    cy = [r for r in res if not r[1]]; mg = [r for r in res if r[1]]
    print("%s vs %s (off %d): %d/%d (%.1f%%) | A as CYAN %d/%d, A as MAGENTA %d/%d" % (
        Path(a).name, Path(b).name, off, w, games, 100 * w / games,
        sum(r[0] for r in cy), len(cy), sum(r[0] for r in mg), len(mg)), flush=True)
