"""Plan A: model.onnx base (linear value + capture/Kernel policy) plus exact attack maps.

Graph uses only Conv shifts, Mul/Add/Sub/Min/Relu/ReduceSum/Slice/MatMul/Reshape (all allow-listed;
no Constant nodes: every constant is an initializer).
"""
import sys
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import build_model as bm  # read-only import: base defaults

PIECE = bm.PIECE
DEFAULTS = dict(
    bm.DEFAULTS,
    kernel_ring=2.0,
    w_win=3.0,     # value bonus when side to move can kill the enemy Kernel this turn
    w_thr=1.5,     # value penalty when the enemy threatens our Kernel (halved with 2 actions left)
    w_kmove=4.0,   # policy penalty for Kernel moves onto attacked squares
    w_hang=0.0,    # value for hanging material (enemy undefended attacked pieces - 0.5*ours)
    w_rd=0.0,      # bare-Kernel endgame: ring difference
    w_mag=0.0,     # bare-Kernel endgame: Magenta wins equal rings
    w_ch=0.0,      # bare-Kernel endgame: penalty for Chebyshev<=2 when we cannot kill
    k_u=0.0,       # value: urgency * ring of own Kernel
    k_pu=0.0,      # policy: urgency * Kernel ring step
    k_e=0.0,       # value: -k_e*urgency_ramp if own Kernel on ring 0 (+ same for enemy)
    use_a2=1.0,    # 1: include 2-action reach (A2); 0: only A1 (plan B fallback)
)

ORTH = [(-1, 0), (1, 0), (0, -1), (0, 1)]
DIAG = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
ALL8 = ORTH + DIAG
LJ = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]


class G:
    def __init__(self):
        self.nodes, self.init, self.n, self.cache = [], [], 0, {}

    def name(self, p="t"):
        self.n += 1
        return "%s%d" % (p, self.n)

    def const(self, arr, dtype=np.float32, key=None):
        arr = np.asarray(arr, dtype)
        k = key or (arr.tobytes(), arr.shape, str(arr.dtype))
        if k in self.cache:
            return self.cache[k]
        nm = self.name("c")
        self.init.append(numpy_helper.from_array(arr, nm))
        self.cache[k] = nm
        return nm

    def op(self, typ, ins, **kw):
        out = self.name()
        self.nodes.append(helper.make_node(typ, ins, [out], **kw))
        return out

    def add(self, a, b): return self.op("Add", [a, b])
    def sub(self, a, b): return self.op("Sub", [a, b])
    def mul(self, a, b): return self.op("Mul", [a, b])
    def relu(self, a): return self.op("Relu", [a])
    def mn(self, a, b): return self.op("Min", [a, b])
    def sc(self, a, v): return self.mul(a, self.const([v]))          # a * scalar
    def mn1(self, a): return self.mn(a, self.const([1.0]))
    def rsum(self, a, axes, keep=0):
        return self.op("ReduceSum", [a, self.const(axes, np.int64)], keepdims=keep)

    def sl(self, a, lo, hi, axis=1):
        return self.op("Slice", [a, self.const([lo], np.int64), self.const([hi], np.int64),
                                 self.const([axis], np.int64)])

    def shift(self, y, offs):
        """(B,n,8,8) with channel i = y[t + offs[i]] (zero outside the board)."""
        key = ("shift", y, tuple(offs))
        if key in self.cache:
            return self.cache[key]
        w = np.zeros((len(offs), 1, 7, 7), np.float32)
        for i, (dr, dc) in enumerate(offs):
            w[i, 0, 3 + dr, 3 + dc] = 1
        out = self.op("Conv", [y, self.const(w)], kernel_shape=[7, 7], pads=[3, 3, 3, 3])
        self.cache[key] = out
        return out

    def ray(self, y, e, dirs, j):
        """Pieces of y at t+j*d with the j-1 squares between them and t empty, summed over dirs."""
        s = self.shift(y, [(j * dr, j * dc) for dr, dc in dirs])
        for i in range(1, j):
            s = self.mul(s, self.shift(e, [(i * dr, i * dc) for dr, dc in dirs]))
        return self.rsum(s, [1], keep=1)

    def total(self, terms):
        acc = terms[0]
        for t in terms[1:]:
            acc = self.add(acc, t)
        return acc


