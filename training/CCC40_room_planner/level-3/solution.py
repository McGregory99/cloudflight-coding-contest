import glob, os, sys

sys.setrecursionlimit(10000)

def build(P, Q):
    """f[p][q] = max number of 1x3 bars in a p-rows x q-cols rectangle (guillotine DP)."""
    f = [[0] * (Q + 1) for _ in range(P + 1)]
    ch = [[None] * (Q + 1) for _ in range(P + 1)]
    for p in range(1, P + 1):
        for q in range(1, Q + 1):
            hb = p * (q // 3)
            vb = (p // 3) * q
            if hb >= vb:
                best, c = hb, ("h",)
            else:
                best, c = vb, ("v",)
            for a in range(1, p // 2 + 1):
                v = f[a][q] + f[p - a][q]
                if v > best:
                    best, c = v, ("r", a)
            for b in range(1, q // 2 + 1):
                v = f[p][b] + f[p][q - b]
                if v > best:
                    best, c = v, ("c", b)
            f[p][q], ch[p][q] = best, c
    return f, ch

def place(ch, p, q):
    """Return list of desks as lists of (row, col) cells."""
    desks = []
    stack = [(p, q, 0, 0)]
    while stack:
        p, q, r0, c0 = stack.pop()
        if p <= 0 or q <= 0:
            continue
        c = ch[p][q]
        if c is None:
            continue
        if c[0] == "h":
            for r in range(p):
                for k in range(q // 3):
                    desks.append([(r0 + r, c0 + 3 * k + j) for j in range(3)])
        elif c[0] == "v":
            for k in range(p // 3):
                for cc in range(q):
                    desks.append([(r0 + 3 * k + j, c0 + cc) for j in range(3)])
        elif c[0] == "r":
            a = c[1]
            stack.append((a, q, r0, c0))
            stack.append((p - a, q, r0 + a, c0))
        else:
            b = c[1]
            stack.append((p, b, r0, c0))
            stack.append((p, q - b, r0, c0 + b))
    return desks

def main():
    files = sorted(glob.glob("in_level-3_*.txt"))
    data = {}
    P = Q = 1
    for path in files:
        toks = open(path).read().split()
        n = int(toks[0])
        rooms = [tuple(int(t) for t in toks[1 + 3 * i: 4 + 3 * i]) for i in range(n)]
        data[path] = rooms
        for x, y, k in rooms:
            P, Q = max(P, y), max(Q, x)
    f, ch = build(P, Q)
    for path in files:
        out = []
        for x, y, k in data[path]:
            desks = place(ch, y, x)
            assert len(desks) == f[y][x]
            if len(desks) != k:
                print("MISMATCH", path, x, y, "expected", k, "got", len(desks), file=sys.stderr)
            grid = [[0] * x for _ in range(y)]
            for i, d in enumerate(desks, 1):
                for r, c in d:
                    grid[r][c] = i
            for row in grid:
                out.append(" ".join(map(str, row)))
            out.append("")
        name = os.path.basename(path)[3:-4]
        with open(name + ".out", "w") as fh:
            fh.write("\n".join(out) + "\n")

main()
