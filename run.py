import argparse
import time
import threading
import sys
from othello.board import Board, BLACK, WHITE
from othello.ai import OthelloAI
from othello.cli import print_board, show_before_after


def human_move_input(board: Board, player: int):
    moves = board.legal_moves(player)
    if not moves:
        print("No legal moves; passing.")
        return None
    print("Legal moves:", moves)
    while True:
        s = input("Enter move as 'r c' or 'undo': ").strip()
        if s.lower() == "undo":
            return "undo"
        try:
            r, c = map(int, s.split())
            if (r,c) in moves:
                return (r,c)
            print("Illegal move; try again.")
        except Exception:
            print("Parse error; provide two ints like '2 3' or 'undo'.")


def play(human_color: str, time_limit: float):
    board = Board()
    ai = OthelloAI()
    player = BLACK  # black moves first by convention
    human = BLACK if human_color.lower() == 'black' else WHITE
    print("Starting board:")
    print_board(board)

    while not board.is_terminal():
        print("---")
        if player == human:
            choice = human_move_input(board, player)
            if choice == "undo":
                popped = board.undo_move()
                if popped is None:
                    print("Nothing to undo")
                else:
                    print("Undid last move")
                    print_board(board)
                    # swap turn back
                    player = -player
                continue
            if choice is None:
                print("Passing turn")
                player = -player
                continue
            show_before_after(board, choice, player)
            board.apply_move(choice, player)
            print("After move:")
            print_board(board)
        else:
            print(f"AI ({'B' if player==BLACK else 'W'}) thinking (max {int(time_limit)}s)...")
            # Run the AI in a background thread and display a countdown timer in the main thread.
            result = {"move": None, "exception": None}

            def ai_worker():
                try:
                    mv = ai.find_best_move(board, player, time_limit=time_limit, max_depth=8)
                    result["move"] = mv
                except Exception as e:
                    result["exception"] = e

            t = threading.Thread(target=ai_worker, daemon=True)
            t.start()
            start = time.time()
            # show countdown while thread is alive and within time_limit
            try:
                while t.is_alive():
                    elapsed = time.time() - start
                    rem = time_limit - elapsed
                    if rem <= 0:
                        # time expired — wait a short moment for AI to notice and stop
                        print(f"\rTime left: 0.0s    ", end="", flush=True)
                        break
                    # print remaining time on single line
                    print(f"\rTime left: {rem:.1f}s", end="", flush=True)
                    time.sleep(0.2)
                # ensure thread finishes if it's still winding down
                t.join(0.1)
            except KeyboardInterrupt:
                print("\nInterrupted by user")
                t.join(0.1)
            print()

            if result.get("exception") is not None:
                print("AI error:", result.get("exception"))

            best_move = result.get("move")
            if best_move is None:
                print("AI has no moves or timed out; passing.")
                player = -player
                continue

            show_before_after(board, best_move, player)
            board.apply_move(best_move, player)
            print("After move:")
            print_board(board)

        player = -player

    b,w = board.get_score()
    print("Game over. Score Black: {}, White: {}".format(b,w))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--human', choices=['black','white'], default='black', help='Human plays as black or white')
    parser.add_argument('--time', type=float, default=30.0, help='AI thinking time per move (seconds)')
    args = parser.parse_args()
    play(args.human, args.time)
