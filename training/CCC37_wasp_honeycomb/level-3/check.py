"""Independent check: dict-of-cells geometry; ray walked as a list of positions."""
from pathlib import Path

d = Path(__file__).parent
NB = [(0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def cells(g):
    return {(r, c): ch for r, row in enumerate(g) for c, ch in enumerate(row) if (r + c) % 2 == 0}


def expected(g):
    m = cells(g)
    (w,), = [[k for k, v in m.items() if v == "W"]]
    for a, b in NB:
        ray = []
        for k in range(1, 200):
            p = (w[0] + a * k, w[1] + b * k)
            if p not in m:
                break
            ray.append(m[p])
        else:
            raise AssertionError
        if all(x == "O" for x in ray):
            return "FREE"
    return "TRAPPED"


def blocks(t):
    return [b.split("\n") for b in t.split("\n", 1)[1].strip().split("\n\n")]


bad = 0
for f in sorted(d.glob("in_level-3_*.txt")):
    exp = [expected(g) for g in blocks(f.read_text())]
    got = (d / f.name.replace("in_", "", 1).replace(".txt", ".out")).read_text().split()
    ok = exp == got
    bad += not ok
    print(f.name, "OK" if ok else "FAIL")
raise SystemExit(bad)
