"""Run every level's solution and checker, print a pass/fail table.

Exit code is non-zero if a solution crashes, an example output differs from the
official one on a unique-answer level, or a checker fails.
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEVELS = range(1, 8)
# Levels 3-6 accept many valid arrangements; their example output differs from
# the official one by design and is validated by check.py instead.
UNIQUE_ANSWER = {1, 2, 7}


def run(script):
    t0 = time.perf_counter()
    proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    return proc, time.perf_counter() - t0


def example_status(level_dir, n):
    if n not in UNIQUE_ANSWER:
        return "multi", True
    ours = level_dir / "output" / ("level-%d_0-example.out" % n)
    official = level_dir / "expected" / ("out_level-%d_0-example.txt" % n)
    if not ours.exists():
        return "missing", False
    same = ours.read_text().split() == official.read_text().split()
    return ("match" if same else "MISMATCH"), same


def main():
    rows = []
    ok_all = True
    for n in LEVELS:
        level_dir = ROOT / ("level-%d" % n)
        proc, secs = run(level_dir / "solution.py")
        sol_ok = proc.returncode == 0
        ex, ex_ok = example_status(level_dir, n) if sol_ok else ("-", False)
        check = level_dir / "check.py"
        if check.exists():
            cproc, _ = run(check)
            chk_ok = cproc.returncode == 0
            chk = "pass" if chk_ok else "FAIL"
            if not chk_ok:
                sys.stderr.write(cproc.stdout + cproc.stderr)
        else:
            chk, chk_ok = "-", True
        if not sol_ok:
            sys.stderr.write(proc.stderr)
        ok = sol_ok and ex_ok and chk_ok
        ok_all &= ok
        n_out = len(list((level_dir / "output").glob("*.out")))
        rows.append((n, "ok" if sol_ok else "CRASH", "%.2fs" % secs, n_out, ex, chk,
                     "PASS" if ok else "FAIL"))

    head = ("level", "solution", "time", "outs", "example", "check", "result")
    widths = [max(len(str(r[i])) for r in rows + [head]) for i in range(len(head))]
    fmt = "  ".join("%%-%ds" % w for w in widths)
    print(fmt % head)
    print(fmt % tuple("-" * w for w in widths))
    for r in rows:
        print(fmt % r)
    print("\nALL PASS" if ok_all else "\nSOME LEVELS FAILED")
    sys.exit(0 if ok_all else 1)


if __name__ == "__main__":
    main()
