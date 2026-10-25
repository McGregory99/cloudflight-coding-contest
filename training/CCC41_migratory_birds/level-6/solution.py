"""Level 6: the 30 new days (761-790) are an exact time-reversal of days 760..731 (wind negated),
so the 'weird' regime simply keeps walking backwards: day 791 == day 730 (reflection sum 761+760)."""
import glob
N = 2500

def load(path):
    """-> {day: [arrivals by BOP]} (BOP rows are 1..2500 in order)"""
    days = {}
    with open(path) as f:
        f.readline()
        for l in f:
            p = l.split(",")
            days.setdefault(int(p[0]), []).append(float(p[2]) if p[2] != "missing" else float("nan"))
    return days

def top50(a):
    return sorted(range(N), key=lambda i: (-a[i], i))[:50]

def solve(path):
    new = load(path)
    hist = load("all_data_from_level_5.in")
    first, last = min(new), max(new)
    # reflection centre: new day first+k mirrors hist day first-1-k; verify on every given day
    mirror = all(new[first + k] == hist.get(first - 1 - k) for k in range(last - first + 1))
    target = last + 1
    if mirror:
        src = 2 * first - 1 - target  # = 730 for target 791
        pred = hist[src]
    else:  # fallback (not triggered on the contest data): persistence of the last known day
        pred = new[last]
    return f"Day,Top 50 Arrivals BOPs\n{target},{' '.join(str(i + 1) for i in top50(pred))}\n", mirror

for f in sorted(glob.glob("in_level-6_*.txt")):
    out, mirror = solve(f)
    open(f.replace("in_", "", 1).replace(".txt", ".out"), "w").write(out)
    print(f, "mirror detected:", mirror)
