# Level 4: 3 implementation plans (architect report, Opus xhigh)

Source data: 10 lost replays in `replays/`; most are from the OLD level-3 model, so the "Kernel on the edge dies at R8" cases are probably already fixed in the current `model.onnx`. The "Kernel killed in line by Daemon/Ice" cases (6 of 10) may still apply.

## Measured facts (experiments in /private/tmp/ccc_arch, untouched CCC)
- A 100-sim game takes ~1 s (~30 ms per action, almost all MCTS in Python; ONNX ~0.3 ms per batch of 8). 80 games with `Pool(4)` take ~20 s, machine already loaded by other agents.
- Games are decided tactically before the firewall. `model.onnx` vs itself mostly ends in rounds 5-8 by Kernel capture; Magenta wins 56%.
- With 100 sims the MCTS is myopic: the top-prior move gets 60-96 of 100 visits, other roots get 1-2. The threat "Daemon C4>C6 then C6>F6 x Kernel" needs both enemy actions, which the tree never expands. So Kernel threat must be inside value and prior. The current value is linear (material + Kernel ring) and sees no threat.
- Cheap exact oracle: `can_kill(board, team, actions_left)` tries all legal sequences with `apply_action`/`undo_action`, counting bodyguard rule; ~2 ms/position. Code: /private/tmp/ccc_arch/t5.py (copy it into your own folder before use).
- PyTorch ready: /private/tmp/ccc_arch/venv/bin/python (torch 2.14.1, numpy, onnx, onnxruntime). Install elsewhere with `pip install --isolated --index-url https://pypi.org/simple torch numpy onnx onnxruntime`.
  - Export with `torch.onnx.export(..., opset_version=17, dynamo=False, dynamic_axes={0:"batch"})`.
  - The validator REJECTS `Constant` nodes. /private/tmp/ccc_arch/fixconst.py turns each `Constant` into an initializer (copy it). A small CNN then validates: 0.9 s CPU in the level-3 match.
- `tourney.py` seeds game g as `seed=2g`: repeating a pairing replays identical games. Use another range (offset) to confirm.
- Parallel rules: no plan edits `build_model.py` or `tourney.py`; copy what you need under your own prefix. Each plan uses at most `Pool(3)` and `torch.set_num_threads(2)` (plan C: 2 processes).

## Common evaluation protocol (all plans)
- Copy `tourney.py` to `<plan>_tourney.py` adding `offset` (game g uses seeds 2(g+off), 2(g+off)+1) and `procs`; print wins per colour too.
- Opponents: `model.onnx`, `model_l3.onnx`, `env/play/random.onnx`, finally the other candidates.
- Upload threshold (all four at once): >=57% in 300 games vs `model.onnx` (offset 1000); >=70% vs `model_l3.onnx` in 200 games; >=95% vs `random.onnx` in 100 games; neither colour under 45% vs `model.onnx`; `validate_submission.py` says ACCEPTED.
- Final: round robin among candidates that pass (200 games per pair); the best gets uploaded. If none passes, `model.onnx` stays.

## Plan A: hand-made tactical evaluator with exact attack maps (low risk, ~70 min, 3 processes)
Idea: compute inside the ONNX the attack maps of each piece type with exact blocking and use them in value and policy, so the leaf "knows" what 100-sim MCTS cannot see. No training: constants plus a weight search by tournaments.

Files: `a_features.py` (graph), `a_build.py` (from `build_model.py` plus new features), `a_test.py`, `a_search.py`, `a_tourney.py`.

Graph (allowed ops only: `Conv` with `pads` and single-1 kernels as shifts, `Mul`, `Add`, `Relu`, `Min`, `ReduceSum`, `Slice` with constants):
- `empty = 1 - ReduceSum(planes 0-12)` (locked squares included in the sum).
- Attack on square t, per `rules.py`:
  - Daemon: orthogonal distance 1 (shot, no block); distance 2 if `D(t+2d)*empty(t+d)`; distance 3 if `D(t+3d)*empty(t+d)*empty(t+2d)`.
  - Ice: 8 directions; distance 1, and distance 2 if the middle square is empty.
  - Ping: diagonal up to 2, middle empty.
  - Trace: diagonal distance 2-3, intermediates empty; an adjacent diagonal piece blocks.
  - Exploit: the 8 L-jumps, no blocking.
  - Kernel: the 8 neighbours.
