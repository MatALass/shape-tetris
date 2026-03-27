from __future__ import annotations

from pathlib import Path

from shape_tetris.game.engine import GameEngine
from shape_tetris.game.enums import BlockSelectionMode, BoardShape
from shape_tetris.game.models import GameConfig
from shape_tetris.game.persistence import load_game_state, save_game_state
from shape_tetris.game.state import create_initial_game_state


class GameSession:
    def __init__(self, engine: GameEngine, save_path: Path) -> None:
        self.engine = engine
        self.save_path = save_path

    @classmethod
    def new(
        cls,
        board_shape: BoardShape,
        board_size: int,
        block_mode: BlockSelectionMode,
        save_path: Path,
        seed: int | None = None,
    ) -> "GameSession":
        config = GameConfig(
            board_shape=board_shape,
            board_size=board_size,
            block_mode=block_mode,
            seed=seed,
        )
        state = create_initial_game_state(config)
        return cls(engine=GameEngine(state), save_path=save_path)

    @classmethod
    def load(cls, save_path: Path) -> "GameSession":
        state = load_game_state(save_path)
        return cls(engine=GameEngine(state), save_path=save_path)

    def save(self) -> None:
        save_game_state(self.save_path, self.engine.state)
