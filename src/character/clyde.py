from src.character.ghost import Ghost
from src.character.pacman import PacMan
from src.data.enums import Direction
from src.data.datas import LevelState

class Clyde(Ghost):
    def update(self, dt: float, level: LevelState) -> None:
        self._get_next_dir = self._get_next_dir(level.pacman)
        self._move(dt)

    def _get_spawn_point(self) -> tuple[int, int]:
        x = 1
        y = 1
        return (x, y)

    def _get_next_dir(self, level: LevelState) -> Direction:
        pacman = level.pacman
        start = (self.x, self.y)
        end = (pacman.x, pacman.y)
        direction = self._a_star(start, end)

        return direction
