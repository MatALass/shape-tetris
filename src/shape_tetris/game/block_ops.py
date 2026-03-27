from __future__ import annotations

from shape_tetris.game.models import BlockDefinition, BlockInstance, Cell


def normalize_cells(cells: tuple[Cell, ...]) -> tuple[Cell, ...]:
    min_row = min(cell.row for cell in cells)
    min_col = min(cell.col for cell in cells)
    normalized = tuple(sorted((Cell(cell.row - min_row, cell.col - min_col) for cell in cells)))
    return normalized


def rotate_cells(cells: tuple[Cell, ...], quarter_turns: int) -> tuple[Cell, ...]:
    quarter_turns = quarter_turns % 4
    rotated = cells
    for _ in range(quarter_turns):
        rotated = tuple(Cell(cell.col, -cell.row) for cell in rotated)
        rotated = normalize_cells(rotated)
    return rotated


def rotate_block(block: BlockDefinition, rotation: int) -> BlockDefinition:
    return BlockDefinition(
        block_id=block.block_id,
        name=block.name,
        cells=rotate_cells(block.cells, rotation),
        tags=block.tags,
    )


def instantiate_block(definition: BlockDefinition, rotation: int = 0) -> BlockInstance:
    return BlockInstance(definition=definition, rotation=rotation % 4)


def get_rotated_cells(block: BlockInstance) -> tuple[Cell, ...]:
    return rotate_cells(block.definition.cells, block.rotation)


def get_block_dimensions(block: BlockInstance) -> tuple[int, int]:
    cells = get_rotated_cells(block)
    max_row = max(cell.row for cell in cells)
    max_col = max(cell.col for cell in cells)
    return max_row + 1, max_col + 1


def get_absolute_cells(block: BlockInstance, anchor: Cell) -> tuple[Cell, ...]:
    return tuple(
        Cell(anchor.row + cell.row, anchor.col + cell.col)
        for cell in get_rotated_cells(block)
    )
