"""
ゲーム内で使用するデータ構造を決定するモジュール。
構造は以下のようになっている。

GameData                    : ゲーム内のすべてのデータ
├── GameConfig              : ゲーム内で変化しないデータ
│   ├──JsonConfig           : levels以外のjson.configのデータ
│   ├──WindowConfig         : pygameで作成するwindowに関するデータ
│   ├──list[LevelConfig]    : 各レベルの変化しないデータのリスト
├── GameScene               : ゲームの状態(MenuやGameOverなど)のデータ(enums.pyに書いている)
├── SessionState            : ゲームをリスタートしたときにリセットされるデータ。ゲームを通して変化する。
└── LevelState              : ゲーム内でレベルが変わる際にリセットされるデータ。レベル内で変化する。
"""

from pydantic import BaseModel, model_validator, Field, ConfigDict
from dataclasses import dataclass, field
from src.enums import GameScene, Direction, CharacterName, GhostMode


class JsonConfig(BaseModel):
    """
    config.jsonの情報のうち、levels以外の情報を格納するデータクラス。
    """
    model_config = ConfigDict(frozen=True)
    highscore_filename: str = Field(min_length=1, default="highscore.json")
    lives: int = Field(ge=1)
    pacgum: int = Field(ge=0)
    points_per_pacgum: int = Field(ge=0)
    points_per_super_pacgum: int = Field(ge=0)
    points_per_ghost: int = Field(ge=0)
    seed: int = Field(ge=1)
    level_max_time: int = Field(ge=1)


@dataclass(frozen=True)
class WindowConfig:
    """"
    pygameで作成するwindowに関するデータを格納するデータクラス
    """
    width: int = field(default=800)
    height: int = field(default=600)
    fps: int = field(default=60)

@dataclass(frozen=True)
class Position:
    """
    座標データを格納するクラス。
    """
    x: int
    y: int


class JsonLevelConfig(BaseModel):
    """
    config.jsonのうち、levelsの情報のみを格納するクラス。
    """
    level: int  = Field(ge=1)
    width: int = Field(ge=3)
    height: int =Field(ge=3)


class LevelConfig(JsonLevelConfig):
    """
    各levelに関する情報を格納するクラス。
    """
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
    setting: JsonConfig
    window: WindowConfig
    levels: list[LevelConfig]

@dataclass
class SessionState:
    """
    新しいゲームを始めた時にリセットされる値を格納するデータクラス。
    """
    score: int
    lives_left: int
    level_index: int


@dataclass
class LevelState:
    """
    次のlevelに進むとリセットされる値を格納するデータクラス
    """
    pos: dict[CharacterName, Position]
    ghost_mode: dict[CharacterName, GhostMode]
    pacman_dir: Direction
    pacgum: set[Position]
    super_pacgum: set[Position]
    eaten_time_left: float
    house_time_left: float
    game_time_left: float


@dataclass
class GameData:
    """
    プロジェクト全体で使用する変数をまとめたクラス。
    """
    config: GameConfig
    scene: GameScene
    session: SessionState
    level: LevelState
