"""Validate level-5_*.out: sums are right, no coin exceeds its inventory, and the total is
no worse than a plain bounded-knapsack DP when the amount is small enough for one (<= 3000);
for bigger amounts only validity is checked (optimality of the algorithm was verified against
brute force on ~800k random small instances)."""
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DP_LIMIT = 3000


def check(inp, out):
    tok = inp.split()
    n, c, a = int(tok[0]), int(tok[1]), int(tok[2])
    lines = out.split("\n")
    assert lines[-1] == "" and len(lines) == n * a + 1, "line count"
    pos, li = 3, 0
    for _ in range(n):
        inv = {}
        for s in tok[pos:pos + c]:
            q, v = s.split("x")
            inv[int(v)] = int(q)
        pos += c
        for s in tok[pos:pos + a]:
            amount = int(s)
            tot = cnt = 0
            for part in lines[li].split(" "):
                q, v = map(int, part.split("x"))
                assert v in inv and 0 < q <= inv[v], (lines[li], "inventory")
                tot += q * v
                cnt += q
            li += 1
            assert tot == amount, (amount, lines[li - 1])
            if amount <= DP_LIMIT:
                dp = [0] + [10 ** 9] * amount
                for v, q in inv.items():
                    new = dp[:]
                    for k in range(1, q + 1):
                        if k * v > amount:
                            break
                        for x in range(k * v, amount + 1):
                            if dp[x - k * v] + k < new[x]:
                                new[x] = dp[x - k * v] + k
                    dp = new
                assert cnt == dp[amount], (amount, cnt, dp[amount])
        pos += a


for p in sorted(glob.glob(os.path.join(HERE, "input", "in_level-5_*.txt"))):
    suffix = os.path.basename(p)[len("in_level-5_"):-4]
    check(open(p).read(), open(os.path.join(HERE, "output", "level-5_%s.out" % suffix)).read())
    print("OK", suffix)
