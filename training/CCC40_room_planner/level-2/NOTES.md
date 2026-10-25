# Level 2
**Statement:** Rooms `x y k` (x divisible by 3, k = max desks = x*y/3). Output a y-row, x-column matrix of desk IDs 1..k (1x3 desks, no gaps). Desk order/IDs free, blank line between rooms optional.
**Approach:** fill every row with x/3 horizontal desks numbered consecutively.
**Complexity:** O(x*y) per room. **Verification:** `check.py` (ids 1..k, each id exactly 3 straight contiguous cells, no empty cell). Not byte-identical to the example (answer not unique).
**Pitfalls:** output ends with a blank line after each room, like the example.
