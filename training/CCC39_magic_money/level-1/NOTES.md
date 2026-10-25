# Level 1 - Magic Money

## Statement
- Input: `N` (currencies), `C` (coins per currency), then `N` lines of `C` sorted coin values.
- Output: one line per currency with the smallest positive integer that is not a coin value.

## Approach
Put the coins in a set and count up from 1 until the number is missing. At most `C+1` steps per currency, so O(N*C) overall.

## Pitfalls
- Answer can be `C+1` or larger when the coins are 1..C.
- Output is newline separated, no trailing spaces; the file ends with a single newline.
