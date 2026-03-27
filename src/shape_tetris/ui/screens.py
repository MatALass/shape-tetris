from __future__ import annotations

from dataclasses import dataclass

from shape_tetris.game.enums import BlockSelectionMode, BoardShape


@dataclass(slots=True)
class MenuState:
    shape_index: int = 0
    size_index: int = 0
    mode_index: int = 0
    selected_row: int = 0

    @property
    def selected_shape(self) -> BoardShape:
        return list(BoardShape)[self.shape_index]

    @property
    def selected_size(self) -> int:
        return [21, 25, 31][self.size_index]

    @property
    def selected_mode(self) -> BlockSelectionMode:
        return list(BlockSelectionMode)[self.mode_index]
