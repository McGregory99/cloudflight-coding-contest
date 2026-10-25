"""Check the attack maps / win_now against the real rules on random positions.
usage: a_test.py [n_positions] [use_a2]"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "env")); sys.path.insert(0, str(HERE.parent / "env" / "play"))
sys.path.insert(0, str(HERE))
import numpy as np
import onnxruntime as ort
from colony_one import encoding
from colony_one.env import ColonyOneEnv
from colony_one.pieces import PieceType
from colony_one.rules import legal_actions_for_team
import a_build


def can_kill(board, team, left):
    for a in legal_actions_for_team(board, team):
        rec = board.apply_action(a)
        try:
            if rec.captured_piece is not None and rec.captured_piece.piece_type is PieceType.KERNEL:
                return True
            if left > 1 and can_kill(board, team, left - 1):
                return True
        finally:
            board.undo_action(rec)
    return False


def kernel_pos(board, team):
    for r in range(8):
        for c in range(8):
            p = board.grid[r][c]
            if p and p.team == team and p.piece_type is PieceType.KERNEL:
                return (r, c)


def geo2(board, team, kpos):
    """exists a1 then an action targeting kpos (geometric reach, bodyguard ignored)."""
    for a in legal_actions_for_team(board, team):
        rec = board.apply_action(a)
        try:
            if any(b.to_pos == kpos for b in legal_actions_for_team(board, team)):
                return True
        finally:
            board.undo_action(rec)
    return False


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    use_a2 = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    out = HERE / "a_test.onnx"
    a_build.build(out, debug=True, use_a2=use_a2)
    sess = ort.InferenceSession(str(out), providers=["CPUExecutionProvider"])
    rng = np.random.default_rng(1)
    stats = dict(sq_tp=0, sq_fn=0, sq_fp=0, sq_tn=0, win=np.zeros((2, 2), int), g2=np.zeros((2, 2), int), pos=0)
    games = 0
    while stats["pos"] < n:
        env = ColonyOneEnv(); games += 1
        while not env.terminated and stats["pos"] < n:
            team, left, b = env.current_team, env.actions_left, env.board
            legal = legal_actions_for_team(b, team)
            obs = env.observation()[None]
            A1o, A2o, win, dwin = [sess.run(["dbg_A1o", "dbg_A2o", "dbg_win"], {"observation": obs})[i][0] for i in range(3)] + [0]
            targets = {encoding.canonical_pos(a.to_pos, team) for a in legal}
            for r in range(8):
                for c in range(8):
                    rp = encoding.real_pos((r, c), team)
                    pc = b.grid[rp[0]][rp[1]]
                    if pc is not None and pc.team != team:
                        pred, ref = A1o[0, r, c] > 0, (r, c) in targets
                        stats["sq_" + ("tp" if pred and ref else "fn" if ref else "fp" if pred else "tn")] += 1
            ref = can_kill(b, team, left)
            stats["win"][int(ref), int(win > 0.5)] += 1
            kp = kernel_pos(b, "MAGENTA" if team == "CYAN" else "CYAN")
            ck = encoding.canonical_pos(kp, team)
            a1k, a2k = A1o[0, ck[0], ck[1]] > 0, A2o[0, ck[0], ck[1]] > 0
            ref2 = geo2(b, team, kp) if left == 2 else any(a.to_pos == kp for a in legal)
            stats["g2"][int(ref2), int(a1k or (a2k and left == 2))] += 1
            stats["pos"] += 1
            idx = env.legal_action_indices()
            caps = [i for i in idx if True]
            env.step(int(rng.choice(idx)))
    s = stats
    print("positions", s["pos"], "games", games)
    print("A1 per-square vs legal targets: tp %d fn %d fp %d tn %d  recall %.4f precision %.4f" % (
        s["sq_tp"], s["sq_fn"], s["sq_fp"], s["sq_tn"], s["sq_tp"] / max(1, s["sq_tp"] + s["sq_fn"]),
        s["sq_tp"] / max(1, s["sq_tp"] + s["sq_fp"])))
    w = s["win"]; print("win_now vs can_kill [ref x pred]:", w.tolist(), "acc %.4f" % (np.trace(w) / w.sum()),
                         "pos recall %.3f" % (w[1, 1] / max(1, w[1].sum())), "precision %.3f" % (w[1, 1] / max(1, w[:, 1].sum())))
    g = s["g2"]; print("kernel reach (<=2 actions, geometric) [ref x pred]:", g.tolist(), "acc %.4f" % (np.trace(g) / g.sum()),
                       "pos recall %.3f" % (g[1, 1] / max(1, g[1].sum())), "precision %.3f" % (g[1, 1] / max(1, g[:, 1].sum())))


if __name__ == "__main__":
    main()
