from shape_tetris.game.block_library import load_common_blocks
from shape_tetris.game.block_ops import instantiate_block
from shape_tetris.game.board_factory import build_board_definition
from shape_tetris.game.enums import BoardShape
from shape_tetris.game.models import BoardState, Cell
from shape_tetris.game.rules import (
    apply_placement,
    clear_rows_and_columns,
    get_full_columns,
    get_full_rows,
    has_any_valid_placement,
    validate_placement,
)


def build_square_board(size: int = 21):
    definition = build_board_definition(BoardShape.CIRCLE, size)
    return BoardState.empty_from_definition(definition)


def test_validate_placement_accepts_empty_valid_position():
    board = build_square_board()
    block = instantiate_block(load_common_blocks()[0])
    result = validate_placement(board, block, Cell(10, 10))
    assert result.is_valid is True


def test_validate_placement_rejects_overlap():
    board = build_square_board()
    block = instantiate_block(load_common_blocks()[0])
    board = apply_placement(board, block, Cell(10, 10))
    result = validate_placement(board, block, Cell(10, 10))
    assert result.is_valid is False


def test_apply_placement_marks_cells_occupied():
    board = build_square_board()
    block = instantiate_block(load_common_blocks()[1])
    new_board = apply_placement(board, block, Cell(10, 10))
    assert new_board.occupied[10][10] is True
    assert new_board.occupied[10][11] is True


def test_get_full_rows_detects_complete_valid_row():
    board = build_square_board()
    row = 10
    for col, valid in enumerate(board.definition.valid_mask[row]):
        if valid:
            board.occupied[row][col] = True
    rows = get_full_rows(board)
    assert rows == [row]


def test_get_full_columns_detects_complete_valid_column():
    board = build_square_board()
    col = 10
    for row in range(board.definition.size):
        if board.definition.valid_mask[row][col]:
            board.occupied[row][col] = True
    columns = get_full_columns(board)
    assert columns == [col]


def test_clear_rows_and_columns_empties_cells():
    board = build_square_board()
    row = 10
    col = 10
    for c, valid in enumerate(board.definition.valid_mask[row]):
        if valid:
            board.occupied[row][c] = True
    for r in range(board.definition.size):
        if board.definition.valid_mask[r][col]:
            board.occupied[r][col] = True
    cleared = clear_rows_and_columns(board, [row], [col])
    for c, valid in enumerate(board.definition.valid_mask[row]):
        if valid:
            assert cleared.occupied[row][c] is False
    for r in range(board.definition.size):
        if board.definition.valid_mask[r][col]:
            assert cleared.occupied[r][col] is False


def test_has_any_valid_placement_detects_available_move():
    board = build_square_board()
    block = instantiate_block(load_common_blocks()[0])
    assert has_any_valid_placement(board, block) is True
