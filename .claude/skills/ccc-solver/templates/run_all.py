"""Run every level's solution and checker, then print a pass/fail table.

Exit code is non-zero if a solution or checker fails, or if the example output differs
from the official one on a level whose answer is unique (level 1). Levels 2-5 accept any
valid/optimal answer, so their example comparison is informational and check.py decides.
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEVELS = [1, 2, 3, 4, 5]
UNIQUE_ANSWER = {1}


def run(script):
    t = time.time()
    proc = subprocess.run([sys.executable, str(script)], capture_output=True, text=True)
    return proc.returncode == 0, time.time() - t, (proc.stdout + proc.stderr).strip()


def main():
    rows = []
    failed = False
    for n in LEVELS:
        d = ROOT / ("level-%d" % n)
        ok_sol, secs, log = run(d / "solution.py")
        if not ok_sol:
            print(log)
        expected = d / "expected" / ("out_level-%d_0-example.txt" % n)
        produced = d / "output" / ("level-%d_0-example.out" % n)
        same = produced.exists() and produced.read_text() == expected.read_text()
        example = "match" if same else ("MISMATCH" if n in UNIQUE_ANSWER else "differs (ok)")
        checker = d / "check.py"
        if checker.exists():
            ok_chk, _, log = run(checker)
            if not ok_chk:
                print(log)
            check = "PASS" if ok_chk else "FAIL"
        else:
            ok_chk, check = True, "-"
        ok = ok_sol and ok_chk and (same or n not in UNIQUE_ANSWER)
        failed |= not ok
        rows.append((n, "ok" if ok_sol else "FAIL", "%.2fs" % secs, example, check,
                     "PASS" if ok else "FAIL"))

    head = ("level", "solution", "time", "example", "check.py", "result")
    widths = [max(len(str(r[i])) for r in rows + [head]) for i in range(len(head))]
    fmt = "  ".join("%%-%ds" % w for w in widths)
    print(fmt % head)
    print(fmt % tuple("-" * w for w in widths))
    for r in rows:
        print(fmt % r)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
