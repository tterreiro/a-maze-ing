#!/usr/bin/env python3
import sys
from src.parsing import parse_map
from src.maze_gen import MazeGenerator
from src.display import MazeVisualizer
sys.setrecursionlimit(10000)


def amazeing() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    try:
        config = parse_map(sys.argv[1])
        maze = MazeGenerator(
            config['WIDTH'],
            config['HEIGHT'],
            config['ENTRY'],
            config['EXIT'],
            config['PERFECT'],
            config['OUTPUT_FILE']
        )

        maze.generate_maze()

        viz = MazeVisualizer(maze)
        viz.draw_window()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    amazeing()
