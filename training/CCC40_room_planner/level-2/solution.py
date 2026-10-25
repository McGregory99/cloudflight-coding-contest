import glob, os

def main():
    for path in sorted(glob.glob("in_level-2_*.txt")):
        toks = open(path).read().split()
        n = int(toks[0])
        out = []
        for i in range(n):
            x, y, k = (int(t) for t in toks[1 + 3 * i: 4 + 3 * i])
            # x divisible by 3: every row holds x/3 horizontal desks, k == y * x/3
            per_row = x // 3
            did = 1
            for r in range(y):
                row = []
                for _ in range(per_row):
                    row += [str(did)] * 3
                    did += 1
                out.append(" ".join(row))
            assert did - 1 == k
            out.append("")
        name = os.path.basename(path)[3:-4]
        with open(name + ".out", "w") as f:
            f.write("\n".join(out) + "\n")

main()
