"""Generate labelled positions. usage: b_gen.py N_GAMES SEED_OFF OUT.npz [procs] [n_bare]"""
import sys
from pathlib import Path
L4 = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(L4 / "env")); sys.path.insert(0, str(L4 / "env" / "play"))
import numpy as np

M, L3, R = str(L4 / "model.onnx"), str(L4 / "model_l3.onnx"), str(L4 / "env/play/random.onnx")
PAIRS = [(M, L3), (L3, M), (M, M), (M, R), (R, M), (L3, L3), (L3, R), (R, L3), (M, L3), (L3, M)]


def can_kill(board, team, left):
    from colony_one.rules import legal_actions_for_team
    from colony_one.pieces import PieceType
    for a in legal_actions_for_team(board, team):
        rec = board.apply_action(a)
        try:
            if rec.captured_piece is not None and rec.captured_piece.piece_type is PieceType.KERNEL: return True
            if left > 1 and can_kill(board, team, left - 1): return True
        finally: board.undo_action(rec)
    return False


SIMS = 40


def opp(t): return "MAGENTA" if t == "CYAN" else "CYAN"


def game(args):
    g, off = args
    from colony_one.env import ColonyOneEnv
    from colony_one.encoding import encode_board
    from model_vs_model import SearchAgent
    gg = g + off
    pa, pb = PAIRS[g % len(PAIRS)]
    cy, ma = SearchAgent(Path(pa), SIMS, seed=2 * gg), SearchAgent(Path(pb), SIMS, seed=2 * gg + 1)
    env = ColonyOneEnv(); X, W, T, S = [], [], [], []
    while not env.terminated:
        t, l, r = env.current_team, env.actions_left, env.round_number
        X.append(encode_board(env.board, t, l, r)); S.append(t)
        W.append(can_kill(env.board, t, l)); T.append(can_kill(env.board, opp(t), 2))
        env.step((cy if t == "CYAN" else ma).select(env.board, t, l, r))
    Z = [1.0 if s == env.winner else -1.0 for s in S]
    return np.array(X, np.float32), np.array(W, np.float32), np.array(T, np.float32), np.array(Z, np.float32)


def bare(args):
    """Two-Kernel positions (mid-turn leaves): exact z by enumerating the mover's sequences."""
    seed, n = args
    from colony_one.board import Board
    from colony_one.pieces import Piece, PieceType
    from colony_one.encoding import encode_board
    from colony_one.rules import legal_actions_for_team
    rng = np.random.default_rng(seed); out = []
    def best(board, t, left):
        for a in legal_actions_for_team(board, t):
            rec = board.apply_action(a)
            try:
                if rec.captured_piece is not None and rec.captured_piece.piece_type is PieceType.KERNEL: return True
                if left > 1:
                    if best(board, t, left - 1): return True
                elif board.kernel_endgame_winner(acting_team=t) == t: return True
            finally: board.undo_action(rec)
        return False
    while len(out) < n:
        b = Board()
        for r in range(8):
            for c in range(8): b.grid[r][c] = None
        rnd = int(rng.choice([r for r in range(1, 27) if r not in (8, 16, 24, 26)]))
        b.locked = Board.locked_cells_for_round(rnd)
        free = [(r, c) for r in range(8) for c in range(8) if not b.locked[r][c]]
        if len(free) < 2: continue
        i, j = rng.choice(len(free), 2, replace=False)
        b.grid[free[i][0]][free[i][1]] = Piece(PieceType.KERNEL, "CYAN")
        b.grid[free[j][0]][free[j][1]] = Piece(PieceType.KERNEL, "MAGENTA")
        t = str(rng.choice(["CYAN", "MAGENTA"])); l = int(rng.integers(1, 3))
        w = best(b, t, l)
        out.append((encode_board(b, t, l, rnd), float(can_kill(b, t, l)), float(can_kill(b, opp(t), 2)), 1.0 if w else -1.0))
    return (np.array([o[0] for o in out]), np.array([o[1] for o in out], np.float32),
            np.array([o[2] for o in out], np.float32), np.array([o[3] for o in out], np.float32))


if __name__ == "__main__":
    from multiprocessing import Pool
    n, off, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    procs = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    nb = int(sys.argv[5]) if len(sys.argv) > 5 else 3000
    import time; dl = time.time() + 60 * float(sys.argv[6])
    with Pool(procs) as p:
        parts = [p.apply_async(bare, ((off + k, nb // procs),)) for k in range(procs)]
        res = []
        for i, r in enumerate(p.imap_unordered(game, [(g, off) for g in range(n)])):
            res.append(r)
            if time.time() > dl: n = i + 1; p.terminate(); break
            if i % 50 == 0: print(i, sum(len(x[0]) for x in res), flush=True)
        res += [x.get() for x in parts]
    X, W, T, Z = (np.concatenate([r[k] for r in res]) for k in range(4))
    isbare = np.concatenate([np.full(len(r[0]), i >= n, bool) for i, r in enumerate(res)])
    np.savez_compressed(out, X=X, W=W, T=T, Z=Z, bare=isbare)
    print("done", X.shape, "win_now", W.mean(), "thr", T.mean(), "bare z>0", (Z[isbare] > 0).mean())
