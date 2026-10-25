"""Validates every rule on every input: format, only O->X changes, <= barrierCount added, wasp trapped.
Trapped test uses union-find (different from the solver's flow/BFS)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from solution import parse  # input parser only

d = Path(__file__).parent
NB = [(0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def trapped(g):
    m = {(r, c): ch for r, row in enumerate(g) for c, ch in enumerate(row) if (r + c) % 2 == 0}
    par = {k: k for k, v in m.items() if v in "OW"}
    par["OUT"] = "OUT"

    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x

    for k in [k for k in par if k != "OUT"]:
        for a, b in NB:
            q = (k[0] + a, k[1] + b)
            if q not in m:
                par[find(k)] = find("OUT")
            elif q in par:
                par[find(k)] = find(q)
    w = next(k for k, v in m.items() if v == "W")
    return find(w) != find("OUT")


bad = 0
for f in sorted(d.glob("in_level-5_*.txt")):
    items = parse(f.read_text())
    out = (d / f.name.replace("in_", "", 1).replace(".txt", ".out")).read_text()
    blocks = out.strip("\n").split("\n\n")
    errs = []
    if int(blocks[0]) != len(items) or len(blocks) != len(items) + 1:
        errs.append("count/format")
    else:
        for i, ((b, g), ob) in enumerate(zip(items, blocks[1:])):
            og = ob.split("\n")
            if len(og) != len(g) or any(len(x) != len(y) for x, y in zip(g, og)):
                errs.append(f"#{i} shape"); continue
            added = 0
            for x, y in zip("".join(g), "".join(og)):
                if x != y:
                    if (x, y) != ("O", "X"):
                        errs.append(f"#{i} illegal change {x}->{y}")
                    added += 1
            if added > b:
                errs.append(f"#{i} used {added} > {b}")
            if not trapped(og):
                errs.append(f"#{i} not trapped")
    bad += bool(errs)
    print(f.name, "OK" if not errs else f"FAIL {errs[:3]}")
raise SystemExit(bad)
