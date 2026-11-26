"""
ゲーム内で使用するデータ構造を決定するモジュール。
config.json内の情報のうち、levelsのみJsonConfigではなく独立してLevelConfigに格納されていることに注意。
"""

from pydantic import BaseModel, model_validator, Field, ConfigDict
from dataclasses import dataclass
from src.enums import GameScene, Direction, CharacterName, GhostMode


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


@dataclass(frozen=True)
class WindowConfig:
    """"
    pygameで作成するwindowに関するデータを格納するデータクラス
    """
    width: int
    height: int

@dataclass(frozen=True)
class Position:
    x: int
    y: int


class JsonLevelConfig(BaseModel):
    level: int
    width: int
    height: int


class LevelConfig(JsonLevelConfig):
    model_config = ConfigDict(frozen=True)
    maze: list[list[int]]
    spawns: dict[CharacterName, Position]
    pacman_dir: Direction
    pacgum: set[Position]
    super_pacgum: set[Position]


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
    新しいゲームを始めた時にリセットされる値を格納するデータクラス。
    """
    scene: GameScene
    score: int
    lives_left: int
    level_index: int


@dataclass
class LevelState:
    """
    Levelの中で変化する値を格納するデータクラス
    """
    pos: dict[CharacterName, Position]
    ghost_mode: dict[CharacterName, GhostMode]
    pacman_dir: Direction
    pacgum: set[Position]
    super_pacgum: set[Position]
    edible_time_left: float
    game_time_left: float


@dataclass
class GameData:
    config: GameConfig
    session: SessionState
    level: LevelState