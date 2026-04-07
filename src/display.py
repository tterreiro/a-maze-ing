from __future__ import annotations
from mlx import Mlx
from .maze_gen import MazeGenerator, Cell
from typing import Any


class Buttons:
    def __init__(self, viz: MazeVisualizer):
        self.viz = viz
        if viz.is_wide:
            btn_h = viz.button_area_height // 3
            btn_w = viz.window_size[0] // 6
            btn_y = viz.window_size[1] - viz.button_area_height // 2 - btn_h//2
            spacing = (viz.window_size[0] - 4 * btn_w) // 5
            self.buttons = {  # button: (x1, y1, x2, y2)
                'regen':   (spacing,
                            btn_y,
                            spacing + btn_w,
                            btn_y + btn_h),
                'path':    (spacing * 2 + btn_w,
                            btn_y,
                            spacing * 2 + btn_w * 2,
                            btn_y + btn_h),
                'colour':  (spacing * 3 + btn_w * 2,
                            btn_y,
                            spacing * 3 + btn_w * 3,
                            btn_y + btn_h),
                'quit':    (spacing * 4 + btn_w * 3,
                            btn_y,
                            spacing * 4 + btn_w * 4,
                            btn_y + btn_h),
            }
        else:
            btn_h = viz.button_area_width // 5
            btn_w = viz.window_size[1] // 6
            btn_x = viz.window_size[0] - viz.button_area_width // 2 - btn_w//2
            gap = 15
            total_h = 4 * btn_h + 3 * gap
            start_y = (viz.window_size[1] - total_h) // 2
            self.buttons = {  # button: (x1, y1, x2, y2)
                'regen':   (btn_x,  # x1
                            start_y,  # y1
                            btn_x + btn_w,  # x2
                            start_y + btn_h),  # y2
                'path':    (btn_x,
                            start_y + btn_h + gap,
                            btn_x + btn_w,
                            start_y + btn_h * 2 + gap),
                'colour':  (btn_x,
                            start_y + btn_h * 2 + gap * 2,
                            btn_x + btn_w,
                            start_y + btn_h * 3 + gap * 2),
                'quit':    (btn_x,
                            start_y + btn_h * 3 + gap * 3,
                            btn_x + btn_w,
                            start_y + btn_h * 4 + gap * 3),
            }
        self.colours = {
            'regen':    0xFF2E7D32,  # dark green
            'path':     0xFF1565C0,  # dark blue
            'colour':   0xFF6A1B9A,  # dark purple
            'quit':     0xFFB71C1C,  # dark red
        }
        self.path_colour = 0xFFFF6EC7
        self.text_colour = 0xFFFFFFFF
        self.colour_index = 0
        self.themes = [
            {'wall': 0xFF0288D1, 'bg': 0xFF00111A},  # blue on blue
            {'wall': 0xFFFFFFFF, 'bg': 0xFF000000},  # white on black
            {'wall': 0xFFFFD600, 'bg': 0xFF1A1400},  # yellow on yellow
            {'wall': 0xFFFF4081, 'bg': 0xFF1A0010},  # pink on dark pink
            {'wall': 0xFFAB47BC, 'bg': 0xFF120018},  # purple on purple
        ]
        self.labels = {
            'regen':   'Regenerate',
            'path':    'Show Path',
            'colour': 'Change color',
            'quit':    'Exit',
        }
        self.path_showing = False

    def draw_button(self) -> None:
        self.labels['path'] = (
            'Hide path' if self.path_showing
            else 'Show path')
        for name, rect in self.buttons.items():
            x1, y1, x2, y2 = rect
            for y in range(y1, y2):
                for x in range(x1, x2):
                    self.viz.put_pixel(x, y, self.colours[name])
        for name, rect in self.buttons.items():
            x1, y1, x2, y2 = rect
            text = self.labels[name]
            text_width = len(text) * 10
            text_height = 19
            cx = (x1 + x2) // 2 - text_width // 2
            cy = (y1 + y2) // 2 - text_height // 2
            self.viz.put_string(cx, cy, self.text_colour, text)

    def handle_mouse(self, button: int, x: int, y: int, _=None) -> None:
        if button != 1:
            return

        if (self.buttons['regen'][0] < x < self.buttons['regen'][2]
                and self.buttons['regen'][1] < y < self.buttons['regen'][3]):
            self.regen()
        elif (self.buttons['path'][0] < x < self.buttons['path'][2]
                and self.buttons['path'][1] < y < self.buttons['path'][3]):
            self.path_showing = not self.path_showing
            self.show_path(self.path_showing)
            self.draw_button()
        elif (self.buttons['quit'][0] < x < self.buttons['quit'][2]
                and self.buttons['quit'][1] < y < self.buttons['quit'][3]):
            self.viz.close()
        elif (self.buttons['colour'][0] < x < self.buttons['colour'][2]
                and self.buttons['colour'][1] < y < self.buttons['colour'][3]):
            self.change_colour()

    def change_colour(self) -> None:
        self.colour_index = (self.colour_index + 1) % len(self.themes)
        theme = self.themes[self.colour_index]
        self.viz.wall_colour = theme['wall']
        self.viz.bg_colour = theme['bg']
        for y in range(self.viz.maze_h):
            for x in range(self.viz.maze_w):
                self.viz.put_pixel(x, y, self.viz.bg_colour)
        self.viz.draw_maze()

    def regen(self) -> None:
        self.viz.maze.grid = [[Cell(x, y) for x in range(self.viz.maze.width)]
                              for y in range(self.viz.maze.height)]
        self.viz.maze.generate_maze()
        for y in range(self.viz.maze_h):
            for x in range(self.viz.maze_w):
                self.viz.put_pixel(x, y, self.viz.bg_colour)
        self.viz.draw_maze()
        self.viz.show_seed()

    def show_path(self, is_showing: bool) -> None:
        for y in range(self.viz.maze_h):
            for x in range(self.viz.maze_w):
                self.viz.put_pixel(x, y, self.viz.bg_colour)
        self.viz.draw_maze()


