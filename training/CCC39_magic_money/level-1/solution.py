import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def solve(text):
    tok = text.split()
    n, c = int(tok[0]), int(tok[1])
    out = []
    pos = 2
    for _ in range(n):
        coins = set(map(int, tok[pos:pos + c]))
        pos += c
        m = 1
        while m in coins:
            m += 1
        out.append(str(m))
    return "\n".join(out) + "\n"


def main():
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    for path in sorted(glob.glob(os.path.join(HERE, "input", "in_level-1_*.txt"))):
        suffix = os.path.basename(path)[len("in_level-1_"):-len(".txt")]
        with open(path) as f:
            res = solve(f.read())
        with open(os.path.join(HERE, "output", "level-1_%s.out" % suffix), "w") as f:
            f.write(res)


if __name__ == "__main__":
    main()