- `A1_X` = number of 1-action attacks of side X. `A2_X` = 2-action reach: each piece's movement map (with blocking) passed through the same attack function. `G_X` = non-Kernel guards adjacent to X's Kernel (3x3 conv of ones).

Which feature attacks each pattern:
- Kernel killed in line by Daemon/Ice (6 of 10):
  - `win_now = Relu(min(A1_own*Kenemy, 1) - G_enemy)`. When 2 actions remain (plane 13 = 1) also add `Relu(min(A2_own*Kenemy, 1) - G_enemy)` and the "2 attacks with 1 guard" case.
  - Value gets `+w_win*win_now`: that makes the leaf after KE G7>F6 worth ~+1 for the opponent.
  - Also `-w_thr*Relu(A1_enemy*Kown + A2_enemy*Kown - G_own)` (null-move threat), weighted more when we have 1 action left.
  - Policy: `-w_kmove*(A1_enemy + A2_enemy)[to]` for Kernel moves, `+w_esc` for the move that captures the attacker, `+w_guard` for moving pieces to squares adjacent to our own Kernel.
- Firewall at R8 (3 of 10, probably already fixed): replace `kernel_ring` by `kernel_ring*(1 + k_u*urgency)` using `Mul` with plane 14; Kernel policy `kernel_move*urgency`. Urgency is 0.625 at R5 and 1.0 at R8.
- Oscillation and hanging pieces (4 of 10): value `-w_out*material*[ring 0]*Relu(urgency - 0.5)`; `w_hang`: own material on squares with `A1_enemy > 0` and no defender; `move_ring` with the previous search value (2.0).
- Bare-Kernel endgame (match 6608): `gate = Relu(1 - ReduceSum(planes 0-4 and 6-10))`. Value `gate*(w_rd*(ring_own - ring_enemy) + w_mag*(plane15 - 0.5)*[same ring] - w_ch*[Chebyshev <= 2 and we are to move])`. Chebyshev <= 2 via a 5x5 conv of own Kernel times the enemy Kernel plane. Kernel policy toward ring 3 when the gate is active.

Steps and times:
1. 25 min: implement and write `a_test.py`: compare in 2000 random positions `A1*Kenemy > 0` against legal actions onto the enemy Kernel square, and `win_now` against `can_kill`. Require >=99% on A1 and >=90% accuracy on A2.
2. 10 min: first tournament with initial weights `w_win=3, w_thr=1.5, w_kmove=4`.
3. 30 min: coordinate search over ~8 weights, 200 games per variant vs `model.onnx` (~90 s each at 3 processes). Accept a variant only if it improves >= 3 points.
4. Stop at 70 min or when a full round accepts nothing.
Size: < 2.5 MB (the 64x4096 tables already exist).
Risks / plan B: a bug in the shifts or perspective mix-ups; `a_test.py` and the per-colour check cover it. If A2 is unreliable, ship only A1 plus the Kernel policy, which still attacks all 6 cases.

## Plan B: value CNN trained on exact oracle labels, residual over `model.onnx` (medium risk, ~75 min, 3 processes + 2 torch threads)
Idea: the exact oracle costs 2 ms, so labelling tens of thousands of positions is cheap. The net learns blocking and 2-action patterns nobody has to write. The policy stays as the current one.

Files: `b_gen.py`, `b_train.py`, `b_export.py` (includes `fixconst`), `b_tourney.py`. Use /private/tmp/ccc_arch/venv (torch).

Data (15 min):
- Games at 100 sims with the referee temperature, mixing `model.onnx`, `model_l3.onnx` and `random.onnx` in every pairing.
- For each position store `encode_board(...)` and three labels: `win_now = can_kill(board, side, actions_left)`; `thr = can_kill(board, opp, 2)`; `z` = result from the side to move.
- Augment with the left-right mirror (rules are symmetric; remap indices).
- Target: ~50-60k positions.

