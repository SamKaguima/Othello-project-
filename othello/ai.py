import time
import math
from typing import Optional, Tuple, Dict, List
from .board import Board, BLACK, WHITE
from .eval import evaluate


class OthelloAI:
    def __init__(self):
        # simple transposition table: key -> (value, depth)
        self.tt: Dict[Tuple[int, ...], Tuple[float, int]] = {}

    def _order_moves(self, board: Board, player: int, moves: List[Tuple[int,int]]) -> List[Tuple[int,int]]:
        # Prioritize corners and moves that flip many discs
        corners = {(0,0),(0,7),(7,0),(7,7)}
        scored = []
        for m in moves:
            if m in corners:
                score = 10000
            else:
                r,c = m
                flips = len(board._flips_for_move(r,c,player))
                score = flips
            scored.append((score,m))
        scored.sort(reverse=True)
        return [m for _,m in scored]

    def _alphabeta(self, board: Board, player: int, depth: int, alpha: float, beta: float, maximizing: bool, start_time: float, time_limit: float) -> float:
        # Time check
        if time.time() - start_time > time_limit:
            raise TimeoutError()

        key = board.as_tuple()
        if key in self.tt and self.tt[key][1] >= depth:
            return self.tt[key][0]

        if depth == 0 or board.is_terminal():
            val = evaluate(board, player)
            self.tt[key] = (val, depth)
            return val

        legal = board.legal_moves(player if maximizing else -player)
        if not legal:
            # pass move
            val = self._alphabeta(board, player, depth-1, alpha, beta, not maximizing, start_time, time_limit)
            self.tt[key] = (val, depth)
            return val

        ordered = self._order_moves(board, player if maximizing else -player, legal)

        if maximizing:
            value = -math.inf
            for mv in ordered:
                r,c = mv
                flips = board._flips_for_move(r,c,player)
                board.apply_move(mv, player)
                try:
                    child_val = self._alphabeta(board, player, depth-1, alpha, beta, False, start_time, time_limit)
                finally:
                    board.undo_move()
                value = max(value, child_val)
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            self.tt[key] = (value, depth)
            return value
        else:
            value = math.inf
            opp = -player
            for mv in ordered:
                r,c = mv
                flips = board._flips_for_move(r,c,opp)
                board.apply_move(mv, opp)
                try:
                    child_val = self._alphabeta(board, player, depth-1, alpha, beta, True, start_time, time_limit)
                finally:
                    board.undo_move()
                value = min(value, child_val)
                beta = min(beta, value)
                if alpha >= beta:
                    break
            self.tt[key] = (value, depth)
            return value

    def find_best_move(self, board: Board, player: int, time_limit: float = 30.0, max_depth: int = 8) -> Optional[Tuple[int,int]]:
        # Iterative deepening
        start_time = time.time()
        best_move = None
        best_score = -math.inf if player == BLACK else math.inf
        depth = 1
        try:
            while depth <= max_depth:
                legal = board.legal_moves(player)
                if not legal:
                    return None
                ordered = self._order_moves(board, player, legal)
                current_best = None
                current_best_score = -math.inf
                for mv in ordered:
                    if time.time() - start_time > time_limit:
                        raise TimeoutError()
                    board.apply_move(mv, player)
                    try:
                        val = self._alphabeta(board, player, depth-1, -math.inf, math.inf, False, start_time, time_limit)
                    finally:
                        board.undo_move()
                    if val > current_best_score:
                        current_best_score = val
                        current_best = mv
                # adopt current_best as best move so far
                if current_best is not None:
                    best_move = current_best
                    best_score = current_best_score
                depth += 1
        except TimeoutError:
            # time ran out — return last best
            pass
        return best_move
