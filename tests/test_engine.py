from pathlib import Path

from shape_tetris.game.engine import GameEngine
from shape_tetris.game.enums import BlockSelectionMode, BoardShape, GameStatus
from shape_tetris.game.models import GameConfig
from shape_tetris.game.persistence import load_game_state, save_game_state
from shape_tetris.game.state import create_initial_game_state


def test_engine_initial_state_has_blocks():
    config = GameConfig(BoardShape.CIRCLE, 21, BlockSelectionMode.RANDOM_THREE, seed=42)
    state = create_initial_game_state(config)
    engine = GameEngine(state)
    assert len(engine.state.available_blocks) == 3
    assert engine.state.status is GameStatus.RUNNING


def test_engine_can_rotate_selected_block():
    config = GameConfig(BoardShape.CIRCLE, 21, BlockSelectionMode.RANDOM_THREE, seed=42)
    state = create_initial_game_state(config)
    engine = GameEngine(state)
    before = engine.get_selected_block().rotation
    engine.rotate_selected_block()
    after = engine.get_selected_block().rotation
    assert after == (before + 1) % 4


def test_engine_save_and_load_round_trip(tmp_path: Path):
    config = GameConfig(BoardShape.DIAMOND, 21, BlockSelectionMode.RANDOM_THREE, seed=7)
    state = create_initial_game_state(config)
    engine = GameEngine(state)
    save_path = tmp_path / "save.json"
    save_game_state(save_path, engine.state)
    loaded = load_game_state(save_path)
    assert loaded.config.board_shape is BoardShape.DIAMOND
    assert len(loaded.available_blocks) == len(engine.state.available_blocks)
