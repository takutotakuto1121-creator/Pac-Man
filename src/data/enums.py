"""
ゲーム内で使用する列挙型(Enum)を列挙するモジュール。
各クラスの役割は以下。

GameScene       : ゲーム画面の状態
Direction       : キャラクターの向く方向
CharacterName   : キャラクターの名前
GhostMode       : ゴーストの状態
"""

from enum import Enum, auto

class GameScene(Enum):
    """
    ゲームの画面の状態を列挙。
    """
    MENU = auto()
    HIGHSCORE = auto()
    INSTRUCTION = auto()
    GAME = auto()
    PAUSE = auto()
    LEVEL_CLEARE = auto()
    GAME_OVER = auto()
    GAME_CLEAR = auto()


class Direction(Enum):
    """
    キャラクターの向く方向を列挙。
    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class CharacterName(Enum):
    """
    キャラクターの名前を列挙。
    """
    PACMAN = auto()
    BLINKY = auto()
    PINKY = auto()
    INKY = auto()
    CLYDE = auto()


class GhostMode(Enum):
    """
    ゴーストの状態を列挙。
    """
    SCATTER = auto()
    CHASE = auto()
    FRIGHTEN = auto()
    EATEN = auto()
    HOUSE = auto()


class Speed(Enum):
    """
    キャラクターの各状態のスピードを列挙
    """
    PACMAN = 13
    GHOST_NORMAL = 9
    GHOST_EATEN = 5
    GHOST_HOUSE = 32
