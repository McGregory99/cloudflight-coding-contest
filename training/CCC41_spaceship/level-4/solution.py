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

# ---- level 4: 2D, axes independent -> optimal 1D sequence per axis ----
from pathlib import Path

D = Path(__file__).parent
for f in sorted(D.glob("in_level-4_*.txt")):
    toks = f.read_text().split()
    n = int(toks[0])
    cases = []
    for i in range(n):
        gx, gy = map(int, toks[1 + 2 * i].split(","))
        cases.append((gx, gy, int(toks[2 + 2 * i])))
    R = max(max(abs(c[0]), abs(c[1])) for c in cases) + 5
    H = build_H(R)
    out = []
    for gx, gy, limit in cases:
        xs = axis_blocks(greedy_axis(gx, H, R))
        ys = axis_blocks(greedy_axis(gy, H, R))
        for s in (xs, ys):
            assert sum(max(1, abs(p)) for p in s) <= limit
        out += [" ".join(map(str, xs)), " ".join(map(str, ys)), ""]
    (D / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out))
