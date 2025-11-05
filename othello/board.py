import copy
from typing import List, Tuple, Optional

# Board representation: 8x8 with 0=empty, 1=black, -1=white
EMPTY = 0
BLACK = 1
WHITE = -1

DIRS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Board:
    def __init__(self):
        # rows 0..7 from bottom to top, cols 0..7 left to right
        self.grid = [[EMPTY for _ in range(8)] for _ in range(8)]
        # Starting config assumption per spec: center left upper is white.
        # Center squares coordinates: (3,3),(3,4),(4,3),(4,4) with row-major bottom-left origin.
        # We set (4,3) as white (left upper). We'll place the classic two-white/two-black diagonal.
        self.grid[3][3] = BLACK
        self.grid[4][4] = BLACK
        self.grid[4][3] = WHITE  # left upper white per spec
        self.grid[3][4] = WHITE

        # History stack for undo: list of (move, player, flips)
        self.history: List[Tuple[Tuple[int, int], int, List[Tuple[int, int]]]] = []

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < 8 and 0 <= c < 8

    def opponent(self, player: int) -> int:
        return -player

    def _flips_for_move(self, r: int, c: int, player: int) -> List[Tuple[int, int]]:
        if self.grid[r][c] != EMPTY:
            return []
        flips: List[Tuple[int, int]] = []
        for dr, dc in DIRS:
            path = []
            rr, cc = r + dr, c + dc
            while self.in_bounds(rr, cc) and self.grid[rr][cc] == self.opponent(player):
                path.append((rr, cc))
                rr += dr
                cc += dc
            if self.in_bounds(rr, cc) and self.grid[rr][cc] == player and path:
                flips.extend(path)
        return flips

    def legal_moves(self, player: int) -> List[Tuple[int, int]]:
        moves = []
        for r in range(8):
            for c in range(8):
                if self._flips_for_move(r, c, player):
                    moves.append((r, c))
        return moves

    def apply_move(self, move: Tuple[int, int], player: int) -> bool:
        r, c = move
        flips = self._flips_for_move(r, c, player)
        if not flips:
            return False
        self.grid[r][c] = player
        for fr, fc in flips:
            self.grid[fr][fc] = player
        self.history.append((move, player, flips))
        return True

    def undo_move(self) -> Optional[Tuple[Tuple[int, int], int, List[Tuple[int, int]]]]:
        if not self.history:
            return None
        move, player, flips = self.history.pop()
        r, c = move
        self.grid[r][c] = EMPTY
        for fr, fc in flips:
            self.grid[fr][fc] = self.opponent(player)
        return (move, player, flips)

    def is_terminal(self) -> bool:
        # Terminal if no legal moves for both players
        return not self.legal_moves(BLACK) and not self.legal_moves(WHITE)

    def get_score(self) -> Tuple[int, int]:
        black = 0
        white = 0
        for r in range(8):
            for c in range(8):
                if self.grid[r][c] == BLACK:
                    black += 1
                elif self.grid[r][c] == WHITE:
                    white += 1
        return black, white

    def copy(self) -> "Board":
        b = Board()
        b.grid = copy.deepcopy(self.grid)
        b.history = copy.deepcopy(self.history)
        return b

    def as_tuple(self) -> Tuple[int, ...]:
        return tuple(cell for row in self.grid for cell in row)
