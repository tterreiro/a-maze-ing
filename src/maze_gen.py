from typing import Tuple, Optional
import random


class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.directions = {
            "N": True,
            "E": True,
            "S": True,
            "W": True,
        }
        self.checked = True


class MazeGenerator:
    def __init__(
            self,
            width: int,
            height: int,
            entry: Tuple[int, int],
            exit: Tuple[int, int],
            perfect: bool,
            output: str,
            seed: Optional[int]
            ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.output = output
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        self.seed = seed
    
