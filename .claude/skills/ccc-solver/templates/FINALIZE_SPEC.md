# Finalize a solved CCC challenge

Applies to one challenge folder `training/<CHALLENGE>/` whose levels are already solved
(each `level-N/` has `solution.py`, generated `*.out`, maybe `check.py`, `NOTES.md`).
All artifacts in English, EXCEPT explainer.html, which must be entirely in Spanish
(neutral/professional Spanish with correct accents: all visible text, captions, step
explanations, labels, buttons, aria-labels, `<html lang="es">`). Code snippets shown inside it stay as-is.

## 1. Folder layout (target)

```
<CHALLENGE>/
  README.md            # overview, levels table (problem | approach | complexity | verification), how to run
  explainer.html       # self-contained animated explainer (see section 2)
  run_all.py           # runs every level's solution + checker, prints a pass/fail table
  outputs/level-N/     # submittable .out files only (no *_0-example.out), for drag-and-drop upload
  level-N/
    statement.pdf      # renamed from level-N.pdf
    input/             # all in_level-N_*.txt
    expected/          # official example output(s) out_level-N_*.txt
    output/            # every generated level-N_*.out (including the example)
    solution.py        # reads ./input, writes ./output (paths relative to the script file, not cwd)
    check.py           # if present: validates ./output against ./input
    NOTES.md
```

Rules:
- Move files with `mv`; never lose an input, PDF or expected file.
- Update `solution.py` / `check.py` paths so they work from any cwd (`Path(__file__).parent`).
- Before restructuring, copy the current `.out` files to a temp dir in the scratchpad. After
  restructuring, re-run every solution and `diff` the new outputs against the saved ones: they
  must be byte-identical (the answers must not change). Re-run every checker; all must pass.
- Rebuild `outputs/level-N/` from `level-N/output/` (excluding `*_0-example.out`).
- `run_all.py` must exit non-zero if any example mismatch (for unique-answer levels) or checker fails.
- Delete stray temp/helper files you created; leave nothing else outside the layout.

## 2. explainer.html

One self-contained file (inline CSS/JS; only Google Fonts allowed as external). Opens offline-ish
by double-click.

- Look: inspired by pixel art (pixel display font such as "Press Start 2P" or "Silkscreen" for
  headings, chunky borders, limited palette echoing the challenge's theme), BUT every animation is
  drawn at full device resolution: `<canvas>` scaled by `devicePixelRatio` or SVG, smooth
  interpolation, crisp lines and text. No blurry upscaled sprites.
- Structure: hero with challenge name + one-line story; sticky level nav; one section per level.
- Each level section:
  - The problem in 2-4 plain sentences + input/output format.
  - A real example taken from that level's `input/` example file and its `expected/` output.
  - An animated, step-by-step visualization of HOW the solution algorithm works on that example
    (e.g. DP table filling, tournament bracket resolving, desks being placed, path being walked).
    Controls: play/pause, step back/forward, restart, speed. Show the current step's explanation
    text under the canvas.
  - "Key idea", complexity, and pitfalls (from NOTES.md).
  - A short collapsible snippet of the core of `solution.py`.
- Responsive down to 390px width; respects `prefers-reduced-motion` (start paused).
- Animation logic must reproduce the real algorithm's steps (port it to JS for the example), not a
  fake canned movie. The final state shown must equal the expected example output.
- Verify by opening the file in a headless check if possible (e.g. `node` to syntax-check the
  extracted script) and by reviewing the JS for runtime errors; make sure every level animates.

## 3. Report

Return: final tree (depth 2), run_all.py result table, confirmation outputs unchanged, and a
one-line description of each level's animation.
