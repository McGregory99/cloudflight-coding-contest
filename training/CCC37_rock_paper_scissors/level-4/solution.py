import glob
import os
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INPUT_DIR = HERE / "input"
OUTPUT_DIR = HERE / "output"

# ---- configuration (per level) -------------------------------------------
STYLES = "RPS"
# BEATS[a] = styles that a beats
BEATS = {'R': 'S', 'P': 'R', 'S': 'P'}
LEVEL = 4
ROUNDS_LIMIT = None  # None = full tournament, int = only that many rounds
# ---------------------------------------------------------------------------

K = len(STYLES)
IDX = {c: i for i, c in enumerate(STYLES)}
S = IDX["S"]
WIN = [[0] * K for _ in range(K)]
for _a in STYLES:
    for _b in STYLES:
        WIN[IDX[_a]][IDX[_b]] = IDX[_a] if (_a == _b or _b in BEATS[_a]) else IDX[_b]
PAIRS = [(a, b) for a in range(K) for b in range(a, K)]
ENEMY = [IDX[c] for c in STYLES if "S" in BEATS[c]]  # styles that beat S


def next_counts(cnt, match):
    nxt = [0] * K
    for (a, b), x in match.items():
        nxt[WIN[a][b]] += x
    return tuple(nxt)


def heuristic_order():
    """Pair types ordered so that enemies of S get eliminated first."""
    def key(p):
        a, b = p
        w = WIN[a][b]
        if a != b and (a in ENEMY) != (b in ENEMY) and w not in ENEMY:
            return 0  # friend kills enemy
        if a != b and a in ENEMY and b in ENEMY:
            return 1  # enemy vs enemy: net -1 enemy
        if a == b and a in ENEMY:
            return 2  # enemy halving
        if a == b:
            return 3  # friendly ties
        if w == S:
            return 4  # S eats someone
        return 5
    return sorted(PAIRS, key=key)


HEUR = heuristic_order()


def build_matching(cnt, order, fracs):
    c = list(cnt)
    match = {}
    for p, frac in zip(order, fracs):
        a, b = p
        m = c[a] // 2 if a == b else min(c[a], c[b])
        t = m if frac is None else int(m * frac + 0.5)
        if t > 0:
            if a == b:
                c[a] -= 2 * t
            else:
                c[a] -= t
                c[b] -= t
            match[p] = match.get(p, 0) + t
    for p in order:  # completion pass: pair up whatever is left
        a, b = p
        m = c[a] // 2 if a == b else min(c[a], c[b])
        if m > 0:
            if a == b:
                c[a] -= 2 * m
            else:
                c[a] -= m
                c[b] -= m
            match[p] = match.get(p, 0) + m
    return match


def candidates(cnt, rng, tries):
    yield build_matching(cnt, HEUR, [None] * len(HEUR))
    seen = set()
    for t in range(tries):
        if t % 2 == 0:
            order = HEUR[:]
            # light perturbation of the heuristic order
            for _ in range(rng.randint(0, 4)):
                i = rng.randrange(len(order))
                j = rng.randrange(len(order))
                order[i], order[j] = order[j], order[i]
        else:
            order = PAIRS[:]
            rng.shuffle(order)
        fracs = [rng.choice((None, None, 0.0, 0.5, rng.random())) for _ in order]
        m = build_matching(cnt, order, fracs)
        key = tuple(sorted(m.items()))
        if key in seen:
            continue
        seen.add(key)
        yield m


def goal(cnt):
    if ROUNDS_LIMIT is None:
        return cnt[S] == 1 and sum(cnt) == 1
    return all(cnt[i] == 0 for i in ENEMY) and cnt[S] >= 1


def search(cnt, rounds_left, rng, failed, tries):
    if rounds_left == 0:
        return [] if goal(cnt) else None
    if cnt[S] == 0:
        return None
    key = (cnt, rounds_left)
    if key in failed:
        return None
    for m in candidates(cnt, rng, tries):
        nxt = next_counts(cnt, m)
        if nxt[S] == 0:
            continue
        sub = search(nxt, rounds_left - 1, rng, failed, tries)
        if sub is not None:
            return [m] + sub
    failed.add(key)
    return None


def materialize(styles_counts, plan):
    buckets = [[] for _ in range(K)]
    for i, c in enumerate(styles_counts):
        buckets[i] = [STYLES[i]] * c
    for match in plan:
        nb = [[] for _ in range(K)]
        for (a, b), x in match.items():
            la, lb = buckets[a], buckets[b]
            for _ in range(x):
                if a == b:
                    u = la.pop()
                    v = la.pop()
                else:
                    u = la.pop()
                    v = lb.pop()
                nb[WIN[a][b]].append(u + v)
        buckets = nb
    return "".join("".join(b) for b in buckets)


def solve_one(cnt, m):
    rounds = m.bit_length() - 1
    if ROUNDS_LIMIT is not None:
        rounds = ROUNDS_LIMIT
    rng = random.Random(12345)
    tries = 8
    while True:
        failed = set()
        plan = search(tuple(cnt), rounds, rng, failed, tries)
        if plan is not None:
            return materialize(cnt, plan)
        tries *= 2
        if tries > 4096:
            raise RuntimeError("no solution found for %r" % (cnt,))


def parse(text):
    lines = text.split("\n")
    n, m = map(int, lines[0].split())
    res = []
    for i in range(1, n + 1):
        tok = lines[i].split()
        cnt = [0] * K
        for t in tok:
            cnt[IDX[t[-1]]] = int(t[:-1])
        res.append(cnt)
    return m, res


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    for path in sorted(glob.glob(str(INPUT_DIR / ("in_level-%d_*.txt" % LEVEL)))):
        suffix = os.path.basename(path)[len("in_level-%d_" % LEVEL):-len(".txt")]
        with open(path) as f:
            m, tests = parse(f.read())
        out = [solve_one(c, m) for c in tests]
        with open(OUTPUT_DIR / ("level-%d_%s.out" % (LEVEL, suffix)), "w") as f:
            f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
