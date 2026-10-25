"""Validate level-2_*.out: each line is two coins of the currency summing to the amount."""
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def check(inp, out):
    tok = inp.split()
    n, c, a = int(tok[0]), int(tok[1]), int(tok[2])
    lines = out.split("\n")
    assert lines[-1] == "" and len(lines) == n * a + 1, "line count"
    pos, li = 3, 0
    for _ in range(n):
        coins = set(map(int, tok[pos:pos + c]))
        pos += c
        for s in tok[pos:pos + a]:
            x, y = map(int, lines[li].split(" "))
            li += 1
            assert x in coins and y in coins and x + y == int(s), (s, x, y)
        pos += a


for p in sorted(glob.glob(os.path.join(HERE, "input", "in_level-2_*.txt"))):
    suffix = os.path.basename(p)[len("in_level-2_"):-4]
    check(open(p).read(), open(os.path.join(HERE, "output", "level-2_%s.out" % suffix)).read())
    print("OK", suffix)
