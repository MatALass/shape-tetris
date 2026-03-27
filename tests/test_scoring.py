from shape_tetris.game.models import ScoreState
from shape_tetris.game.scoring import compute_score_breakdown, update_score


def test_compute_score_breakdown_counts_all_components():
    breakdown = compute_score_breakdown(
        placed_cell_count=4,
        cleared_row_count=1,
        cleared_column_count=1,
        combo_count=2,
    )
    assert breakdown.placed_cells_points == 4
    assert breakdown.cleared_rows_points == 10
    assert breakdown.cleared_columns_points == 10
    assert breakdown.total_points >= 24


def test_update_score_accumulates_values():
    score = ScoreState()
    breakdown = compute_score_breakdown(3, 1, 0, 1)
    updated = update_score(score, breakdown, 1, 0, 3)
    assert updated.points == breakdown.total_points
    assert updated.lines_cleared == 1
    assert updated.cells_placed == 3
