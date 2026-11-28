from src.character.character import Character
from src.data.enums import Speed

class PacMan(Character):
    def update(self, ):
        ...

    def _get_spawn_point(self) -> tuple[int, int]:
        x = self.config.width // 2 + 1
        y = self.config.height // 2 + 1
        return (x, y)

    def _get_default_speed(self) -> int:
        return Speed.PACMAN