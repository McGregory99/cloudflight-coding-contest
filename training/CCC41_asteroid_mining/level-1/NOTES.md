# Level 1 - Asteroid Mining

**Statement.** N asteroids; each is a "minable rectangle" W x H surrounded by one layer of bedrock.
Input: `N`, then N lines `W H`. Output: for each asteroid a paragraph of H+2 rows, `#` = bedrock, `:` = minable cell.

**Approach.** Print `#*(W+2)`, H rows of `#` + `:`*W + `#`, `#*(W+2)`.

**Pitfalls.** The example output ends every asteroid (the last too) with a blank line: file ends with `\n\n`. Verified with an exact diff against the example. Complexity O(total cells).
