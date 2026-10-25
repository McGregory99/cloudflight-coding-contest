# Level 1 - Room Planner (CCC40)
**Statement:** N rooms `x y` (x divisible by 3). Desks are 1x3 (rotation allowed). Output the max number of desks per room, one per line.
**Approach:** x divisible by 3, so every row tiles perfectly with horizontal desks: answer = (x/3)*y = area/3, which is also the area upper bound.
**Complexity:** O(N). **Pitfalls:** none; matches the example exactly.
