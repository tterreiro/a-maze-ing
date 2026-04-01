from mlx import Mlx
from .maze_gen import MazeGenerator, Cell
from typing import Any


class MazeVisualizer:
    """Magic maze display class using mlx"""
    def __init__(self, maze: MazeGenerator, screen_res: int = 800) -> None:
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        self.maze = maze
        self.wall_thickness = 10
        self.image_size = (screen_res, screen_res)
        self.window_size = self.image_size

        self.cell_size = (
            (screen_res - self.wall_thickness) //
            max(maze.width, maze.height))

        self.x_offset = (screen_res - self.cell_size * maze.width) // 2
        self.y_offset = 10
        self.win_ptr = self.mlx.mlx_new_window(
                                        self.mlx_ptr,
                                        self.window_size[0],
                                        self.window_size[1], "A-maze-ing")
        self.button_area_height = 50
        self.usable_height = screen_res - self.button_area_height
        self.bg_colour = 0xFF000000
        self.wall_colour = 0xFFFFFFFF
        self.colour_42 = 0xFF0000FF
        self.entry_colour = 0xFF4CAF50
        self.exit_colour = 0xFFE53935
        self.mlx.mlx_hook(self.win_ptr, 17, 0, self.close, None)
        self.mlx.mlx_hook(self.win_ptr, 2, 1 << 0, self.handle_keypress, None)

    def put_pixel(self, x: int, y: int, colour: int) -> None:
        """
        Self-explanatory
        """
        self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, colour)

    def draw_cell_walls(self, x: int, y: int, cell: Cell) -> None:
        """
        Draws the cell's walls in the window, based on the walls thickness
        """
        pixel_x = x * self.cell_size + self.x_offset
        pixel_y = y * self.cell_size + self.y_offset
        thickness = self.cell_size // self.wall_thickness

        if (cell.x, cell.y) == self.maze.entry:
            for i in range(self.cell_size):
                for j in range(self.cell_size):
                    self.put_pixel(
                        pixel_x + i + 3,
                        pixel_y + j + 3,
                        self.entry_colour)

        if (cell.x, cell.y) == self.maze.exit:
            for i in range(self.cell_size):
                for j in range(self.cell_size):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.exit_colour)

        if cell.is_42:
            for i in range(self.cell_size):
                for j in range(self.cell_size):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.colour_42)

        if cell.walls["N"]:
            for i in range(self.cell_size + thickness):
                for j in range(thickness):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.wall_colour)

        if cell.walls["W"]:
            for i in range(thickness):
                for j in range(self.cell_size + thickness):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.wall_colour)

        if cell.walls["S"]:
            for i in range(self.cell_size + thickness):
                for j in range(thickness):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + self.cell_size + j,
                        self.wall_colour)

        if cell.walls["E"]:
            for i in range(thickness):
                for j in range(self.cell_size + thickness):
                    self.put_pixel(
                        pixel_x + self.cell_size + i,
                        pixel_y + j,
                        self.wall_colour)

    def draw_maze(self) -> None:
        """
        This daws the maze!!
        """
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell((x, y))
                self.draw_cell_walls(x, y, cell)
        self.mlx.mlx_loop(self.mlx_ptr)

    def close(self, _: Any = None) -> None:
        """Close the window and exit the MLX loop."""
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def handle_keypress(self, keycode: int, _: Any = None) -> None:
        """Exit if the ESC key is pressed."""
        if keycode == 65307:  # 65307 is the esc key code
            self.close()
