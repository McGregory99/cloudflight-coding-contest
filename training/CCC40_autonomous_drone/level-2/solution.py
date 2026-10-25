from pathlib import Path
d = Path(__file__).parent

def final_height(acc):
    v = h = 0
    for a in acc:
        v += a - 10
        h += v
    return h

for f in sorted(d.glob("in_level-2_*.txt")):
    L = f.read_text().split("\n")
    n = int(L[0])
    out = [str(final_height(map(int, L[1 + i].split()))) for i in range(n)]
    (d / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out) + "\n")
