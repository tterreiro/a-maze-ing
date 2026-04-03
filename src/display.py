from __future__ import annotations
from mlx import Mlx
from .maze_gen import MazeGenerator, Cell
from typing import Any


class Buttons:
    def __init__(self, viz: MazeVisualizer):
        self.viz = viz
        if viz.is_wide:
            btn_h = viz.button_area_height // 3
            btn_w = viz.window_size[0] // 5
            btn_y = viz.window_size[1] - viz.button_area_height // 2 - btn_h//2
            spacing = (viz.window_size[0] - 3 * btn_w) // 4
            self.buttons = {
                'regen': (spacing,
                          btn_y,
                          spacing + btn_w,
                          btn_y + btn_h),
                'path':  (spacing * 2 + btn_w,
                          btn_y,
                          spacing * 2 + btn_w * 2,
                          btn_y + btn_h),
                'quit':  (spacing * 3 + btn_w * 2,
                          btn_y,
                          spacing * 3 + btn_w * 3,
                          btn_y + btn_h),
            }
        else:
            btn_w = viz.button_area_width // 3
            btn_h = viz.window_size[1] // 5
            btn_x = viz.window_size[0] - viz.button_area_width // 2 - btn_w//2
            spacing = (viz.window_size[1] - 3 * btn_h) // 4
            self.buttons = {
                'regen': (btn_x,
                          spacing,
                          btn_x + btn_w,
                          spacing + btn_h),
                'path':  (btn_x,
                          spacing * 2 + btn_h,
                          btn_x + btn_w,
                          spacing * 2 + btn_h * 2),
                'quit':  (btn_x,
                          spacing * 3 + btn_h * 2,
                          btn_x + btn_w,
                          spacing * 3 + btn_h * 3),
            }
        self.colours = {
            'regen': 0xFF2E7D32,  # dark green
            'path':  0xFF1565C0,  # dark blue
            'quit':  0xFFB71C1C,  # dark red
        }
        self.text_colour = 0xFFFFFFFF

    def draw_button(self) -> None:
        for name, rect in self.buttons.items():
            x1, y1, x2, y2 = rect
            for y in range(y1, y2):
                for x in range(x1, x2):
                    self.viz.put_pixel(x, y, self.colours[name])
        labels = {
            'regen': 'Regenerate',
            'path':  'Find path',
            'quit':  'Quit',
        }
        for name, rect in self.buttons.items():
            x1, y1, x2, y2 = rect
            text = labels[name]
            text_width = len(text) * 10
            text_height = 17
            cx = (x1 + x2) // 2 - text_width // 2
            cy = (y1 + y2) // 2 - text_height // 2
            self.viz.put_string(cx, cy, self.text_colour, text)

    def handle_mouse(self, button: int, x: int, y: int, _=None) -> None:
        if button != 1:
            return

        if (self.buttons['regen'][0] < x < self.buttons['regen'][2]
                and self.buttons['regen'][1] < y < self.buttons['regen'][3]):
            self.viz.regen()
        elif (self.buttons['path'][0] < x < self.buttons['path'][2]
                and self.buttons['path'][1] < y < self.buttons['path'][3]):
            self.viz.find_path()
        elif (self.buttons['quit'][0] < x < self.buttons['quit'][2]
                and self.buttons['quit'][1] < y < self.buttons['quit'][3]):
            self.viz.close()


class MazeVisualizer:
    """Magic maze display class using mlx"""
    def __init__(self, maze: MazeGenerator) -> None:
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        self.maze = maze
        self.screen_res = 800
        self.wall_thickness = 6
        self.button_area_height = 130
        self.button_area_width = 10
        diff = abs(maze.width - maze.height)
        self.is_wide = maze.width >= maze.height
        self.screen_res = (
            min(800 + diff *
                (self.screen_res // max(maze.width, maze.height)), 1000))
        self.cell_size = (
            (self.screen_res - self.wall_thickness) //
            max(maze.width, maze.height))
        self.maze_w = self.cell_size * maze.width + self.wall_thickness
        self.maze_h = self.cell_size * maze.height + self.wall_thickness
        if self.is_wide:
            self.window_size = (self.maze_w + 10,
                                self.maze_h + 10 + self.button_area_height)
        else:
            self.window_size = (self.maze_w + 10 + self.button_area_width,
                                self.maze_h + 10)

        self.x_offset = 5
        self.y_offset = 5
        self.win_ptr = self.mlx.mlx_new_window(
                                        self.mlx_ptr,
                                        self.window_size[0],
                                        self.window_size[1], "A-maze-ing")
        self.bg_colour = 0xFF000000
        self.wall_colour = 0xFFFFFFFF
        self.colour_42 = 0xFF0000FF
        self.entry_colour = 0xFF4CAF50
        self.exit_colour = 0xFFE53935
        self.btn = Buttons(self)

        self.mlx.mlx_hook(self.win_ptr, 17, 0, self.close, None)
        self.mlx.mlx_hook(self.win_ptr, 2, 1 << 0, self.handle_keypress, None)
        self.mlx.mlx_hook(self.win_ptr, 4, 1 << 2, self.btn.handle_mouse, None)

    def put_string(self, x: int, y: int, colour: int,  string: str,) -> None:
        """
        Self-explanatory
        """
        self.mlx.mlx_string_put(self.mlx_ptr, self.win_ptr, x, y,
                                colour, string)

    def put_pixel(self, x: int, y: int, colour: int) -> None:
        """
        Self-explanatory
        """
        self.mlx.mlx_pixel_put(self.mlx_ptr, self.win_ptr, x, y, colour)

    def show_seed(self) -> None:
        print("Seed:", self.maze.seed)

    def close(self, _: Any = None) -> None:
        """Close the window and exit the MLX loop."""
        self.mlx.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.mlx.mlx_loop_exit(self.mlx_ptr)

    def draw_cell_walls(self, x: int, y: int, cell: Cell) -> None:
        """
        Draws the cell's walls in the window, based on the walls thickness,
        cell size and coordinates offset (the extra space in the window, used
        to center the maze)
        """
        pixel_x = x * self.cell_size + self.x_offset
        pixel_y = y * self.cell_size + self.y_offset
        thickness = self.cell_size // self.wall_thickness

        if (cell.x, cell.y) == self.maze.entry:
            for i in range(self.cell_size + 3):
                for j in range(self.cell_size + 3):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.entry_colour)

        if (cell.x, cell.y) == self.maze.exit:
            for i in range(self.cell_size + 2):
                for j in range(self.cell_size + 2):
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
                        self.wall_colour)

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
        This draws the maze!!
        """
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell((x, y))
                self.draw_cell_walls(x, y, cell)

    def handle_keypress(self, keycode: int, _=None) -> None:
        """Exit if the ESC key is pressed."""
        if keycode == 65307:  # 65307 is the esc key code
            self.close()
        if keycode == 114:
            self.regen()
        if keycode == 102:
            self.find_path()

    def find_path(self) -> None:
        pass

    def regen(self) -> None:
        self.maze.grid = [[Cell(x, y) for x in range(self.maze.width)]
                          for y in range(self.maze.height)]
        self.maze.generate_maze()
        for y in range(self.maze_h):
            for x in range(self.maze_w):
                self.put_pixel(x, y, self.bg_colour)
        self.draw_maze()
        self.show_seed()

    def draw_window(self) -> None:
        self.draw_maze()
        self.btn.draw_button()
        self.show_seed()
        self.mlx.mlx_loop(self.mlx_ptr)
