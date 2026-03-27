from __future__ import annotations

from shape_tetris.game.models import Cell


def pixel_to_board_cell(
    x: int,
    y: int,
    board_origin: tuple[int, int],
    cell_size: int,
    board_size: int,
) -> Cell | None:
    origin_x, origin_y = board_origin
    rel_x = x - origin_x
    rel_y = y - origin_y
    if rel_x < 0 or rel_y < 0:
        return None
    col = rel_x // cell_size
    row = rel_y // cell_size
    if row >= board_size or col >= board_size:
        return None
    return Cell(int(row), int(col))
