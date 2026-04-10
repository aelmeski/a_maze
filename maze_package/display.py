import curses
from .maze_generator import Cell
from .parsing import MazeData
import random


class Display:
    def __init__(self, screen) -> None:
        self.maze: list[list[Cell]] = []  # here we have the maze data
        self.screen = screen  # this where the maze screen is been stored

        # input + drawing behavior
        curses.curs_set(0)          # hide cursor (optional)
        self.screen.keypad(True)

        # colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, 0)
        curses.init_pair(2, curses.COLOR_GREEN, 0)
        curses.init_pair(3, curses.COLOR_RED, 0)

        self.maze_data: MazeData | None = None
        self.path: list[tuple] | None = None
        self.show_path = False
        self.x = 10

    def change_colors(self) -> None:
        colors = [curses.COLOR_BLUE, curses.COLOR_GREEN, curses.COLOR_RED]
        random.shuffle(colors)
        curses.init_pair(1, colors[0], 0)
        curses.init_pair(2, colors[1], 0)
        curses.init_pair(3, colors[2], 0)
        self.display()

    def set_maze(self, maze: list[list[Cell]]) -> None:
        self.maze = maze

    def set_path(self, path: list[tuple]) -> None:
        self.path = path

    def show_hide_path(self):
        self.show_path = not self.show_path
        self.display()

    def __print_path(self):
        for i in range(len(self.path)):
            x1 = self.path[i][0] * 4 + 1
            y1 = self.path[i][1] * 2 + 1

            self.screen.addstr(y1, x1, "██", curses.color_pair(2))

            if i+1 < len(self.path):
                x2 = self.path[i+1][0] * 4 + 1
                y2 = self.path[i+1][1] * 2 + 1

                self.screen.addstr(int((y1+y2)/2), int((x1+x2)/2), "██",
                                   curses.color_pair(2))

    def set_maze_data(self, maze_data: MazeData) -> None:
        self.maze_data = maze_data

    def print_box(self, x, y, cell: Cell) -> None:
        box_x = x * 4
        box_y = y * 2

        self.screen.addstr(box_y, box_x, "█", curses.color_pair(1))
        self.screen.addstr(box_y, box_x+3, "█", curses.color_pair(1))

        self.screen.addstr(box_y+2, box_x, "█", curses.color_pair(1))
        self.screen.addstr(box_y+2, box_x+3, "█", curses.color_pair(1))

        if cell.N:
            self.screen.addstr(box_y, box_x+1, "██", curses.color_pair(1))
        if cell.E:
            self.screen.addstr(box_y+1, box_x+3, "█", curses.color_pair(1))
        if cell.S:
            self.screen.addstr(box_y+2, box_x+1, "██", curses.color_pair(1))
        if cell.W:
            self.screen.addstr(box_y+1, box_x, "█", curses.color_pair(1))
        if cell.is42:
            self.screen.addstr(box_y+1, box_x+1, "██", curses.color_pair(2))

    def set_choices(self) -> None:
        y = len(self.maze) * 2
        self.screen.addstr(y+1, 0, "=== A-Maze-ing ===")
        self.screen.addstr(y+2, 0, "1. Re-generate a new maze")
        self.screen.addstr(y+3, 0, "2. Show/Hide path from entry to exit")
        self.screen.addstr(y+4, 0, "3. Rotate maze colors")
        self.screen.addstr(y+5, 0, "4. Quit")
        self.screen.addstr(y+6, 0, "Choice? (1-4):")

    def set_enter_exit(self) -> None:
        x1 = self.maze_data.entery[0] * 4 + 1
        y1 = self.maze_data.entery[1] * 2 + 1
        self.screen.addstr(y1, x1, "██", curses.color_pair(2))

        x2 = self.maze_data.exit[0] * 4 + 1
        y2 = self.maze_data.exit[1] * 2 + 1
        self.screen.addstr(y2, x2, "██", curses.color_pair(3))

    def display(self) -> None:
        self.screen.clear()

        for y, row in enumerate(self.maze):
            for x, col in enumerate(row):
                self.print_box(x, y, col)

        if self.show_path:
            self.__print_path()

        self.set_enter_exit()

        self.set_choices()

        self.screen.refresh()
        self.x += 1

    def get_pressed_key(self) -> int:
        return self.screen.getch()

    def __del__(self) -> None:
        self.close()

    def close(self):
        pass
