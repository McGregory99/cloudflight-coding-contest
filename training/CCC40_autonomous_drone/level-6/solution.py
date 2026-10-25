from pathlib import Path

HERE = Path(__file__).parent
G = 10      # gravity
A = 10      # max change of a velocity component per tick when hovering (ay = 10 + dvy)


def smin(u):
    """Minimal remaining sum when braking from speed u down to 0 in steps of A."""
    k = (u - 1) // A
    return k * u - A * k * (k + 1) // 2


def rt(S):
    """Rest-to-rest speed profile: speeds s_1..s_n >= 0 (s_0 = 0, |ds| <= A, sum = S), a final 0 is implied.
    Greedy: at each tick take the largest speed that still leaves a feasible braking tail."""
    out = []
    u, R = 0, S
    while not (R == 0 and u <= A):
        lo, hi = max(0, u - A), min(u + A, R)
        a, b = lo, hi
        while a < b:                       # R-u'-smin(u') is decreasing in u'
            mid = (a + b + 1) // 2
            if R - mid >= smin(mid):
                a = mid
            else:
                b = mid - 1
        out.append(a)
        u, R = a, R - a
    return out


def ascent(H):
    """ay list: from ground to apex height exactly H (>=1) with vy = 0 at the apex."""
    seq = [0] + rt(H) + [0]
    return [G + seq[i + 1] - seq[i] for i in range(len(seq) - 1)]


def descent(R):
    """ay list: from hover (vy=0) descend R (>=1) and land with vy = -1."""
    seq = [0] + [-s for s in rt(R - 1)] + [-1]
    return [G + seq[i + 1] - seq[i] for i in range(len(seq) - 1)]


def horizontal(D):
    """(ax, ay) list: move D (signed) at hover (ay=10) from rest to rest."""
    if D == 0:
        return []
    sg = 1 if D > 0 else -1
    seq = [0] + rt(abs(D)) + [0]
    return [(sg * (seq[i + 1] - seq[i]), G) for i in range(len(seq) - 1)]


def fmt(accs):
    return " ".join(f"{ax},{ay}" for ax, ay in accs)

from bisect import bisect_left


def parse(text):
    t = text.split()
    n, p = int(t[0]), 1
    for _ in range(n):
        px, py, lim = int(t[p]), int(t[p + 1]), int(t[p + 2]); p += 3
        b = int(t[p]); p += 1
        bs = [tuple(map(int, t[p + 3 * j: p + 3 * j + 3])) for j in range(b)]; p += 3 * b
        s = int(t[p]); p += 1
        zs = [tuple(map(int, t[p + 2 * j: p + 2 * j + 2])) for j in range(s)]; p += 2 * s
        yield px, py, lim, bs, zs


# ---------------------------------------------------------------- baseline (no silent zone on the way)
def baseline(X, Y, buildings):
    lo, hi = min(0, X), max(0, X)
    H = max([h for l, r, h in buildings if r >= lo and l <= hi] + [Y, 0]) + 1
    return [(0, ay) for ay in ascent(H)] + horizontal(X) + [(0, ay) for ay in descent(H - Y)]


# ---------------------------------------------------------------- horizontal schedule with silent zones (X > 0)
def ramp_up(V):
    s, v = [], 0
    while v < V:
        v = min(v + A, V); s.append(v)
    return s


def ramp_down(V):
    s, v = [], V
    while v > 0:
        v = max(v - A, 0); s.append(v)
    return s


def horizontal_candidates(X, zones):
    """Cruise at constant speed V (zones are crossed without acceleration), brake after the last zone,
    stop at P (maybe overshooting the pad inside the free window) and finish with a rest-to-rest correction."""
    mid = [z for z in zones if z[1] >= 0 and z[0] < X]
    zl1 = min(l for l, r in mid)
    zr = max(r for l, r in mid)
    beyond = min([l for l, r in zones if l > X] + [10 ** 18])
    cands = []
    vmax = int((10 * X) ** 0.5) + 30
    for V in range(vmax, 9, -1):
        up, dn = ramp_up(V), ramp_down(V)
        Ru, Rd = sum(up), sum(dn)
        if Ru >= zl1 or Ru + Rd > X + V:
            continue
        cmin = 0 if Ru > zr else (zr - Ru) // V + 1
        c = max(cmin, round((X - Ru - Rd) / V))
        while c > cmin and Ru + c * V + Rd >= beyond:
            c -= 1
        P = Ru + c * V + Rd
        if Ru + c * V <= zr or P >= beyond:
            continue
        D = X - P
        t2 = 0 if D == 0 else len(rt(abs(D))) + 1
        cands.append((len(up) + c + len(dn) + t2, V, c))
    cands.sort()
    return cands


def speeds_for(X, V, c):
    up, dn = ramp_up(V), ramp_down(V)
    P = sum(up) + c * V + sum(dn)
    sp = up + [V] * c + dn
    D = X - P
    if D:
        sg = 1 if D > 0 else -1
        sp += [sg * s for s in rt(abs(D)) + [0]]
    return sp


# ---------------------------------------------------------------- vertical planning: convex piecewise-linear viability DP
def prune(pts):
    out = []
    for p in pts:
        if out and abs(p[0] - out[-1][0]) < 1e-9:
            out[-1] = (out[-1][0], min(out[-1][1], p[1]))
            continue
        while len(out) >= 2:
            (x0, y0), (x1, y1) = out[-2], out[-1]
            if abs((x1 - x0) * (p[1] - y1) - (p[0] - x1) * (y1 - y0)) <= 1e-7:
                out.pop()
            else:
                break
        out.append(p)
    return out


