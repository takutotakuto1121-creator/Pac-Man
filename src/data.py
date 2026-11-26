"""
ゲーム内で使用するデータ構造を決定するモジュール。
"""

from pydantic import BaseModel, model_validator, Field
from dataclasses import dataclass
from src.enum import GameScene, Direction, CharacterName

@dataclass(frozen=True)
class Level(BaseModel):
    """
    config.jsonのlevelsの情報を格納するクラス。
    """
    level: int
    width: int
    height: int


@dataclass(frozen=True)
class JsonConfig(BaseModel):
    """
    config.jsonの情報を格納するデータクラス。
    """
    highscore_filename: str
    lives: int = Field(ge=1)
    pacgum: int = Field(ge=1)
    points_per_pacgum: int = Field(ge=1)
    points_per_super_pacgum: int = Field(ge=1)
    points_per_ghost: int = Field(ge=1)
    seed: int
    level_max_time: int = Field(ge=1)
    levels: list[Level]


@dataclass(frozen=True)
class WindowConfig(BaseModel):
    """"
    pygameで作成するwindowに関するデータを格納するデータクラス
    """
    width: int
    height: int

@dataclass
class Position:
    x: int
    y: int


@dataclass(frozen=True)
class LevelConfig:
    level: int
    width: int
    height: int
    maze: list[list[int]]
    spawns: dict[CharacterName, Position]
    pacman_dir: Direction
    pacgum: set[Position]
    super_pucgum: set[Position]


@dataclass(frozen=True)
class GameConfig:
    """
    ゲーム上で終始変化しない値を格納するデータクラス。
    """
    json: JsonConfig
    window: WindowConfig
    levels: list[LevelConfig]

@dataclass
class SessionState:
    """
    Level毎に変化する値を格納するデータクラス。
    """
    scene: GameScene
    score: int
    until_dead: int
    level_index: int


@dataclass
class LevelState:
    """
    Levelの中で変化する値を格納するデータクラス
    """
    pos: dict[Position]
    pacman_dir: Direction
    pacgum: set[Position]
    super_pucgum: set[Position]
    edible_time_left: float
    game_time_left: float


@dataclass
class GameData:
    config: GameConfig
    session: SessionState
    level: LevelState