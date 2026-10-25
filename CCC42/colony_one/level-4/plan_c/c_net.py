import numpy as np, onnx, torch, torch.nn as nn, torch.nn.functional as F
from onnx import numpy_helper
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "model.onnx"


class Net(nn.Module):
    def __init__(self, ch=48, delta_policy=True, delta_value=True):
        super().__init__()
        init = {i.name: torch.from_numpy(numpy_helper.to_array(i).copy()) for i in onnx.load(str(BASE)).graph.initializer}
        for k in ("value_w", "cap_w", "to_map", "kmap", "move"):
            self.register_buffer(k, init[k])
        self.c0 = nn.Conv2d(16, ch, 3, padding=1)
        self.cs = nn.ModuleList([nn.Conv2d(ch, ch, 3, padding=1) for _ in range(4)])
        self.pol = nn.Conv2d(ch, 64, 1)
        self.v1 = nn.Conv2d(ch, 8, 1)
        self.v2 = nn.Linear(512, 64)
        self.v3 = nn.Linear(64, 1)
        for m in (self.pol, self.v3):
            nn.init.zeros_(m.weight); nn.init.zeros_(m.bias)
        self.delta_value = delta_value

    def base(self, x):
        raw = x.reshape(-1, 1024) @ self.value_w  # (B,1)
        em = F.conv2d(x[:, 6:12], self.cap_w).reshape(-1, 64)
        ok = x[:, 5:6].reshape(-1, 64)
        pol = em @ self.to_map + ok @ self.kmap + self.move
        return pol, raw

    def forward(self, x):
        pol, raw = self.base(x)
        h = F.relu(self.c0(x))
        for c in self.cs:
            h = F.relu(c(h))
        d = self.pol(h).reshape(-1, 64, 64).transpose(1, 2).reshape(-1, 4096)
        v = self.v3(F.relu(self.v2(F.relu(self.v1(h)).reshape(-1, 512))))
        if not self.delta_value:
            v = v * 0
        return pol + d, torch.tanh(raw + v)[:, 0]
