import re
from pathlib import Path

d = Path(__file__).parent
bad = 0
for f in sorted(d.glob("in_level-1_*.txt")):
    exp = sum(1 for ch in re.sub(r"\s", "", f.read_text()) if ch == "O")
    got = (d / f.name.replace("in_", "", 1).replace(".txt", ".out")).read_text().split()
    ok = got == [str(exp)]
    bad += not ok
    print(f.name, "OK" if ok else f"FAIL exp={exp} got={got}")
raise SystemExit(bad)
