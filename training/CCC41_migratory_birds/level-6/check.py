l = open("level-6_1-main.out").read().splitlines()
assert l[0] == "Day,Top 50 Arrivals BOPs" and len(l) == 2
d, ids = l[1].split(","); ids = [int(x) for x in ids.split()]
assert d == "791" and len(ids) == len(set(ids)) == 50 and all(1 <= i <= 2500 for i in ids)
# independent check: mirror property of the given block, then day-730 arrivals ranking
import csv
rows = {}
for r in csv.reader(open("all_data_from_level_5.in")):
    if r[0] == "730": rows[int(r[1])] = float(r[2])
top = sorted(rows, key=lambda b: (-rows[b], b))[:50]
assert top == ids
print("ok")
