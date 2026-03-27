from __future__ import annotations

from shape_tetris.game.models import ScoreBreakdown, ScoreState


ROW_CLEAR_POINTS = 10
COLUMN_CLEAR_POINTS = 10
PLACED_CELL_POINTS = 1
COMBO_MULTIPLIER = 5


def compute_score_breakdown(
    placed_cell_count: int,
    cleared_row_count: int,
    cleared_column_count: int,
    combo_count: int,
) -> ScoreBreakdown:
    placed_cells_points = placed_cell_count * PLACED_CELL_POINTS
    cleared_rows_points = cleared_row_count * ROW_CLEAR_POINTS
    cleared_columns_points = cleared_column_count * COLUMN_CLEAR_POINTS
    line_count = cleared_row_count + cleared_column_count
    combo_points = max(0, line_count - 1) * COMBO_MULTIPLIER + max(0, combo_count - 1) * 2
    total_points = (
        placed_cells_points
        + cleared_rows_points
        + cleared_columns_points
        + combo_points
    )
    return ScoreBreakdown(
        placed_cells_points=placed_cells_points,
        cleared_rows_points=cleared_rows_points,
        cleared_columns_points=cleared_columns_points,
        combo_points=combo_points,
        total_points=total_points,
    )


def update_score(
    score: ScoreState,
    breakdown: ScoreBreakdown,
    cleared_row_count: int,
    cleared_column_count: int,
    placed_cell_count: int,
) -> ScoreState:
    combo_count = score.combo_count + 1 if (cleared_row_count + cleared_column_count) > 0 else 0
    return ScoreState(
        points=score.points + breakdown.total_points,
        lines_cleared=score.lines_cleared + cleared_row_count,
        columns_cleared=score.columns_cleared + cleared_column_count,
        cells_placed=score.cells_placed + placed_cell_count,
        combo_count=combo_count,
    )
