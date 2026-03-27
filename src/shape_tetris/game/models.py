from __future__ import annotations

from dataclasses import dataclass, field

from shape_tetris.game.enums import BlockSelectionMode, BoardShape, GameStatus


@dataclass(frozen=True, slots=True, order=True)
class Cell:
    row: int
    col: int


@dataclass(frozen=True, slots=True)
class BlockDefinition:
    block_id: str
    name: str
    cells: tuple[Cell, ...]
    tags: tuple[str, ...] = ()

    def cell_count(self) -> int:
        return len(self.cells)


@dataclass(frozen=True, slots=True)
class BlockInstance:
    definition: BlockDefinition
    rotation: int = 0

    @property
    def block_id(self) -> str:
        return self.definition.block_id


@dataclass(frozen=True, slots=True)
class Placement:
    block: BlockInstance
    anchor: Cell


@dataclass(frozen=True, slots=True)
class BoardDefinition:
    shape: BoardShape
    size: int
    valid_mask: tuple[tuple[bool, ...], ...]

    def is_valid_cell(self, row: int, col: int) -> bool:
        return 0 <= row < self.size and 0 <= col < self.size and self.valid_mask[row][col]


@dataclass(slots=True)
class BoardState:
    definition: BoardDefinition
    occupied: list[list[bool]]

    @classmethod
    def empty_from_definition(cls, definition: BoardDefinition) -> "BoardState":
        occupied = [[False for _ in range(definition.size)] for _ in range(definition.size)]
        return cls(definition=definition, occupied=occupied)

    def clone(self) -> "BoardState":
        return BoardState(
            definition=self.definition,
            occupied=[row[:] for row in self.occupied],
        )


@dataclass(slots=True)
class ScoreState:
    points: int = 0
    lines_cleared: int = 0
    columns_cleared: int = 0
    cells_placed: int = 0
    combo_count: int = 0


@dataclass(frozen=True, slots=True)
class GameConfig:
    board_shape: BoardShape
    board_size: int
    block_mode: BlockSelectionMode
    seed: int | None = None


@dataclass(slots=True)
class GameState:
    status: GameStatus
    config: GameConfig
    board: BoardState
    score: ScoreState
    available_blocks: list[BlockInstance]
    selected_block_index: int | None = None
    turn_index: int = 0
    total_moves: int = 0
    save_version: int = 1


@dataclass(frozen=True, slots=True)
class PlacementValidation:
    is_valid: bool
    reason: str | None = None
    cells: tuple[Cell, ...] = ()


@dataclass(frozen=True, slots=True)
class ScoreBreakdown:
    placed_cells_points: int
    cleared_rows_points: int
    cleared_columns_points: int
    combo_points: int
    total_points: int


@dataclass(frozen=True, slots=True)
class MoveResult:
    success: bool
    reason: str | None
    lines_cleared: int
    columns_cleared: int
    score_gained: int
    game_over: bool
    consumed_block_index: int | None = None


@dataclass(frozen=True, slots=True)
class SaveData:
    version: int
    config: dict
    status: str
    score: dict
    occupied: list[list[bool]]
    available_blocks: list[dict]
    selected_block_index: int | None
    turn_index: int
    total_moves: int


@dataclass(frozen=True, slots=True)
class BlockOffer:
    blocks: tuple[BlockInstance, ...]
    source_ids: tuple[str, ...] = field(default_factory=tuple)
