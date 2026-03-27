# Architecture

## Goal

Shape Tetris is designed around a strict separation between the game engine and the graphical interface.

## Layers

### 1. Core domain (`shape_tetris.game`)
Pure Python logic with no dependency on `pygame`.

Responsibilities:
- board geometry generation
- block definitions and rotation
- placement validation
- row / column detection
- clearing
- scoring
- game over detection
- save / load serialization

### 2. Application layer (`shape_tetris.app`)
Thin orchestration layer for a playable session.

Responsibilities:
- create new game sessions
- load persisted sessions
- expose a UI-friendly facade around the engine

### 3. Presentation layer (`shape_tetris.ui`)
`pygame-ce` rendering and input handling.

Responsibilities:
- menus
- board rendering
- block rendering
- preview overlays
- HUD
- pause / game over screens

## Core data model

The key design choice is to separate immutable definitions from mutable state.

- `BoardDefinition`: board shape, size, valid mask
- `BoardState`: current occupancy
- `BlockDefinition`: immutable local block cells
- `BlockInstance`: definition + runtime rotation
- `GameConfig`: game parameters
- `GameState`: full mutable state of one session

## Important simplification

The original academic brief discussed line removals with falling behavior for rows above.
For the first robust version of this project, clearing is intentionally implemented as:

- detect full valid rows and columns
- set their occupied cells back to empty
- no gravity propagation

This keeps the rules clean and predictable on non-rectangular boards.

## Why this is maintainable

- rules are testable without the UI
- game state is serializable
- alternate UIs could be added later
- scoring is isolated from placement logic
- board geometry is generated algorithmically
