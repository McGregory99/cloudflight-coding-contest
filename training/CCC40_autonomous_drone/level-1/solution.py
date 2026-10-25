from pathlib import Path
d = Path(__file__).parent
for f in sorted(d.glob("in_level-1_*.txt")):
    L = f.read_text().split("\n")
    n = int(L[0])
    out = [str(sum(map(int, L[1 + i].split()))) for i in range(n)]
    (d / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out) + "\n")
