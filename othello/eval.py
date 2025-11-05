from typing import Tuple, List
from .board import Board, BLACK, WHITE

# Positional weight table favoring corners and penalizing X-squares etc.
WEIGHTS = [
    [120, -20, 20, 5, 5, 20, -20, 120],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [5, -5, 3, 3, 3, 3, -5, 5],
    [20, -5, 15, 3, 3, 15, -5, 20],
    [-20, -40, -5, -5, -5, -5, -40, -20],
    [120, -20, 20, 5, 5, 20, -20, 120],
]


def evaluate(board: Board, player: int) -> float:
    # Returns score from perspective of `player` (higher = better)
    black, white = board.get_score()
    material = (black - white) * (1 if player == BLACK else -1)

    # Mobility
    my_moves = len(board.legal_moves(player))
    opp_moves = len(board.legal_moves(-player))
    mobility = 0
    if my_moves + opp_moves > 0:
        mobility = 100 * (my_moves - opp_moves) / (my_moves + opp_moves)

    # Positional weights
    pos = 0
    for r in range(8):
        for c in range(8):
            v = board.grid[r][c]
            if v == 0:
                continue
            if v == player:
                pos += WEIGHTS[r][c]
            else:
                pos -= WEIGHTS[r][c]

    # Frontier discs: count pieces adjacent to empty squares
    frontier_my = 0
    frontier_opp = 0
    for r in range(8):
        for c in range(8):
            if board.grid[r][c] == 0:
                continue
            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
                rr, cc = r+dr, c+dc
                if 0 <= rr < 8 and 0 <= cc < 8 and board.grid[rr][cc] == 0:
                    if board.grid[r][c] == player:
                        frontier_my += 1
                    else:
                        frontier_opp += 1
                    break

    frontier = (frontier_opp - frontier_my)  # fewer frontier discs is better

    # Stability approx: corners owned and stable edges contiguous from corners
    stability = 0
    corners = [(0,0),(0,7),(7,0),(7,7)]
    for (r,c) in corners:
        v = board.grid[r][c]
        if v == 0:
            continue
        if v == player:
            stability += 1
        else:
            stability -= 1

    # Parity small bonus: prefer having parity on endgame
    empty = sum(1 for r in range(8) for c in range(8) if board.grid[r][c] == 0)
    parity = 0
    if empty % 2 == 1:
        parity = 1 if player == BLACK else -1

    # Weighted sum — constants can be tuned
    score = (10 * material) + (78 * pos) + (10 * mobility) + (74 * stability) + (-10 * frontier) + (5 * parity)

    # Terminal overriding
    if board.is_terminal():
        b, w = board.get_score()
        if (b - w) * (1 if player == BLACK else -1) > 0:
            return 1e6
        elif (b - w) * (1 if player == BLACK else -1) < 0:
            return -1e6
        else:
            return 0

    return float(score)
