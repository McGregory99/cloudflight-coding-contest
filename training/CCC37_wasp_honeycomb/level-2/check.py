"""Independent check: dict-of-cells geometry (cells exist only where row+col is even)."""
from pathlib import Path

d = Path(__file__).parent
NB = [(0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def cells(g):
    return {(r, c): ch for r, row in enumerate(g) for c, ch in enumerate(row) if (r + c) % 2 == 0}


def expected(g):
    m = cells(g)
    (r, c), = [k for k, v in m.items() if v == "W"]
    return sum(m.get((r + a, c + b)) == "O" for a, b in NB)


def blocks(t):
    return [b.split("\n") for b in t.split("\n", 1)[1].strip().split("\n\n")]


bad = 0
for f in sorted(d.glob("in_level-2_*.txt")):
    exp = [str(expected(g)) for g in blocks(f.read_text())]
    got = (d / f.name.replace("in_", "", 1).replace(".txt", ".out")).read_text().split()
    ok = exp == got
    bad += not ok
    print(f.name, "OK" if ok else "FAIL")
raise SystemExit(bad)
