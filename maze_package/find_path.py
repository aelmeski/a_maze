from collections import deque
from .maze_generator import Cell
from .parsing import MazeData

class FindPath:
    def __init__(self) -> None:
        self.maze: list[list[Cell]] = None
        self.entry: tuple = (0, 0)
        self.exit: tuple = (0, 0)

    def set_maze(self, maze: list[list[Cell]]) -> None:
        self.maze = maze

    def set_maze_data(self, maze_data: MazeData) -> None:
        self.entry = maze_data.entery
        self.exit = maze_data.exit
    
    def get_path(self) -> list[tuple] | None:
        if not self.maze:
            return None
        
        height = len(self.maze)
        width = len(self.maze[0])
        
        queue = deque()
        queue.append(self.entry)
        visited = {self.entry: None}
        
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
    
    def _reconstruct_path(self, visited: dict) -> list[tuple]:
        path = []
        current = self.exit
        while current is not None:
            path.append(current)
            current = visited[current]
        path.reverse()
        return path