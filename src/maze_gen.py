from typing import Tuple
import random


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
        self.seed = seed
    
=======
        self.seed = random.randint(1, 1000000)

    def generate():
        """John pork"""
        pass

    def solve():
        pass
>>>>>>> ca92ea8c2e07f0250c6aed900fc3fe8d2789240a
