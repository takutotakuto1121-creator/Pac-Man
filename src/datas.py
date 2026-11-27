"""
ゲーム内で使用するデータ構造を決定するモジュール。
構造は以下のようになっている。

GameData                    : ゲーム内のすべてのデータ
├── GameConfig              : ゲーム内で変化しないデータ
│   ├── JsonConfig          : levels以外のjson.configのデータ
│   ├── WindowConfig        : pygameで作成するwindowに関するデータ
│   └── list[LevelConfig]   : 各レベルの変化しないデータのリスト
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
    level: int


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
    eat_count: int
    eaten_time_left: float
    house_time_left: float
    game_time_left: float

    def pacman_moveとか適当に作る


class GameData:
    """
    プロジェクト全体で使用する変数をまとめたクラス。
    """
    config: GameConfig
    scene: GameScene
    session: SessionState
    level: LevelState

    def __init__(self, config: GameConfig) -> None:
        self.config = config
        self.scene = GameScene.MENU
        self.session = self._init_session()
        self.level = self.reset_level_as(0)

    def _init_session(self) -> SessionState:
        score = 0
        lives_left = self.config.setting.lives
        level_index = 0

        return SessionState(
            score=score
            lives_left=lives_left
            level_index=level_index
        )

    def reset_level_as(self, level: int) -> LevelState:
        level_config = self.congig.levels[level]

        pos = self._init_level_pos(level_config)
        ghost_mode = self._init_ghost_mode()
        pacman_dir = Direction.RIGHT
        pacgum = self._init_pacgum(level_config)
        super_pacgum = self._init_super_pacgum(level_config)
        eat_count = 0
        eaten_time_left = 0
        house_time_left = 0
        game_time_left = self.config.setting.level_max_time

        return LevelState(
            pos=pos,
            ghost_mode=ghost_mode,
            pacman_dir=pacman_dir,
            pacgum=pacgum,
            super_pacgum=super_pacgum,
            eat_count=eat_count,
            eaten_time_left=eaten_time_left,
            house_time_left=house_time_left,
            game_time_left=game_time_left
        )

    def _init_level_pos(self, level_config: LevelConfig) -> dict[CharacterName, Position]:
        width = level_config.width
        height = level_config.height

        pacman_pos = Position(x=width // 2, y=height // 2)
        blinky_pos = Positoin(x=0, y=0)
        pinky_pos = Position(x=width - 1, y=0)
        inky_pos = Position(x=width -1 , y=height - 1)
        clyde_pos = Position(x=0, y=height - 1)

        pos = {
            CharacterName.PACMAN: pacman_pos,
            CharacterName.BLINKY: blinky_pos,
            CharacterName.PINKY: pinky_pos,
            CharacterName.INKY: inky_pos,
            CharacterName.CLYDE: clyde_pos
        }

        return pos

    def _init_ghost_mode(self) -> dict[CharacterName, GhostMode]:
        return {
            CharacterName.BLINKY: GhostMode.SCATTER,
            CharacterName.PINKY: GhostMode.SCATTER,
            CharacterName.INKY: GhostMode.SCATTER,
            CharacterName.CLYDE: GhostMode.SCATTER
        }

    def _init_pacgum(self, level_config: LevelConfig) -> set[Position]:
        pacgum = {}
        pacgum_num = self.config.setting.pacgum

    def _init_super_pacgum(self, level_config: LevelCongig) -> set[Position]:
        width = level_config.width
        height = level_config.height

        return {
            Position(0, 0),
            Position(width - 1, 0),
            Position(width - 1, height - 1),
            Position(0, height - 1)
        }


if __name__ == "__main__":
