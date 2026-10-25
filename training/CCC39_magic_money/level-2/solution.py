import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))


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
        cs = set(coins)
        for s in amounts:
            t = int(s)
            for x in coins:  # ascending -> smaller coin printed first
                if (t - x) in cs:
                    out.append("%d %d" % (x, t - x))
                    break
            else:
                raise ValueError("no pair for %d" % t)
    return "\n".join(out) + "\n"


def main():
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    for path in sorted(glob.glob(os.path.join(HERE, "input", "in_level-2_*.txt"))):
        suffix = os.path.basename(path)[len("in_level-2_"):-len(".txt")]
        with open(path) as f:
            res = solve(f.read())
        with open(os.path.join(HERE, "output", "level-2_%s.out" % suffix), "w") as f:
            f.write(res)


if __name__ == "__main__":
    main()
