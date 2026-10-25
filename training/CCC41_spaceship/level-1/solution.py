from pathlib import Path

D = Path(__file__).parent
for f in sorted(D.glob("in_level-1_*.txt")):
    lines = f.read_text().split("\n")
    n = int(lines[0])
    out = [str(sum(map(int, lines[1 + i].split()))) for i in range(n)]
    (D / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out) + "\n")
