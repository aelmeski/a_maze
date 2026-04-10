import curses
from maze_package import Parsing, MazeGenerator, Display, FindPath, SaveMaze


def main(stdscr):
    parsing = Parsing()
    data = parsing.parse()
    if not data:
        stdscr.addstr(0, 0, parsing.get_error())
        stdscr.getch()
        return

    maze_generator = MazeGenerator()
    maze_generator.set_maze_data(data)

    display = Display(stdscr)
    display.set_maze_data(data)
    bfs = FindPath()
    bfs.set_maze_data(data)

    save_maze = SaveMaze()
    save_maze.set_output_file(data.output_file)
    save_maze.set_enter(data.entery)
    save_maze.set_exit(data.exit)

    def generate_maze():
        maze = maze_generator.generate_maze()
        bfs.set_maze(maze)
        path = bfs.get_path()
        display.set_maze(maze)
        display.set_path(path)
        display.display()

        save_maze.set_maze(maze)
        save_maze.set_path(path)
        save_maze.save_to_file()

    generate_maze()

    while True:
        key = display.get_pressed_key()
        if key == ord('1'):
            generate_maze()
        elif key == ord('2'):
            display.show_hide_path()
        elif key == ord('3'):
            display.change_colors()
        elif key == ord('4'):
            break


if __name__ == "__main__":
    curses.wrapper(main)
