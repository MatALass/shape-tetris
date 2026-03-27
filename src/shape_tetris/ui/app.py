from __future__ import annotations

from pathlib import Path

import pygame

from shape_tetris.app.session import GameSession
from shape_tetris.game.enums import BlockSelectionMode, BoardShape, GameStatus
from shape_tetris.game.models import Cell
from shape_tetris.settings import DEFAULT_UI_SETTINGS
from shape_tetris.ui.input_mapper import pixel_to_board_cell
from shape_tetris.ui.renderer import GameRenderer
from shape_tetris.ui.screens import MenuState


def run_game() -> None:
    pygame.init()
    settings = DEFAULT_UI_SETTINGS
    screen = pygame.display.set_mode((settings.window_width, settings.window_height))
    pygame.display.set_caption(settings.title)
    clock = pygame.time.Clock()
    renderer = GameRenderer(screen, settings)

    menu = MenuState()
    ui_mode = "menu"
    session: GameSession | None = None
    hovered_cell: Cell | None = None
    validation = None

    options = {
        "shapes": [shape.value for shape in BoardShape],
        "sizes": [21, 25, 31],
        "modes": [mode.value for mode in BlockSelectionMode],
    }

    running = True
    while running:
        if ui_mode == "menu":
            renderer.render_menu(
                menu.shape_index,
                menu.size_index,
                menu.mode_index,
                menu.selected_row,
                settings.save_path.exists(),
                options,
            )
        else:
            assert session is not None
            layout = renderer.render_game(session.engine, hovered_cell, validation)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if ui_mode == "menu":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        menu.selected_row = (menu.selected_row - 1) % 5
                    elif event.key == pygame.K_DOWN:
                        menu.selected_row = (menu.selected_row + 1) % 5
                    elif event.key == pygame.K_LEFT:
                        _update_menu(menu, -1)
                    elif event.key == pygame.K_RIGHT:
                        _update_menu(menu, 1)
                    elif event.key == pygame.K_RETURN:
                        session = GameSession.new(
                            board_shape=menu.selected_shape,
                            board_size=menu.selected_size,
                            block_mode=menu.selected_mode,
                            save_path=settings.save_path,
                        )
                        ui_mode = "game"
                        hovered_cell = None
                        validation = None
                    elif event.key == pygame.K_l and settings.save_path.exists():
                        session = GameSession.load(settings.save_path)
                        ui_mode = "game"
                        hovered_cell = None
                        validation = None
            else:
                assert session is not None
                engine = session.engine
                if event.type == pygame.KEYDOWN:
                    if engine.state.status is GameStatus.GAME_OVER:
                        if event.key == pygame.K_RETURN:
                            ui_mode = "menu"
                        elif event.key == pygame.K_q:
                            running = False
                    elif event.key == pygame.K_ESCAPE:
                        if engine.state.status is GameStatus.RUNNING:
                            engine.pause()
                        elif engine.state.status is GameStatus.PAUSED:
                            engine.resume()
                    elif event.key == pygame.K_q:
                        running = False
                    elif event.key == pygame.K_s:
                        session.save()
                    elif event.key == pygame.K_r:
                        shift_pressed = bool(event.mod & pygame.KMOD_SHIFT)
                        engine.rotate_selected_block(clockwise=not shift_pressed)
                    elif event.key == pygame.K_e:
                        engine.rotate_selected_block(clockwise=False)
                    elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        index = event.key - pygame.K_1
                        if index < len(engine.state.available_blocks):
                            engine.select_block(index)

                if event.type == pygame.MOUSEMOTION:
                    layout = renderer.compute_layout(engine.state.board.definition.size)
                    board_origin, cell_size, panel_rect = layout
                    hovered_cell = pixel_to_board_cell(
                        event.pos[0],
                        event.pos[1],
                        board_origin,
                        cell_size,
                        engine.state.board.definition.size,
                    )
                    if hovered_cell is not None:
                        validation = engine.preview_selected_block(hovered_cell)
                    else:
                        validation = None

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    layout = renderer.compute_layout(engine.state.board.definition.size)
                    board_origin, cell_size, panel_rect = layout
                    panel_x = panel_rect.x
                    if event.pos[0] >= panel_x:
                        clicked_index = _get_clicked_block_index(event.pos, panel_rect)
                        if clicked_index is not None and clicked_index < len(engine.state.available_blocks):
                            engine.select_block(clicked_index)
                    elif hovered_cell is not None and engine.state.status is GameStatus.RUNNING:
                        result = engine.place_selected_block(hovered_cell)
                        validation = engine.preview_selected_block(hovered_cell) if not result.game_over else None

        clock.tick(settings.fps)

    pygame.quit()


def _update_menu(menu: MenuState, delta: int) -> None:
    if menu.selected_row == 0:
        menu.shape_index = (menu.shape_index + delta) % 3
    elif menu.selected_row == 1:
        menu.size_index = (menu.size_index + delta) % 3
    elif menu.selected_row == 2:
        menu.mode_index = (menu.mode_index + delta) % 2


def _get_clicked_block_index(pos: tuple[int, int], panel_rect: pygame.Rect) -> int | None:
    x, y = pos
    local_y = y - (panel_rect.y + 90)
    if x < panel_rect.x + 16 or x > panel_rect.x + 196 or local_y < 0:
        return None
    block_span = 100
    index = local_y // block_span
    return int(index)
