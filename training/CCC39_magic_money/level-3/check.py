"""Validate level-3_*.out: sums are right, coins exist, and coin counts are minimal (independent DP)."""
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def check(inp, out):
    tok = inp.split()
    n, c = int(tok[0]), int(tok[1])
    lines = out.split("\n")
    assert lines[-1] == "" and len(lines) == n * 100 + 1, "line count"
    pos, li = 2, 0
    for _ in range(n):
        coins = list(map(int, tok[pos:pos + c]))
        pos += c
        dp = [0] + [10 ** 9] * 100
        for a in range(1, 101):
            dp[a] = min(dp[a - x] + 1 for x in coins if x <= a)
        for amount in range(1, 101):
            tot = cnt = 0
            for part in lines[li].split(" "):
                q, v = map(int, part.split("x"))
                assert v in coins and q > 0
                tot += q * v
                cnt += q
            li += 1
            assert tot == amount and cnt == dp[amount], (amount, lines[li - 1])


for p in sorted(glob.glob(os.path.join(HERE, "input", "in_level-3_*.txt"))):
    suffix = os.path.basename(p)[len("in_level-3_"):-4]
    check(open(p).read(), open(os.path.join(HERE, "output", "level-3_%s.out" % suffix)).read())
    print("OK", suffix)
