from __future__ import annotations

import pygame

from shape_tetris.game.enums import BlockSelectionMode
from shape_tetris.game.models import BlockInstance
from shape_tetris.game.block_ops import get_rotated_cells, get_block_dimensions
from shape_tetris.settings import UISettings


def draw_text(
    surface: pygame.Surface,
    font: pygame.font.Font,
    text: str,
    color: tuple[int, int, int],
    pos: tuple[int, int],
) -> None:
    rendered = font.render(text, True, color)
    surface.blit(rendered, pos)


def draw_available_blocks(
    surface: pygame.Surface,
    blocks: list[BlockInstance],
    selected_index: int | None,
    settings: UISettings,
    panel_rect: pygame.Rect,
    font: pygame.font.Font,
    small_font: pygame.font.Font,
    mode: BlockSelectionMode,
) -> list[pygame.Rect]:
    pygame.draw.rect(surface, settings.panel_color, panel_rect, border_radius=18)
    draw_text(surface, font, "Available Blocks", settings.text_color, (panel_rect.x + 20, panel_rect.y + 18))
    draw_text(
        surface,
        small_font,
        "Mode: Random Three" if mode is BlockSelectionMode.RANDOM_THREE else "Mode: Full Catalog",
        settings.text_color,
        (panel_rect.x + 20, panel_rect.y + 54),
    )
    rects: list[pygame.Rect] = []
    y = panel_rect.y + 90
    for index, block in enumerate(blocks):
        width, height = 180, 88
        item_rect = pygame.Rect(panel_rect.x + 16, y, width, height)
        selected = index == selected_index
        border_color = settings.accent_color if selected else settings.grid_line_color
        pygame.draw.rect(surface, (28, 30, 38), item_rect, border_radius=14)
        pygame.draw.rect(surface, border_color, item_rect, 2, border_radius=14)
        draw_text(surface, small_font, f"{index + 1}. {block.definition.name}", settings.text_color, (item_rect.x + 12, item_rect.y + 10))
        draw_block_miniature(surface, block, item_rect, settings)
        rects.append(item_rect)
        y += height + 12
        if y > panel_rect.bottom - 92:
            break
    return rects


def draw_block_miniature(
    surface: pygame.Surface,
    block: BlockInstance,
    rect: pygame.Rect,
    settings: UISettings,
) -> None:
    cells = get_rotated_cells(block)
    max_rows, max_cols = get_block_dimensions(block)
    cell_size = min(18, max(12, min((rect.height - 26) // max_rows, (rect.width - 90) // max_cols)))
    origin_x = rect.right - (max_cols * cell_size) - 16
    origin_y = rect.centery - (max_rows * cell_size) // 2
    occupied = set(cells)
    for row in range(max_rows):
        for col in range(max_cols):
            cell_rect = pygame.Rect(origin_x + col * cell_size, origin_y + row * cell_size, cell_size - 2, cell_size - 2)
            color = settings.occupied_cell_color if any(c.row == row and c.col == col for c in occupied) else settings.outside_cell_color
            pygame.draw.rect(surface, color, cell_rect, border_radius=4)
