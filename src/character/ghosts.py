from src.character.character import Character
from src.data.enums import GhostMode, Speed, Direction
from src.data.datas import LevelConfig, LevelState
import heapq
import random
from abc import abstractmethod


class Ghost(Character):
    mode: GhostMode

    def __init__(self, config: LevelConfig) -> None:
        super().__init__(config)
        self.mode = GhostMode.SCATTER

    @abstractmethod
    def _get_next_dir_chase(self, level: LevelState) -> Direction:
        ...

    def update(self, dt: float, level: LevelState) -> None:
        self.next_dir = self._get_next_dir(level)
        self._move(dt)

    def _get_default_speed(self):
        return Speed.GHOST_NORMAL

    def _get_next_dir(self, level: LevelState) -> Direction:
        if self.mode == GhostMode.SCATTER:
            return self._get_next_dir_scatter()
        elif self.mode == GhostMode.CHASE:
            return self._get_next_dir_chase(level)
        elif self.mode == GhostMode.FRIGHTEN:
            return self._get_next_dir_frighten()
        elif self.mode == GhostMode.EATEN:
            return self._get_next_dir_eaten()
        elif self.mode == GhostMode.HOUSE:
            return self._get_next_dir_frighten()

    def _get_nearest_center(self, pos: tuple[float, float]) -> tuple[int, int]:
        x, y = pos
        near_x = int(round(x))
        near_y = int(round(y))
        return (near_x, near_y)

    def _a_star(self, start: tuple[int, int], end: tuple[int, int]) -> Direction:
        if start == end:
            return None

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
        while parent[current] is not None:
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

    def _get_next_dir_scatter(self) -> Direction:
        org_next = self._get_next_center()
        org_x, org_y = org_next
        next = int(org_x), int(org_y)

        return self._a_star(next, self.spawn)

    def _get_next_dir_frighten(self) -> Direction:
        org_next = self._get_next_center()
        org_x, org_y = org_next
        next = int(org_x), int(org_y)

        candidates = []
        if self._is_open(Direction.UP, next):
            candidates.append(Direction.UP)
        if self._is_open(Direction.DOWN, next):
            candidates.append(Direction.DOWN)
        if self._is_open(Direction.RIGHT, next):
            candidates.append(Direction.RIGHT)
        if self._is_open(Direction.LEFT, next):
            candidates.append(Direction.LEFT)

        return random.choice(candidates)

    def _get_next_dir_eaten(self) -> Direction:
        org_next = self._get_next_center()
        org_x, org_y = org_next
        next = int(org_x), int(org_y)
    
        x = self.config.width // 2 + 1
        y = self.config.height // 2 + 1

        return self._a_star(next, (x, y))
        

class Blynky(Ghost):
    def _get_spawn_point(self) -> tuple[int, int]:
        x = 1
        y = 1

        return (x, y)

    def _get_next_dir_chase(self, level: LevelState) -> Direction:
        pacman = level.pacman
        start = self._get_next_center()
        end = self._get_nearest_center((pacman.x, pacman.y))
        direction = self._a_star(start, end)

        return direction


class Pinky(Ghost):
    def _get_spawn_point(self) -> tuple[int, int]:
        x = self.config.width
        y = 1

        return (x, y)

    def _get_next_dir_chase(self, level: LevelState) -> Direction:
        width = self.config.width
        height = self.config.height
        pacman = level.pacman
        start = self._get_next_center()
        pac_x, pac_y = self._get_nearest_center((pacman.x, pacman.y))
    
        if pacman.current_dir == Direction.UP:
            end = (pac_x, pac_y - 4)
        elif pacman.current_dir == Direction.DOWN:
            end = (pac_x, pac_y + 4)
        elif pacman.current_dir == Direction.RIGHT:
            end = (pac_x + 4, pac_y)
        elif pacman.current_dir == Direction.LEFT:
            end = (pac_x - 4, pac_y)
        
        direction = self._a_star(start, end)

        return direction


class Inky(Ghost):
    def _get_spawn_point(self) -> tuple[int, int]:
        x = self.config.width
        y = self.config.height

        return (x, y)

    def _get_next_dir_chase(self, level: LevelState) -> Direction:
        pacman = level.pacman
        start = self._get_next_center()
        end = self._get_nearest_center((pacman.x, pacman.y))
        direction = self._a_star(start, end)

        return direction


class Clyde(Ghost):
    def _get_spawn_point(self) -> tuple[int, int]:
        x = 1
        y = self.config.height

        return (x, y)

    def _get_next_dir_chase(self, level: LevelState) -> Direction:
        pacman = level.pacman
        start = self._get_next_center()
        end = self._get_nearest_center((pacman.x, pacman.y))
        direction = self._a_star(start, end)

        return direction
