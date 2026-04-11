from collections import deque
from .maze_generator import Cell
from .parsing import MazeData


class FindPath:
    """Find a path from entry to exit using breadth-first search."""

    def __init__(self) -> None:
        """Initialize maze and endpoint placeholders."""
        self.maze: list[list[Cell]] | None = None
        self.entry: tuple[int, int] = (0, 0)
        self.exit: tuple[int, int] = (0, 0)

    def set_maze(self, maze: list[list[Cell]]) -> None:
        """Set the maze grid to search through."""
        self.maze = maze

    def set_maze_data(self, maze_data: MazeData) -> None:
        """Set entry and exit coordinates from parsed data."""
        assert maze_data.entery is not None
        assert maze_data.exit is not None
        self.entry = maze_data.entery
        self.exit = maze_data.exit

    def get_path(self) -> list[tuple[int, int]] | None:
        """Return the shortest valid path or None when unreachable."""
        if not self.maze:
            return None

        height = len(self.maze)
        width = len(self.maze[0])

        queue: deque[tuple[int, int]] = deque()
        queue.append(self.entry)
        visited: dict[tuple[int, int], tuple[int, int] | None] = {
            self.entry: None
        }

        while queue:
            x, y = queue.popleft()

            if (x, y) == self.exit:
                return self._reconstruct_path(visited)

            cell = self.maze[y][x]

            # Check North
            if not cell.N and y > 0 and (x, y - 1) not in visited:
                visited[(x, y - 1)] = (x, y)
                queue.append((x, y - 1))

            # Check East
            if not cell.E and x < width - 1 and (x + 1, y) not in visited:
                visited[(x + 1, y)] = (x, y)
                queue.append((x + 1, y))

            # Check South
            if not cell.S and y < height - 1 and (x, y + 1) not in visited:
                visited[(x, y + 1)] = (x, y)
                queue.append((x, y + 1))

            # Check West
            if not cell.W and x > 0 and (x - 1, y) not in visited:
                visited[(x - 1, y)] = (x, y)
                queue.append((x - 1, y))

        return None

    def _reconstruct_path(
        self,
        visited: dict[tuple[int, int], tuple[int, int] | None]
    ) -> list[tuple[int, int]]:
        """Build the path by backtracking from exit to entry."""
        path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = self.exit
        while current is not None:
            path.append(current)
            current = visited[current]
        path.reverse()
        return path
