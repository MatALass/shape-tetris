from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class UISettings:
    window_width: int = 1280
    window_height: int = 840
    title: str = "Shape Tetris"
    fps: int = 60
    save_path: Path = Path("shape_tetris_save.json")
    background_color: tuple[int, int, int] = (22, 24, 31)
    panel_color: tuple[int, int, int] = (36, 39, 49)
    grid_line_color: tuple[int, int, int] = (55, 60, 75)
    empty_cell_color: tuple[int, int, int] = (65, 70, 88)
    occupied_cell_color: tuple[int, int, int] = (140, 180, 255)
    invalid_preview_color: tuple[int, int, int] = (230, 85, 85)
    valid_preview_color: tuple[int, int, int] = (95, 205, 120)
    outside_cell_color: tuple[int, int, int] = (18, 20, 27)
    text_color: tuple[int, int, int] = (240, 243, 250)
    accent_color: tuple[int, int, int] = (255, 201, 87)


DEFAULT_UI_SETTINGS = UISettings()
