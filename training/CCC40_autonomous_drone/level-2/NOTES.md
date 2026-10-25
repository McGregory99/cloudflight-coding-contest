# Level 2 - final height from accelerations

**Input:** N, then N lines of non-negative accelerations (one per tick). **Output:** N lines, final height.
Per tick: `v += a - 10` (gravity 10), then `h += v` (the NEW velocity is used within the same tick).

**Algorithm:** plain simulation, O(total ticks). Unique answer, verified by exact diff with the example.
**Pitfalls:** update velocity first, then position; velocity is not clamped (can be negative), only the height is guaranteed >= 0.
