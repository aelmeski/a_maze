*This project has been created as part of the 42 curriculum by amine.*

# A-Maze-ing

## Description
A-Maze-ing is a terminal-based maze generator and solver written in Python.

The project reads a configuration file, generates a maze with a central blocked "42" pattern, computes a path from entry to exit, displays everything with an interactive curses UI, and exports the maze and solution data to a text file.

Project goals:
- Build a configurable maze generation system.
- Guarantee a valid path search from entry to exit (when reachable).
- Provide a clean terminal visualization and simple controls.
- Save a compact output representation of the maze and the solved path.

## Features
- Config-file driven behavior.
- Randomized maze generation with optional imperfect carving.
- BFS pathfinding from ENTRY to EXIT.
- Interactive curses display:
  - Regenerate maze.
  - Show or hide computed path.
  - Rotate maze colors.
- Export to output file in hexadecimal wall encoding plus path directions.
- Optional seed for deterministic generation.

## Project Structure
- a_maze_ing.py: Main entry point and application loop.
- maze_package/parsing.py: Config parsing and validation.
- maze_package/maze_generator.py: Maze grid, cell model, and generation algorithm.
- maze_package/find_path.py: BFS solver.
- maze_package/display.py: Curses rendering and interaction.
- maze_package/save_maze.py: Maze/path serialization to file.
- config.txt: Example runtime configuration.
- maze.txt: Example generated output.

## Instructions
### Requirements
- Python 3.10+ (recommended).
- Terminal with curses support.

Windows note:
- If curses is missing on Windows, install windows-curses:

```bash
pip install windows-curses
```

### Run
From the repository root:

```bash
python a_maze_ing.py config.txt
```

The program opens an interactive UI. Available actions:
- 1: Re-generate a new maze.
- 2: Show or hide the solution path.
- 3: Rotate maze colors.
- 4: Quit.

### Output
On each generation, the maze is written to OUTPUT_FILE from the config.

Output format:
- First block: maze rows encoded as hexadecimal digits.
- Then one line: ENTRY as x,y.
- Then one line: EXIT as x,y.
- Final line: path directions as a string of N/E/S/W characters.

## Config File: Complete Structure and Format
The config file is a .txt file with one KEY=VALUE per line.

Ignored lines:
- Empty lines.
- Lines starting with # (comments).

Supported keys:
- WIDTH: integer in [10, 100].
- HEIGHT: integer in [10, 100].
- ENTRY: coordinates as x,y.
- EXIT: coordinates as x,y.
- OUTPUT_FILE: file name ending with .txt.
- PERFECT: True or False.
- SEED: integer or None.

Validation rules:
- All keys above are required except SEED, which can be set to None.
- ENTRY and EXIT must be different.
- ENTRY and EXIT must be inside maze bounds.
- ENTRY and EXIT cannot be inside the fixed "42" blocked pattern.

Example:

```txt
# Example configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
```

## Maze Generation Algorithm
Chosen algorithm: randomized depth-first search (recursive backtracker style using an explicit stack).

How it works in this project:
- Initialize a grid of closed cells (all walls present).
- Mark a fixed central "42" pattern as visited/blocked so it is preserved.
- Start from ENTRY.
- Repeatedly:
  - Collect unvisited neighbors.
  - Randomly choose next neighbor.
  - Remove wall between current and next cell.
  - Push current cell to stack and move forward.
- If stuck, backtrack with stack.
- Stop when stack is empty and no neighbor remains.

Imperfect mode behavior:
- When PERFECT=False, the generator sometimes removes an additional wall, creating loops and multiple routes.

## Why This Algorithm
- Simple and robust to implement with clear control over carving.
- Naturally produces mazes with long corridors and good visual variety.
- Works well with deterministic seeding.
- Easy to adapt for both perfect and imperfect maze variants.
- Integrates cleanly with the blocked "42" pattern constraint.

## Reusable Code and How to Reuse It
Reusable modules:
- Parsing layer (maze_package/parsing.py): reusable for any key-value text config with validation extension.
- Generation core (maze_package/maze_generator.py): reusable Cell + generator engine for other maze-based apps.
- Solver (maze_package/find_path.py): standalone BFS pathfinding over the same cell/wall model.
- Persistence (maze_package/save_maze.py): reusable serializer for compact maze representations.
- Display (maze_package/display.py): reusable curses renderer for grid-based maps and overlays.

How to reuse:
1. Create MazeData-like configuration.
2. Call MazeGenerator.set_maze_data(...) then generate_maze().
3. Pass grid and endpoints to FindPath to get a path.
4. Use Display to render or SaveMaze to persist outputs.

## Team and Project Management
### Team Roles
Current implementation is single-developer:
- amine:
  - Architecture and module decomposition.
  - Parsing and validation design.
  - Maze generation and pathfinding.
  - Curses UI and file export.
  - Testing and iterative debugging.

### Planned Timeline vs Actual Evolution
Initial plan:
1. Parse configuration safely.
2. Generate maze.
3. Add pathfinding.
4. Add UI.
5. Add output export and polish.

How it evolved:
- Core generation and parsing were implemented first.
- Pathfinding was integrated to guarantee playable output.
- UI controls were expanded (toggle path and color rotation).
- Export format was finalized after solver integration.
- Documentation and code quality pass came at the end.

### What Worked Well
- Clear separation by module responsibilities.
- Strong validation reduced runtime failures.
- BFS integration made correctness easy to verify.
- Seed support helped debugging and reproducibility.

### What Could Be Improved
- Better error message consistency and typo cleanup.
- Add automated tests for parser and generator invariants.
- Add optional alternative generation algorithms.
- Improve Windows terminal compatibility notes and CI checks.

### Tools Used
- Python 3.
- Git.
- VS Code.
- curses (and windows-curses on Windows when needed).

## Advanced Features Implemented
- Perfect and imperfect maze behavior via PERFECT flag.
- Optional deterministic generation via SEED.
- Interactive display options:
  - path visibility toggle,
  - dynamic color rotation,
  - on-demand regeneration.

## Resources
Classic references:
- Python Documentation: https://docs.python.org/3/
- curses (Python): https://docs.python.org/3/library/curses.html
- Breadth-First Search (BFS): https://en.wikipedia.org/wiki/Breadth-first_search
- Depth-First Search and backtracking concepts: https://en.wikipedia.org/wiki/Depth-first_search
- Maze generation overview: https://en.wikipedia.org/wiki/Maze_generation_algorithm

AI usage in this project:
- Used AI for:
  - documentation drafting and section structuring,
  - docstring generation and wording improvements,
  - minor code review suggestions and readability checks.
- Not used to replace core algorithmic decisions or project architecture.
- Final integration choices, debugging, and validation were done manually.