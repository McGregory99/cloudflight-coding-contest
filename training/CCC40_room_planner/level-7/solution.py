import glob, os, sys

# Mixed desk lengths 1..7, maximise covered cells, desks must not touch (8-neighbourhood).
# Territory trick: a desk of length l owns a 2 x (l+1) block (the desk plus a gap cell/row
# on its far side). Disjoint territories inside the (H+1) x (W+1) box <=> non-touching desks.
# A territory 2 x m (m = 2..8, either orientation) is worth m-1 cells. Maximise the total
# value: guillotine DP + pinwheel (five-block) splits for small boxes.

PW_MAX = 22
PW_CENTER = 6

def value_ub(p, q):
    A = p * q - (p * q) % 2
    return A // 2 - (-(-A // 16))

def build(P, Q):
    f = [[0] * (Q + 1) for _ in range(P + 1)]
    ch = [[None] * (Q + 1) for _ in range(P + 1)]
    for p in range(1, P + 1):
        for q in range(1, Q + 1):
            best, c = 0, None
            if p == 2 and 2 <= q <= 8:
                best, c = q - 1, ("t",)
            elif q == 2 and 2 <= p <= 8:
                best, c = p - 1, ("t",)
            for a in range(1, p // 2 + 1):
                v = f[a][q] + f[p - a][q]
                if v > best:
                    best, c = v, ("r", a)
            for b in range(1, q // 2 + 1):
                v = f[p][b] + f[p][q - b]
                if v > best:
                    best, c = v, ("c", b)
            if p <= PW_MAX and q <= PW_MAX and best < value_ub(p, q):
                for h in range(1, min(PW_CENTER, p - 2) + 1):
                    for w in range(1, min(PW_CENTER, q - 2) + 1):
                        fc = f[h][w]
                        for a in range(1, p - h):
                            c2 = a + h
                            for d in range(1, q - w):
                                b = d + w
                                v = (f[a][b] + f[c2][q - b] + f[p - c2][q - d]
                                     + f[p - a][d] + fc)
                                if v > best:
                                    best, c = v, ("p", a, c2, b, d)
            f[p][q], ch[p][q] = best, c
    return f, ch

def place(ch, p, q):
    """List of (row, col, height, width) territories (2 x m or m x 2)."""
    res = []
    stack = [(p, q, 0, 0)]
    while stack:
        p, q, r0, c0 = stack.pop()
        if p <= 0 or q <= 0:
            continue
        c = ch[p][q]
        if c is None:
            continue
        if c[0] == "t":
            res.append((r0, c0, p, q))
        elif c[0] == "p":
            _, a, c2, b, d = c
            stack.append((a, b, r0, c0))
            stack.append((c2, q - b, r0, c0 + b))
            stack.append((p - c2, q - d, r0 + c2, c0 + d))
            stack.append((p - a, d, r0 + a, c0))
            stack.append((c2 - a, b - d, r0 + a, c0 + d))
        elif c[0] == "r":
            a = c[1]
            stack.append((a, q, r0, c0))
            stack.append((p - a, q, r0 + a, c0))
        else:
            b = c[1]
            stack.append((p, b, r0, c0))
            stack.append((p, q - b, r0, c0 + b))
    return res

def render(terrs, x, y):
    grid = [["."] * x for _ in range(y)]
    for r, c, h, w in terrs:
        if h == 2:   # horizontal territory, desk on its top row
            for k in range(w - 1):
                grid[r][c + k] = "X"
        else:        # vertical territory, desk on its left column
            for k in range(h - 1):
                grid[r + k][c] = "X"
    return ["".join(row) for row in grid]

def main():
    files = sorted(glob.glob("in_level-7_*.txt"))
    data = {}
    P = Q = 1
    for path in files:
        toks = open(path).read().split()
        n = int(toks[0])
        rooms = [tuple(int(t) for t in toks[1 + 3 * i: 4 + 3 * i]) for i in range(n)]
        data[path] = rooms
        for x, y, k in rooms:
            P, Q = max(P, y + 1), max(Q, x + 1)
    f, ch = build(P, Q)
    for path in files:
        out = []
        for x, y, k in data[path]:
            terrs = place(ch, y + 1, x + 1)
            grid = render(terrs, x, y)
            covered = sum(row.count("X") for row in grid)
            if covered != k:
                print("MISMATCH", path, x, y, "expected", k, "got", covered, file=sys.stderr)
            out += grid
            out.append("")
        name = os.path.basename(path)[3:-4]
        with open(name + ".out", "w") as fh:
            fh.write("\n".join(out) + "\n")

main()
