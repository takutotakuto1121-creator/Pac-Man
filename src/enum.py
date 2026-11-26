from enum import Enum, auto

class GameScene(Enum):
    MENU = auto()
    HIGHSCORE = auto()
    INSTRUCTION = auto()
    GAME = auto()
    PAUSE = auto()
    LEVEL_CLEARED = auto()
    GAME_OVER = auto()
    GAME_CLEAR = auto()


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class CharacterName(Enum):
    BLINKY = auto()
    PINKY = auto()
    INKY = auto()
    CLYDE = auto()
    PACMAN = auto()