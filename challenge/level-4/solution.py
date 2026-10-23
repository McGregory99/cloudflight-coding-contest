from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "outputs" / "level-4"

DIRS = {1: (0, 2), 2: (1, 1), 3: (1, -1), 4: (0, -2), 5: (-1, -1), 6: (-1, 1)}


def empty_board(r):
    rows = []
    for i in range(2 * r + 1):
        d = abs(i - r)
        if d == r:
            body = "*" + "-*" * r
        else:
            body = "*" + "-O" * (2 * r - 1 - d) + "-*"
        rows.append(list("-" * d + body + "-" * d))
    return rows


def ring(r):
    """Border cells (row, col) clockwise, starting at the left corner (emitter 1)."""
    cells = [(r, 0)]
    cells += [(i, r - i) for i in range(r - 1, -1, -1)]
    cells += [(0, r + 2 * j) for j in range(1, r + 1)]
    cells += [(i, 3 * r + i) for i in range(1, r + 1)]
    cells += [(i, 5 * r - i) for i in range(r + 1, 2 * r + 1)]
    cells += [(2 * r, 3 * r - 2 * j) for j in range(1, r + 1)]
    cells += [(i, i - r) for i in range(2 * r - 1, r, -1)]
    assert len(cells) == 6 * r
    return cells


def run(r, prog):
    grid = empty_board(r)
    cells = ring(r)
    n = len(cells)
    pos = [k * r for k in range(6)]
    active = [False] * 6
    for line in prog:
        for k, ins in enumerate(line):
            if ins == "F":
                pos[k] = (pos[k] + 1) % n
            elif ins == "B":
                pos[k] = (pos[k] - 1) % n
            elif ins == "T":
                active[k] = not active[k]
        hits = {}
        for k in range(6):
            if not active[k]:
                continue
            dr, dc = DIRS[k + 1]
            r2, c2 = cells[pos[k]][0] + dr, cells[pos[k]][1] + dc
            while 0 <= r2 < len(grid) and 0 <= c2 < len(grid[r2]) and grid[r2][c2] in "OM":
                hits[(r2, c2)] = hits.get((r2, c2), 0) + 1
                r2 += dr
                c2 += dc
        for (a, b), h in hits.items():
            if h == 2:
                grid[a][b] = "M"
            elif h >= 3:
                grid[a][b] = "O"
    return "\n".join("".join(row) for row in grid) + "\n\n"


def solve(text):
    t = text.split()
    n = int(t[0])
    p = 1
    out = []
    for _ in range(n):
        r, l = int(t[p]), int(t[p + 1])
        p += 2
        prog = [t[p + 6 * i:p + 6 * i + 6] for i in range(l)]
        p += 6 * l
        out.append(run(r, prog))
    return "".join(out)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(HERE.glob("in_level-4_*.txt")):
        name = f.name.replace("in_", "", 1).replace("txt", "out")
        if "0-example" in name:
            assert solve(f.read_text()) == (HERE / "out_level-4_0-example.txt").read_text(), "example mismatch"
            print("example OK")
            continue
        (OUT / name).write_text(solve(f.read_text()))
        print("wrote", name)
