import glob, os

def main():
    for path in sorted(glob.glob("in_level-1_*.txt")):
        toks = open(path).read().split()
        n = int(toks[0])
        out = []
        for i in range(n):
            x, y = int(toks[1 + 2 * i]), int(toks[2 + 2 * i])
            out.append(str((x // 3) * y))  # x divisible by 3 -> area / 3
        name = os.path.basename(path)[3:-4]
        with open(name + ".out", "w") as f:
            f.write("\n".join(out) + "\n")

main()
