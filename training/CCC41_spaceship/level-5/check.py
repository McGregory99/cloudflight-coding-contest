"""Independent validator for levels 4-8 (a port of the rules in the official sandbox/visualizer).
Usage: python3 check.py  -> validates every level-N_<suffix>.out against in_level-N_<suffix>.txt
"""
import re
import sys
from pathlib import Path

D = Path(__file__).parent
LEVEL = int(D.name.split("-")[1])
PACE_RE = re.compile(r"^-?\d+( -?\d+)*$")


def valid_next(p):
    if p == 0:
        return {-5, 0, 5}
    s = 1 if p > 0 else -1
    a = abs(p)
    r = {s * b for b in (a - 1, a, a + 1) if 1 <= b <= 5}
    if a == 5:
        r.add(0)
    return r


def parse_input(path):
    toks = path.read_text().split()
    n, i, cases = int(toks[0]), 1, []
    for _ in range(n):
        g, t = toks[i], int(toks[i + 1])
        i += 2
        gx, gy = map(int, g.split(","))
        if LEVEL <= 4:
            na = 0
        elif LEVEL <= 6:
            na = 1
        else:
            na = int(toks[i])
            i += 1
        ast = []
        for _ in range(na):
            v = list(map(int, toks[i].split(",")))
            i += 1
            ast.append(v if len(v) == 4 else v + [0, 0])
        cases.append((gx, gy, t, ast))
    return cases


def ticks_of(paces):
    """Expanded per-tick pace list."""
    return [p for p in paces for _ in range(max(1, abs(p)))]


def positions(paces, total):
    """Ship coordinate after every step 0..total (counter logic of the sandbox's Entity.move)."""
    exp = ticks_of(paces)
    exp += [0] * (total - len(exp))
    pos, cnt, res, v_last = 0, 0, [0], 0
    for v in exp:
        if v != 0:
            cnt += 1
            if cnt >= abs(v):
                cnt = 0
                pos += 1 if v > 0 else -1
        res.append(pos)
        v_last = v
    return res, v_last


def check_case(gx, gy, limit, ast, lx, ly):
    for line in (lx, ly):
        if not PACE_RE.match(line):
            return "bad pace format"
    px, py = list(map(int, lx.split())), list(map(int, ly.split()))
    for ps in (px, py):
        if ps[0] != 0 or ps[-1] != 0:
            return "first/last pace must be 0"
        for a, b in zip(ps, ps[1:]):
            if b not in valid_next(a):
                return f"illegal progression {a} {b}"
        if any(p and not 1 <= abs(p) <= 5 for p in ps):
            return "pace out of range"
    total = max(sum(max(1, abs(p)) for p in px), sum(max(1, abs(p)) for p in py))
    if total > limit:
        return f"too slow {total} > {limit}"
    X, vx = positions(px, total)
    Y, vy = positions(py, total)
    if (X[-1], Y[-1]) != (gx, gy):
        return f"ends at {(X[-1], Y[-1])}, goal {(gx, gy)}"
    if vx != 0 or vy != 0:
        return "not stopped"
    static = all(a[2] == 0 and a[3] == 0 for a in ast)
    if static:
        centers = {(a[0], a[1]) for a in ast}
    for i in range(total + 1):
        if not static:
            centers = set()
            for ax, ay, avx, avy in ast:
                centers.add((ax + (0 if avx == 0 else (1 if avx > 0 else -1) * (i // abs(avx))),
                             ay + (0 if avy == 0 else (1 if avy > 0 else -1) * (i // abs(avy)))))
        sx, sy = X[i], Y[i]
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if (sx + dx, sy + dy) in centers:
                    return f"collision at step {i}"
    return None


bad = 0
for inp in sorted(D.glob(f"in_level-{LEVEL}_*.txt")):
    out = D / inp.name.replace("in_", "").replace(".txt", ".out")
    cases = parse_input(inp)
    lines = [re.sub(r"\s+", " ", l).strip() for l in out.read_text().split("\n")]
    lines = [l for l in lines if l]
    errs = []
    if len(lines) != 2 * len(cases):
        errs.append(f"expected {2 * len(cases)} lines, got {len(lines)}")
    else:
        for k, (gx, gy, t, ast) in enumerate(cases):
            e = check_case(gx, gy, t, ast, lines[2 * k], lines[2 * k + 1])
            if e:
                errs.append(f"case {k}: {e}")
    print(inp.name, "OK" if not errs else f"FAIL ({len(errs)}): {errs[:3]}")
    bad += bool(errs)
sys.exit(bad)
