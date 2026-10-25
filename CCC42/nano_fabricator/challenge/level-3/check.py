"""Independent check: per-cell approach (for each cell, count emitters whose ray reaches it)."""
from pathlib import Path
import sys

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from solution import solve  # noqa: E402

STEP = {1: (2, 0), 2: (1, 1), 3: (-1, 1), 4: (-2, 0), 5: (-1, -1), 6: (1, -1)}


def parse(text):
    t = text.split(); n = int(t[0]); p = 1; boards = []
    for _ in range(n):
        rows = int(t[p + 1]); boards.append(t[p + 3:p + 3 + rows]); p += 3 + rows
    return boards


def reaches(a, ex, ey, d, x, y):
    """walk from emitter toward (x, y); True if the ray gets there over O/M cells."""
    dx, dy = STEP[d]
    cx, cy = ex + dx, ey + dy
    while 0 <= cy < len(a) and 0 <= cx < len(a[cy]) and a[cy][cx] in "OM":
        if (cx, cy) == (x, y):
            return True
        cx += dx; cy += dy
    return False


def check(inp, out):
    ins = parse(inp)
    outs = [b.split("\n") for b in out.strip("\n").split("\n\n")]
    assert len(ins) == len(outs)
    for a, b in zip(ins, outs):
        ems = [(x, y, int(ch)) for y, row in enumerate(a) for x, ch in enumerate(row) if ch in "123456"]
        for y, row in enumerate(a):
            for x, ch in enumerate(row):
                if ch in "OM":
                    k = sum(reaches(a, ex, ey, d, x, y) for ex, ey, d in ems)
                    exp = "M" if k == 2 else "O" if k >= 3 else ch
                    assert b[y][x] == exp, (x, y)
                else:
                    assert b[y][x] == ch


for f in sorted(HERE.glob("in_level-3_*.txt")):
    check(f.read_text(), solve(f.read_text())); print("OK", f.name)
