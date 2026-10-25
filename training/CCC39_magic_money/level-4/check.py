"""Validate level-4_*.out: sums are right and coin counts are minimal.
Optimality uses an independent method: Dijkstra over residues mod the largest coin M
(edge weight M-c per coin c, total coins = (dist[r] + amount) / M), valid when amount >= M*M;
smaller amounts use a plain DP."""
import glob
import heapq
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def residue_dist(coins):
    m = max(coins)
    dist = [float("inf")] * m
    dist[0] = 0
    pq = [(0, 0)]
    while pq:
        d, r = heapq.heappop(pq)
        if d > dist[r]:
            continue
        for c in coins:
            if c == m:
                continue
            nr, nd = (r + c) % m, d + m - c
            if nd < dist[nr]:
                dist[nr] = nd
                heapq.heappush(pq, (nd, nr))
    return m, dist


def check(inp, out):
    tok = inp.split()
    n, c, a = int(tok[0]), int(tok[1]), int(tok[2])
    lines = out.split("\n")
    assert lines[-1] == "" and len(lines) == n * a + 1, "line count"
    pos, li = 3, 0
    for _ in range(n):
        coins = list(map(int, tok[pos:pos + c]))
        pos += c
        m, dist = residue_dist(coins)
        small = [0] + [10 ** 9] * (m * m)
        for x in range(1, m * m + 1):
            small[x] = min(small[x - k] + 1 for k in coins if k <= x)
        for s in tok[pos:pos + a]:
            amount = int(s)
            tot = cnt = 0
            for part in lines[li].split(" "):
                q, v = map(int, part.split("x"))
                assert v in coins and q > 0
                tot += q * v
                cnt += q
            li += 1
            if amount > m * m:
                best = (dist[amount % m] + amount) // m
            else:
                best = small[amount]
            assert tot == amount and cnt == best, (amount, lines[li - 1], best)
        pos += a


for p in sorted(glob.glob(os.path.join(HERE, "input", "in_level-4_*.txt"))):
    suffix = os.path.basename(p)[len("in_level-4_"):-4]
    check(open(p).read(), open(os.path.join(HERE, "output", "level-4_%s.out" % suffix)).read())
    print("OK", suffix)
