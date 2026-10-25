"""Asteroid Mining (CCC41 school) - connected tunnel network (connected dominating set of a grid) with a dig limit.

Search space: every row (or every column) of the minable rectangle holds ONE interval of tunnel cells
(+ optional empty first/last line, + one extra cell for the outpost).  A small DP over the lines with
state (previous interval, current interval) finds the cheapest comb layout; both orientations are tried.
"""
from pathlib import Path

HERE = Path(__file__).parent

SPECS = ["l0:h0", "l1:h0", "l1:l1", "h1:h1", "l0:h1", "l1:h1", "l0:l0",
         "l2:l2", "h2:h2", "l0:l2", "h1:h0", "l0:l1"]


def candidates(L):
    out = []
    for sp in SPECS:
        x, y = sp.split(":")
        a = int(x[1:]) if x[0] == "l" else L - 1 - int(x[1:])
        b = int(y[1:]) if y[0] == "l" else L - 1 - int(y[1:])
        if 0 <= a <= b < L and (a, b) not in out:
            out.append((a, b))
    return out


def covered(L, p, c, q):
    """rows of a line with interval c (None=empty) are dominated given neighbour intervals p, q"""
    if c is None:
        need = [(0, L - 1)]
    else:
        need = []
        if c[0] >= 2:
            need.append((0, c[0] - 2))
        if c[1] + 2 <= L - 1:
            need.append((c[1] + 2, L - 1))
    segs = sorted(x for x in (p, q) if x)
    for lo, hi in need:
        cur = lo
        for s, e in segs:
            if s <= cur <= e:
                cur = e + 1
        if cur <= hi:
            return False
    return True


def solve_oriented(n, L, cs, rs, limit=None):
    """n lines, each a dug interval along 0..L-1; the cell (line cs, pos rs) must be dug and connected.
    Returns (cost, intervals per line) or None."""
    cand = candidates(L)
    opts = cand + [None]
    m = len(opts)
    E = m - 1
    ln = [0 if x is None else x[1] - x[0] + 1 for x in opts]
    has = [x is not None and x[0] <= rs <= x[1] for x in opts]
    adj = [x is not None and (rs == x[0] - 1 or rs == x[1] + 1) for x in opts]

    def ov(x, y):
        return x is None or y is None or (x[0] <= y[1] and y[0] <= x[1])

    # valid[p*m+c] = list of q
    valid = {}
    for p in range(m):
        for c in range(m):
            if c != E or True:
                valid[p * m + c] = [q for q in range(m)
                                    if ov(opts[c], opts[q]) and covered(L, opts[p], opts[c], opts[q])]
    INF = 10 ** 9
    cur = {}
    for c in range(m):
        if c == E and n < 2:
            continue
        cost = ln[c] + (1 if cs == 0 and not has[c] else 0)
        cur[E * m + c] = (cost, -1)
    back = [None] * n
    for j in range(1, n):
        nxt = {}
        par = {}
        last = j == n - 1
        for key, (cost, _) in cur.items():
            p, c = divmod(key, m)
            if j - 1 == cs and not (has[c] or adj[c] or has[p] or False):
                # need neighbour q containing rs; checked per q below
                needq = True
            else:
                needq = False
            for q in valid[key]:
                if q == E and not last:
                    continue
                if needq and not has[q]:
                    continue
                w = cost + ln[q] + (1 if j == cs and not has[q] else 0)
                k2 = c * m + q
                old = nxt.get(k2)
                if old is None or w < old[0]:
                    nxt[k2] = (w, p)
        back[j] = nxt
        cur = nxt
    best = INF
    bk = None
    for key, (cost, _) in cur.items():
        p, c = divmod(key, m)
        if n - 1 == cs and not (has[c] or adj[c] or has[p]):
            continue
        if covered(L, opts[p], opts[c], None) and cost < best:
            best, bk = cost, key
    if bk is None:
        return None
    ch = [None] * n
    key = bk
    for j in range(n - 1, 0, -1):
        p, c = divmod(key, m)
        ch[j] = c
        key = back[j][key][1] * m + p
    ch[0] = key % m
    return best, [opts[i] for i in ch]


def build(W, H, s, limit=None):
    """grid of W x H cells (True=dug) for a rect with outpost above column s"""
    res = []
    r = solve_oriented(W, H, s, 0)
    if r:
        res.append(("A", r))
    if not (r and limit is not None and r[0] <= limit):
        r2 = solve_oriented(H, W, 0, s)
        if r2:
            res.append(("B", r2))
    o, (cost, ivs) = min(res, key=lambda t: t[1][0])
    dug = [[False] * W for _ in range(H)]
    if o == "A":
        for c, iv in enumerate(ivs):
            if iv:
                for r_ in range(iv[0], iv[1] + 1):
                    dug[r_][c] = True
        dug[0][s] = True
    else:
        for r_, iv in enumerate(ivs):
            if iv:
                for c in range(iv[0], iv[1] + 1):
                    dug[r_][c] = True
        dug[0][s] = True
    return dug


def parse(text):
    lines = text.split("\n")
    n = int(lines[0])
    i, res = 1, []
    for _ in range(n):
        while not lines[i].strip():
            i += 1
        w, h, lim = map(int, lines[i].split()[:3])
        g = lines[i + 1:i + h + 3]
        res.append((w, h, lim, g[0].index("S") - 1))
        i += h + 3
    return res


def solve(text):
    out = []
    for w, h, lim, s in parse(text):
        dug = build(w, h, s, lim)
        out.append("#" * (s + 1) + "S" + "#" * (w - s))
        for r in range(h):
            out.append("#" + "".join("X" if d else ":" for d in dug[r]) + "#")
        out += ["#" * (w + 2), ""]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for f in sorted(HERE.glob("in_level-4_*.txt")):
        (HERE / f.name.replace("in_", "").replace(".txt", ".out")).write_text(solve(f.read_text()))
