from typing import Tuple
import random
from collections import deque


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
        self.is_42 = False
        self.is_path = False


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
        self.seed = None

    def generate_maze(self):
        self.seed = random.randint(1, 999999999)
        random.seed(self.seed)

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
                    if self.height > 10 and self.width > 10:
                        if self.get_cell_type(nx, ny) == "wall":
                            continue
                    if not neighbor.checked:
                        neighbors.append((neighbor, wall, opposite))
            return neighbors

        def carve(cell):
            cell.checked = True

            neighbors = get_neighbors(cell)
            random.shuffle(neighbors)

            for neighbor, wall, opposite in neighbors:
                if not neighbor.checked:
                    cell.walls[wall] = False
                    neighbor.walls[opposite] = False
                    carve(neighbor)

        start_x, start_y = self.entry
        carve(self.grid[start_y][start_x])

        if not self.perfect:
            self.add_loops()
        self.solve()

    def get_cell_type(self, x, y):
        pattern = self.get_42_pattern()

        start_x = self.width // 2 - len(pattern[0]) // 2
        start_y = self.height // 2 - len(pattern) // 2

        for dy, row in enumerate(pattern):
            for dx, char in enumerate(row):
                px = start_x + dx
                py = start_y + dy

                if x == px and y == py:
                    if char == " ":
                        return "path"   # aberto
                    else:
                        self.get_cell((x, y)).is_42 = True
                        return "wall"   # bloqueado
        return None

    def to_matrix(self):
        w = self.width * 2 + 1
        h = self.height * 2 + 1

        maze = [['#' for _ in range(w)] for _ in range(h)]

        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]

                mx = x * 2 + 1
                my = y * 2 + 1

                cell_type = self.get_cell_type(x, y)

                # 🔴 desenhar o 42
                if cell_type == "wall":
                    maze[my][mx] = '#'
                    continue

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

    def get_42_pattern(self):
        return [
            "4   222",
            "4 4   2",
            "444 222",
            "  4 2  ",
            "  4 222"
        ]

    def get_cell(self, coords: tuple[int, int]) -> Cell:
        """
        return a cell using (x, y) coordinates.
        """
        x, y = coords
        return self.grid[y][x]

    def solve(self):
        maze = self.to_matrix()
        self.place_entry_exit(maze)
        h = len(maze)
        w = len(maze[0])

        # Find start and end
        for y in range(h):
            for x in range(w):
                if maze[y][x] == 'S':
                    start = (x, y)
                if maze[y][x] == 'E':
                    end = (x, y)

        queue = deque([start])
        visited = set([start])
        parent = {}

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while queue:
            x, y = queue.popleft()

            if (x, y) == end:
                break

            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < w and 0 <= ny < h:
                    if maze[ny][nx] != '#' and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))
                        parent[(nx, ny)] = (x, y)

        # Reconstruct path
        path = []
        cur = end

        while cur != start:
            path.append(cur)
            mx, my = cur
            self.get_cell((mx//2, my//2)).is_path = True
            cur = parent.get(cur)
            if cur is None:
                return None  # no solving

        path.append(start)
        path.reverse()

        return path

    def add_loops(self, probability=0.1):
        changed = 0
        for y in random.sample(range(self.height), self.height):
            for x in random.sample(range(self.width), self.width):
                if changed > (self.height*self.width)//15:
                    return
                changed
                cell = self.grid[y][x]

                directions = [
                    (0, -1, "N", "S"),
                    (1, 0, "E", "W"),
                    (0, 1, "S", "N"),
                    (-1, 0, "W", "E")
                ]

                for dx, dy, wall, opposite in directions:
                    if changed > (self.height*self.width)//10:
                        return
                    nx = x + dx
                    ny = y + dy

                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        neighbor = self.grid[ny][nx]
                        if self.height > 10 and self.width > 10:
                            if self.get_cell_type(x, y) == "wall":
                                continue
                            if self.get_cell_type(nx, ny) == "wall":
                                continue

                        # só abre paredes aleatoriamente
                        if cell.walls[wall] and random.random() < probability:
                            cell.walls[wall] = False
                            neighbor.walls[opposite] = False
                            changed += 1
