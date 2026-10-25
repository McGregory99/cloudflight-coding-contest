"""Hand-built policy/value ONNX: material + Kernel-centrality value, capture-greedy policy prior.

Planes 0-5 own Ping, Daemon, Exploit, Trace, Ice, Kernel; 6-11 the enemy's (docs/observation.md).
The referee's MCTS supplies the lookahead. The firewall destroys pieces on the outer ring at the end
of round 8 (then 16, 24, 26), so a Kernel must drift toward the centre: ring term on planes 5 and 11.
"""
import sys
from pathlib import Path

import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

PIECE = np.array([15, 45, 25, 30, 50, 0], dtype=np.float32) / 25.0  # Ping, Daemon, Exploit, Trace, Ice, Kernel
VALUE_SCALE = 1.0
POLICY_SCALE = 10.0
KERNEL_RING = 2.0   # value per ring step toward the centre (0 edge .. 3 central 2x2)
ENEMY_RING = 0.0    # same for the enemy Kernel, subtracted


def ring_map() -> np.ndarray:
    return np.array([[min(r, 7 - r, c, 7 - c) for c in range(8)] for r in range(8)], np.float32).reshape(64)


def build(path: Path) -> None:
    value_w = np.zeros((16 * 64, 1), np.float32)
    for p in range(6):
        value_w[p * 64:(p + 1) * 64, 0] = PIECE[p] * VALUE_SCALE
        value_w[(6 + p) * 64:(7 + p) * 64, 0] = -PIECE[p] * VALUE_SCALE
    value_w[5 * 64:6 * 64, 0] += KERNEL_RING * ring_map()
    value_w[11 * 64:12 * 64, 0] -= ENEMY_RING * ring_map()

    cap_w = (PIECE * POLICY_SCALE).reshape(1, 6, 1, 1).astype(np.float32)  # enemy piece value per plane
    to_map = np.zeros((64, 4096), np.float32)
    for f in range(64):
        for t in range(64):
            to_map[t, f * 64 + t] = 1.0

    init = [
        numpy_helper.from_array(value_w, "value_w"),
        numpy_helper.from_array(cap_w, "cap_w"),
        numpy_helper.from_array(to_map, "to_map"),
        numpy_helper.from_array(np.array([6, 0, 0], np.int64), "sl_starts"),
        numpy_helper.from_array(np.array([12, 8, 8], np.int64), "sl_ends"),
        numpy_helper.from_array(np.array([1, 2, 3], np.int64), "sl_axes"),
        numpy_helper.from_array(np.array([-1, 64], np.int64), "flat_shape"),
        numpy_helper.from_array(np.array([1], np.int64), "sq_axes"),
    ]
    nodes = [
        helper.make_node("Flatten", ["observation"], ["flat_obs"], axis=1),
        helper.make_node("MatMul", ["flat_obs", "value_w"], ["raw"]),
        helper.make_node("Tanh", ["raw"], ["v2"]),
        helper.make_node("Squeeze", ["v2", "sq_axes"], ["value"]),
        # policy: logit(from,to) = value of the enemy piece standing on `to`
        helper.make_node("Slice", ["observation", "sl_starts", "sl_ends", "sl_axes"], ["enemy"]),
        helper.make_node("Conv", ["enemy", "cap_w"], ["enemy_map"], kernel_shape=[1, 1]),
        helper.make_node("Reshape", ["enemy_map", "flat_shape"], ["enemy_flat"]),
        helper.make_node("MatMul", ["enemy_flat", "to_map"], ["policy"]),
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
    out = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent / "model.onnx")
    build(out)
    print("wrote", out, out.stat().st_size, "bytes")
