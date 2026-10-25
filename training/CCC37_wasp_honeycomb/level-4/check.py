"""Independent check: union-find over O/W cells + a virtual 'outside' node."""
from pathlib import Path

d = Path(__file__).parent
NB = [(0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def expected(g):
    m = {(r, c): ch for r, row in enumerate(g) for c, ch in enumerate(row) if (r + c) % 2 == 0}
    par = {k: k for k, v in m.items() if v in "OW"}
    par["OUT"] = "OUT"

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for (r, c) in [k for k in par if k != "OUT"]:
        for a, b in NB:
            q = (r + a, c + b)
            if q not in m:
                par[find((r, c))] = find("OUT")
            elif q in par:
                par[find((r, c))] = find(q)
    w = next(k for k, v in m.items() if v == "W")
    return "FREE" if find(w) == find("OUT") else "TRAPPED"


def blocks(t):
    return [b.split("\n") for b in t.split("\n", 1)[1].strip().split("\n\n")]


bad = 0
for f in sorted(d.glob("in_level-4_*.txt")):
    exp = [expected(g) for g in blocks(f.read_text())]
    got = (d / f.name.replace("in_", "", 1).replace(".txt", ".out")).read_text().split()
    ok = exp == got
    bad += not ok
    print(f.name, "OK" if ok else "FAIL")
raise SystemExit(bad)
