# Othello project

An implementation of the Othello (Reversi) board game using a Minimax search with Alpha-Beta pruning and optional iterative deepening.

This repository contains a small Python implementation with:

- Core board logic (legal move generation, apply/undo, terminal detection).
- A heuristic evaluation function (material, mobility, positional weights, frontier, simple stability, parity).
- An AI implementing iterative deepening + alpha-beta pruning + move ordering + simple transposition table.
- A CLI runner that prints the board before and after each move and supports a single-move undo.

Overview
--------

Coordinate system: row-major where (i, j) means i-th row, j-th column; i and j range 0..7. Row 0 is the bottom row and column 0 is the leftmost column (bottom-left origin).

Starting board: the center-left-upper of the four central squares is white per project spec. If you want the alternate standard orientation, tell me and I'll change it.

Requirements
------------

- Python 3.8+ recommended.
- See `requirements.txt` for optional test dependencies.

Makefile (convenience)
----------------------

If you have `make` available (Unix or Windows with GNU Make), the repository includes a `Makefile` with these targets:

- `make install` — install runtime/test dependencies from `requirements.txt`.
- `make run` — run the CLI runner (`run.py`) with default options.
- `make test` — run a quick syntax-check using `py_compile`.

PowerShell (Windows) commands
----------------------------

If you don't have `make`, here are equivalent PowerShell commands:

```powershell
# install dependencies
python -m pip install --upgrade pip ; python -m pip install -r requirements.txt

# run the game (human plays black by default, AI time limit 30s)
python .\run.py --human black --time 30

# quick syntax check
python -m py_compile run.py othello\board.py othello\ai.py othello\eval.py othello\cli.py
```

Usage notes
-----------

- When prompted for a move, enter `r c` (two integers) representing row and column (0..7). The CLI prints the board before and after each move.
- Type `undo` to retract the last move if you made a mistake.
- Change AI thinking time with `--time` (seconds). The default is 30 seconds per move.

Next steps
----------

Possible improvements:

- Add unit tests and CI.
- Improve the transposition table using Zobrist hashing.
- Add GUI (Tkinter) or web interface for click-based play and a visual countdown.
- Tune evaluation weights via self-play.
# Othello-project-
An implementation of the Othello Board game using  a standard Min-Max search with Alpha-Beta pruning and optional iterative deepening.
