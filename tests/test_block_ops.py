from shape_tetris.game.block_library import load_common_blocks
from shape_tetris.game.block_ops import get_absolute_cells, get_block_dimensions, instantiate_block, rotate_cells
from shape_tetris.game.models import Cell


def test_rotate_cells_keeps_cell_count():
    block = load_common_blocks()[3]
    rotated = rotate_cells(block.cells, 1)
    assert len(rotated) == len(block.cells)


def test_get_block_dimensions_after_rotation():
    block = load_common_blocks()[1]
    instance = instantiate_block(block, rotation=1)
    dims = get_block_dimensions(instance)
    assert dims == (2, 1)


def test_get_absolute_cells_offsets_coords():
    block = load_common_blocks()[0]
    instance = instantiate_block(block)
    cells = get_absolute_cells(instance, Cell(5, 7))
    assert cells == (Cell(5, 7),)
