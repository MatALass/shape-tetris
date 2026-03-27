from __future__ import annotations

from shape_tetris.game.models import Cell


def add_cells(a: Cell, b: Cell) -> Cell:
    return Cell(a.row + b.row, a.col + b.col)
