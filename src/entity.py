from abc import ABC, abstractmethod

class Entity(ABC):
    def __init__(self, config: Config) -> None:
        self.config = config

    @abstractmethod
    def update(self):
        ...


class Ghost(Entity):
    def __init__(self, config: Config) -> None:
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
    def update():


class Clyde(Ghost):
    """ オレンジ """
    def update():


class PacMan(Entity):
    # 押されたボタンの情報とか
    def __init__():

    def update():
