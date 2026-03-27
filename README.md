# Shape Tetris

A geometric puzzle game built in **Python** with **pygame-ce**, inspired by an academic Tetris-like project and redesigned as a structured, testable, modern software project.

Instead of falling tetrominoes in real time, the player strategically places blocks on a **geometric board** — **circle**, **diamond**, or **triangle** — to complete and clear rows and columns, maximize score, and survive as long as possible.

## Features

- 3 board shapes:
  - Circle
  - Diamond
  - Triangle
- Strategic block placement gameplay
- Block rotation
- Row and column clearing
- Score system
- Save / load support
- Two block selection modes:
  - Random three
  - Full catalog
- Testable game engine separated from the UI
- `src/` project layout
- Automated tests with `pytest`

## Why this project matters

This project is not a basic Tetris clone.

It is a full redesign of an older academic assignment into a cleaner and more maintainable game project with:
- a separated domain engine,
- explicit game models,
- testable rules,
- a structured architecture,
- and a real graphical interface.

The goal was to preserve the original idea — geometric boards, block placement, row/column clearing — while turning it into a more serious and defendable software project.

## Tech stack

- Python 3.11+
- pygame-ce
- pytest
- ruff

## Project structure

```text
shape-tetris/
├─ assets/
├─ configs/
├─ docs/
├─ src/
│  └─ shape_tetris/
│     ├─ app/
│     ├─ game/
│     ├─ ui/
│     └─ main.py
├─ tests/
├─ pyproject.toml
└─ README.md