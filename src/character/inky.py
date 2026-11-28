from src.character.ghost import Ghost

class Inky(Ghost):
    def update():
        ...

    def _get_spawn_point(self) -> tuple[int, int]:
        x = self.config.width
        y = 1
        return (x, y)