from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, pos: tuple[int, int]) -> None:
        self.pos = pos

    @abstractmethod
    def update(self):
        ...


class Ghost(Entity):
    def __init__(self, pos: tuple[int, int]) -> None:
        super().__init__()
        self.edible = False


class Blinky(Ghost):
    """ 赤 """
    def update():


class Pinky(Ghost):
    """ ピンク """
    def update():


class Inky(Ghost):
    """ 水色 """
    def update()


class Clyde(Ghost):
    """ オレンジ """
    def update():


class PacMan(Entity):
    def update()
