# Level 1 - Bird Observation Points

**Statement.** CSV `BOP,Temperature [°C],Humidity [%]`. Output the BOP ids sorted from most to least popular, space separated.
Birds prefer higher temperature; for equal temperature, lower humidity; remaining ties: lower BOP id first.

**Approach.** Sort key `(-temperature, humidity, id)`. Output has no trailing newline (like the example).

**Data pitfalls (not in the statement).**
- Number words: `seventeen` appears instead of `17` (a: BOP 4, e: BOP 287). `num()` parses words 0-99.
- degF bug: file `e` contains ~860 temperatures between 70 and 113 (true degC range is -5..45; observed degC never exceeds 45, observed degF never below 70).
  Level 2 explicitly says "some degC values were mistakenly reported in degF", levels 3/4 say "beware of the degF-bug". Level 1 does not mention it.
  Default: values > 45 are converted `(F-32)*5/9` (exact `Fraction`, so ties stay exact). `RAW=1 python3 solution.py` disables the conversion.
- Humidity values and ids parse as numbers; some inputs are only one temperature (file d: all 19 degC, so only the humidity/id tie rules matter).

**Verification.** Example output matches exactly (`2 3 4 1`). `check.py` validates that every output is a permutation of the input ids.
Corrected vs raw order differs in ~1094 of 2171 positions for file `e`, so this choice decides `e`.

**Doubt (biggest).** Whether the level-1 grader expects degF-corrected temperatures for `e`. a-d have no degF values. I chose correction (physically right, and the file clearly contains the bug); if `e` fails, resubmit with `RAW=1`.

## Grader feedback

Level 1 file e: converting the ~860 degF values to Celsius was WRONG (grader: 1077/2171 positions correct, exactly the overlap between raw and converted orders). Sort on the temperatures as given. Lesson: do not "fix" suspicious data silently; the grader reflects the generator, not physical sense.
