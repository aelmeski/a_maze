

class SaveMaze:
    def __init__(self):
        self.maze = None
        self.path = None
        self.enter = None
        self.exit = None
        self.output_file = ""

    def set_output_file(self, output_file) -> None:
        self.output_file = output_file

    def set_enter(self, enter) -> None:
        self.enter = enter

    def set_exit(self, exit) -> None:
        self.exit = exit

    def set_maze(self, maze) -> None:
        self.maze = maze

    def set_path(self, path) -> None:
        self.path = path

    def save_to_file(self) -> None:
        with open(self.output_file, 'w') as file:
            base16 = "0123456789ABCDEF"
            for array in self.maze:
                line = ""
                for cell in array:
                    num = 0
                    if not cell.N:
                        num += 1
                    if not cell.E:
                        num += 2
                    if not cell.S:
                        num += 4
                    if not cell.W:
                        num += 8
                    line += base16[num]
                line += '\n'
                file.write(line)
            file.write(f"\n{self.enter[0]},{self.enter[1]}")
            file.write(f"\n{self.exit[0]},{self.exit[1]}")
            line = "\n"
            for i in range(len(self.path)):
                if i + 1 >= len(self.path):
                    break
                line += self.get_deration(self.path[i], self.path[i+1])
            file.write(line)

    @staticmethod
    def get_deration(point1, point2) -> str:
        a = point1[0] - point2[0]
        b = point1[1] - point2[1]
        if a > 0:
            return "W"
        if a < 0:
            return "E"
        if b > 0:
            return "N"
        if b < 0:
            return "S"
