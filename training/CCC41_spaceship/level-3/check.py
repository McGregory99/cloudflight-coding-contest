"""Independent validator for level 3 (1D): paces legal, ends at the station, within the time limit."""
import sys
from pathlib import Path

D = Path(__file__).parent


def valid_next(p):
    if p == 0:
        return {-5, 0, 5}
    s = 1 if p > 0 else -1
    a = abs(p)
    r = {s * b for b in (a - 1, a, a + 1) if 1 <= b <= 5}
    if a == 5:
        r.add(0)
    return r


bad = 0
for inp in sorted(D.glob("in_level-3_*.txt")):
    out = D / inp.name.replace("in_", "").replace(".txt", ".out")
    cases = [tuple(map(int, l.split())) for l in inp.read_text().split("\n")[1:] if l.strip()]
    seqs = [l.split() for l in out.read_text().split("\n") if l.strip()]
    ok = len(cases) == len(seqs)
    for (pos, limit), s in zip(cases, seqs):
        p = list(map(int, s))
        ok &= p[0] == 0 and p[-1] == 0
        ok &= all(b in valid_next(a) for a, b in zip(p, p[1:]))
        # position = number of non-zero blocks with sign; time = sum max(1,|p|)
        ok &= sum((q > 0) - (q < 0) for q in p) == pos
        ok &= sum(max(1, abs(q)) for q in p) <= limit
    print(inp.name, "OK" if ok else "FAIL")
    bad += not ok
sys.exit(bad)
