from __future__ import annotations

from shape_tetris.game.block_ops import get_absolute_cells
from shape_tetris.game.models import BoardState, BlockInstance, Cell, PlacementValidation


def validate_placement(board: BoardState, block: BlockInstance, anchor: Cell) -> PlacementValidation:
    absolute_cells = get_absolute_cells(block, anchor)
    for cell in absolute_cells:
        if not board.definition.is_valid_cell(cell.row, cell.col):
            return PlacementValidation(
                is_valid=False,
                reason="Block extends outside the playable shape.",
                cells=absolute_cells,
            )
        if board.occupied[cell.row][cell.col]:
            return PlacementValidation(
                is_valid=False,
                reason="Block overlaps an occupied cell.",
                cells=absolute_cells,
            )
    return PlacementValidation(is_valid=True, cells=absolute_cells)


def apply_placement(board: BoardState, block: BlockInstance, anchor: Cell) -> BoardState:
    validation = validate_placement(board, block, anchor)
    if not validation.is_valid:
        raise ValueError(validation.reason or "Invalid placement.")
    new_board = board.clone()
    for cell in validation.cells:
        new_board.occupied[cell.row][cell.col] = True
    return new_board


def get_full_rows(board: BoardState) -> list[int]:
    rows: list[int] = []
    size = board.definition.size
    for row in range(size):
        valid_cells = [col for col in range(size) if board.definition.valid_mask[row][col]]
        if valid_cells and all(board.occupied[row][col] for col in valid_cells):
            rows.append(row)
    return rows


def get_full_columns(board: BoardState) -> list[int]:
    cols: list[int] = []
    size = board.definition.size
    for col in range(size):
        valid_cells = [row for row in range(size) if board.definition.valid_mask[row][col]]
        if valid_cells and all(board.occupied[row][col] for row in valid_cells):
            cols.append(col)
    return cols


def clear_rows_and_columns(board: BoardState, rows: list[int], columns: list[int]) -> BoardState:
    new_board = board.clone()
    size = board.definition.size
    for row in rows:
        for col in range(size):
            if board.definition.valid_mask[row][col]:
                new_board.occupied[row][col] = False
    for col in columns:
        for row in range(size):
            if board.definition.valid_mask[row][col]:
                new_board.occupied[row][col] = False
    return new_board


def has_any_valid_placement(board: BoardState, block: BlockInstance) -> bool:
    size = board.definition.size
    for row in range(size):
        for col in range(size):
            if validate_placement(board, block, Cell(row, col)).is_valid:
                return True
    return False


def has_any_playable_block(board: BoardState, blocks: list[BlockInstance]) -> bool:
    return any(has_any_valid_placement(board, block) for block in blocks)
