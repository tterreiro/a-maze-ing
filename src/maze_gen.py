from typing import Tuple
import random
from .parsing import parse_map


class Cell:
    """
    Represents each cell of the grid, with position in the grid, walls
    and if it has been checked or not.
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.walls = {
            "N": True,
            "E": True,
            "S": True,
            "W": True
        }
        self.checked = False


class MazeGenerator:
    """
    Main class, will take care of generating, solving, and displaying maze
    (probably).
    """
    def __init__(
            self,
            width: int,
            height: int,
            entry: Tuple[int, int],
            exit: Tuple[int, int],
            perfect: bool,
            output: str
            ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.output = output
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.seed = random.randint(1, 1000000)

    def generate_maze(self):
        def get_neighbors(cell):
            directions = [
                (0, -1, "N", "S"),
                (1, 0, "E", "W"),
                (0, 1, "S", "N"),
                (-1, 0, "W", "E")
            ]

            neighbors = []

            for dx, dy, wall, opposite in directions:
                nx = cell.x + dx
                ny = cell.y + dy

                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbor = self.grid[ny][nx]
                    if not neighbor.checked:
                        neighbors.append((neighbor, wall, opposite))

            return neighbors

        def carve(cell):
            cell.checked = True

            neighbors = get_neighbors(cell)
            random.shuffle(neighbors)

            for neighbor, wall, opposite in neighbors:
                if not neighbor.checked:
                    # remover paredes entre células
                    cell.walls[wall] = False
                    neighbor.walls[opposite] = False

                    carve(neighbor)

        start_x, start_y = self.entry
        carve(self.grid[start_y][start_x])

    def to_matrix(self):
        w = self.width * 2 + 1
        h = self.height * 2 + 1

        maze = [['#' for _ in range(w)] for _ in range(h)]

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                mx = x * 2 + 1
                my = y * 2 + 1

                maze[my][mx] = ' '

                if not cell.walls["N"]:
                    maze[my - 1][mx] = ' '
                if not cell.walls["S"]:
                    maze[my + 1][mx] = ' '
                if not cell.walls["E"]:
                    maze[my][mx + 1] = ' '
                if not cell.walls["W"]:
                    maze[my][mx - 1] = ' '
        return maze

    def place_entry_exit(self, maze):
        ex, ey = self.entry
        tx, ty = self.exit

        row_e = ey * 2 + 1
        col_e = ex * 2 + 1

        row_t = ty * 2 + 1
        col_t = tx * 2 + 1

        maze[row_e][col_e] = 'S'
        maze[row_t][col_t] = 'E'

    def generate_from_config(self):
        self.generate_maze()  # gera estrutura (Cells)

        maze = self.to_matrix()  # converte para matriz

        self.place_entry_exit(maze)  # coloca S e E

        return maze


config = parse_map('config.txt')

maze_gen = MazeGenerator(
    config['WIDTH'],
    config['HEIGHT'],
    config['ENTRY'],
    config['EXIT'],
    config['PERFECT'],
    config['OUTPUT_FILE']
)

maze = maze_gen.generate_from_config()

for row in maze:
    print(''.join(row))


def generate():
    """John pork"""
    pass


def solve():
    pass
