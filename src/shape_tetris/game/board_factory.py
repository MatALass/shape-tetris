from __future__ import annotations

from shape_tetris.game.enums import BoardShape
from shape_tetris.game.models import BoardDefinition


def build_board_definition(shape: BoardShape, size: int) -> BoardDefinition:
    if size < 21 or size % 2 == 0:
        raise ValueError("Board size must be an odd integer >= 21.")
    if shape is BoardShape.CIRCLE:
        mask = build_circle_mask(size)
    elif shape is BoardShape.DIAMOND:
        mask = build_diamond_mask(size)
    elif shape is BoardShape.TRIANGLE:
        mask = build_triangle_mask(size)
    else:
        raise ValueError(f"Unsupported shape: {shape}")
    return BoardDefinition(shape=shape, size=size, valid_mask=mask)


def build_circle_mask(size: int) -> tuple[tuple[bool, ...], ...]:
    center = size // 2
    radius_sq = center * center
    return tuple(
        tuple((row - center) ** 2 + (col - center) ** 2 <= radius_sq for col in range(size))
        for row in range(size)
    )


def build_diamond_mask(size: int) -> tuple[tuple[bool, ...], ...]:
    center = size // 2
    radius = center
    return tuple(
        tuple(abs(row - center) + abs(col - center) <= radius for col in range(size))
        for row in range(size)
    )


def build_triangle_mask(size: int) -> tuple[tuple[bool, ...], ...]:
    center = size // 2
    mask: list[tuple[bool, ...]] = []
    for row in range(size):
        half_width = row // 2
        left = center - half_width
        right = center + half_width
        line = tuple(left <= col <= right for col in range(size))
        mask.append(line)
    return tuple(mask)
