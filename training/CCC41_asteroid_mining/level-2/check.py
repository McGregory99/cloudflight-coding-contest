"""Validator for level 2: every output asteroid = input grid + X column straight down below the outpost."""
import sys
from pathlib import Path

HERE = Path(__file__).parent


def blocks(text):
    b, cur = [], []
    for ln in text.split("\n"):
        if ln.strip():
            cur.append(ln)
        elif cur:
            b.append(cur); cur = []
    return b + ([cur] if cur else [])


ok = True
for f in sorted(HERE.glob("in_level-2_*.txt")):
    o = HERE / f.name.replace("in_", "").replace(".txt", ".out")
    first, *rest = f.read_text().split("\n")
    ib = [b[1:] for b in blocks("\n".join(rest))]
    ob = blocks(o.read_text())
    good = int(first) == len(ib) == len(ob)
    for g, x in zip(ib, ob):
        s = g[0].index("S")
        exp = [g[0]] + [r[:s] + "X" + r[s + 1:] for r in g[1:-1]] + [g[-1]]
        good &= exp == x
    print("OK  " if good else "FAIL", f.name)
    ok &= good
sys.exit(0 if ok else 1)
