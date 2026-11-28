from src.character.ghost import Ghost

class Pinky(Ghost):
    def update():
        ...

    def _get_spawn_point(self) -> tuple[int, int]:
        x = self.config.width
        y = self.config.height
        return (x, y)