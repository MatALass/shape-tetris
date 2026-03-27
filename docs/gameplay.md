# Gameplay

## Loop

1. Select a board shape and size
2. Start a run
3. Select one of the available blocks
4. Preview the placement with the mouse
5. Rotate if needed
6. Click to place
7. Clear full valid rows and columns
8. Continue until no available block can be placed

## Game modes

### Random three
Three blocks are available at a time. Once all three have been used, a new trio is generated.

### Full catalog
All blocks remain selectable at all times.

## Validation rules

A placement is valid only if:
- every block cell lands inside a valid board cell
- and none of those cells are already occupied

## Scoring

- +1 per placed cell
- +10 per cleared row
- +10 per cleared column
- combo bonus if several lines are cleared in one move

## End condition

Game over occurs when no currently available block can be legally placed anywhere on the board.
