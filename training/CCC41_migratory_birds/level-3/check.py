import glob
S = set(open("level_3_species.in").read().split("\n")) - {""}
for f in sorted(glob.glob("in_level-3_*.txt")):
    ids = sorted({int(l.split(",")[0]) for l in open(f).read().splitlines()[1:]})
    o = open(f.replace("in_", "", 1).replace(".txt", ".out")).read().splitlines()
    assert o[0] == "Flock ID,Species"
    got = [l.split(",", 1) for l in o[1:]]
    assert [int(a) for a, _ in got] == ids and {b for _, b in got} == S and len(got) == 6 or f.endswith("0-example.txt"), f
    print("ok", f, dict((int(a), b) for a, b in got))
