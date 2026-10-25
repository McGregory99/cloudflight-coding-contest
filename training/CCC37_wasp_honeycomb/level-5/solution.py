from collections import deque
from pathlib import Path

DIRS = [(0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]
INF = 10**9


def parse(text):
    """-> list of (barrierCount, grid rows)."""
    lines = text.split("\n")
    n = int(lines[0])
    res, cur = [], []
    for ln in lines[1:]:
        if ln.strip():
            cur.append(ln.strip())
        elif cur:
            res.append(cur)
            cur = []
    if cur:
        res.append(cur)
    assert len(res) == n
    return [(int(b[0]), b[1:]) for b in res]


def inside(g, r, c):
    return 0 <= r < len(g) and 0 <= c < len(g[r])


def min_cut(g):
    """Min vertex cut between W and the outside: node-split max flow (flow <= 6)."""
    H = len(g)
    # node ids: cell (r,c) -> in = 2*i, out = 2*i+1 ; sink = T
    ids = {}
    for r in range(H):
        for c in range(len(g[r])):
            if g[r][c] in "OW":
                ids[(r, c)] = len(ids)
    T = 2 * len(ids)
    adj = [[] for _ in range(T + 1)]  # edge: [to, cap, rev index]

    def add(u, v, cap):
        adj[u].append([v, cap, len(adj[v])])
        adj[v].append([u, 0, len(adj[u]) - 1])

    for (r, c), i in ids.items():
        add(2 * i, 2 * i + 1, INF if g[r][c] == "W" else 1)
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not inside(g, nr, nc):
                add(2 * i + 1, T, INF)
            elif (nr, nc) in ids:
                add(2 * i + 1, 2 * ids[(nr, nc)], INF)
    s = 2 * ids[next((r, c) for (r, c) in ids if g[r][c] == "W")]
    flow = 0
    while True:
        prev = {s: None}
        q = deque([s])
        while q and T not in prev:
            u = q.popleft()
            for k, (v, cap, _) in enumerate(adj[u]):
                if cap > 0 and v not in prev:
                    prev[v] = (u, k)
                    q.append(v)
        if T not in prev:
            break
        v = T
        while prev[v]:
            u, k = prev[v]
            adj[u][k][1] -= 1
            adj[v][adj[u][k][2]][1] += 1
            v = u
        flow += 1
    reach = set(prev)  # last BFS = residual reachability from source
    cut = [(r, c) for (r, c), i in ids.items() if 2 * i in reach and 2 * i + 1 not in reach]
    return flow, cut


def solve(budget, g):
    flow, cut = min_cut(g)
    assert flow <= budget, (flow, budget)
    g = [list(row) for row in g]
    for r, c in cut:
        g[r][c] = "X"
    return ["".join(row) for row in g]


def main():
    d = Path(__file__).parent
    for f in sorted(d.glob("in_level-5_*.txt")):
        out = f.name.replace("in_", "", 1).replace(".txt", ".out")
        items = parse(f.read_text())
        parts = ["\n".join(solve(b, g)) + "\n" for b, g in items]
        (d / out).write_text(f"{len(items)}\n\n" + "\n".join(parts))


if __name__ == "__main__":
    main()
