from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE.parent.parent / "outputs" / "level-2"

# direction -> (d_row, d_col) in the character grid
DIRS = {1: (0, 2), 2: (1, 1), 3: (1, -1), 4: (0, -2), 5: (-1, -1), 6: (-1, 1)}


def fire(grid):
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch in "123456":
                dr, dc = DIRS[int(ch)]
                r2, c2 = r + dr, c + dc
                while 0 <= r2 < len(grid) and 0 <= c2 < len(grid[r2]) and grid[r2][c2] == "O":
                    grid[r2][c2] = "M"
                    r2 += dr
                    c2 += dc
                return


def solve(text):
    t = text.split()
    n = int(t[0])
    p = 1
    out = []
    for _ in range(n):
        rows = int(t[p + 1])
        grid = [list(s) for s in t[p + 3:p + 3 + rows]]
        p += 3 + rows
        fire(grid)
        out.append("\n".join("".join(row) for row in grid) + "\n\n")
    return "".join(out)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(HERE.glob("in_level-2_*.txt")):
        name = f.name.replace("in_", "", 1).replace("txt", "out")
        if "0-example" in name:
            assert solve(f.read_text()) == (HERE / "out_level-2_0-example.txt").read_text(), "example mismatch"
            print("example OK")
            continue
        (OUT / name).write_text(solve(f.read_text()))
        print("wrote", name)
