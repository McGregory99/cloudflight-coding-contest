# ---- shared core: per-axis pace automaton + exact free-space distance table ----
from collections import deque

# Axis state after a tick = (pace p of the current block, rem = ticks still to run in the block).
# rem == 0 means a block boundary: the next pace must be one of valid(p).
# A block of pace p lasts max(1,|p|) ticks and moves the ship sign(p) cells on its LAST tick.
STATES = []
IDX = {}
for _p in range(-5, 6):
    for _r in range(max(1, abs(_p))):
        IDX[(_p, _r)] = len(STATES)
        STATES.append((_p, _r))
S0 = IDX[(0, 0)]


def sgn(v):
    return (v > 0) - (v < 0)


def valid(p):
    """Paces that may follow pace p (gradual speed changes, direction change only through 0)."""
    if p == 0:
        return (-5, 0, 5)
    s, a = sgn(p), abs(p)
    nxt = [s * b for b in (a + 1, a, a - 1) if 1 <= b <= 5]
    if a == 5:
        nxt.append(0)
    return tuple(nxt)


def _next(p, r):
    """[(new state index, dpos)] for one tick from state (p, r)."""
    if r > 0:
        return [(IDX[(p, r - 1)], sgn(p) if r - 1 == 0 else 0)]
    out = []
    for q in valid(p):
        b = max(1, abs(q))
        out.append((IDX[(q, b - 1)], sgn(q) if b == 1 else 0))
    return out


NXT = [_next(p, r) for (p, r) in STATES]


def build_H(R):
    """H[s][d+R] = min ticks to finish (reach d == 0 resting with pace 0) from state s with d cells to go."""
    W = 2 * R + 1
    n = len(STATES)
    rev = [[] for _ in range(n * W)]
    for s in range(n):
        for d in range(-R, R + 1):
            u = s * W + d + R
            for s2, dp in NXT[s]:
                d2 = d - dp
                if -R <= d2 <= R:
                    rev[s2 * W + d2 + R].append(u)
    INF = 10 ** 9
    dist = [INF] * (n * W)
    start = S0 * W + R
    dist[start] = 0
    dq = deque([start])
    while dq:
        v = dq.popleft()
        for u in rev[v]:
            if dist[u] == INF:
                dist[u] = dist[v] + 1
                dq.append(u)
    return [dist[s * W:(s + 1) * W] for s in range(n)]


def axis_blocks(states):
    """Tick-level axis states (one per tick, starting with the forced first 0 tick) -> list of paces."""
    paces = [0]
    for prev, cur in zip(states, states[1:]):
        if STATES[prev][1] == 0:
            paces.append(STATES[cur][0])
    return paces


def greedy_axis(goal, H, R):
    """Time-optimal 1D pace sequence (leading and trailing 0) as per-tick states."""
    s, d = S0, goal
    sts = [S0]
    while H[s][d + R] > 0:
        for s2, dp in NXT[s]:
            if H[s2][d - dp + R] == H[s][d + R] - 1:
                s, d = s2, d - dp
                sts.append(s)
                break
    return sts

# ---- joint 2D search (levels 5-8) ----
import heapq


