import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def build_table(coins):
    """Fewest-coins DP for amounts 0 .. M*M + M - 1 (M = largest coin)."""
    m = coins[-1]
    size = m * m + m
    inf = float("inf")
    dp = [0] + [inf] * (size - 1)
    last = [0] * size
    for a in range(1, size):
        best = inf
        bc = 0
        for c in coins:  # ascending, strict '<' -> smallest coin on ties
            if c > a:
                break
            v = dp[a - c] + 1
            if v < best:
                best = v
                bc = c
        dp[a] = best
        last[a] = bc
    return last


def construct(amount, coins, last):
    m = coins[-1]
    base = m * m
    cnt = {}
    if amount >= base + m:
        k = (amount - base) // m  # for x >= M^2 an optimal solution uses a largest coin
        amount -= k * m
        cnt[m] = k
    while amount:
        c = last[amount]
        cnt[c] = cnt.get(c, 0) + 1
        amount -= c
    return " ".join("%dx%d" % (cnt[v], v) for v in sorted(cnt, reverse=True))


def solve(text):
    tok = text.split()
    n, c, a = int(tok[0]), int(tok[1]), int(tok[2])
    pos = 3
    out = []
    for _ in range(n):
        coins = sorted(set(map(int, tok[pos:pos + c])))
        pos += c
        amounts = tok[pos:pos + a]
        pos += a
        last = build_table(coins)
        for s in amounts:
            out.append(construct(int(s), coins, last))
    return "\n".join(out) + "\n"


def main():
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    for path in sorted(glob.glob(os.path.join(HERE, "input", "in_level-4_*.txt"))):
        suffix = os.path.basename(path)[len("in_level-4_"):-len(".txt")]
        with open(path) as f:
            res = solve(f.read())
        with open(os.path.join(HERE, "output", "level-4_%s.out" % suffix), "w") as f:
            f.write(res)


if __name__ == "__main__":
    main()
