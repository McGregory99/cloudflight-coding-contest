from pathlib import Path

HERE = Path(__file__).parent
G = 10      # gravity
A = 10      # max change of a velocity component per tick when hovering (ay = 10 + dvy)


def smin(u):
    """Minimal remaining sum when braking from speed u down to 0 in steps of A."""
    k = (u - 1) // A
    return k * u - A * k * (k + 1) // 2


def rt(S):
    """Rest-to-rest speed profile: speeds s_1..s_n >= 0 (s_0 = 0, |ds| <= A, sum = S), a final 0 is implied.
    Greedy: at each tick take the largest speed that still leaves a feasible braking tail."""
    out = []
    u, R = 0, S
    while not (R == 0 and u <= A):
        lo, hi = max(0, u - A), min(u + A, R)
        a, b = lo, hi
        while a < b:                       # R-u'-smin(u') is decreasing in u'
            mid = (a + b + 1) // 2
            if R - mid >= smin(mid):
                a = mid
            else:
                b = mid - 1
        out.append(a)
        u, R = a, R - a
    return out


def ascent(H):
    """ay list: from ground to apex height exactly H (>=1) with vy = 0 at the apex."""
    seq = [0] + rt(H) + [0]
    return [G + seq[i + 1] - seq[i] for i in range(len(seq) - 1)]


def descent(R):
    """ay list: from hover (vy=0) descend R (>=1) and land with vy = -1."""
    seq = [0] + [-s for s in rt(R - 1)] + [-1]
    return [G + seq[i + 1] - seq[i] for i in range(len(seq) - 1)]


def horizontal(D):
    """(ax, ay) list: move D (signed) at hover (ay=10) from rest to rest."""
    if D == 0:
        return []
    sg = 1 if D > 0 else -1
    seq = [0] + rt(abs(D)) + [0]
    return [(sg * (seq[i + 1] - seq[i]), G) for i in range(len(seq) - 1)]


def fmt(accs):
    return " ".join(f"{ax},{ay}" for ax, ay in accs)



def solve(X, Hmin, limit):
    """Three phases: vertical ascent to hover, horizontal move at hover, vertical landing."""
    H = max(Hmin, 1)
    accs = [(0, ay) for ay in ascent(H)] + horizontal(X) + [(0, ay) for ay in descent(H)]
    assert len(accs) <= limit, (X, Hmin, limit, len(accs))
    return accs


def main():
    for f in sorted(HERE.glob("in_level-4_*.txt")):
        t = f.read_text().split()
        n = int(t[0])
        out = []
        for i in range(n):
            x, h, lim = map(int, t[1 + 3 * i: 4 + 3 * i])
            out.append(fmt(solve(x, h, lim)))
        (HERE / f.name.replace("in_", "").replace(".txt", ".out")).write_text("\n".join(out) + "\n")


main()
