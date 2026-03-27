from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from shape_tetris.game.block_library import get_blocks_for_shape
from shape_tetris.game.block_ops import instantiate_block
from shape_tetris.game.board_factory import build_board_definition
from shape_tetris.game.enums import BlockSelectionMode, BoardShape, GameStatus
from shape_tetris.game.models import BoardState, GameConfig, GameState, SaveData, ScoreState


def _serialize_config(config: GameConfig) -> dict:
    return {
        "board_shape": config.board_shape.value,
        "board_size": config.board_size,
        "block_mode": config.block_mode.value,
        "seed": config.seed,
    }


def _serialize_state(state: GameState) -> SaveData:
    return SaveData(
        version=state.save_version,
        config=_serialize_config(state.config),
        status=state.status.value,
        score={
            "points": state.score.points,
            "lines_cleared": state.score.lines_cleared,
            "columns_cleared": state.score.columns_cleared,
            "cells_placed": state.score.cells_placed,
            "combo_count": state.score.combo_count,
        },
        occupied=state.board.occupied,
        available_blocks=[
            {
                "block_id": block.definition.block_id,
                "rotation": block.rotation,
            }
            for block in state.available_blocks
        ],
        selected_block_index=state.selected_block_index,
        turn_index=state.turn_index,
        total_moves=state.total_moves,
    )


def save_game_state(path: str | Path, state: GameState) -> None:
    save_data = _serialize_state(state)
    Path(path).write_text(json.dumps(asdict(save_data), indent=2), encoding="utf-8")


def load_game_state(path: str | Path) -> GameState:
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    config = GameConfig(
        board_shape=BoardShape(raw["config"]["board_shape"]),
        board_size=raw["config"]["board_size"],
        block_mode=BlockSelectionMode(raw["config"]["block_mode"]),
        seed=raw["config"]["seed"],
    )
    definition = build_board_definition(config.board_shape, config.board_size)
    board = BoardState(definition=definition, occupied=raw["occupied"])
    score = ScoreState(**raw["score"])
    catalog = {block.block_id: block for block in get_blocks_for_shape(config.board_shape)}
    available_blocks = [
        instantiate_block(catalog[item["block_id"]], item["rotation"])
        for item in raw["available_blocks"]
    ]
    return GameState(
        status=GameStatus(raw["status"]),
        config=config,
        board=board,
        score=score,
        available_blocks=available_blocks,
        selected_block_index=raw["selected_block_index"],
        turn_index=raw["turn_index"],
        total_moves=raw["total_moves"],
        save_version=raw["version"],
    )
