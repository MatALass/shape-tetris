from __future__ import annotations

import random

from shape_tetris.game.block_library import get_blocks_for_shape
from shape_tetris.game.block_ops import get_rotated_cells, instantiate_block
from shape_tetris.game.enums import BlockSelectionMode, GameStatus
from shape_tetris.game.models import Cell, GameState, MoveResult
from shape_tetris.game.rules import (
    apply_placement,
    clear_rows_and_columns,
    get_full_columns,
    get_full_rows,
    has_any_playable_block,
    validate_placement,
)
from shape_tetris.game.scoring import compute_score_breakdown, update_score


class GameEngine:
    def __init__(self, initial_state: GameState) -> None:
        self._state = initial_state
        self._catalog = get_blocks_for_shape(initial_state.config.board_shape)
        self._rng = random.Random(initial_state.config.seed)

    @property
    def state(self) -> GameState:
        return self._state

    def select_block(self, index: int) -> None:
        if not 0 <= index < len(self._state.available_blocks):
            raise IndexError("Selected block index is out of range.")
        self._state.selected_block_index = index

    def get_selected_block(self):
        if self._state.selected_block_index is None:
            return None
        if not self._state.available_blocks:
            return None
        if self._state.selected_block_index >= len(self._state.available_blocks):
            return None
        return self._state.available_blocks[self._state.selected_block_index]

    def rotate_selected_block(self, clockwise: bool = True) -> None:
        selected = self.get_selected_block()
        if selected is None:
            return
        delta = 1 if clockwise else -1
        new_rotation = (selected.rotation + delta) % 4
        self._state.available_blocks[self._state.selected_block_index] = instantiate_block(
            selected.definition,
            new_rotation,
        )

    def preview_selected_block(self, anchor: Cell):
        selected = self.get_selected_block()
        if selected is None:
            return validate_placement(self._state.board, instantiate_block(self._catalog[0]), anchor)
        return validate_placement(self._state.board, selected, anchor)

    def place_selected_block(self, anchor: Cell) -> MoveResult:
        selected = self.get_selected_block()
        if selected is None:
            return MoveResult(False, "No block selected.", 0, 0, 0, self.is_game_over(), None)

        validation = validate_placement(self._state.board, selected, anchor)
        if not validation.is_valid:
            return MoveResult(False, validation.reason, 0, 0, 0, self.is_game_over(), None)

        new_board = apply_placement(self._state.board, selected, anchor)
        full_rows = get_full_rows(new_board)
        full_columns = get_full_columns(new_board)
        if full_rows or full_columns:
            new_board = clear_rows_and_columns(new_board, full_rows, full_columns)

        breakdown = compute_score_breakdown(
            placed_cell_count=len(get_rotated_cells(selected)),
            cleared_row_count=len(full_rows),
            cleared_column_count=len(full_columns),
            combo_count=self._state.score.combo_count + 1,
        )
        self._state.score = update_score(
            self._state.score,
            breakdown,
            len(full_rows),
            len(full_columns),
            len(get_rotated_cells(selected)),
        )
        self._state.board = new_board
        consumed_index = self._state.selected_block_index
        self._consume_selected_block()
        self._state.turn_index += 1
        self._state.total_moves += 1

        game_over = self.is_game_over()
        if game_over:
            self._state.status = GameStatus.GAME_OVER

        return MoveResult(
            success=True,
            reason=None,
            lines_cleared=len(full_rows),
            columns_cleared=len(full_columns),
            score_gained=breakdown.total_points,
            game_over=game_over,
            consumed_block_index=consumed_index,
        )

    def _consume_selected_block(self) -> None:
        index = self._state.selected_block_index
        if index is None:
            return
        mode = self._state.config.block_mode
        if mode is BlockSelectionMode.RANDOM_THREE:
            self._state.available_blocks.pop(index)
            if not self._state.available_blocks:
                self.refill_available_blocks()
            self._state.selected_block_index = 0 if self._state.available_blocks else None
            return

        self._state.available_blocks[index] = instantiate_block(self._catalog[index % len(self._catalog)], 0)

    def refill_available_blocks(self) -> None:
        if self._state.config.block_mode is not BlockSelectionMode.RANDOM_THREE:
            return
        self._state.available_blocks = [
            instantiate_block(self._rng.choice(self._catalog))
            for _ in range(3)
        ]

    def is_game_over(self) -> bool:
        return not has_any_playable_block(self._state.board, self._state.available_blocks)

    def pause(self) -> None:
        if self._state.status is GameStatus.RUNNING:
            self._state.status = GameStatus.PAUSED

    def resume(self) -> None:
        if self._state.status is GameStatus.PAUSED:
            self._state.status = GameStatus.RUNNING