class MazeVisualizer:
    """Magic maze display class using mlx"""
    def __init__(self, maze: MazeGenerator) -> None:
        self.mlx = Mlx()
        self.mlx_ptr = self.mlx.mlx_init()

        self.maze = maze
        self.screen_res = 800
        self.wall_thickness = 6
        self.button_area_height = 130
        self.button_area_width = 230
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
        self.wall_colour = 0xFF0288D1
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
        # path
        if cell.is_path and self.btn.path_showing:
            for i in range(self.cell_size):
                for j in range(self.cell_size):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.btn.path_colour)
        # maze entry
        if (cell.x, cell.y) == self.maze.entry:
            for i in range(self.cell_size):
                for j in range(self.cell_size):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.entry_colour)
        # maze exit
        if (cell.x, cell.y) == self.maze.exit:
            for i in range(self.cell_size):
                for j in range(self.cell_size):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.exit_colour)
        # 42 icon
        if cell.is_42:
            for i in range(self.cell_size):
                for j in range(self.cell_size):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.wall_colour)

        if cell.walls["N"]:
            for i in range(self.cell_size):
                for j in range(thickness):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.wall_colour)

        if cell.walls["W"]:
            for i in range(thickness):
                for j in range(self.cell_size):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + j,
                        self.wall_colour)

        if cell.walls["S"]:
            for i in range(self.cell_size):
                for j in range(thickness):
                    self.put_pixel(
                        pixel_x + i,
                        pixel_y + self.cell_size - thickness + j,
                        self.wall_colour)

        if cell.walls["E"]:
            for i in range(thickness):
                for j in range(self.cell_size):
                    self.put_pixel(
                        pixel_x + self.cell_size - thickness + i,
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
        if keycode == 114:  # 114 keycode for 'r'
            self.btn.regen()
        if keycode == 102:  # 102 keycode for 'f'
            self.btn.show_path()
        if keycode == 99:  # 99 keycode for 'c'
            self.btn.change_colour()

    def draw_window(self) -> None:
        self.draw_maze()
        self.btn.draw_button()
        self.show_seed()
        self.mlx.mlx_loop(self.mlx_ptr)
