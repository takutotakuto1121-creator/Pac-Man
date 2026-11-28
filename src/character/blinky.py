from src.character.ghost import Ghost

class Blinky(Ghost):
    def update():
        ...

    def _get_spawn_point(self) -> tuple[int, int]:
        x = 1
        y = self.config.height
        return (x, y)