def solve_case(gx, gy, T, asts, H, R, margin, w):
    """Best-first search over (time, x, y, state_x, state_y). Returns (xs, ys) pace lists or None.
    Pruned with the exact free-space lower bound: g + h > T can never finish in time, so the
    search is complete inside the window whatever the weight w is (w only steers the order)."""
    xlo, xhi = min(0, gx) - margin, max(0, gx) + margin
    ylo, yhi = min(0, gy) - margin, max(0, gy) + margin
    moving = any(a[2] or a[3] for a in asts)

    def rel_static(a):
        return xlo - 2 <= a[0] <= xhi + 2 and ylo - 2 <= a[1] <= yhi + 2

    def rel_moving(a):  # trajectory over [0, T] is a segment: test its bounding box against the window
        ex = a[0] + sgn(a[2]) * (T // abs(a[2])) if a[2] else a[0]
        ey = a[1] + sgn(a[3]) * (T // abs(a[3])) if a[3] else a[1]
        return (max(a[0], ex) >= xlo - 2 and min(a[0], ex) <= xhi + 2 and
                max(a[1], ey) >= ylo - 2 and min(a[1], ey) <= yhi + 2)

    rel = [a for a in asts if (rel_moving(a) if moving else rel_static(a))]
    cache = {}

    def rows_at(t):
        r = cache.get(t)
        if r is None:
            r = {}
            for ax, ay, vx, vy in rel:
                if vx:
                    ax += sgn(vx) * (t // abs(vx))
                if vy:
                    ay += sgn(vy) * (t // abs(vy))
                if ax < xlo - 2 or ax > xhi + 2:
                    continue
                m = 31 << (ax - xlo + 2)
                for yy in range(ay - 2, ay + 3):
                    r[yy] = r.get(yy, 0) | m
            cache[t] = r
        return r

    static_rows = None if moving else rows_at(0)

    def blocked(t, x, y):
        rows = static_rows if static_rows is not None else rows_at(t)
        return (rows.get(y, 0) >> (x - xlo + 4)) & 1

    if blocked(0, 0, 0) or blocked(1, 0, 0):
        return None
    GD = None
    if not moving:
        # king-move BFS distance to the goal over free cells: a ship moves <= 1 cell per axis per tick,
        # so it lower-bounds the remaining ticks (cells never reached get the last BFS level: still a bound)
        Wd = xhi - xlo + 1
        INFD = 1 << 20
        GD = [INFD] * (Wd * (yhi - ylo + 1))
        if not blocked(0, gx, gy):
            q = [(gx - xlo) + (gy - ylo) * Wd]
            GD[q[0]] = 0
            d = 0
            Hh = yhi - ylo + 1
            seen_start = False
            while q:
                d += 1
                nq = []
                for c in q:
                    cy, cx = divmod(c, Wd)
                    for yy in (cy - 1, cy, cy + 1):
                        if 0 <= yy < Hh:
                            rowm = static_rows.get(yy + ylo, 0)
                            base = yy * Wd
                            for xx in (cx - 1, cx, cx + 1):
                                if 0 <= xx < Wd and GD[base + xx] == INFD and not (rowm >> (xx + 4)) & 1:
                                    GD[base + xx] = d
                                    nq.append(base + xx)
                q = nq
                if GD[(0 - xlo) + (0 - ylo) * Wd] != INFD:
                    if seen_start:
                        break
                    seen_start = True
            LAST = d
            INF_FILL = LAST
            for i in range(len(GD)):
                if GD[i] == INFD:
                    GD[i] = INF_FILL
    h0 = max(H[S0][gx + R], H[S0][gy + R])
    if GD is not None:
        h0 = max(h0, GD[(0 - xlo) + (0 - ylo) * Wd])
    if 1 + h0 > T:
        return None
    start = (0, 0, S0, S0)
    best = {(start if not moving else (1,) + start): 1}
    parent = {}
    heap = [(1 + w * h0, -1, 0, 0, S0, S0)]
    nxt = NXT
    while heap:
        f, ng, x, y, sx, sy = heapq.heappop(heap)
        g = -ng
        key = (x, y, sx, sy) if not moving else (g, x, y, sx, sy)
        if best.get(key, 1 << 30) < g and not moving:
            continue
        g1 = g + 1
        for sx2, dx in nxt[sx]:
            x2 = x + dx
            if x2 < xlo or x2 > xhi:
                continue
            hx = H[sx2][gx - x2 + R]
            if g1 + hx > T:
                continue
            for sy2, dy in nxt[sy]:
                y2 = y + dy
                if y2 < ylo or y2 > yhi:
                    continue
                hy = H[sy2][gy - y2 + R]
                h = hx if hx > hy else hy
                if g1 + h > T:
                    continue
                if blocked(g1, x2, y2):
                    continue
                if GD is not None:
                    hg = GD[(x2 - xlo) + (y2 - ylo) * Wd]
                    if g1 + hg > T:
                        continue
                    if hg > h:
                        h = hg
                k2 = (x2, y2, sx2, sy2) if not moving else (g1, x2, y2, sx2, sy2)
                if moving:
                    if k2 in best:
                        continue
                    best[k2] = g1
                else:
                    if best.get(k2, 1 << 30) <= g1:
                        continue
                    best[k2] = g1
                parent[k2] = key
                if x2 == gx and y2 == gy and sx2 == S0 and sy2 == S0:
                    # reached the goal at rest
                    path = [k2]
                    while path[-1] in parent:
                        path.append(parent[path[-1]])
                    path.reverse()
                    # first element = start key (tick 1)
                    off = 1 if moving else 0
                    xs = [p[off + 2] for p in path]
                    ys = [p[off + 3] for p in path]
                    return axis_blocks(xs), axis_blocks(ys)
                heapq.heappush(heap, (g1 + w * h, -g1, x2, y2, sx2, sy2))
    return None

# ---- driver: levels 5, 6, 8 (pure Python) ----
from pathlib import Path

D = Path(__file__).parent
LEVEL = int(D.name.split("-")[1])
LADDER = ((20, 2.0), (60, 2.0), (150, 1.5), (400, 1.2))  # (window margin, A* weight)


def parse(path):
    toks = path.read_text().split()
    n, i, cases = int(toks[0]), 1, []
    for _ in range(n):
        gx, gy = map(int, toks[i].split(","))
        T = int(toks[i + 1])
        i += 2
        if LEVEL <= 6:
            na = 1
        else:
            na = int(toks[i])
            i += 1
        asts = []
        for _ in range(na):
            v = tuple(map(int, toks[i].split(",")))
            i += 1
            asts.append(v if len(v) == 4 else v + (0, 0))
        cases.append((gx, gy, T, asts))
    return cases


def solve(case, H, R):
    gx, gy, T, asts = case
    for margin, w in LADDER:
        if max(abs(gx), abs(gy)) + margin > R - 2:
            continue
        res = solve_case(gx, gy, T, asts, H, R, margin, w)
        if res:
            return res
    raise RuntimeError(f"no plan found for {case[:3]}")


def main():
    files = sorted(D.glob(f"in_level-{LEVEL}_*.txt"))
    allc = {f: parse(f) for f in files}
    R = max(max(abs(c[0]), abs(c[1])) for cs in allc.values() for c in cs) + 460
    H = build_H(R)
    for f, cases in allc.items():
        out = []
        for c in cases:
            xs, ys = solve(c, H, R)
            out += [" ".join(map(str, xs)), " ".join(map(str, ys)), ""]
        (D / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out))


if __name__ == "__main__":
    main()