def attack_map(g, y, e):
    """Per-target-square count of attacks (1 action) by the pieces in y (dict by type index 0..5)."""
    P, D, X, T, I, K = (y[i] for i in range(6))
    return g.total([
        g.ray(D, e, ALL8, 1), g.ray(D, e, ORTH, 2), g.ray(D, e, ORTH, 3),
        g.ray(I, e, ALL8, 1), g.ray(I, e, ALL8, 2),
        g.ray(P, e, DIAG, 1), g.ray(P, e, DIAG, 2),
        g.ray(T, e, DIAG, 2), g.ray(T, e, DIAG, 3),
        g.rsum(g.shift(X, LJ), [1], keep=1),
        g.ray(K, e, ALL8, 1),
    ])


def reach_maps(g, y, e):
    """Empty squares each piece type can move to in 1 action."""
    P, D, X, T, I, K = (y[i] for i in range(6))
    mv = lambda t: g.mul(t, e)
    return {
        0: mv(g.add(g.ray(P, e, ORTH, 1), g.ray(P, e, ORTH, 2))),
        1: mv(g.total([g.ray(D, e, ORTH, j) for j in (1, 2, 3)])),
        2: mv(g.rsum(g.shift(X, LJ), [1], keep=1)),
        3: mv(g.ray(T, e, ORTH, 1)),
        4: mv(g.add(g.ray(I, e, ALL8, 1), g.ray(I, e, ALL8, 2))),
        5: mv(g.ray(K, e, ALL8, 1)),
    }


