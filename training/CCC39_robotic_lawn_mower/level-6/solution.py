import sys
from pathlib import Path
d = Path(__file__).parent
sys.path.insert(0, str(d))
import lawn

for f in sorted(d.glob("in_level-6""_*.txt")):
    out = []
    for w, h, g in lawn.parse(f.read_text()):
        r = lawn.solve(w, h, g, "cycle")
        assert r is not None, (f.name, w, h)
        out.append(r)
    (d / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out) + "\n")
