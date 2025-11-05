import time
from typing import Tuple, Optional
from .board import Board, BLACK, WHITE


def print_board(board: Board):
    # Print header and row/col indices
    print("   " + " ".join(str(c) for c in range(8)))
    for r in range(7, -1, -1):
        row = []
        for c in range(8):
            v = board.grid[r][c]
            if v == BLACK:
                row.append("B")
            elif v == WHITE:
                row.append("W")
            else:
                row.append(".")
        print(f"{r}  " + " ".join(row))


def show_before_after(board: Board, move: Tuple[int,int], player: int):
    print("Before move:")
    print_board(board)
    print(f"Player {'B' if player==BLACK else 'W'} moves at {move}")


def countdown_timer(seconds: float):
    # simple countdown printed to console
    end = time.time() + seconds
    while True:
        rem = end - time.time()
        if rem <= 0:
            print("\rTime left: 0.0s    ")
            break
        print(f"\rTime left: {rem:.1f}s", end="")
        time.sleep(0.2)
    print()
