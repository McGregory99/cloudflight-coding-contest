from pathlib import Path

DIRS = [(0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def blocks(text):
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
    return res


def inside(g, r, c):
    return 0 <= r < len(g) and 0 <= c < len(g[r])


def find_wasp(g):
    for r, row in enumerate(g):
        c = row.find("W")
        if c >= 0:
            return r, c


def solve(g):
    """BFS over O cells; FREE if any reached cell has a neighbour outside the grid."""
    start = find_wasp(g)
    seen, stack = {start}, [start]
    while stack:
        r, c = stack.pop()
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if not inside(g, nr, nc):
                return "FREE"
            if g[nr][nc] == "O" and (nr, nc) not in seen:
                seen.add((nr, nc))
                stack.append((nr, nc))
    return "TRAPPED"


def main():
    d = Path(__file__).parent
    for f in sorted(d.glob("in_level-4_*.txt")):
        out = f.name.replace("in_", "", 1).replace(".txt", ".out")
        (d / out).write_text("".join(f"{solve(g)}\n" for g in blocks(f.read_text())))


if __name__ == "__main__":
    main()
