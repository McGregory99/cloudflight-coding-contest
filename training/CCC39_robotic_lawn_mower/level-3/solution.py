from pathlib import Path
d = Path(__file__).parent
D = {"W": (0, -1), "D": (1, 0), "S": (0, 1), "A": (-1, 0)}

def valid(w, h, grid, path):
    free = sum(r.count(".") for r in grid)
    cells = [(0, 0)]
    x = y = 0
    for c in path:
        dx, dy = D[c]; x += dx; y += dy
        cells.append((x, y))
    if len(cells) != free or len(set(cells)) != len(cells):
        return False
    xs = [c[0] for c in cells]; ys = [c[1] for c in cells]
    bw = max(xs) - min(xs) + 1; bh = max(ys) - min(ys) + 1
    if bw > w or bh > h:
        return False
    for ox in range(-min(xs), w - max(xs)):  # start offset is free: the path has no given start
        for oy in range(-min(ys), h - max(ys)):
            if all(grid[cy + oy][cx + ox] == "." for cx, cy in cells):
                return True
    return False

for f in sorted(d.glob("in_level-3_*.txt")):
    t = f.read_text().split()
    n = int(t[0]); p = 1; out = []
    for _ in range(n):
        w, h = int(t[p]), int(t[p + 1]); p += 2
        grid = t[p:p + h]; p += h
        path = t[p]; p += 1
        out.append("VALID" if valid(w, h, grid, path) else "INVALID")
    (d / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out) + "\n")
