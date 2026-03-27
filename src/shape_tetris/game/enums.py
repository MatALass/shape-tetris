from __future__ import annotations

from enum import Enum


class BoardShape(str, Enum):
    CIRCLE = "circle"
    DIAMOND = "diamond"
    TRIANGLE = "triangle"


class BlockSelectionMode(str, Enum):
    RANDOM_THREE = "random_three"
    FULL_CATALOG = "full_catalog"


class GameStatus(str, Enum):
    MENU = "menu"
    RUNNING = "running"
    PAUSED = "paused"
    GAME_OVER = "game_over"
