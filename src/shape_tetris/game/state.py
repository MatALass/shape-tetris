from __future__ import annotations

import random

from shape_tetris.game.block_library import get_blocks_for_shape
from shape_tetris.game.block_ops import instantiate_block
from shape_tetris.game.board_factory import build_board_definition
from shape_tetris.game.enums import BlockSelectionMode, GameStatus
from shape_tetris.game.models import BoardState, GameConfig, GameState, ScoreState


def create_initial_game_state(config: GameConfig) -> GameState:
    definition = build_board_definition(config.board_shape, config.board_size)
    board = BoardState.empty_from_definition(definition)
    score = ScoreState()
    catalog = get_blocks_for_shape(config.board_shape)
    rng = random.Random(config.seed)
    if config.block_mode is BlockSelectionMode.RANDOM_THREE:
        available_blocks = [instantiate_block(rng.choice(catalog)) for _ in range(3)]
        selected_block_index = 0
    else:
        available_blocks = [instantiate_block(block) for block in catalog]
        selected_block_index = 0 if available_blocks else None
    return GameState(
        status=GameStatus.RUNNING,
        config=config,
        board=board,
        score=score,
        available_blocks=available_blocks,
        selected_block_index=selected_block_index,
        turn_index=0,
        total_moves=0,
    )
