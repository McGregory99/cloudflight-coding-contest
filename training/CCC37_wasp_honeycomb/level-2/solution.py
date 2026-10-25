from pathlib import Path

DIRS = [(0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def blocks(text):
    """Split the file after the first line into blank-line separated blocks."""
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
    r, c = find_wasp(g)
    return sum(inside(g, r + dr, c + dc) and g[r + dr][c + dc] == "O" for dr, dc in DIRS)


def main():
    d = Path(__file__).parent
    for f in sorted(d.glob("in_level-2_*.txt")):
        out = f.name.replace("in_", "", 1).replace(".txt", ".out")
        (d / out).write_text("".join(f"{solve(g)}\n" for g in blocks(f.read_text())))


if __name__ == "__main__":
    main()