def step(pts, dmin, dmax):
    """f(v) = min over d in [dmin,dmax] of (L(v+d) - (v+d)); L convex piecewise linear."""
    g = [(v, L - v) for v, L in pts]
    m = min(range(len(g)), key=lambda i: g[i][1])
    return [(v - dmax, val) for v, val in g[:m + 1]] + [(v - dmin, val) for v, val in g[m:]]


def clip(pts, req):
    out = []
    for i, (v, val) in enumerate(pts):
        if i:
            pv, pval = pts[i - 1]
            if (pval < req) != (val < req) and pval != req and val != req:
                out.append((pv + (req - pval) / (val - pval) * (v - pv), req))
        out.append((v, max(val, req)))
    return prune(out)


def evaluate(pts, v):
    if v < pts[0][0] - 1e-9 or v > pts[-1][0] + 1e-9:
        return None
    xs = [p[0] for p in pts]
    i = bisect_left(xs, v)
    if i == 0:
        return pts[0][1]
    if i >= len(pts):
        return pts[-1][1]
    (x0, y0), (x1, y1) = pts[i - 1], pts[i]
    return y0 + (y1 - y0) * (v - x0) / (x1 - x0) if x1 != x0 else y0


def vertical_plan(vx, buildings, zones, Yp, margin, max_idle=400):
    """vx: horizontal speed per tick (after `a` idle ticks).  Returns (vy per tick incl. idle ticks, final y) or None."""
    T = len(vx)
    xs = [0]
    for v in vx:
        xs.append(xs[-1] + v)
    seg = [None] + [(min(xs[t - 1], xs[t]), max(xs[t - 1], xs[t])) for t in range(1, T + 1)]
    ax = [0] + [vx[0]] + [vx[t] - vx[t - 1] for t in range(1, T)]
    dmin, dmax = [0] * (T + 1), [0] * (T + 1)
    for t in range(1, T + 1):
        lo, hi = seg[t]
        if any(lo <= zr and hi >= zl for zl, zr in zones):          # conservative: touching a zone => no thrust at all
            if ax[t] != 0:
                return None
            dmin[t] = dmax[t] = -G
        else:
            dmin[t], dmax[t] = -G, G - abs(ax[t])
    req = []
    for t in range(T + 1):
        lo = min(xs[t], xs[t + 1] if t < T else xs[t], xs[t - 1] if t else xs[t])
        hi = max(xs[t], xs[t + 1] if t < T else xs[t], xs[t - 1] if t else xs[t])
        h = max([bh for bl, br, bh in buildings if bl <= hi and br >= lo] + [0])
        req.append(max(h + 1, 1) + margin)
    req[T] = max(req[T], Yp + 1 + margin)
    arr = [None] * (T + 1)
    arr[T] = [(0.0, float(req[T]))]
    for t in range(T - 1, -1, -1):
        arr[t] = clip(step(arr[t + 1], dmin[t + 1], dmax[t + 1]), req[t])
    idle = [arr[0]]
    a = 0
    while True:
        pre = step(idle[-1], -G, G)
        val = evaluate(pre, 0)
        if val is not None and val <= 1e-9:
            a = len(idle)
            break
        if len(idle) > max_idle:
            return None
        idle.append(clip(pre, 1 + margin))
    # forward reconstruction (integers), always the lowest altitude that keeps the future viable
    seq_arrs = [idle[a - 1 - i] for i in range(a)] + arr[1:]
    seq_dmin = [-G] * a + dmin[1:]
    seq_dmax = [G] * a + dmax[1:]
    y = vy = 0
    vys = []
    for L, lo_d, hi_d in zip(seq_arrs, seq_dmin, seq_dmax):
        for nv in range(vy + lo_d, vy + hi_d + 1):
            e = evaluate(L, nv)
            if e is not None and y + nv >= e - 1e-9:
                break
        else:
            return None
        vy = nv
        y += vy
        vys.append(vy)
    if vy != 0:
        return None
    return vys, y, a


def zone_flight(X, Y, limit, buildings, zones):
    """X > 0.  Returns accs list or None."""
    best = None
    for cost, V, c in horizontal_candidates(X, zones)[:6]:
        sp = speeds_for(X, V, c)
        for margin in (3, 40, 400):
            res = vertical_plan(sp, buildings, zones, Y, margin)
            if res:
                break
        else:
            continue
        vys, yT, a = res
        T = len(sp)
        accs = []
        pv = 0
        for i in range(a):
            accs.append((0, G + vys[i] - pv)); pv = vys[i]
        pvx = 0
        for i in range(T):
            accs.append((sp[i] - pvx, G + vys[a + i] - pv)); pv = vys[a + i]; pvx = sp[i]
        accs += [(0, ay) for ay in descent(yT - Y)]
        if best is None or len(accs) < len(best):
            best = accs
        if len(best) <= limit:
            break
    return best


def solve(X, Y, limit, buildings, zones):
    lo, hi = min(0, X), max(0, X)
    if X == 0 or not any(r >= lo and l <= hi for l, r in zones):
        accs = baseline(X, Y, buildings)
    else:
        sg = 1 if X > 0 else -1
        if sg > 0:
            bs, zs = buildings, zones
        else:
            bs = [(-r, -l, h) for l, r, h in buildings]
            zs = [(-r, -l) for l, r in zones]
        accs = zone_flight(abs(X), Y, limit, bs, zs)
        if accs is None:
            raise RuntimeError(f"no plan for X={X} Y={Y} limit={limit}")
        accs = [(sg * ax, ay) for ax, ay in accs]
    if len(accs) > limit:
        print(f"WARNING: {len(accs)} ticks > limit {limit} (X={X})")
    return accs


def main():
    for f in sorted(HERE.glob("in_level-6_*.txt")):
        out = [fmt(solve(*case)) for case in parse(f.read_text())]
        (HERE / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out) + "\n")


main()
