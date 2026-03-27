from __future__ import annotations

import pygame

from shape_tetris.game.block_ops import get_rotated_cells
from shape_tetris.game.enums import GameStatus
from shape_tetris.game.models import Cell, PlacementValidation
from shape_tetris.settings import UISettings
from shape_tetris.ui.hud import draw_available_blocks, draw_text


class GameRenderer:
    def __init__(self, surface: pygame.Surface, settings: UISettings) -> None:
        self.surface = surface
        self.settings = settings
        self.title_font = pygame.font.SysFont("arial", 34, bold=True)
        self.body_font = pygame.font.SysFont("arial", 24)
        self.small_font = pygame.font.SysFont("arial", 18)

    def compute_layout(self, board_size: int) -> tuple[tuple[int, int], int, pygame.Rect]:
        max_cell_w = 760 // board_size
        max_cell_h = 760 // board_size
        cell_size = max(16, min(max_cell_w, max_cell_h))
        board_origin = (48, 48)
        panel_rect = pygame.Rect(930, 48, 240, 744)
        return board_origin, cell_size, panel_rect

    def render_game(
        self,
        engine,
        hovered_cell: Cell | None,
        validation: PlacementValidation | None,
    ) -> dict:
        self.surface.fill(self.settings.background_color)
        state = engine.state
        board_origin, cell_size, panel_rect = self.compute_layout(state.board.definition.size)
        self._draw_board(engine, board_origin, cell_size, validation)
        block_rects = draw_available_blocks(
            self.surface,
            state.available_blocks,
            state.selected_block_index,
            self.settings,
            panel_rect,
            self.body_font,
            self.small_font,
            state.config.block_mode,
        )
        self._draw_header(engine, board_origin, panel_rect)
        self._draw_footer(engine, panel_rect)
        if state.status is GameStatus.PAUSED:
            self._draw_overlay("Paused", "Press Esc to resume")
        elif state.status is GameStatus.GAME_OVER:
            self._draw_overlay("Game Over", "Press Enter to return to menu")
        return {
            "board_origin": board_origin,
            "cell_size": cell_size,
            "panel_rect": panel_rect,
            "block_rects": block_rects,
        }

    def _draw_header(self, engine, board_origin: tuple[int, int], panel_rect: pygame.Rect) -> None:
        state = engine.state
        draw_text(self.surface, self.title_font, "Shape Tetris", self.settings.text_color, (board_origin[0], 10))
        draw_text(
            self.surface,
            self.small_font,
            f"Shape: {state.config.board_shape.value.title()}  |  Size: {state.config.board_size}",
            self.settings.text_color,
            (board_origin[0], 810),
        )
        draw_text(
            self.surface,
            self.small_font,
            f"Score: {state.score.points}  |  Lines: {state.score.lines_cleared}  |  Cols: {state.score.columns_cleared}",
            self.settings.text_color,
            (board_origin[0] + 360, 810),
        )

    def _draw_footer(self, engine, panel_rect: pygame.Rect) -> None:
        help_lines = [
            "R / Shift+R: rotate",
            "1 / 2 / 3: select block",
            "S: save",
            "Esc: pause",
            "Q: quit",
        ]
        y = panel_rect.bottom - 150
        for line in help_lines:
            draw_text(self.surface, self.small_font, line, self.settings.text_color, (panel_rect.x + 20, y))
            y += 24

    def _draw_board(
        self,
        engine,
        board_origin: tuple[int, int],
        cell_size: int,
        validation: PlacementValidation | None,
    ) -> None:
        state = engine.state
        preview_cells = {}
        if validation is not None:
            preview_color = (
                self.settings.valid_preview_color if validation.is_valid else self.settings.invalid_preview_color
            )
            preview_cells = {(cell.row, cell.col): preview_color for cell in validation.cells}
        for row in range(state.board.definition.size):
            for col in range(state.board.definition.size):
                x = board_origin[0] + col * cell_size
                y = board_origin[1] + row * cell_size
                rect = pygame.Rect(x, y, cell_size - 1, cell_size - 1)
                if not state.board.definition.valid_mask[row][col]:
                    color = self.settings.outside_cell_color
                elif (row, col) in preview_cells:
                    color = preview_cells[(row, col)]
                elif state.board.occupied[row][col]:
                    color = self.settings.occupied_cell_color
                else:
                    color = self.settings.empty_cell_color
                pygame.draw.rect(self.surface, color, rect, border_radius=4)

    def render_menu(
        self,
        shape_index: int,
        size_index: int,
        mode_index: int,
        selected_row: int,
        save_exists: bool,
        options: dict,
    ) -> None:
        self.surface.fill(self.settings.background_color)
        title = self.title_font.render("Shape Tetris", True, self.settings.text_color)
        subtitle = self.body_font.render("Geometric puzzle placement game", True, self.settings.text_color)
        self.surface.blit(title, (72, 70))
        self.surface.blit(subtitle, (72, 118))

        rows = [
            ("Shape", options["shapes"][shape_index].title()),
            ("Size", str(options["sizes"][size_index])),
            ("Mode", options["modes"][mode_index].replace("_", " ").title()),
            ("Start", "Press Enter"),
            ("Load", "Press L" if save_exists else "No save available"),
        ]
        y = 220
        for idx, (label, value) in enumerate(rows):
            selected = idx == selected_row
            rect = pygame.Rect(72, y, 560, 58)
            fill = self.settings.panel_color if selected else (28, 30, 38)
            pygame.draw.rect(self.surface, fill, rect, border_radius=16)
            pygame.draw.rect(
                self.surface,
                self.settings.accent_color if selected else self.settings.grid_line_color,
                rect,
                2,
                border_radius=16,
            )
            draw_text(self.surface, self.body_font, label, self.settings.text_color, (92, y + 14))
            draw_text(self.surface, self.body_font, value, self.settings.text_color, (320, y + 14))
            y += 76

        help_texts = [
            "Use arrow keys to change settings.",
            "Press Enter to start a new game.",
            "Press L to load the save file.",
        ]
        y = 640
        for text in help_texts:
            draw_text(self.surface, self.small_font, text, self.settings.text_color, (72, y))
            y += 30

    def _draw_overlay(self, title: str, subtitle: str) -> None:
        overlay = pygame.Surface((self.surface.get_width(), self.surface.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.surface.blit(overlay, (0, 0))
        box = pygame.Rect(360, 300, 560, 180)
        pygame.draw.rect(self.surface, self.settings.panel_color, box, border_radius=20)
        pygame.draw.rect(self.surface, self.settings.accent_color, box, 3, border_radius=20)
        draw_text(self.surface, self.title_font, title, self.settings.text_color, (box.x + 170, box.y + 48))
        draw_text(self.surface, self.body_font, subtitle, self.settings.text_color, (box.x + 135, box.y + 108))
