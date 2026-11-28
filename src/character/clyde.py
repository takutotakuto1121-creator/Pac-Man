from src.character.ghost import Ghost

class Clyde(Ghost):
    def update():
        ...

    def _get_spawn_point(self) -> tuple[int, int]:
        x = 1
        y = 1
        return (x, y)