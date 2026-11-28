from src.character.character import Character
from src.data.enums import GhostMode, Speed, Direction
from src.data.datas import LevelConfig
import heapq

class Ghost(Character):
    mode: GhostMode

    def __init__(self, config: LevelConfig) -> None:
        self.super().__init__()
        self.mode = GhostMode.SCATTER

    def _get_default_speed(self):
        return Speed.GHOST_NORMAL

    def _a_star(self, start: tuple[int, int], end: tuple[int, int]) -> Direction:
        parent = {start: None}
        g_score = {start: 0}
        start_f = self._get_f(start, end, 0)
        queue = [(start_f, start)]

        while queue:
            _, current = heapq.heappop(queue)

            if current == end:
                break

            neighbors = self._get_neighbors(current)
            for neighbor in neighbors:
                if self._is_visited(neighbor, g_score.keys()):
                    pass
                else:
                    parent[neighbor] = current
                    g_score[neighbor] = g_score[current] + 1
                    neighbor_f = self._get_f(neighbor, end, g_score[neighbor])
                    heapq.heappush(queue, (neighbor_f, neighbor))

        if current != end:
            return None

        path = []
        while current is not None:
            x, y = current
            nx, ny = parent[current]
            direction = self._get_direction((x, y), (nx, ny))
            path.append(direction)
            current = parent[current]

        return path[-1]

    def _get_f(self, cell: tuple[int, int], end: tuple[int, int], g: int) -> int:
        cur_x, cur_y = cell
        end_x, end_y = end
        h = abs(cur_x - end_x) + abs(cur_y - end_y)

        return g + h

    def _get_neighbors(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        maze = self.config.maze
        neighbors = []
        x, y = cell

        if maze[y][x] & 8 == 0:
            neighbors.append((x, y - 1))
        if maze[y][x] & 4 == 0:
            neighbors.append((x + 1, y))
        if maze[y][x] & 2 == 0:
            neighbors.append((x, y + 1))
        if maze[y][x] & 1 == 0:
            neighbors.append((x - 1, y))

        return neighbors

    def _is_visited(self, cell: tuple[int, int], visited: list[tuple[int, int]]) -> bool:
        if cell in visited:
            return True
        else:
            return False

    def _get_direction(self, current: tuple[int, int], parent: tuple[int, int]) -> Direction:
        x, y = current
        nx, ny = parent
        if x - nx == 1:
            return Direction.RIGHT
        elif x - nx == -1:
            return Direction.LEFT
        elif y - ny == 1:
            return Direction.DOWN
        elif y - ny == -1:
            return Direction.UP
        else:
            raise ValueError("current or parent is invalid")
    
        




            


