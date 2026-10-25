from pathlib import Path

D = Path(__file__).parent
for f in sorted(D.glob("in_level-2_*.txt")):
    lines = f.read_text().split("\n")
    n = int(lines[0])
    out = []
    for i in range(n):
        ps = list(map(int, lines[1 + i].split()))
        pos = sum((p > 0) - (p < 0) for p in ps)  # a pace moves one unit in its direction, 0 stands still
        time = sum(max(1, abs(p)) for p in ps)  # pace 0 still costs 1 tick
        out.append(f"{pos} {time}")
    (D / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out) + "\n")
