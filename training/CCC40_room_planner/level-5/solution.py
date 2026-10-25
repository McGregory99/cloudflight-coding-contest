import glob, os, sys

# Non-touching straight desks of length L in a W x H room.
# Territory trick: a desk of length L owns a 2 x (L+1) block (desk + 1 gap cell on
# the far side and 1 gap row/col). Disjoint territories in the (H+1) x (W+1) box
# <=> non-touching desks (8-neighbourhood). So: pack 2 x m (m=L+1) rectangles
# (both orientations) into a (H+1) x (W+1) box, maximising their count.
# Guillotine DP with homogeneous-block base cases.

PW_MAX = 22   # pinwheel (non-guillotine) blocks only tried for boxes up to this size
PW_CENTER = 6  # max side of the pinwheel's centre block

def build(P, Q, m):
    f = [[0] * (Q + 1) for _ in range(P + 1)]
    ch = [[None] * (Q + 1) for _ in range(P + 1)]
    for p in range(1, P + 1):
        for q in range(1, Q + 1):
            hb = (p // 2) * (q // m)   # territories 2 rows x m cols (horizontal desk)
            vb = (p // m) * (q // 2)   # territories m rows x 2 cols (vertical desk)
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
            if p <= PW_MAX and q <= PW_MAX and best < (p * q) // (2 * m):
                # five-block (pinwheel) split: blocks around a small centre (h x w)
                #   B1 = a x b (top-left)      B2 = c x (q-b)   (top-right)
                #   B3 = (p-c) x (q-d) (bottom-right)   B4 = (p-a) x d (bottom-left)
                #   centre = (c-a) x (b-d)
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

def place(ch, p, q, m):
    """List of (row, col, horizontal?) territory origins."""
    res = []
    stack = [(p, q, 0, 0)]
    while stack:
        p, q, r0, c0 = stack.pop()
        if p <= 0 or q <= 0:
            continue
        c = ch[p][q]
        if c is None:
            continue
        if c[0] == "h":
            for i in range(p // 2):
                for j in range(q // m):
                    res.append((r0 + 2 * i, c0 + m * j, True))
        elif c[0] == "v":
            for i in range(p // m):
                for j in range(q // 2):
                    res.append((r0 + m * i, c0 + 2 * j, False))
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

def render(terrs, x, y, L):
    grid = [["."] * x for _ in range(y)]
    for r, c, hor in terrs:
        for k in range(L):
            if hor:
                grid[r][c + k] = "X"
            else:
                grid[r + k][c] = "X"
    return ["".join(row) for row in grid]

LEVEL, L = 5, 2

def main():
    files = sorted(glob.glob(f"in_level-{LEVEL}_*.txt"))
    data = {}
    P = Q = 1
    for path in files:
        toks = open(path).read().split()
        n = int(toks[0])
        rooms = [tuple(int(t) for t in toks[1 + 3 * i: 4 + 3 * i]) for i in range(n)]
        data[path] = rooms
        for x, y, k in rooms:
            P, Q = max(P, y + 1), max(Q, x + 1)
    f, ch = build(P, Q, L + 1)
    for path in files:
        out = []
        for x, y, k in data[path]:
            terrs = place(ch, y + 1, x + 1, L + 1)
            if len(terrs) != k:
                print("MISMATCH", path, x, y, "expected", k, "got", len(terrs), file=sys.stderr)
            out += render(terrs, x, y, L)
            out.append("")
        name = os.path.basename(path)[3:-4]
        with open(name + ".out", "w") as fh:
            fh.write("\n".join(out) + "\n")

main()
