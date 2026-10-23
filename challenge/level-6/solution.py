"""Level 6 baseline: two active beams; their intersection cell is traced along a short walk
through the pattern (TSP over Chebyshev moves in emitter-position space). K copies are built by
walking the path forward and backward."""
from pathlib import Path
import sys
import numpy as np

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "outputs" / "level-6"
sys.path.insert(0, str(HERE.parent / "level-5"))

AX = {1: (1, 0), 2: (0, 1), 3: (-1, 1), 4: (-1, 0), 5: (0, -1), 6: (1, -1)}
FAM = {1: 0, 4: 0, 2: 1, 5: 1, 3: 2, 6: 2}
INF = 10 ** 6


class Geo:
    def __init__(self, R):
        self.R = R
        step = [(1, -1), (1, 0), (0, 1), (-1, 1), (-1, 0), (0, -1)]
        ring = [(-R, 0)]
        for s in step:
            for _ in range(R):
                ring.append((ring[-1][0] + s[0], ring[-1][1] + s[1]))
        ring.pop()
        self.ring = ring
        self.n = len(ring)
        inside = lambda q, r: max(abs(q), abs(r), abs(q + r)) < R
        self.inside = inside
        self.cells = [(q, r) for q in range(-R, R + 1) for r in range(-R, R + 1) if inside(q, r)]
        # window of each emitter: ring idx -> beam cells (non-empty only)
        self.idx_of = {}      # (k, cell) -> ring idx
        self.window = {}
        for k in range(1, 7):
            d = AX[k]
            win = []
            for p, (q, r) in enumerate(ring):
                cs = []
                a, b = q + d[0], r + d[1]
                while inside(a, b):
                    cs.append((a, b)); a += d[0]; b += d[1]
                if cs:
                    win.append(p)
                    for c in cs:
                        assert (k, c) not in self.idx_of
                        self.idx_of[(k, c)] = p
            ws = set(win)
            s = next(p for p in win if (p - 1) % self.n not in ws)
            order = [(s + t) % self.n for t in range(len(win))]
            assert set(order) == ws
            self.window[k] = order
        self.t_of = {k: {p: t for t, p in enumerate(self.window[k])} for k in range(1, 7)}


_geo = {}


def geo(R):
    if R not in _geo:
        _geo[R] = Geo(R)
    return _geo[R]