def build(path, debug=False, **kw):
    p = {**DEFAULTS, **kw}
    g = G()
    ring = bm.ring_map()
    # ---- base model.onnx pieces
    value_w = np.zeros((16 * 64, 1), np.float32)
    for k in range(6):
        value_w[k * 64:(k + 1) * 64, 0] = PIECE[k] * p["value_scale"]
        value_w[(6 + k) * 64:(7 + k) * 64, 0] = -PIECE[k] * p["value_scale"]
    for k in range(5):
        value_w[k * 64:(k + 1) * 64, 0] += p["piece_ring"] * ring
    value_w[5 * 64:6 * 64, 0] += p["kernel_ring"] * ring
    value_w[11 * 64:12 * 64, 0] -= p["enemy_ring"] * ring
    value_w /= p["temp"]
    cap = PIECE.copy(); cap[5] = p["kernel_cap"]
    cap_w = (cap * p["cap_scale"]).reshape(1, 6, 1, 1).astype(np.float32)
    to_map = np.zeros((64, 4096), np.float32)
    kmap = np.zeros((64, 4096), np.float32)
    move = np.zeros((1, 4096), np.float32)
    for f in range(64):
        for t in range(64):
            to_map[t, f * 64 + t] = 1.0
            kmap[f, f * 64 + t] = p["kernel_move"] * (ring[t] - ring[f])
            move[0, f * 64 + t] = p["move_ring"] * (ring[t] - ring[f])

    obs = "observation"
    flat_obs = g.op("Flatten", [obs], axis=1)
    raw = g.op("Squeeze", [g.op("MatMul", [flat_obs, g.const(value_w)]), g.const([1], np.int64)])  # (B,)

    # ---- planes
    pl = [g.sl(obs, k, k + 1) for k in range(12)]           # each (B,1,8,8)
    own, en = {k: pl[k] for k in range(6)}, {k: pl[6 + k] for k in range(6)}
    occ = g.rsum(g.sl(obs, 0, 13), [1], keep=1)
    e = g.sub(g.const([1.0]), occ)                           # empty & unlocked squares
    K_own, K_en = own[5], en[5]
    nonk_own = g.rsum(g.sl(obs, 0, 5), [1], keep=1)
    nonk_en = g.rsum(g.sl(obs, 6, 11), [1], keep=1)

    A1o, A1e = attack_map(g, own, e), attack_map(g, en, e)
    if p["use_a2"]:
        A2o = attack_map(g, reach_maps(g, own, e), e)
        A2e = attack_map(g, reach_maps(g, en, e), e)
    else:
        A2o = g.sc(A1o, 0.0); A2e = g.sc(A1e, 0.0)

    nb = np.ones((1, 1, 3, 3), np.float32); nb[0, 0, 1, 1] = 0
    conv3 = lambda y, w: g.op("Conv", [y, g.const(w)], kernel_shape=[3, 3], pads=[1, 1, 1, 1])
    ones3 = np.ones((1, 1, 3, 3), np.float32)
    G_en = g.rsum(g.mul(nonk_en, conv3(K_en, ones3)), [1, 2, 3])    # guards of the enemy Kernel
    G_own = g.rsum(g.mul(nonk_own, conv3(K_own, ones3)), [1, 2, 3])
    one = g.const([1.0]); two = g.const([2.0])
    g0 = lambda G_: g.mn1(g.relu(g.sub(one, G_)))            # guards == 0
    g1 = lambda G_: g.mn1(g.relu(g.sub(two, G_)))            # guards <= 1
    sr = lambda m, k: g.rsum(g.mul(m, k), [1, 2, 3])
    a1o, a2o = g.mn1(sr(A1o, K_en)), g.mn1(sr(A2o, K_en))
    a1e, a2e = g.mn1(sr(A1e, K_own)), g.mn1(sr(A2e, K_own))
    is2 = g.sc(g.sub(g.op("ReduceMean", [g.sl(obs, 13, 14)], axes=[1, 2, 3], keepdims=0), g.const([0.5])), 2.0)  # 1 if 2 actions left
    win1 = g.mul(a1o, g0(G_en))
    win2 = g.mn1(g.add(g.mul(a1o, g1(G_en)), g.mul(a2o, g0(G_en))))
    win_now = g.add(win1, g.mul(is2, g.sub(win2, win1)))
    thr = g.mn1(g.add(g.mul(a1e, g1(G_own)), g.mul(a2e, g0(G_own))))   # enemy kills with a full turn
    thr_eff = g.relu(g.sub(thr, win_now))
    thr_w = g.sub(one, g.sc(is2, 0.5))
    v = g.add(raw, g.sc(win_now, p["w_win"]))
    v = g.sub(v, g.sc(g.mul(thr_eff, thr_w), p["w_thr"]))

    # ---- hanging material (undefended attacked pieces)
    if p["w_hang"]:
        mat = np.array(PIECE[:5], np.float32).reshape(1, 5, 1, 1)
        own_mat = g.op("Conv", [g.sl(obs, 0, 5), g.const(mat)], kernel_shape=[1, 1])
        en_mat = g.op("Conv", [g.sl(obs, 6, 11), g.const(mat)], kernel_shape=[1, 1])
        und_e = g.sub(one, g.mn1(A1e)); und_o = g.sub(one, g.mn1(A1o))
        hang_en = g.rsum(g.mul(g.mul(en_mat, g.mn1(A1o)), und_e), [1, 2, 3])
        hang_own = g.rsum(g.mul(g.mul(own_mat, g.mn1(A1e)), und_o), [1, 2, 3])
        v = g.add(v, g.sc(g.sub(hang_en, g.sc(hang_own, 0.5)), p["w_hang"]))

    # ---- bare-Kernel endgame
    if p["w_rd"] or p["w_mag"] or p["w_ch"]:
        others = g.add(g.rsum(g.sl(obs, 0, 5), [1, 2, 3]), g.rsum(g.sl(obs, 6, 11), [1, 2, 3]))
        gate = g.relu(g.sub(one, others))
        ringc = g.const(ring.reshape(1, 1, 8, 8))
        r_o, r_e = sr(K_own, ringc), sr(K_en, ringc)
        diff = g.sub(r_o, r_e)
        eq = g.sub(one, g.mn1(g.op("Abs", [diff])))
        p15 = g.rsum(g.sl(obs, 15, 16), [1, 2, 3])
        p15 = g.sc(p15, 1.0 / 64)
        ch = g.mn1(sr(conv5(g, K_own), K_en))
        end = g.add(g.sc(diff, p["w_rd"]), g.sc(g.mul(g.sub(g.sc(p15, 2.0), one), eq), p["w_mag"]))
        end = g.sub(end, g.sc(g.mul(ch, g.sub(one, win_now)), p["w_ch"]))
        v = g.add(v, g.mul(gate, end))

    urg = g.op("ReduceMean", [g.sl(obs, 14, 15)], axes=[1, 2, 3], keepdims=0)   # (B,)
    if p["k_u"]:
        rk = g.rsum(g.mul(K_own, g.const(ring.reshape(1, 1, 8, 8))), [1, 2, 3])
        v = g.add(v, g.sc(g.mul(urg, rk), p["k_u"]))
    if p["k_e"]:
        r0 = g.const((ring == 0).astype(np.float32).reshape(1, 1, 8, 8))
        ramp = g.sc(g.relu(g.sub(urg, g.const([0.5]))), 2.0)
        v = g.sub(v, g.sc(g.mul(ramp, g.sub(sr(K_own, r0), sr(K_en, r0))), p["k_e"]))
    value = g.op("Tanh", [v])

    # ---- policy: base (captures + Kernel ring) minus Kernel moves into attacked squares
    enemy = g.sl(obs, 6, 12)
    enemy_map = g.op("Conv", [enemy, g.const(cap_w)], kernel_shape=[1, 1])
    flat_shape = g.const([-1, 64], np.int64)
    enemy_flat = g.op("Reshape", [enemy_map, flat_shape])
    cap_logits = g.op("MatMul", [enemy_flat, g.const(to_map)])
    own_k_flat = g.op("Reshape", [K_own, flat_shape])
    k_logits = g.op("MatMul", [own_k_flat, g.const(kmap)])
    pol = g.total([cap_logits, k_logits, g.const(move)])
    if p["k_pu"]:
        kmap1 = np.zeros((64, 4096), np.float32)
        for f in range(64):
            for t in range(64):
                kmap1[f, f * 64 + t] = ring[t] - ring[f]
        ku = g.op("MatMul", [own_k_flat, g.const(kmap1)])
        pol = g.add(pol, g.sc(g.mul(ku, g.op("Unsqueeze", [urg, g.const([1], np.int64)])), p["k_pu"]))
    if p["w_kmove"]:
        gm = conv3(nonk_own, nb)                                          # own guards adjacent to each square
        gle1 = g.mn1(g.relu(g.sub(two, gm))); gz = g.relu(g.sub(one, gm))
        danger = g.mn1(g.add(g.mul(g.mn1(A1e), gle1), g.mul(g.mn1(A2e), gz)))
        dflat = g.op("Reshape", [danger, g.const([-1, 1, 64], np.int64)])
        kcol = g.op("Reshape", [K_own, g.const([-1, 64, 1], np.int64)])
        kd = g.op("Reshape", [g.mul(kcol, dflat), g.const([-1, 4096], np.int64)])
        pol = g.sub(pol, g.sc(kd, p["w_kmove"]))
    g.nodes.append(helper.make_node("Identity", [pol], ["policy"]))
    g.nodes.append(helper.make_node("Identity", [value], ["value"]))

    outs = [helper.make_tensor_value_info("policy", TensorProto.FLOAT, ["batch", 4096]),
            helper.make_tensor_value_info("value", TensorProto.FLOAT, ["batch"])]
    if debug:
        for nm, t in (("dbg_A1o", A1o), ("dbg_A2o", A2o), ("dbg_A1e", A1e), ("dbg_win", win_now),
                      ("dbg_thr", thr), ("dbg_Gen", G_en)):
            g.nodes.append(helper.make_node("Identity", [t], [nm]))
            outs.append(helper.make_tensor_value_info(nm, TensorProto.FLOAT, ["batch", 1, 8, 8] if nm[4] == "A" else ["batch"]))
    graph = helper.make_graph(g.nodes, "colony_plan_a",
                              [helper.make_tensor_value_info("observation", TensorProto.FLOAT, ["batch", 16, 8, 8])],
                              outs, g.init)
    model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 17)])
    model.ir_version = 8
    onnx.checker.check_model(model)
    onnx.save(model, str(path))


def conv5(g, y):
    return g.op("Conv", [y, g.const(np.ones((1, 1, 5, 5), np.float32))], kernel_shape=[5, 5], pads=[2, 2, 2, 2])


if __name__ == "__main__":
    import json
    out = Path(sys.argv[1]); build(out, **(json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}))
    print("wrote", out, out.stat().st_size, "bytes")
