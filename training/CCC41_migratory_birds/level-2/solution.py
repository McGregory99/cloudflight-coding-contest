import glob, os, random, math

def solve_lin(A, b):
    n = len(A); M = [r[:] + [b[i]] for i, r in enumerate(A)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i])); M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                for c in range(i, n + 1): M[r][c] -= f * M[i][c]
    return [M[i][n] / M[i][i] for i in range(n)]

def fit(X, y, lam=1e-6):  # ridge via normal equations (no numpy on this box)
    k = len(X[0])
    A = [[sum(x[i] * x[j] for x in X) + (lam if i == j else 0) for j in range(k)] for i in range(k)]
    return solve_lin(A, [sum(x[i] * t for x, t in zip(X, y)) for i in range(k)])

W = dict(zip("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split(), range(20)))
T = dict(zip("twenty thirty forty fifty sixty seventy eighty ninety".split(), range(20, 100, 10)))
def num(s):
    try: return float(s)
    except ValueError: return float(sum(W[p] if p in W else T[p] for p in s.lower().replace("-", " ").split()))

# level-1 table: temperature (degF bug fixed: true degC lies in -5..45) and humidity per BOP
weather = {}
for l in open("all_data_from_level_1.in").read().splitlines()[1:]:
    b, t, h = l.split(",")
    t = num(t); t = (t - 32) * 5 / 9 if t > 45 else t
    weather[int(b)] = (t, float(h))

def feat(b, v): return [1, v[0], v[1], v[2], weather[b][0], weather[b][1]]

files = sorted(glob.glob("in_level-2_*.txt"))
data, rows = {}, {}
for f in files:
    rows[f] = []
    for l in open(f).read().splitlines()[1:]:
        p = l.split(",")
        b = int(p[0]); v = [float(x) for x in p[1:4]]
        rows[f].append((b, v, p[4]))
        if p[4] != "missing": data[b] = (v, float(p[4]))

# train once on every labelled row of every input file (they are disjoint BOPs of the same 2500)
X = [feat(b, v) for b, (v, y) in data.items()]; Y = [y for v, y in data.values()]
w = fit(X, Y)

def cv(folds=5):
    ids = list(data); random.seed(0); random.shuffle(ids); se = 0
    for k in range(folds):
        te = ids[k::folds]; tr = [i for j, i in enumerate(ids) if j % folds != k]
        wk = fit([feat(b, data[b][0]) for b in tr], [data[b][1] for b in tr])
        se += sum((sum(a * c for a, c in zip(wk, feat(b, data[b][0]))) - data[b][1]) ** 2 for b in te)
    return math.sqrt(se / len(ids))

for f in files:
    out = ["BOP,Bird Love Score [<3]"]
    for b, v, s in rows[f]:
        if s == "missing":
            # same BOP labelled in another input file -> use it, else predict
            y = data[b][1] if b in data else sum(a * c for a, c in zip(w, feat(b, v)))
            out.append(f"{b},{y:.2f}")
    open(f.replace("in_", "", 1).replace(".txt", ".out"), "w").write("\n".join(out) + "\n")

if os.environ.get("CV"): print("5-fold CV RMSE", cv())
