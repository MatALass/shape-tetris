from shape_tetris.game.board_factory import (
    build_board_definition,
    build_circle_mask,
    build_diamond_mask,
    build_triangle_mask,
)
from shape_tetris.game.enums import BoardShape


def test_build_circle_mask_has_valid_center():
    mask = build_circle_mask(21)
    assert mask[10][10] is True


def test_build_diamond_mask_corners_are_invalid():
    mask = build_diamond_mask(21)
    assert mask[0][0] is False
    assert mask[10][10] is True


def test_build_triangle_mask_top_is_single_cell():
    mask = build_triangle_mask(21)
    assert sum(mask[0]) == 1
    assert sum(mask[-1]) >= sum(mask[0])


def test_build_board_definition_rejects_even_size():
    try:
        build_board_definition(BoardShape.CIRCLE, 20)
    except ValueError:
        assert True
    else:
        assert False
