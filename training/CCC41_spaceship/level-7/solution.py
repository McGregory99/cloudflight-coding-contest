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

# ---- level 7: dense static asteroid fields -> same weighted A*, written in C, built on the fly ----
import ctypes
import multiprocessing
import os
import subprocess
import tempfile
from pathlib import Path

C_SOURCE = r"""/* Weighted A* over (x, y, state_x, state_y) for static asteroids (levels 5-7).
   Same search as the pure Python fallback, just fast. Built on the fly with `cc -O2 -shared`. */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#define NS 31

typedef struct { int64_t key; int32_t node; } HE;

static HE *heap; static long hn, hcap;

static void hpush(int64_t key, int32_t node) {
    if (hn == hcap) { hcap = hcap ? hcap * 2 : 1 << 16; heap = realloc(heap, hcap * sizeof(HE)); }
    long i = hn++;
    while (i > 0) {
        long p = (i - 1) >> 1;
        if (heap[p].key <= key) break;
        heap[i] = heap[p]; i = p;
    }
    heap[i].key = key; heap[i].node = node;
}

static HE hpop(void) {
    HE top = heap[0], last = heap[--hn];
    long i = 0;
    for (;;) {
        long c = 2 * i + 1;
        if (c >= hn) break;
        if (c + 1 < hn && heap[c + 1].key < heap[c].key) c++;
        if (heap[c].key >= last.key) break;
        heap[i] = heap[c]; i = c;
    }
    if (hn > 0) heap[i] = last;
    return top;
}

/* returns path length (ticks) >= 1, or -1 no plan inside the window / T, -2 node/expansion budget exhausted, -3 bad input */
int astar(int gx, int gy, int T, int xlo, int xhi, int ylo, int yhi, double w,
          const int *H, int R, const int *nn, const int *nsx, const int *ndx, int S0,
          int na, const int *ax, const int *ay,
          int *out_sx, int *out_sy, long maxnodes, long maxexp, long *expanded)
{
    int Wd = xhi - xlo + 1, Hh = yhi - ylo + 1, W2 = 2 * R + 1;
    long cells = (long)Wd * Hh;
    unsigned char *blk = calloc(cells, 1);
    short *gd = malloc(cells * sizeof(short));
    int *q = malloc(cells * sizeof(int));
    for (int i = 0; i < na; i++)
        for (int y = ay[i] - 2; y <= ay[i] + 2; y++) {
            if (y < ylo || y > yhi) continue;
            for (int x = ax[i] - 2; x <= ax[i] + 2; x++)
                if (x >= xlo && x <= xhi) blk[(long)(y - ylo) * Wd + (x - xlo)] = 1;
        }
    long start = (long)(0 - ylo) * Wd + (0 - xlo), goal = (long)(gy - ylo) * Wd + (gx - xlo);
    int rc = -3;
    if (blk[start] || blk[goal]) goto done0;
    for (long i = 0; i < cells; i++) gd[i] = 30000;
    long qh = 0, qt = 0; gd[goal] = 0; q[qt++] = goal;
    while (qh < qt) {
        long c = q[qh++]; int cy = c / Wd, cx = c % Wd; short d = gd[c] + 1;
        for (int dy = -1; dy <= 1; dy++) for (int dx = -1; dx <= 1; dx++) {
            int ny = cy + dy, nx = cx + dx;
            if (ny < 0 || ny >= Hh || nx < 0 || nx >= Wd) continue;
            long k = (long)ny * Wd + nx;
            if (!blk[k] && gd[k] == 30000) { gd[k] = d; q[qt++] = k; }
        }
    }
    if (gd[start] >= 30000) { rc = -1; goto done0; }

    uint32_t *key = malloc(maxnodes * sizeof(uint32_t));
    int32_t *par = malloc(maxnodes * sizeof(int32_t));
    int32_t *gg = malloc(maxnodes * sizeof(int32_t));
    long hsz = 1; while (hsz < maxnodes * 2) hsz <<= 1;
    int32_t *tab = calloc(hsz, sizeof(int32_t));
    long nodes = 0, exp = 0;
    hn = 0;
    #define KEY(c, sx, sy) ((uint32_t)(((c) * NS + (sx)) * NS + (sy)))
    uint32_t k0 = KEY(start, S0, S0);
    key[0] = k0; par[0] = -1; gg[0] = 1; nodes = 1;
    tab[(k0 * 2654435761u) & (hsz - 1)] = 1;
    int h0 = H[S0 * W2 + gx + R]; { int h = H[S0 * W2 + gy + R]; if (h > h0) h0 = h; if (gd[start] > h0) h0 = gd[start]; }
    if (1 + h0 > T) { rc = -1; goto done1; }
    hpush(((int64_t)((1 + w * h0) * 16) << 20) + (1048575 - 1), 0);
    rc = -1;
    while (hn > 0) {
        HE e = hpop(); int32_t nd = e.node; int g = gg[nd];
        if ((int)(1048575 - (e.key & 1048575)) != g) continue; /* stale */
        if (exp >= maxexp) { rc = -2; goto done1; }
        exp++;
        uint32_t kk = key[nd]; int sy = kk % NS; int sx = (kk / NS) % NS; long c = kk / (NS * NS);
        int cy = c / Wd, cx = c % Wd; int x = cx + xlo, y = cy + ylo;
        int g1 = g + 1;
        for (int a = 0; a < nn[sx]; a++) {
            int sx2 = nsx[sx * 3 + a], x2 = x + ndx[sx * 3 + a];
            if (x2 < xlo || x2 > xhi) continue;
            int hx = H[sx2 * W2 + gx - x2 + R];
            if (g1 + hx > T) continue;
            for (int b = 0; b < nn[sy]; b++) {
                int sy2 = nsx[sy * 3 + b], y2 = y + ndx[sy * 3 + b];
                if (y2 < ylo || y2 > yhi) continue;
                int hy = H[sy2 * W2 + gy - y2 + R];
                int h = hx > hy ? hx : hy;
                if (g1 + h > T) continue;
                long c2 = (long)(y2 - ylo) * Wd + (x2 - xlo);
                if (blk[c2]) continue;
                int hg = gd[c2];
                if (g1 + hg > T) continue;
                if (hg > h) h = hg;
                uint32_t k2 = KEY(c2, sx2, sy2);
                long hi = (k2 * 2654435761u) & (hsz - 1);
                int32_t found = 0;
                while (tab[hi]) { if (key[tab[hi] - 1] == k2) { found = tab[hi]; break; } hi = (hi + 1) & (hsz - 1); }
                int32_t id;
                if (found) { id = found - 1; if (gg[id] <= g1) continue; gg[id] = g1; par[id] = nd; }
                else {
                    if (nodes >= maxnodes) { rc = -2; goto done1; }
                    id = nodes++; key[id] = k2; gg[id] = g1; par[id] = nd; tab[hi] = id + 1;
                }
                if (x2 == gx && y2 == gy && sx2 == S0 && sy2 == S0) {
                    int len = 0; for (int32_t p = id; p >= 0; p = par[p]) len++;
                    int i = len - 1;
                    for (int32_t p = id; p >= 0; p = par[p]) {
                        uint32_t kp = key[p]; out_sy[i] = kp % NS; out_sx[i] = (kp / NS) % NS; i--;
                    }
                    rc = len; goto done1;
                }
                hpush(((int64_t)((g1 + w * h) * 16) << 20) + (1048575 - g1), id);
            }
        }
    }
done1:
    *expanded = exp;
    free(key); free(par); free(gg); free(tab);
done0:
    free(blk); free(gd); free(q);
    return rc;
}
"""

