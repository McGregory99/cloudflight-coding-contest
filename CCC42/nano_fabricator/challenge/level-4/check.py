"""Independent check: axial/cube hex coordinates instead of character-grid arithmetic."""
from pathlib import Path
import sys

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from solution import solve  # noqa: E402

AX = {1: (1, 0), 2: (0, 1), 3: (-1, 1), 4: (-1, 0), 5: (0, -1), 6: (1, -1)}


def sim(R, prog):
    ring = [(-R, 0)]
    for step in [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]:
        for _ in range(R):
            q, r = ring[-1]; ring.append((q + step[0], r + step[1]))
    assert ring.pop() == (-R, 0) and len(ring) == 6 * R
    inside = lambda q, r: max(abs(q), abs(r), abs(q + r)) < R
    pos = [k * R for k in range(6)]; act = [False] * 6; m = set()
    for line in prog:
        for k, c in enumerate(line):
            pos[k] = (pos[k] + (c == "F") - (c == "B")) % len(ring)
            act[k] ^= (c == "T")
        cnt = {}
        for k in range(6):
            if act[k]:
                q, r = ring[pos[k]]
                while True:
                    q += AX[k + 1][0]; r += AX[k + 1][1]
                    if not inside(q, r): break
                    cnt[(q, r)] = cnt.get((q, r), 0) + 1
        for c, h in cnt.items():
            if h == 2: m.add(c)
            elif h >= 3: m.discard(c)
    return m


def render_matters(R, text_board):
    got = set()
    for i, row in enumerate(text_board):
        for j, ch in enumerate(row):
            if ch == "M":
                r = i - R; q = (j - R * 2 - r) // 2
                assert 2 * q + r + 2 * R == j
                got.add((q, r))
    return got


def check(inp, out):
    t = inp.split(); n = int(t[0]); p = 1
    outs = [b.split("\n") for b in out.strip("\n").split("\n\n")]
    assert len(outs) == n
    for b in outs:
        R = int(t[p]); L = int(t[p + 1]); p += 2
        prog = [t[p + 6 * i:p + 6 * i + 6] for i in range(L)]; p += 6 * L
        assert render_matters(R, b) == sim(R, prog)


for f in sorted(HERE.glob("in_level-4_*.txt")):
    check(f.read_text(), solve(f.read_text())); print("OK", f.name)
