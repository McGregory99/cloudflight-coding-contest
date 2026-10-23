"""Independent check: cube-coordinate ray vs. solution output, on every input."""
from pathlib import Path
import sys

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
from solution import solve  # noqa: E402

# step in (col, row) char units per direction, validated via axial coords
STEP = {1: (2, 0), 2: (1, 1), 3: (-1, 1), 4: (-2, 0), 5: (-1, -1), 6: (1, -1)}


def parse(text):
    t = text.split(); n = int(t[0]); p = 1; boards = []
    for _ in range(n):
        rows = int(t[p + 1]); boards.append(t[p + 3:p + 3 + rows]); p += 3 + rows
    return boards


def check(inp, out):
    ins = parse(inp)
    outs = [b.split("\n") for b in out.strip("\n").split("\n\n")]
    assert len(ins) == len(outs)
    for a, b in zip(ins, outs):
        assert len(a) == len(b)
        pos = [(x, y, int(ch)) for y, row in enumerate(a) for x, ch in enumerate(row) if ch in "123456"]
        assert len(pos) == 1
        x, y, d = pos[0]
        exp = set()
        while True:
            x += STEP[d][0]; y += STEP[d][1]
            if not (0 <= y < len(a) and 0 <= x < len(a[y])) or a[y][x] != "O":
                break
            exp.add((x, y))
        got = {(x, y) for y, row in enumerate(b) for x, ch in enumerate(row) if ch == "M"}
        assert exp == got
        for ya, yb in zip(a, b):
            assert len(ya) == len(yb) and all(p == q or (p == "O" and q == "M") for p, q in zip(ya, yb))


for f in sorted(HERE.glob("in_level-2_*.txt")):
    check(f.read_text(), solve(f.read_text())); print("OK", f.name)