D = Path(__file__).parent
LEVEL = int(D.name.split("-")[1])
LADDER_PY = ((120, 3.0), (250, 2.0), (400, 1.5))   # (window margin, A* weight) for the pure Python fallback
LADDER_C = ((120, 2.0, 4_000_000), (250, 2.0, 8_000_000), (120, 3.0, 8_000_000),
            (120, 1.5, 30_000_000), (400, 2.0, 60_000_000))  # (window margin, A* weight, expansion budget)
_lib = _tabs = _H = _R = None


def build_c():
    """Compile the C search; returns the loaded library or None (then pure Python is used)."""
    try:
        d = tempfile.mkdtemp()
        src, so = os.path.join(d, "astar.c"), os.path.join(d, "astar.so")
        Path(src).write_text(C_SOURCE)
        subprocess.check_call(["cc", "-O2", "-shared", "-fPIC", "-o", so, src],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        lib = ctypes.CDLL(so)
        lib.astar.restype = ctypes.c_int
        return lib
    except Exception:
        return None


def c_tables(H, R):
    n = len(STATES)
    Hflat = (ctypes.c_int * (n * (2 * R + 1)))()
    k = 0
    for s in range(n):
        for v in H[s]:
            Hflat[k] = min(v, 10 ** 8)
            k += 1
    nn = (ctypes.c_int * n)()
    nsx = (ctypes.c_int * (n * 3))()
    ndx = (ctypes.c_int * (n * 3))()
    for s in range(n):
        nn[s] = len(NXT[s])
        for i, (s2, d) in enumerate(NXT[s]):
            nsx[s * 3 + i] = s2
            ndx[s * 3 + i] = d
    return Hflat, nn, nsx, ndx


def c_solve(gx, gy, T, asts, margin, w, maxexp):
    Hflat, nn, nsx, ndx = _tabs
    xlo, xhi = min(0, gx) - margin, max(0, gx) + margin
    ylo, yhi = min(0, gy) - margin, max(0, gy) + margin
    rel = [a for a in asts if xlo - 2 <= a[0] <= xhi + 2 and ylo - 2 <= a[1] <= yhi + 2]
    na = len(rel)
    ax = (ctypes.c_int * max(1, na))(*[a[0] for a in rel])
    ay = (ctypes.c_int * max(1, na))(*[a[1] for a in rel])
    osx = (ctypes.c_int * (T + 5))()
    osy = (ctypes.c_int * (T + 5))()
    exp = ctypes.c_long(0)
    n = _lib.astar(gx, gy, T, xlo, xhi, ylo, yhi, ctypes.c_double(w), Hflat, _R, nn, nsx, ndx, S0,
                   na, ax, ay, osx, osy, ctypes.c_long(12_000_000), ctypes.c_long(maxexp), ctypes.byref(exp))
    if n < 0:
        return None
    return axis_blocks(list(osx[:n])), axis_blocks(list(osy[:n]))


def parse(path):
    toks = path.read_text().split()
    n, i, cases = int(toks[0]), 1, []
    for _ in range(n):
        gx, gy = map(int, toks[i].split(","))
        T, na = int(toks[i + 1]), int(toks[i + 2])
        i += 3
        asts = []
        for _ in range(na):
            px, py = map(int, toks[i].split(","))
            i += 1
            asts.append((px, py, 0, 0))
        cases.append((gx, gy, T, asts))
    return cases


def init_worker(R):
    global _lib, _tabs, _H, _R
    if _H is None:  # spawn start method: rebuild; with fork the parent's globals are inherited
        _R = R
        _H = build_H(R)
        _lib = build_c()
        _tabs = c_tables(_H, R) if _lib else None


def solve(case):
    gx, gy, T, asts = case
    if _lib:
        for margin, w, cap in LADDER_C:
            res = c_solve(gx, gy, T, asts, margin, w, cap)
            if res:
                return res
    for margin, w in LADDER_PY:  # fallback (slow): no C compiler, or the C search found nothing
        res = solve_case(gx, gy, T, asts, _H, _R, margin, w)
        if res:
            return res
    raise RuntimeError(f"no plan found for {case[:3]}")


def main():
    global _lib, _tabs, _H, _R
    files = sorted(D.glob(f"in_level-{LEVEL}_*.txt"))
    allc = {f: parse(f) for f in files}
    _R = max(max(abs(c[0]), abs(c[1])) for cs in allc.values() for c in cs) + 460
    _H = build_H(_R)
    _lib = build_c()
    _tabs = c_tables(_H, _R) if _lib else None
    print("C accelerator:", "on" if _lib else "off (pure Python fallback, slow)")
    try:
        ctx = multiprocessing.get_context("fork")
    except ValueError:
        ctx = multiprocessing.get_context()
    with ctx.Pool(os.cpu_count() or 1, initializer=init_worker, initargs=(_R,)) as pool:
        for f, cases in allc.items():
            order = sorted(range(len(cases)), key=lambda i: -cases[i][2])  # big time limits first: balances the pool
            res = {}
            for i, r in zip(order, pool.imap(solve, [cases[i] for i in order], chunksize=1)):
                res[i] = r
            out = []
            for i in range(len(cases)):
                xs, ys = res[i]
                out += [" ".join(map(str, xs)), " ".join(map(str, ys)), ""]
            (D / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out))


if __name__ == "__main__":
    main()
