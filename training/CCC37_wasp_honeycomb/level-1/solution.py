from pathlib import Path

d = Path(__file__).parent
for f in sorted(d.glob("in_level-1_*.txt")):
    out = f.name.replace("in_", "", 1).replace(".txt", ".out")
    (d / out).write_text(f"{f.read_text().count('O')}\n")
