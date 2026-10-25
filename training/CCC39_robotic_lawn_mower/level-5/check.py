"""Independent validator: re-simulates every path against its lawn (start cell is inferred by trying all offsets)."""
import sys
from pathlib import Path
d = Path(__file__).parent
CYCLE = False
D = {"W": (0, -1), "D": (1, 0), "S": (0, 1), "A": (-1, 0)}

def lawns(text):
    t = text.split(); n = int(t[0]); p = 1
    for _ in range(n):
        w, h = int(t[p]), int(t[p + 1]); p += 2
        yield w, h, t[p:p + h]; p += h

def ok(w, h, g, path):
    free = {(x, y) for y in range(h) for x in range(w) if g[y][x] == "."}
    if set(path) - set(D) or len(path) + 1 != len(free): return False
    rel = [(0, 0)]
    for c in path:
        rel.append((rel[-1][0] + D[c][0], rel[-1][1] + D[c][1]))
    if len(set(rel)) != len(rel): return False
    if CYCLE and abs(rel[0][0] - rel[-1][0]) + abs(rel[0][1] - rel[-1][1]) != 1: return False
    mx = min(c[0] for c in rel); my = min(c[1] for c in rel)
    for ox in range(-mx, w - max(c[0] for c in rel)):
        for oy in range(-my, h - max(c[1] for c in rel)):
            if all((x + ox, y + oy) in free for x, y in rel): return True  # distinct + same size => covers all
    return False

bad = 0
for f in sorted(d.glob("in_level-5""_*.txt")):
    o = d / f.name.replace("in_", "").replace(".txt", ".out")
    L = list(lawns(f.read_text())); lines = o.read_text().split("\n")
    assert lines[-1] == "" and len(lines) == len(L) + 1, f.name
    res = [ok(w, h, g, p) for (w, h, g), p in zip(L, lines)]
    print(f.name, "OK" if all(res) else f"FAIL {res.count(False)}/{len(res)}")
    bad += not all(res)
sys.exit(bad)
