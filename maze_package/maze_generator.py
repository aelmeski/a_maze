import random
from .parsing import MazeData


class Cell:
    def __init__(self) -> None:
        self.N = True
        self.E = True
        self.S = True
        self.W = True
        self.is42 = False
        self.visited = False
    
    def reset(self) -> None:
        self.N = False
        self.E = False
        self.S = False
        self.W = False



class MazeGenerator:
    def __init__(self) -> None:
        self.width = 0
        self.height = 0
        self.entry: tuple = (0, 0)
        self.exit: tuple = (0, 0)
        self.perfect = False
        self.maze: list[list[Cell]] = []

    def generate_maze(self) -> list[list[Cell]]:
        self.maze = [[Cell() for _ in range(self.width)] for _ in range(self.height)]
        
        stack = []
        start_x, start_y = self.entry
        current = (start_x, start_y)
        self.maze[start_y][start_x].visited = True
        
        while True:
            x, y = current
            neighbors = self._get_unvisited_neighbors(x, y)
            
            if neighbors:
                next_cell = random.choice(neighbors)
                nx, ny, direction = next_cell
                stack.append(current)
                self._remove_wall(x, y, nx, ny, direction)
                self.maze[ny][nx].visited = True
                current = (nx, ny)
            elif stack:
                current = stack.pop()
            else:
                break
        
        return self.maze
    
    def _get_unvisited_neighbors(self, x: int, y: int) -> list:
        neighbors = []
        if y > 0 and not self.maze[y - 1][x].visited:
            neighbors.append((x, y - 1, 'N'))
        if x < self.width - 1 and not self.maze[y][x + 1].visited:
            neighbors.append((x + 1, y, 'E'))
        if y < self.height - 1 and not self.maze[y + 1][x].visited:
            neighbors.append((x, y + 1, 'S'))
        if x > 0 and not self.maze[y][x - 1].visited:
            neighbors.append((x - 1, y, 'W'))
        return neighbors
    
    def _remove_wall(self, x: int, y: int, nx: int, ny: int, direction: str) -> None:
        if direction == 'N':
            self.maze[y][x].N = False
            self.maze[ny][nx].S = False
        elif direction == 'E':
            self.maze[y][x].E = False
            self.maze[ny][nx].W = False
        elif direction == 'S':
            self.maze[y][x].S = False
            self.maze[ny][nx].N = False
        elif direction == 'W':
            self.maze[y][x].W = False
            self.maze[ny][nx].E = False
    
    def set_maze_data(self, maze_data: MazeData) -> None:
        self.width = maze_data.width
        self.height = maze_data.height
        self.entry = maze_data.entery
        self.exit = maze_data.exit
        self.perfect = maze_data.perfect

