from __future__ import annotations

from shape_tetris.game.enums import BoardShape
from shape_tetris.game.models import BlockDefinition, Cell


def _make_block(block_id: str, name: str, coords: list[tuple[int, int]], *tags: str) -> BlockDefinition:
    return BlockDefinition(
        block_id=block_id,
        name=name,
        cells=tuple(Cell(row, col) for row, col in coords),
        tags=tuple(tags),
    )


def load_common_blocks() -> list[BlockDefinition]:
    return [
        _make_block("mono", "Monomino", [(0, 0)], "starter"),
        _make_block("domino_h", "Domino", [(0, 0), (0, 1)], "starter"),
        _make_block("tromino_i", "I Tromino", [(0, 0), (0, 1), (0, 2)]),
        _make_block("tromino_l", "L Tromino", [(0, 0), (1, 0), (1, 1)]),
        _make_block("tetro_o", "Square", [(0, 0), (0, 1), (1, 0), (1, 1)]),
        _make_block("tetro_i", "I Tetromino", [(0, 0), (0, 1), (0, 2), (0, 3)]),
        _make_block("tetro_t", "T Tetromino", [(0, 0), (0, 1), (0, 2), (1, 1)]),
        _make_block("tetro_l", "L Tetromino", [(0, 0), (1, 0), (2, 0), (2, 1)]),
        _make_block("tetro_s", "S Tetromino", [(0, 1), (0, 2), (1, 0), (1, 1)]),
        _make_block("pento_plus", "Plus", [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], "advanced"),
        _make_block("pento_u", "U", [(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)], "advanced"),
    ]


def load_circle_blocks() -> list[BlockDefinition]:
    return [
        _make_block("arc_3", "Arc 3", [(0, 0), (0, 1), (1, 1)], "circle"),
        _make_block("arc_5", "Arc 5", [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2)], "circle"),
    ]


def load_diamond_blocks() -> list[BlockDefinition]:
    return [
        _make_block("diamond_small", "Small Diamond", [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)], "diamond"),
        _make_block("arrow", "Arrow", [(0, 1), (1, 0), (1, 1), (2, 1)], "diamond"),
    ]


def load_triangle_blocks() -> list[BlockDefinition]:
    return [
        _make_block("wedge", "Wedge", [(0, 0), (1, 0), (1, 1)], "triangle"),
        _make_block("stair_4", "Stair 4", [(0, 0), (1, 0), (1, 1), (2, 1)], "triangle"),
    ]


def get_blocks_for_shape(shape: BoardShape) -> list[BlockDefinition]:
    base = load_common_blocks()
    if shape is BoardShape.CIRCLE:
        return base + load_circle_blocks()
    if shape is BoardShape.DIAMOND:
        return base + load_diamond_blocks()
    if shape is BoardShape.TRIANGLE:
        return base + load_triangle_blocks()
    raise ValueError(f"Unsupported shape: {shape}")
