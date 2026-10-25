"""Self-play with MCTS -> shards of (planes, visits, legal mask, z, Q).
usage: c_selfplay.py MODEL.onnx OUTPREFIX GAMES_PER_WORKER SEED0 MINUTES [SIMS]"""
import sys, time
from multiprocessing import Pool
from pathlib import Path
HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "env"))
import numpy as np


def worker(args):
    model, prefix, w, ngames, seed0, deadline, sims = args
    from colony_one import mcts, encoding
    from colony_one.env import ColonyOneEnv
    from colony_one.onnx_runner import OnnxEvaluator
    ev = OnnxEvaluator(Path(model), num_threads=1)
    cfg = mcts.MCTSConfig(simulations=sims, batch_size=8)
    P, V, M, Z, Q = [], [], [], [], []
    st = {"shard": 0}
    done = 0
    def flush():
        nonlocal P, V, M, Z, Q
        if P:
            np.savez_compressed("%s_w%d_s%d.npz" % (prefix, w, st["shard"]), planes=np.array(P, np.float16),
                                visits=np.array(V, np.uint8), legal=np.array(M, np.uint8), z=np.array(Z, np.float32), q=np.array(Q, np.float32))
            st["shard"] += 1
        P, V, M, Z, Q = [], [], [], [], []
    for g in range(ngames):
        if time.time() > deadline:
            break
        rng = np.random.default_rng(seed0 + w * 100000 + g)
        env = ColonyOneEnv()
        rec = []
        n = 0
        while not env.terminated:
            team = env.current_team
            root = mcts.run(env.board, team, env.actions_left, env.round_number, ev, cfg, rng=rng)
            temp = 1.0 if n < 8 else 0.25
            a = mcts.select_action_index(root, temp, rng)
            tot = sum(root.N.values())
            q = sum(root.W.values()) / max(1, tot)
            vis = np.zeros(4096, np.uint8)
            for k, c in root.N.items(): vis[k] = c
            leg = np.zeros(4096, np.uint8)
            for k in root.P: leg[k] = 1
            rec.append((encoding.encode_board(env.board, team, env.actions_left, env.round_number), vis, np.packbits(leg), team, q))
            env.step(encoding.decode_action(a, team, env.board)); n += 1
        for pl, vis, leg, team, q in rec:
            P.append(pl); V.append(vis); M.append(leg); Z.append(env.result_for(team)); Q.append(q)
        done += 1
        if done % 5 == 0: flush()
    flush()
    return done


if __name__ == "__main__":
    model, prefix, ng, seed0, minutes, sims, w = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
    print("games", worker((model, prefix, w, ng, seed0, time.time() + minutes * 60, sims)), flush=True)
