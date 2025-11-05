"""Simple Othello package."""

from .board import Board
from .ai import OthelloAI
from .eval import evaluate

__all__ = ["Board", "OthelloAI", "evaluate"]
