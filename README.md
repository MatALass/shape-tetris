# Shape Tetris

> A geometric puzzle game in Python built with **pygame-ce**, featuring circle, diamond, and triangle boards, a clean architecture, and a fully testable game engine.

---

## Overview

**Shape Tetris** is a strategic puzzle game inspired by a university project and redesigned into a modern, maintainable software product.

Instead of real-time falling blocks, players **place shapes manually** on a **non-rectangular board** to complete and clear rows and columns.

This project focuses on:
- clean architecture
- separation of concerns
- testability
- scalability

---

## Features

- 3 geometric boards:
  - Circle
  - Diamond
  - Triangle
- Strategic block placement gameplay
- Block rotation system
- Row & column clearing
- Scoring system with combos
- Save / Load system (JSON)
- Two game modes:
  - Random 3 blocks
  - Full catalog
- Fully testable game engine (pytest)
- Clean architecture (domain / app / UI separation)

---

## Why this project matters

This is **not a simple Tetris clone**.

This project demonstrates:
- how to turn a **basic academic project into a production-ready application**
- how to design a **testable game engine**
- how to structure a **Python project with long-term maintainability**

---

## Architecture

The project follows a layered architecture:

```
shape-tetris/
├─ src/shape_tetris/
│  ├─ game/       # Core domain logic (pure Python)
│  ├─ app/        # Application orchestration
│  ├─ ui/         # Pygame rendering & input
│  └─ main.py
├─ tests/         # Unit tests
```

### Key design principles

- **Core engine independent from UI**
- **Data models clearly separated**
- **Testable rules and scoring**
- **No hidden global state**

---

## Tech Stack

- Python 3.11+
- pygame-ce
- pytest
- ruff

---

## Installation

```bash
git clone https://github.com/MatALass/shape-tetris.git
cd shape-tetris
py -m venv .venv
.venv\Scripts\activate
py -m pip install -e .[dev]
```

---

## Run the game

```bash
shape-tetris
```

or

```bash
py -m shape_tetris.main
```

---

## Run tests

```bash
py -m pytest
```

---

## Controls

### Menu
- ↑ ↓ : navigate
- ← → : change option
- Enter : confirm
- L : load save

### In-game
- Mouse : place blocks
- 1 / 2 / 3 : select block
- R : rotate clockwise
- Shift + R / E : rotate counterclockwise
- S : save
- ESC : pause
- Q : quit

---

## Roadmap

### V1 (current)
- Core gameplay
- UI
- Save/load
- Tests

### V1.1
- UI polish
- Better UX feedback
- Improved scoring balance

### V2
- Animations
- High scores
- Themes
- Sound design

---

## Demo 

---

## License

MIT License
