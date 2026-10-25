from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "outputs" / "level-5"

DIRS = {1: (0, 2), 2: (1, 1), 3: (1, -1), 4: (0, -2), 5: (-1, -1), 6: (-1, 1)}
NEIGH = [(0, 2), (0, -2), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def ring(r):
    """Border cells (row, col) clockwise, starting at the left corner (emitter 1)."""
    cells = [(r, 0)]
    cells += [(i, r - i) for i in range(r - 1, -1, -1)]
    cells += [(0, r + 2 * j) for j in range(1, r + 1)]
    cells += [(i, 3 * r + i) for i in range(1, r + 1)]
    cells += [(i, 5 * r - i) for i in range(r + 1, 2 * r + 1)]
    cells += [(2 * r, 3 * r - 2 * j) for j in range(1, r + 1)]
    cells += [(i, i - r) for i in range(2 * r - 1, r, -1)]
    return cells


def run(r, pattern_rows, prog):
    pat = {(i, j) for i, row in enumerate(pattern_rows) for j, ch in enumerate(row) if ch == "M"}
    # playable cells: O cells of an empty board
    play = set()
    for i in range(2 * r + 1):
        d = abs(i - r)
        if d != r:
            for k in range(2 * r - 1 - d):
                play.add((i, d + 2 + 2 * k))
    matter = set()
    cells = ring(r)
    n = len(cells)
    pos = [k * r for k in range(6)]
    active = [False] * 6
    count = 0
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
            a, b = cells[pos[k]][0] + dr, cells[pos[k]][1] + dc
            while (a, b) in play:
                hits[(a, b)] = hits.get((a, b), 0) + 1
                a += dr
                b += dc
        for c, h in hits.items():
            if h == 2:
                matter.add(c)
            elif h >= 3:
                matter.discard(c)
        if pat and pat <= matter:
            if all(not ((p[0] + dr, p[1] + dc) in matter and (p[0] + dr, p[1] + dc) not in pat)
                   for p in pat for dr, dc in NEIGH):
                matter -= pat
                count += 1
    return count


def solve(text):
    t = text.split()
    n = int(t[0])
    p = 1
    out = []
    for _ in range(n):
        r, rows = int(t[p]), int(t[p + 1])
        pat = t[p + 3:p + 3 + rows]
        p += 3 + rows
        l = int(t[p])
        p += 1
        prog = [t[p + 6 * i:p + 6 * i + 6] for i in range(l)]
        p += 6 * l
        out.append(f"{run(r, pat, prog)}\n")
    return "".join(out)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(HERE.glob("in_level-5_*.txt")):
        name = f.name.replace("in_", "", 1).replace("txt", "out")
        if "0-example" in name:
            assert solve(f.read_text()) == (HERE / "out_level-5_0-example.txt").read_text(), "example mismatch"
            print("example OK")
            continue
        (OUT / name).write_text(solve(f.read_text()))
        print("wrote", name)
