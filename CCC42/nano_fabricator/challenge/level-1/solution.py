from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "outputs" / "level-1"


def board(r):
    rows = []
    for i in range(2 * r + 1):
        d = abs(i - r)
        if d == r:
            body = "*" + "-*" * r
        else:
            body = "*" + "-O" * (2 * r - 1 - d) + "-*"
        rows.append("-" * d + body + "-" * d)
    return "\n".join(rows)


def solve(text):
    t = text.split()
    n = int(t[0])
    return "".join(board(int(x)) + "\n\n" for x in t[1:1 + n])


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(HERE.glob("in_level-1_*.txt")):
        name = f.name.replace("in_", "", 1).replace("txt", "out")
        if "0-example" in name:
            assert solve(f.read_text()) == (HERE / "out_level-1_0-example.txt").read_text(), "example mismatch"
            print("example OK")
            continue
        (OUT / name).write_text(solve(f.read_text()))
        print("wrote", name)
