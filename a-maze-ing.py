#!/usr/bin/env python3
import sys
from src import parse_map, MazeGenerator


def amazeing() -> None:
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: 'a_maze_ing.py config.txt'")
        exit(1)

    try:
        config = parse_map(sys.argv[1])
    except Exception as e:
        print("Error:", e)
        exit(1)

    try:
        maze = MazeGenerator(
            config['WIDTH'],
            config['HEIGHT'],
            config['ENTRY'],
            config['EXIT'],
            config['PERFECT'],
            config['OUTPUT'],
            config['SEED']
        )
    except PlaceHolderError as e:
        print("Error:", e)
        exit(1)

if __name__ == "__main__":
    amazeing()
