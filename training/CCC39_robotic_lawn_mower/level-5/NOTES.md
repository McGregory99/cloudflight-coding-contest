# Level 5 - Hamiltonian path, tree anywhere

Same I/O as L4, but the tree can be on the edge/corner and lawns can be any size. Same algorithm and `lawn.py` as L4 (mode "path"); nothing level-specific was needed because the flow + flip method makes no assumption about where the tree is. Endpoint colours are chosen from colour counts (statement guarantees solvable).

**Verification**: `check.py` (independent path re-simulation) passes on all inputs. Runtime a few seconds total.

**Pitfall**: with a corner/edge tree narrow strips appear; random endpoint restarts handle bad parity/endpoint choices.
