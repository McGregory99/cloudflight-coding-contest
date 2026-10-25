"""Format check + (training-run only) true score: the level-6 pool file contains the real arrivals of days 731-760."""
import os
lines = open("level-5_1-main.out").read().splitlines()
assert lines[0] == "Day,Top 50 Arrivals BOPs" and len(lines) == 31
pred = {}
for i, l in enumerate(lines[1:]):
    d, ids = l.split(","); ids = [int(x) for x in ids.split()]
    assert int(d) == 731 + i and len(ids) == len(set(ids)) == 50 and all(1 <= x <= 2500 for x in ids)
    pred[int(d)] = set(ids)
print("format ok")
truth_file = "../level-6/all_data_from_level_5.in"
if os.path.exists(truth_file):
    arr = {}
    for l in open(truth_file):
        p = l.split(",")
        if p[0].isdigit() and 731 <= int(p[0]) <= 760:
            arr.setdefault(int(p[0]), []).append(float(p[2]))
    acc = []
    for d in range(731, 761):
        a = arr[d]; top = set(sorted(range(2500), key=lambda i: (-a[i], i))[:50])
        acc.append(len(top & {i - 1 for i in pred[d]}) / 50)
    print("true mean top-50 overlap %.3f min %.2f max %.2f" % (sum(acc) / 30, min(acc), max(acc)))
    print([round(x, 2) for x in acc])
