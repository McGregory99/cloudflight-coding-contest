from pathlib import Path
d = Path(__file__).parent
for f in sorted(d.glob("in_level-1_*.txt")):
    t = f.read_text().split()
    n = int(t[0])
    out = [" ".join(str(s.count(c)) for c in "WDSA") for s in t[1:1 + n]]
    (d / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out) + "\n")
