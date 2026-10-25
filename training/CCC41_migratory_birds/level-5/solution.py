"""Level 5: forecast the top-50 arrival BOPs for each of the 30 missing days.
Ensemble (normalised score sum) of three forecasts that all use the *known* future occupancy:
  graph  - departures dep(d)=arr(d)-(occ(d)-occ(d-1)) are re-distributed along the migration graph (edges = consecutive BOPs of the level-4 paths),
           arrivals(d+1) = sum over edges dep(d,a)/outdeg(a). Total departures == total next-day arrivals exactly in the data.
  ar     - autoregression arr(d)=c0+c1*arr(d-1)+c2*(occ(d)-occ(d-1))+c3*occ(d-1), rolled forward (coefficients by OLS on history)
  occ    - last known arrivals scaled by occupancy(d)/occupancy(last)
No numpy on this machine, everything is plain python lists."""
import array, glob

N = 2500

def load(path):
    arr = array.array("f"); occ = array.array("f")
    with open(path) as f:
        f.readline()
        for l in f:
            p = l.split(",")
            arr.append(float(p[2]) if p[2] != "missing" else float("nan")); occ.append(float(p[3]))
    return arr, occ

def solve_lin(A, b):
    n = len(A); M = [A[i][:] + [b[i]] for i in range(n)]
    for i in range(n):
        p = max(range(i, n), key=lambda r: abs(M[r][i])); M[i], M[p] = M[p], M[i]
        for r in range(n):
            if r != i:
                f = M[r][i] / M[i][i]
                for c in range(i, n + 1): M[r][c] -= f * M[i][c]
    return [M[i][n] / M[i][i] for i in range(n)]

def edges_out():
    out = {}
    seen = set()
    for l in open("all_data_from_level_4.in").read().splitlines()[1:]:
        p = l.split(",")[1].split()
        for a, b in zip(p, p[1:]):
            e = (int(a) - 1, int(b) - 1)
            if e not in seen:
                seen.add(e); out.setdefault(e[0], []).append(e[1])
    return out

def norm(v):
    s = sum(v) / len(v); return [x / s for x in v]

def solve(path):
    arr, occ = load(path)
    D = lambda col, d: col[(d - 1) * N: d * N]
    nd = len(arr) // N
    known = [d for d in range(1, nd + 1) if D(arr, d)[0] == D(arr, d)[0]]  # not NaN
    T = max(known); days = list(range(T + 1, nd + 1)); H = len(days)
    out = edges_out()

    # AR coefficients on known history
    k = 4; A = [[0.0] * k for _ in range(k)]; bb = [0.0] * k
    for d in range(2, T + 1, 3):
        a1 = D(arr, d - 1); o1 = D(occ, d - 1); o0 = D(occ, d); y = D(arr, d)
        for i in range(N):
            x = (1.0, a1[i], o0[i] - o1[i], o1[i])
            for p in range(k):
                bb[p] += x[p] * y[i]
                for q in range(p, k): A[p][q] += x[p] * x[q]
    for p in range(k):
        for q in range(p): A[p][q] = A[q][p]
    w = solve_lin(A, bb)

    preds = []  # per method: list of H score vectors
    a = list(D(arr, T)); g = []
    for d in days:  # graph rollout: day d arrivals from departures of day d-1
        pass
    ah = list(D(arr, T))
    for d in days:
        o1 = D(occ, d - 2); o0 = D(occ, d - 1)  # dep of day d-1 needs occ(d-1)-occ(d-2)
        dep = [max(0.0, ah[i] - (o0[i] - o1[i])) for i in range(N)]
        new = [0.0] * N
        for s, lst in out.items():
            share = dep[s] / len(lst)
            if share:
                for b in lst: new[b] += share
        ah = new; g.append(ah)
    ar = []; ah = list(D(arr, T))
    for d in days:
        o1 = D(occ, d - 1); o0 = D(occ, d)
        ah = [w[0] + w[1] * ah[i] + w[2] * (o0[i] - o1[i]) + w[3] * o1[i] for i in range(N)]
        ar.append(ah)
    aT = D(arr, T); oT = D(occ, T)
    oc = [[aT[i] * D(occ, d)[i] / max(oT[i], 1.0) for i in range(N)] for d in days]

    res = []
    for h, d in enumerate(days):
        s = [x + 0.5 * y + 0.5 * z for x, y, z in zip(norm(g[h]), norm(ar[h]), norm(oc[h]))]
        res.append((d, sorted(range(N), key=lambda i: (-s[i], i))[:50]))
    return res

for f in sorted(glob.glob("in_level-5_*.txt")):
    res = solve(f)
    open(f.replace("in_", "", 1).replace(".txt", ".out"), "w").write(
        "Day,Top 50 Arrivals BOPs\n" + "".join(f"{d},{' '.join(str(i + 1) for i in t)}\n" for d, t in res))
