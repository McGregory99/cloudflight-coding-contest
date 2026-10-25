"""Hand-built Level 4 policy/value ONNX (linear features + tanh, a few constant tables).

Observation planes: 0-5 own Ping, Daemon, Exploit, Trace, Ice, Kernel; 6-11 enemy (docs/observation.md).
The firewall destroys the outer ring at the end of rounds 8/16/24/26, so everything is shaped by
"ring" = distance to the board edge (0 edge .. 3 central 2x2).
"""
import sys
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

PIECE = np.array([15, 45, 25, 30, 50, 0], dtype=np.float32) / 25.0  # Ping, Daemon, Exploit, Trace, Ice, Kernel
DEFAULTS = dict(
    value_scale=1.0,    # material weight in the value
    kernel_ring=2.0,    # value per ring step of our Kernel
    enemy_ring=0.0,     # value per ring step of the enemy Kernel (subtracted)
    piece_ring=0.0,     # value per ring step of each own non-Kernel piece
    cap_scale=10.0,     # policy prior for captures (x piece value)
    kernel_cap=4.0,     # policy weight of capturing the enemy Kernel (x cap_scale)
    move_ring=0.0,      # policy prior for any move toward the centre
    kernel_move=0.0,    # extra policy prior for Kernel moves toward the centre
    temp=1.0,           # value = tanh(raw / temp)
)


def ring_map() -> np.ndarray:
    return np.array([[min(r, 7 - r, c, 7 - c) for c in range(8)] for r in range(8)], np.float32).reshape(64)


def build(path: Path, **kw) -> None:
    p = {**DEFAULTS, **kw}
    ring = ring_map()
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

    i64 = lambda n, v: numpy_helper.from_array(np.array(v, np.int64), n)
    init = [
        numpy_helper.from_array(value_w, "value_w"), numpy_helper.from_array(cap_w, "cap_w"),
        numpy_helper.from_array(to_map, "to_map"), numpy_helper.from_array(kmap, "kmap"),
        numpy_helper.from_array(move, "move"),
        i64("en_s", [6, 0, 0]), i64("en_e", [12, 8, 8]), i64("k_s", [5, 0, 0]), i64("k_e", [6, 8, 8]),
        i64("sl_axes", [1, 2, 3]), i64("flat_shape", [-1, 64]), i64("sq_axes", [1]),
    ]
    nodes = [
        helper.make_node("Flatten", ["observation"], ["flat_obs"], axis=1),
        helper.make_node("MatMul", ["flat_obs", "value_w"], ["raw"]),
        helper.make_node("Tanh", ["raw"], ["v2"]),
        helper.make_node("Squeeze", ["v2", "sq_axes"], ["value"]),
        helper.make_node("Slice", ["observation", "en_s", "en_e", "sl_axes"], ["enemy"]),
        helper.make_node("Conv", ["enemy", "cap_w"], ["enemy_map"], kernel_shape=[1, 1]),
        helper.make_node("Reshape", ["enemy_map", "flat_shape"], ["enemy_flat"]),
        helper.make_node("MatMul", ["enemy_flat", "to_map"], ["cap_logits"]),
        helper.make_node("Slice", ["observation", "k_s", "k_e", "sl_axes"], ["own_k"]),
        helper.make_node("Reshape", ["own_k", "flat_shape"], ["own_k_flat"]),
        helper.make_node("MatMul", ["own_k_flat", "kmap"], ["k_logits"]),
        helper.make_node("Add", ["cap_logits", "k_logits"], ["pre"]),
        helper.make_node("Add", ["pre", "move"], ["policy"]),
    ]
    graph = helper.make_graph(
        nodes, "colony_handmade",
        [helper.make_tensor_value_info("observation", TensorProto.FLOAT, ["batch", 16, 8, 8])],
        [helper.make_tensor_value_info("policy", TensorProto.FLOAT, ["batch", 4096]),
         helper.make_tensor_value_info("value", TensorProto.FLOAT, ["batch"])],
        init,
    )
    model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 17)])
    model.ir_version = 8
    onnx.checker.check_model(model)
    onnx.save(model, str(path))


if __name__ == "__main__":
    import json
    out = Path(sys.argv[1]); build(out, **(json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}))
    print("wrote", out, out.stat().st_size, "bytes")