Net and value:
- Conv3x3 16->48, then 4 Conv3x3 48 with ReLU (receptive field = whole board). Head: Conv1x1 to 8 channels, Gemm 512->64, Gemm 64->3 (logit `win_now`, logit `thr`, `z`). ~130k parameters, ~0.5 MB.
- `value = tanh(base_raw + a*sigmoid(win) - b*sigmoid(thr) + c*z_hat)`. `base_raw` and the policy come from the `model.onnx` initializers (`value_w`, `cap_w`, `to_map`, `kmap`, `move`), loaded as fixed buffers.

Training (10 min): BCE + BCE + MSE, Adam 1e-3, 8-10 epochs, 10% validation. Report AUC of `win_now` >= 0.97.
Tournament: try 3-4 triples (a, b, c), e.g. (3,1,0.5), (4,2,1), (2,1,1), 200 games each.

Which feature attacks each pattern:
- Daemon/Ice line: `win_now` and `thr` are exactly that pattern, blocking and bodyguard included.
- Bare-Kernel endgame: the oracle does not cover it. Generate 3000 two-Kernel positions with exact label (play 1 turn then `kernel_endgame_winner`) and feed them into `z`.
- Firewall and hanging pieces: learned by `z_hat` from the result.
Risks / plan B: low precision gives false `thr` and a scared net; `z` with little data adds noise: if it fails set `c=0`. If the net does not reach the threshold, hand the labels to plan A as test or tuning data.

## Plan C: AlphaZero-lite (expert iteration, policy and value) bootstrapped from `model.onnx` (high risk, highest ceiling, ~80 min, 2 processes)
Idea: distil into the net what a 200-sim MCTS does, so with the referee's 100 sims it plays like it searched twice as much.

Files: `c_selfplay.py`, `c_train.py`, `c_export.py`, `c_gate.py`.

Loop:
- Self-play with `mcts.run` at 200 sims, temperature 1 in the first 8 actions and 0.25 after. Store `policy_target(root)`, the legal mask, `z` and the root mean Q.
- Iteration 1 (20 min, 2 processes): ~900 games, ~35k positions. Training: 8 min.
- Gate: >= 55% in 200 games vs `model.onnx`. If it passes, iteration 2 with the new net as generator. Stop at 80 min.

Net:
- Trunk as in B.
- Policy delta: Conv1x1 48->64 gives (B, to, from); `Reshape` to (B,64,64), `Transpose` perm [0,2,1], `Reshape` to (B,4096). Final policy `base + delta`, last layer initialised to zero: the starting net is exactly `model.onnx`.
- Value: `tanh(base_raw + Gemm)`, also zero-initialised.
Loss: cross-entropy with masked logits vs visits, plus MSE vs `0.5*z + 0.5*Q`.

Which feature attacks each pattern:
- Daemon/Ice line: only indirectly; with 200 sims the tree sometimes sees the reply and the policy learns not to move the Kernel there. Not guaranteed.
- Bare-Kernel endgame: MCTS resolves it at the turn boundary, so the policy learns to approach ring 3.
- Oscillation: the learned Q breaks the flatness of the value.
Risks / plan B: little data and noisy `z`; may not improve in 80 min. It competes most for CPU. If the gate fails, keep only the policy delta with the base value untouched. The exporter was not tested for the `Transpose` policy head in C, only the plain net.

## Recommendation
1. Launch A now: exact and verifiable attack on the dominant pattern (6 of 10 losses), no dependence on training.
2. Launch B in parallel: shares the oracle and gives A a cross-test.
3. Launch C with 2 processes only if machine load drops below ~12; otherwise cut it to "policy delta only, 1 iteration".
4. Cut-off: ~85 min after launch, round robin and upload the best that meets the threshold. Never upload anything that does not clearly beat `model.onnx`.

Not checked by the architect: replay dates versus the time `model.onnx` was deployed. Load on the machine can double the times.
