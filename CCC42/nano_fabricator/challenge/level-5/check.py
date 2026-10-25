"""Independent check: axial hex coordinates, neighbours via the 6 axial directions."""
from pathlib import Path
import sys

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from solution import solve  # noqa: E402

AX = {1: (1, 0), 2: (0, 1), 3: (-1, 1), 4: (-1, 0), 5: (0, -1), 6: (1, -1)}


def to_axial(R, i, j):
    r = i - R
    return ((j - 2 * R - r) // 2, r)


def count(R, pat_rows, prog):
    pat = {to_axial(R, i, j) for i, row in enumerate(pat_rows) for j, ch in enumerate(row) if ch == "M"}
    ring = [(-R, 0)]
    for step in [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]:
        for _ in range(R):
            ring.append((ring[-1][0] + step[0], ring[-1][1] + step[1]))
    ring.pop()
    inside = lambda q, r: max(abs(q), abs(r), abs(q + r)) < R
    pos = [k * R for k in range(6)]; act = [False] * 6; m = set(); res = 0
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
        if pat <= m:
            near = {(q + dq, r + dr) for q, r in pat for dq, dr in AX.values()}
            if not ((m - pat) & near):
                m -= pat; res += 1
    return res


def check(inp, out):
    t = inp.split(); n = int(t[0]); p = 1; got = out.split()
    assert len(got) == n
    for g in got:
        R, rows = int(t[p]), int(t[p + 1]); pat = t[p + 3:p + 3 + rows]; p += 3 + rows
        L = int(t[p]); p += 1
        prog = [t[p + 6 * i:p + 6 * i + 6] for i in range(L)]; p += 6 * L
        assert int(g) == count(R, pat, prog)


for f in sorted(HERE.glob("in_level-5_*.txt")):
    check(f.read_text(), solve(f.read_text())); print("OK", f.name)