def parse_pattern(rows, R):
    P = set()
    for i, row in enumerate(rows):
        for j, ch in enumerate(row):
            if ch == "M":
                r = i - R
                P.add(((j - 2 * R - r) // 2, r))
    return P


def plan_pair(g, P, NP, a, b):
    """Return (D, cells, node_of, bfs) data for emitter pair (a,b); None if infeasible."""
    wa, wb = len(g.window[a]), len(g.window[b])
    cellnode = {}
    for c in g.cells:
        cellnode[c] = (g.t_of[a][g.idx_of[(a, c)]], g.t_of[b][g.idx_of[(b, c)]])
    node_cell = {v: c for c, v in cellnode.items()}
    forb = np.zeros((wa, wb), dtype=bool)
    for c in NP:
        if c in cellnode:
            x, y = cellnode[c]; forb[x, y] = True
    return wa, wb, cellnode, forb


def bfs(wa, wb, forb, src):
    dist = np.full((wa, wb), INF, dtype=np.int32)
    par = {}
    dist[src] = 0
    fr = [src]
    d = 0
    while fr:
        d += 1
        nf = []
        for x, y in fr:
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < wa and 0 <= ny < wb and not forb[nx, ny] and dist[nx, ny] == INF:
                        dist[nx, ny] = d
                        par[(nx, ny)] = (x, y)
                        nf.append((nx, ny))
        fr = nf
    return dist, par


def two_opt(D, tour):
    n = len(tour)
    improved = True
    while improved:
        improved = False
        for i in range(n - 1):
            a, b = tour[i], tour[i + 1]
            hi = n if i > 0 else n - 1
            if i + 2 >= hi:
                continue
            js = np.arange(i + 2, hi)
            c = tour[js]; d = tour[(js + 1) % n]
            delta = D[a, c] + D[b, d] - D[a, b] - D[c, d]
            k = int(np.argmin(delta))
            if delta[k] < 0:
                j = js[k]
                tour[i + 1:j + 1] = tour[i + 1:j + 1][::-1].copy()
                improved = True
    return tour


def open_path(D, starts):
    """Open Hamiltonian path heuristic via dummy node + NN + 2-opt. D: m x m."""
    m = len(D)
    if m == 1:
        return [0], 0
    n = m + 1
    M = np.zeros((n, n), dtype=np.int64)
    M[:m, :m] = D
    best = None
    for s in starts:
        seen = np.zeros(n, dtype=bool)
        tour = [m]; seen[m] = True
        cur = s; tour.append(cur); seen[cur] = True
        for _ in range(m - 1):
            row = np.where(seen, INF * 10, M[cur])
            cur = int(np.argmin(row)); tour.append(cur); seen[cur] = True
        tour = np.array(tour)
        tour = two_opt(M, tour)
        z = int(np.where(tour == m)[0][0])
        path = list(np.concatenate([tour[z + 1:], tour[:z]]))
        L = int(sum(D[path[i], path[i + 1]] for i in range(m - 1)))
        if best is None or L < best[1]:
            best = (path, L)
    return best


def ring_delta(g, frm, to):
    d = (to - frm) % g.n
    return d if d <= g.n // 2 else d - g.n


def build_program(R, rows, K):
    g = geo(R)
    P = parse_pattern(rows, R)
    cells = sorted(P)
    NP = {(q + d[0], r + d[1]) for q, r in P for d in AX.values()} - P
    best = None
    for a in range(1, 7):
        for b in range(a + 1, 7):
            if FAM[a] == FAM[b]:
                continue
            wa, wb, cellnode, forb = plan_pair(g, P, NP, a, b)
            nodes = [cellnode[c] for c in cells]
            m = len(nodes)
            D = np.zeros((m, m), dtype=np.int64)
            bfss = []
            ok = True
            for i, nd in enumerate(nodes):
                dist, par = bfs(wa, wb, forb, nd)
                bfss.append(par)
                for j, nd2 in enumerate(nodes):
                    D[i, j] = dist[nd2]
                if (D[i] >= INF).any():
                    ok = False
                    break
            if not ok:
                continue
            starts = [0] if m == 1 else sorted(range(m), key=lambda i: (nodes[i][0] + nodes[i][1]))[:: max(1, m // 3)][:3]
            path, L = open_path(D, starts)
            for orient in (path, path[::-1]):
                f = nodes[orient[0]]
                da = abs(ring_delta(g, (a - 1) * R, g.window[a][f[0]]))
                db = abs(ring_delta(g, (b - 1) * R, g.window[b][f[1]]))
                total = max(da, db) + 1 + L + (K - 1) * (L + 1)
                if best is None or total < best[0]:
                    best = (total, a, b, orient, nodes, bfss, wa, wb)
    total, a, b, orient, nodes, bfss, wa, wb = best
    # expand node walk
    walk = [nodes[orient[0]]]
    for u, v in zip(orient, orient[1:]):
        par = bfss[u]  # BFS from nodes[u]
        seg = [nodes[v]]
        while seg[-1] != nodes[u]:
            seg.append(par[seg[-1]])
        walk.extend(seg[::-1][1:])
    lines = []

    def emit(ia, ib):
        line = ["-"] * 6
        line[a - 1], line[b - 1] = ia, ib
        lines.append(line)

    # startup
    def moves(k, target_idx):
        d = ring_delta(g, (k - 1) * R, target_idx)
        return ["F" if d > 0 else "B"] * abs(d)

    f = walk[0]
    ma = moves(a, g.window[a][f[0]]) + ["T"]
    mb = moves(b, g.window[b][f[1]]) + ["T"]
    for t in range(max(len(ma), len(mb))):
        emit(ma[t] if t < len(ma) else "-", mb[t] if t < len(mb) else "-")

    def walk_lines(w):
        for (x, y), (x2, y2) in zip(w, w[1:]):
            emit({1: "F", -1: "B", 0: "-"}[x2 - x], {1: "F", -1: "B", 0: "-"}[y2 - y])

    walk_lines(walk)
    cur = walk
    for _ in range(K - 1):
        emit("-", "-")
        cur = cur[::-1]
        walk_lines(cur)
    return lines


def solve(text):
    t = text.split()
    n = int(t[0]); p = 1; out = []
    for _ in range(n):
        R, rows, cols, K = map(int, t[p:p + 4]); p += 4
        pat = t[p:p + rows]; p += rows
        prog = build_program(R, pat, K)
        out.append("".join(" ".join(l) + "\n" for l in prog) + "\n")
    return "".join(out)


def verify(text, out):
    from solution import run  # level-5 simulator (char-grid based)
    t = text.split(); n = int(t[0]); p = 1
    progs = [b.split("\n") for b in out.strip("\n").split("\n\n")]
    assert len(progs) == n
    total = 0
    for pr in progs:
        R, rows, cols, K = map(int, t[p:p + 4]); p += 4
        pat = t[p:p + rows]; p += rows
        prog = [l.split() for l in pr]
        assert all(len(l) == 6 for l in prog)
        got = run(R, pat, prog)
        assert got == K, (got, K)
        total += len(prog)
    return total


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    only = sys.argv[1:]
    for f in sorted(HERE.glob("in_level-6_*.txt")):
        name = f.name.replace("in_", "", 1).replace("txt", "out")
        if only and not any(o in name for o in only):
            continue
        text = f.read_text()
        out = solve(text)
        total = verify(text, out)
        if "0-example" in name:
            ex = (HERE / "out_level-6_0-example.txt").read_text()
            print("example lines ours", total, "reference", sum(1 for b in ex.strip("\n").split("\n\n") for _ in b.split("\n")))
            continue
        (OUT / name).write_text(out)
        print("wrote", name, "lines", total)
