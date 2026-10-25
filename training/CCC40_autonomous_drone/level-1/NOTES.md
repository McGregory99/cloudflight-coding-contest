# Level 1 - final height from velocities

**Input:** N, then N lines, each a list of integer velocities (one per tick). **Output:** N lines, the final height of each flight.
Height starts at 0 and `h_i = h_{i-1} + v_i`, so the answer is simply the sum of the line.

**Algorithm:** `sum(map(int, line.split()))` per flight, O(total ticks).
**Pitfalls:** none; the answer is unique, verified by exact diff with the example output.
