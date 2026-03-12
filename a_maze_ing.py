from maze_package import Parsing, MazeGenerator, Display, FindPath


if __name__ == "__main__":

    parsing = Parsing()

    data = parsing.parse()

    if not data:
        print(parsing.get_error())
        exit(1)
    
    maze_generator = MazeGenerator()
    maze_generator.set_maze_data(data)

    display = Display()
    display.set_maze_data(data)

    bfs = FindPath()
    bfs.set_maze_data(data)

    def generate_maze() -> None:
        maze = maze_generator.generate_maze()
        bfs.set_maze(maze)
        path = bfs.get_path()
        display.set_maze(maze)
        display.set_path(path)
        display.display()

    generate_maze()

    while True:
        key = display.get_pressed_key()

        if key == 49:
            generate_maze()
        elif key == 50:
            display.show_hide_path()
        elif key == 51:
            display.change_colors()
        elif key == 52:
            break

    display.close()
    