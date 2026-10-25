import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
INF = 10 ** 18


class Currency:
    """Bounded fewest-coins solver for one currency (see NOTES.md for the proof sketch).

    Optimal solutions satisfy an exchange property: a coin type that is not
    "nearly saturated" (deficit u-x >= Vmax) forces every smaller type to be used
    fewer than (its value) times. So there is at most one "free" type j; types
    above j are within Vmax-1 of their inventory; types below j are used < v_j times.
    Everything except the free type is a small bounded knapsack over
    "extra" coins y_i, solved once per currency, and each amount is answered by
    a lookup in the residue class of the free type.
    """

    def __init__(self, inv):
        inv = sorted(inv, key=lambda p: p[1])  # (count, value) ascending value
        self.u = [p[0] for p in inv]
        self.v = [p[1] for p in inv]
        self.k = len(inv)
        vmax = self.v[-1]
        self.cases = []
        for j in list(range(self.k)) + [None]:
            self.cases.append(self._build(j, vmax))

    def _build(self, j, vmax):
        k, u, v = self.k, self.u, self.v
        base = [0] * k
        ym = [0] * k
        items = []  # (type index, max extra, value)
        for i in range(k):
            if i == j:
                continue
            if j is None or i > j:
                dm = min(u[i], vmax - 1)
                base[i] = u[i] - dm
                ym[i] = dm
            else:
                ym[i] = min(u[i], v[j] - 1)
            items.append(i)
        size = sum(ym[i] * v[i] for i in items) + 1
        layers = [[0] + [INF] * (size - 1)]
        for i in items:
            old = layers[-1]
            new = old[:]
            w = v[i]
            for c in range(1, ym[i] + 1):
                sh = c * w
                if sh >= size:
                    break
                new[sh:] = [x if x <= y + c else y + c for x, y in zip(new[sh:], old)]
            layers.append(new)
        g = layers[-1]
        base_cnt = sum(base)
        base_val = sum(base[i] * v[i] for i in range(k))
        lists = None
        if j is not None:
            vj = v[j]
            lists = [[] for _ in range(vj)]
            for s in range(size):
                if g[s] < INF:
                    lists[s % vj].append((vj * g[s] - s, s))
            for lst in lists:
                lst.sort()
        return {"j": j, "base": base, "ym": ym, "items": items, "layers": layers,
                "g": g, "base_cnt": base_cnt, "base_val": base_val, "lists": lists}

    def solve(self, t):
        best = None
        for case in self.cases:
            j = case["j"]
            r = t - case["base_val"]
            if r < 0:
                continue
            if j is None:
                if r < len(case["g"]) and case["g"][r] < INF:
                    total = case["base_cnt"] + case["g"][r]
                    if best is None or total < best[0]:
                        best = (total, case, r, 0)
                continue
            vj = self.v[j]
            lo = r - vj * self.u[j]
            for _, s in case["lists"][r % vj]:
                if lo <= s <= r:
                    xj = (r - s) // vj
                    total = case["base_cnt"] + case["g"][s] + xj
                    if best is None or total < best[0]:
                        best = (total, case, s, xj)
                    break
        if best is None:
            raise ValueError("amount %d cannot be built" % t)
        _, case, s, xj = best
        cnt = {}
        base, items, layers, v = case["base"], case["items"], case["layers"], self.v
        y = {}
        for pos in range(len(items) - 1, -1, -1):
            i = items[pos]
            prev, cur = layers[pos], layers[pos + 1]
            for c in range(case["ym"][i] + 1):
                sh = c * v[i]
                if sh > s:
                    break
                if prev[s - sh] + c == cur[s]:
                    y[i] = c
                    s -= sh
                    break
        for i in range(self.k):
            n = base[i] + y.get(i, 0)
            if i == case["j"]:
                n = xj
            if n:
                cnt[v[i]] = n
        return " ".join("%dx%d" % (cnt[x], x) for x in sorted(cnt, reverse=True))


def solve(text):
    tok = text.split()
    n, c, a = int(tok[0]), int(tok[1]), int(tok[2])
    pos = 3
    out = []
    for _ in range(n):
        inv = []
        for s in tok[pos:pos + c]:
            cnt, val = s.split("x")
            inv.append((int(cnt), int(val)))
        pos += c
        amounts = tok[pos:pos + a]
        pos += a
        cur = Currency(inv)
        for s in amounts:
            out.append(cur.solve(int(s)))
    return "\n".join(out) + "\n"


def main():
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    for path in sorted(glob.glob(os.path.join(HERE, "input", "in_level-5_*.txt"))):
        suffix = os.path.basename(path)[len("in_level-5_"):-len(".txt")]
        with open(path) as f:
            res = solve(f.read())
        with open(os.path.join(HERE, "output", "level-5_%s.out" % suffix), "w") as f:
            f.write(res)


if __name__ == "__main__":
    main()
