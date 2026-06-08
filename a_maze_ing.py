#!/usr/bin/env python3
import sys
from src import parse_map, MazeVisualizer, MazeGenerator
sys.setrecursionlimit(10000)


def amazeing() -> None:
    """Main entry point for the maze generator and visualizer."""
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
            config['OUTPUT_FILE'],
            config['SEED']
        )
        maze.generate_maze()

        viz = MazeVisualizer(maze)
        viz.draw_window()

    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    amazeing()
