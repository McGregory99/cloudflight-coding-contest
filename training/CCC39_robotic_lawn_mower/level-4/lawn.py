"""Hamiltonian path / cycle on a grid with trees: bipartite 2-factor by max-flow + 2x2 flip merging."""
import random
from collections import deque

def parse(text):
    t = text.split()
    n = int(t[0]); p = 1; res = []
    for _ in range(n):
        w, h = int(t[p]), int(t[p + 1]); p += 2
        res.append((w, h, t[p:p + h])); p += h
    return res

def _flow_two_factor(nodes, nbrs, deg, rng):
    """Dinic: select edges so every vertex v has degree deg[v]. Returns adj sets or None."""
    B = [v for v in nodes if v[2]]  # v = (x,y,color)
    # node ids: S=0, T=1, vertices 2+
    ids = {v: i + 2 for i, v in enumerate(nodes)}
    N = len(nodes) + 2
    g = [[] for _ in range(N)]
    to = []; cap = []
    def add(u, v, c):
        g[u].append(len(to)); to.append(v); cap.append(c)
        g[v].append(len(to)); to.append(u); cap.append(0)
    need = 0
    for v in nodes:
        i = ids[v]
        if v[2]:
            add(0, i, deg[v]); need += deg[v]
            ns = list(nbrs[v]); rng.shuffle(ns)
            for u in ns: add(i, ids[u], 1)
        else:
            add(i, 1, deg[v])
    if sum(deg[v] for v in nodes if not v[2]) != need:
        return None
    flow = 0
    while True:
        lvl = [-1] * N; lvl[0] = 0; q = deque([0])
        while q:
            u = q.popleft()
            for e in g[u]:
                if cap[e] and lvl[to[e]] < 0:
                    lvl[to[e]] = lvl[u] + 1; q.append(to[e])
        if lvl[1] < 0: break
        it = [0] * N
        def dfs(u, f):  # iterative would be safer; depth is only 4 (S-b-w-T) in the first phase, grows later
            if u == 1: return f
            while it[u] < len(g[u]):
                e = g[u][it[u]]
                v = to[e]
                if cap[e] and lvl[v] == lvl[u] + 1:
                    r = dfs(v, min(f, cap[e]))
                    if r:
                        cap[e] -= r; cap[e ^ 1] += r
                        return r
                it[u] += 1
            return 0
        while True:
            f = dfs(0, 10**9)
            if not f: break
            flow += f
    if flow != need: return None
    adj = {v: set() for v in nodes}
    byid = {ids[v]: v for v in nodes}
    for v in nodes:
        if v[2]:
            for e in g[ids[v]]:
                if e % 2 == 0 and to[e] != 0 and cap[e] == 0 and to[e] != 1:
                    u = byid[to[e]]; adj[v].add(u); adj[u].add(v)
    return adj

def _components(adj):
    comp = {}; members = []
    for v in adj:
        if v in comp: continue
        c = len(members); comp[v] = c; st = [v]; m = [v]
        while st:
            u = st.pop()
            for z in adj[u]:
                if z not in comp:
                    comp[z] = c; st.append(z); m.append(z)
        members.append(m)
    return comp, members

def _merge_and_walk(adj, blocks, rng, deadline_iters):
    comp, members = _components(adj)
    ncomp = len(members)
    alive = {i: m for i, m in enumerate(members)}
    for it in range(deadline_iters):
        if len(alive) == 1: break
        progress = False
        rng.shuffle(blocks)
        for a, b, c, d in blocks:
            if len(alive) == 1: break
            for (p, q, r, s) in ((a, b, c, d), (a, c, b, d)):  # (p-q),(r-s) parallel; p-r,q-s new
                if q in adj[p] and s in adj[r] and r not in adj[p] and s not in adj[q] and comp[p] != comp[r]:
                    adj[p].discard(q); adj[q].discard(p); adj[r].discard(s); adj[s].discard(r)
                    adj[p].add(r); adj[r].add(p); adj[q].add(s); adj[s].add(q)
                    cp, cr = comp[p], comp[r]
                    if len(alive[cp]) < len(alive[cr]): cp, cr = cr, cp
                    for v in alive[cr]: comp[v] = cp
                    alive[cp].extend(alive[cr]); del alive[cr]
                    progress = True
                    break
        if len(alive) == 1: break
        # stuck or slow: random perturbation flips (may split), then relabel
        k = 1 + len(blocks) // 50
        for _ in range(k):
            a, b, c, d = blocks[rng.randrange(len(blocks))]
            for (p, q, r, s) in ((a, b, c, d), (a, c, b, d)):
                if q in adj[p] and s in adj[r] and r not in adj[p] and s not in adj[q]:
                    adj[p].discard(q); adj[q].discard(p); adj[r].discard(s); adj[s].discard(r)
                    adj[p].add(r); adj[r].add(p); adj[q].add(s); adj[s].add(q)
                    break
        comp, members = _components(adj)
        alive = {i: m for i, m in enumerate(members)}
    return len(alive) == 1

def _moves(adj, start, n):
    D = {(0, -1): "W", (1, 0): "D", (0, 1): "S", (-1, 0): "A"}
    out = []; prev = None; cur = start
    for _ in range(n - 1):
        nxt = [u for u in adj[cur] if u != prev]
        u = nxt[0]
        out.append(D[(u[0] - cur[0], u[1] - cur[1])])
        prev, cur = cur, u
    return "".join(out)

def solve(w, h, grid, mode, seed=1, tries=200):
    rng = random.Random(seed)
    nodes = [(x, y, (x + y) & 1) for y in range(h) for x in range(w) if grid[y][x] == "."]
    key = {(v[0], v[1]): v for v in nodes}
    nbrs = {v: [key[(v[0] + dx, v[1] + dy)] for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)) if (v[0] + dx, v[1] + dy) in key] for v in nodes}
    blocks = []
    for y in range(h - 1):
        for x in range(w - 1):
            q = [(x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
            if all(c in key for c in q): blocks.append(tuple(key[c] for c in q))
    nb = sum(1 for v in nodes if v[2]); nw = len(nodes) - nb
    for t in range(tries):
        deg = {v: 2 for v in nodes}
        if mode == "cycle":
            if nb != nw: return None
        else:
            def pick(col, k):
                c = [v for v in nodes if v[2] == col]
                return rng.sample(c, k)
            if nb == nw + 1: ends = pick(1, 2)
            elif nw == nb + 1: ends = pick(0, 2)
            elif nb == nw: ends = pick(1, 1) + pick(0, 1)
            else: return None
            for e in ends: deg[e] = 1
        adj = _flow_two_factor(nodes, nbrs, deg, rng)
        if adj is None: continue
        if _merge_and_walk(adj, list(blocks), rng, 60):
            if mode == "cycle": start = nodes[0]
            else: start = next(v for v in nodes if len(adj[v]) == 1)
            return _moves(adj, start, len(nodes))
    return None
