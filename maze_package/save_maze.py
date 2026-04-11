
from typing import Any


class SaveMaze:
    """Persist maze data and solved path to an output file."""

    def __init__(self) -> None:
        """Initialize output and maze serialization fields."""
        self.maze: list[list[Any]] | None = None
        self.path: list[tuple[int, int]] | None = None
        self.enter: tuple[int, int] | None = None
        self.exit: tuple[int, int] | None = None
        self.output_file = ""

    def set_output_file(self, output_file: str | None) -> None:
        """Set the destination file path for maze export."""
        if output_file is not None:
            self.output_file = output_file

    def set_enter(self, enter: tuple[int, int] | None) -> None:
        """Set the maze entry coordinate."""
        self.enter = enter

    def set_exit(self, exit: tuple[int, int] | None) -> None:
        """Set the maze exit coordinate."""
        self.exit = exit

    def set_maze(self, maze: list[list[Any]]) -> None:
        """Set the maze grid to serialize."""
        self.maze = maze

    def set_path(self, path: list[tuple[int, int]] | None) -> None:
        """Set the solved path to append in the export."""
        self.path = path

    def save_to_file(self) -> None:
        """Write maze walls, endpoints, and path directions to disk."""
        assert self.maze is not None
        assert self.enter is not None
        assert self.exit is not None
        assert self.path is not None

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
    def get_deration(point1: tuple[int, int], point2: tuple[int, int]) -> str:
        """Return movement direction from point1 to point2."""
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
        return ""
