import numpy as np, onnx, torch, torch.nn as nn
from onnx import numpy_helper
from pathlib import Path
L4 = Path(__file__).resolve().parent.parent


class Net(nn.Module):
    def __init__(s, w=48, a=3.0, b=1.0, c=0.5):
        super().__init__()
        s.trunk = nn.Sequential(nn.Conv2d(16, w, 3, padding=1), nn.ReLU(),
                                *[m for _ in range(4) for m in (nn.Conv2d(w, w, 3, padding=1), nn.ReLU())],
                                nn.Conv2d(w, 8, 1), nn.ReLU(), nn.Flatten(), nn.Linear(512, 64), nn.ReLU(), nn.Linear(64, 3))
        s.abc = (a, b, c)
        init = {i.name: numpy_helper.to_array(i) for i in onnx.load(str(L4 / "model.onnx")).graph.initializer}
        for k in ("value_w", "cap_w", "to_map", "kmap", "move"):
            s.register_buffer(k, torch.from_numpy(init[k].copy()))

    def heads(s, x): return s.trunk(x)

    def forward(s, x):
        h = s.trunk(x); a, b, c = s.abc
        raw = torch.flatten(x, 1) @ s.value_w
        v = torch.tanh(raw + a * torch.sigmoid(h[:, 0:1]) - b * torch.sigmoid(h[:, 1:2]) + c * torch.tanh(h[:, 2:3]))
        enemy = nn.functional.conv2d(x[:, 6:12], s.cap_w).reshape(-1, 64)
        own_k = x[:, 5:6].reshape(-1, 64)
        pol = enemy @ s.to_map + own_k @ s.kmap + s.move
        return pol, v.squeeze(1)


def export(net, path, a, b, c):
    import subprocess, sys, tempfile
    net.abc = (a, b, c); net.eval()
    tmp = tempfile.mktemp(suffix=".onnx")
    torch.onnx.export(net, torch.zeros(2, 16, 8, 8), tmp, opset_version=17, dynamo=False,
                      input_names=["observation"], output_names=["policy", "value"],
                      dynamic_axes={"observation": {0: "batch"}, "policy": {0: "batch"}, "value": {0: "batch"}})
    m = onnx.load(tmp, load_external_data=True)
    g = m.graph; keep = []
    for n in g.node:
        if n.op_type == "Constant":
            g.initializer.append(numpy_helper.from_array(numpy_helper.to_array(n.attribute[0].t), n.output[0]))
        else: keep.append(n)
    del g.node[:]; g.node.extend(keep)
    m.ir_version = 8
    onnx.checker.check_model(m); onnx.save(m, str(path), save_as_external_data=False)
