import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LIMIT = 100


def min_coins_table(coins):
    """dp[a] = fewest coins for amount a; last[a] = a coin used (smallest on ties)."""
    inf = float("inf")
    dp = [0] + [inf] * LIMIT
    last = [0] * (LIMIT + 1)
    for a in range(1, LIMIT + 1):
        for c in coins:  # ascending; strict '<' keeps the smallest coin on ties
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
                last[a] = c
    return last


def solve(text):
    tok = text.split()
    n, c = int(tok[0]), int(tok[1])
    pos = 2
    out = []
    for _ in range(n):
        coins = sorted(set(map(int, tok[pos:pos + c])))
        pos += c
        last = min_coins_table(coins)
        for amount in range(1, LIMIT + 1):
            cnt = {}
            a = amount
            while a:
                cnt[last[a]] = cnt.get(last[a], 0) + 1
                a -= last[a]
            out.append(" ".join("%dx%d" % (cnt[v], v) for v in sorted(cnt, reverse=True)))
    return "\n".join(out) + "\n"


def main():
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    for path in sorted(glob.glob(os.path.join(HERE, "input", "in_level-3_*.txt"))):
        suffix = os.path.basename(path)[len("in_level-3_"):-len(".txt")]
        with open(path) as f:
            res = solve(f.read())
        with open(os.path.join(HERE, "output", "level-3_%s.out" % suffix), "w") as f:
            f.write(res)


if __name__ == "__main__":
    main()
