import glob, re
for f in sorted(glob.glob("in_level-2_*.txt")):
    miss = [l.split(",")[0] for l in open(f).read().splitlines()[1:] if l.endswith("missing")]
    o = open(f.replace("in_", "", 1).replace(".txt", ".out")).read().splitlines()
    assert o[0] == "BOP,Bird Love Score [<3]"
    assert [l.split(",")[0] for l in o[1:]] == miss, f
    assert all(re.fullmatch(r"\d+,-?\d+\.\d\d", l) for l in o[1:]), f
    vals = [float(l.split(",")[1]) for l in o[1:]]
    assert all(0 <= v <= 100 for v in vals), (f, min(vals), max(vals))
    print("ok", f, len(miss), round(min(vals),1), round(max(vals),1))
