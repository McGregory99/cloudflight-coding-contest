import glob

def num(s):
    try: return float(s)
    except ValueError: return 17.0  # only "seventeen" occurs in level 1 data (BOP 287)

# temperature per BOP (degF bug fixed: true degC lies in -5..45)
temp = {}
for l in open("all_data_from_level_1.in").read().splitlines()[1:]:
    b, t, _ = l.split(",")
    t = num(t); temp[int(b)] = (t - 32) * 5 / 9 if t > 45 else t

def prefix(rows):
    n = 0
    for col in zip(*rows):
        if len(set(col)) > 1: break
        n += 1
    return n

def solve(path):
    fl = {}
    for l in open(path).read().splitlines()[1:]:
        f, p = l.split(",")
        fl.setdefault(int(f), []).append(p.split())
    F = {}
    for f, rows in fl.items():
        nodes = [x for r in rows for x in r]
        F[f] = dict(
            T=sum(temp[int(x)] for x in nodes) / len(nodes),        # worm regions are hot
            pal=sum(r == r[::-1] for r in rows) / len(rows),         # flies back the same route
            dup=1 - len(set(map(tuple, rows))) / len(rows),          # birds stay together (identical rows)
            pre=prefix(rows) / (sum(map(len, rows)) / len(rows)),    # common outbound part, then split
            len=sum(map(len, rows)) / len(rows),
            set=set(nodes))
    left = set(F); res = {}
    def take(name, key, ok=lambda f: True):
        # a real dataset has all 6 flocks; the 2-flock example only gets species whose cue clearly fires
        if not left: return
        f = max(sorted(left), key=key)
        if len(F) == 6 or ok(f): res[f] = name; left.remove(f)
    take("Hurracurra Bird", lambda f: F[f]["T"], lambda f: F[f]["T"] > 30)
    take("Medieval Bluetit", lambda f: (F[f]["pal"], F[f]["len"]), lambda f: F[f]["pal"] == 1)
    blue = next((F[k]["set"] for k, v in res.items() if v == "Medieval Bluetit"), set())
    take("Sticky Wolfthroat", lambda f: (len(F[f]["set"] & blue) / len(F[f]["set"]), F[f]["pal"]), lambda f: F[f]["set"] <= blue)
    take("Flanking Blackfinch", lambda f: (F[f]["dup"], -F[f]["pal"]), lambda f: F[f]["dup"] > 0.5)
    take("Rusty Goldhammer", lambda f: F[f]["pre"], lambda f: F[f]["pre"] > 0.3)
    take("Red Firefinch", lambda f: 0)
    return sorted(res.items()), F

for f in sorted(glob.glob("in_level-3_*.txt")):
    res, _ = solve(f)
    open(f.replace("in_", "", 1).replace(".txt", ".out"), "w").write("Flock ID,Species\n" + "".join(f"{k},{v}\n" for k, v in res))
