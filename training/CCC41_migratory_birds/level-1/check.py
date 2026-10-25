import glob, re
for f in sorted(glob.glob("in_level-1_*.txt")):
    o = open(f.replace("in_", "", 1).replace(".txt", ".out")).read()
    ids = [int(l.split(",")[0]) for l in open(f).read().splitlines()[1:] if l.strip()]
    got = o.split(" ")
    assert o == o.strip() and re.fullmatch(r"\d+( \d+)*", o), f
    assert sorted(map(int, got)) == sorted(ids), f
    print("ok", f, len(ids))
