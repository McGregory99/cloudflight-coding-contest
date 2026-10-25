from pathlib import Path
d = Path(__file__).parent
D = {"W": (0, -1), "D": (1, 0), "S": (0, 1), "A": (-1, 0)}
for f in sorted(d.glob("in_level-2_*.txt")):
    t = f.read_text().split()
    n = int(t[0])
    out = []
    for s in t[1:1 + n]:
        x = y = 0
        xs, ys = [0], [0]
        for c in s:
            dx, dy = D[c]
            x += dx; y += dy
            xs.append(x); ys.append(y)
        out.append(f"{max(xs)-min(xs)+1} {max(ys)-min(ys)+1}")
    (d / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out) + "\n")
