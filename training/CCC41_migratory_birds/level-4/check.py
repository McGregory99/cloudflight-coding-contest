import glob, collections
S = {l for l in open("level_4_species.in").read().splitlines() if l}
for f in sorted(glob.glob("in_level-4_*.txt")):
    miss = sorted({int(l.split(",")[0]) for l in open(f).read().splitlines()[1:] if l.endswith(",missing")})
    o = open(f.replace("in_", "", 1).replace(".txt", ".out")).read().splitlines()
    assert o[0] == "Flock ID,Species"
    got = [l.split(",") for l in o[1:]]
    assert [int(a) for a, _ in got] == miss and all(b in S for _, b in got), f
    print("ok", f, len(got), dict(collections.Counter(b for _, b in got)))
