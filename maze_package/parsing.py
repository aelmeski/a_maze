import sys


class MazeData:
    """Data container for maze configuration parameters."""

    def __init__(self) -> None:
        """Initialize maze data with default values."""
        self.width: int | None = None
        self.height: int | None = None
        self.entery: tuple | None = None
        self.exit: tuple | None = None
        self.output_file: str | None = None
        self.perfect: bool | None = None
        self.seed: int | None = None

    def validate(self) -> str | None:
        """Validate maze data and return error message or None if valid."""

        if self.width is None:
            return "the width is missing!"
        if self.height is None:
            return "the height is missing!"
        if self.entery is None:
            return "the entery is missing!"
        if self.exit is None:
            return "the exit is missing!"
        if self.output_file is None:
            return "the output_file is missing!"
        if self.perfect is None:
            return "the perfect is missing!"

        if self.entery == self.exit:
            return "the entry and exit should not be the same."
        if self.width < 10:
            return f"the width '{self.width}' should be more or equal to 10!"
        if self.width > 100:
            return f"the width '{self.width}' should be less then or equal to 100!"
        if self.height < 10:
            return f"the height '{self.height}' should be more or equal to 10!"
        if self.height > 100:
            return f"the height '{self.height}' should be less then or equal to 100!"
        if (self.entery[0] < 0 or self.entery[0] >= self.width or self.entery[1] < 0 or self.entery[1] >= self.height):
            return f"the entry point {self.entery} is not in the maze map."
        if (self.exit[0] < 0 or self.exit[0] >= self.width or
            self.exit[1] < 0 or self.exit[1] >= self.height):
            return f"the exit point {self.exit} is not in the maze map."

        if (self.is_in_patern42(self.entery)):
            return "the entry can't be above the patern 42!"
        if (self.is_in_patern42(self.exit)):
            return "the exit can't be above the patern 42!"

        return None

    def is_in_patern42(self, point: tuple) -> bool:
        """Check whether a point lies inside the blocked 42 pattern."""
        x = (self.height - 5) // 2
        y = (self.width - 7) // 2
        for i in range(3):
            if point == (x + i, y):
                return True
            if point == (x + i, y + 6):
                return True
            if point == (x + 2, y + i):
                return True
            if point == (x + 2, y + i + 4):
                return True
            if point == (x, y + i + 4):
                return True
            if point == (x + 4, y + i + 4):
                return True
            if point == (x + 2 + i, y + 2):
                return True
            if point == (x + 2 + i, y + 4):
                return True
        return False


class Parsing:
    """Parser for reading and processing maze configuration files."""

    def __init__(self) -> None:
        """Initialize parser with default settings."""
        self.error = "hey !"
        self.file_path = ""
        self.parameters: tuple[str] = (
            "WIDTH",
            "HEIGHT",
            "ENTRY",
            "EXIT",
            "OUTPUT_FILE",
            "PERFECT",
            "SEED"
        )

    def __get_file_data(self) -> list[str] | None:
        """Read and return lines from the configuration file."""
        lines: list[str] = []
        try:
            if len(sys.argv) != 2:
                self.error = "wrong arguments!"
                return None
            self.file_path = sys.argv[1]
            if not self.file_path.endswith(".txt"):
                self.error = "the config file should be '.txt'!"
                return None
            with open(self.file_path, "r") as file:
                lines = file.readlines()
            if not lines:
                raise ValueError
        except ValueError:
            self.error = str("file 'config.txt' is empty")
            return None
        except (FileNotFoundError, Exception):
            self.error = str("file 'config.txt' not found")
            return None
        return lines

    def parse(self) -> MazeData | None:
        """Parse configuration file and return MazeData or None on error."""
        maze_data = MazeData()

        lines: list[str] = self.__get_file_data()
        if not lines:
            return None

        for line in lines:
            if not line.strip() or line.startswith("#"):
                continue
            line = line.strip()
            values = line.split("=")
            if len(values) != 2:
                self.error = f"invalid format in line: '{line}'"
                return None

            if values[0] not in self.parameters:
                self.error = f"unknown parameter '{values[0]}'"
                return None

            if values[0] == "WIDTH":
                num: int | None = self.__get_int(values[1])
                if not num:
                    return None
                maze_data.width = num

            elif values[0] == "HEIGHT":
                num: int | None = self.__get_int(values[1])
                if not num:
                    return None
                maze_data.height = num

            elif values[0] == "ENTRY":
                xy: tuple | None = self.__is_xy(values[1])
                if xy is None:
                    return None
                maze_data.entery = xy

            elif values[0] == "EXIT":
                xy: tuple | None = self.__is_xy(values[1])
                if xy is None:
                    return None
                maze_data.exit = xy

            elif values[0] == "OUTPUT_FILE":
                if not values[1].endswith(".txt"):
                    self.error = f"Invalid Output File '{values[1]}'"
                    return None
                maze_data.output_file = values[1]

            elif values[0] == "PERFECT":
                if values[1] == "True":
                    maze_data.perfect = True
                elif values[1] == "False":
                    maze_data.perfect = False
                else:
                    self.erorr = f"Invalid Perfect Value '{values[1]}'"
                    return None
            
            elif values[0] == "SEED":
                if values[1] == "None":
                    maze_data.seed = None
                else:
                    try:
                        maze_data.seed = int(values[1])
                    except (Exception):
                        self.error = f"Invalid int value '{values[1]}'!."
                        return None

            else:
                self.erorr = f"Unkown Line '{line}'"
                return None

        error: str | None = maze_data.validate()
        if error:
            self.error = error
            return None
        return maze_data

    def __is_xy(self, value: str) -> tuple | None:
        """Parse a comma-separated string into an (x, y) tuple."""
        values = value.split(',')
        if len(values) != 2:
            self.erorr = f"Invalid Coordinates '{value}'"
            return None
        x: int | None = self.__get_int(values[0])
        y: int | None = self.__get_int(values[1])
        if x is None or y is None:
            self.error = f"Invalid Integer in '{value}'"
            return None
        return (x, y)

    def __get_int(self, value: str) -> int | None:
        """Convert string to integer or return None on failure."""
        try:
            num = int(value)
            return num
        except (ValueError):
            self.error = f"invalid int value '{value}'"
            return None

    def get_error(self) -> str:
        """Return the current error message."""
        return self.error
