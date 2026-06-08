*This project has been created as part of the 42 curriculum by hde-andr, crodrigo.*

## Description
This project is a complete maze generation tool designed to build, parse, customize, and visually render unique mazes. The main objective is to provide an automated, algorithmic solution to generate solvable paths while offering a highly adjustable rendering environment. The application reads user configurations, processes a specialized layout structure, and uses a graphical engine to display the final output, providing an engaging experience for both technical evaluation and general demonstration.

## Instructions

### Installation
You can build and install the core generation engine as a standalone, reusable Python module. To compile the module into a single pip-installable wheel asset at the repository root, run:

```bash
make install
```

```bash
make build-package
```

Alternatively, you can install the required internal runtime dependencies manually using:

```bash
pip install -r requirements.txt
```

## Execution
To execute the primary generation and visualization pipeline, run the root python script while supplying your configuration layout:

```bash
make run
```

To debug you can run:
```bash
make debug
```

## Static Analysis
To check type hints and ensure structural compliance across the source directory, invoke the linting tool:

```bash
make lint
```

```bash
make lint-strict
```

## Config File Structure
The application relies on a config.txt file located at the root of the repository to manage dimensions, entry points, and generation criteria. The file must follow this exact format:

WIDTH=25
HEIGHT=25
ENTRY=1,5
EXIT=0,1
OUTPUT_FILE=maze.txt
PERFECT=TRUE
SEED=982398252382
WIDTH / HEIGHT: Integer values defining the grid dimensions for the maze.

ENTRY / EXIT: Coordinate pairs (X,Y) specifying the start and completion points of the maze layout.

OUTPUT_FILE: The target filename where the generated maze structure is exported.

PERFECT: A boolean flag determining whether the maze has one or more ways to the exit.

SEED: Custom seed to generate a specific maze

## Maze Generation Algorithm
## Chosen Algorithm
This project utilizes the Recursive Backtracking Algorithm to construct its grid paths. The process initializes by picking a starting cell, marking it as visited, randomly selecting an unvisited neighbor, carving a path through the separating wall, and recursively moving forward. If the generator hits a dead end where all surrounding cells are already visited, it backtracks along the active path until it finds a cell with available neighbors to continue carving.

## Why We Chose It
We selected Recursive Backtracking because it was conceptually the most interesting algorithm to implement and dynamically analyze. Visually, it produces the prettiest mazes characterized by long, winding, and intricate corridors with fewer shallow branches compared to alternative approach strategies, offering a highly aesthetic and complex layout generation.

## Reusable Module
The core functionality of this project is decoupled into a completely self-contained, reusable package called mazegen.

# What is Reusable
parsing.py: Handles map validation, coordinate registration, and config parsing pipelines.

maze_gen.py: The complete matrix handling, pathfinding logic, and layout generation state machine for the Recursive Backtracking algorithm.

display.py: A clean, abstracted visualizer class managing window lifecycles and matrix drawings.

# How to Use It
Once built and installed via pip (pip install mazegen-1.0.0-py3-none-any.whl), you can import the distinct layers into any outside Python project:

Python
from mazegen import MazeGenerator, MazeVisualizer

# Generate a raw layout matrix using the configuration standards
matrix = MazeGenerator(width=25, height=25).generate()

# Render the matrix independently
visualizer = MazeVisualizer(matrix)
visualizer.show()

## Team and Project Management
# Roles of Each Team Member

**hde-andr**: Focused on the graphical user interface integration using the MiniLibX (mlx) library, configuring the automated compiler system within the Makefile, structure layout management, and generating documentation.

**crodrigo**: Focused on config file data parsing, building the core grid architecture, implementing the Recursive Backtracking generation mechanics, and developing the foundational DFS pathfinding algorithm.

## Anticipated Planning and Evolution
Our original planning structured the development into sequential phases: environment scaffolding, parsing implementation, core algorithm coding, and visual integration. While the layout parsing and graphical shell structures moved quickly, aligning internal matrix coordinate updates with recursive stack boundaries took extra refinement. We adapted by lengthening our algorithm verification windows to guarantee stability on larger matrix profiles.

## Successes and Improvements
What worked well: Decoupling the graphical interface pipeline from the algorithmic matrix calculation engine early on allowed both team members to develop and test modules concurrently without version conflicts.

What could be improved: The performance could be improved. The graphical part was made using a method that works very slowly and we couldve implemented animation and extra features. Also we couldve been more communicative.

## Tools Used
Git / GitHub: For version control and collaborative branch synchronization.

## Resources
Documentation — Standard documentation for building wheels, distributing source modules and mlx.
Peers — Asked peers for help and approval.
Github repositories

## AI Usage Disclosure
AI was used in the understanding of some concepts and error checking.
