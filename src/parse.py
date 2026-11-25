from pydantic import BaseModel, model_validator, Field
import sys
import json
from mazegenerator import MazeGenerator
from enum import Enum
import random

Pos = tuple[int, int]   # (x, y), maze[y][x]でアクセス。

class Config(BaseModel):
    highscore_filename: str
    level: list[int]
    width: list[int]
    height: list[int]
    lives: int = Field(ge=1)
    pacgum: int = Field(ge=1)
    points_per_pacgum: int = Field(ge=1)
    points_per_super_pacgum: int = Field(ge=1)
    points_per_ghost: int = Field(ge=1)
    seed: int
    level_max_time: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_details(self):
        if self.height * self.width - 5 < self.points_per_pacgum:
            raise ValueError("the number of pacgum must be less than (width * height - 5)")
        if len(self.level) != len(self.width):
            raise ValueError("the number of width must be equal to width")
        if len(self.level) != len(self.height):
            raise ValueError("the number of level must be equal to height")
        for index in len(self.level):
            if self.height[index] < 10:
                raise ValueError(f"{index}-th of height is too small")
            if self.width[index] < 10:
                raise ValueError(f"{index}-th of width is too small")
            if self.height[index] * self.width[index] - 5 < self.points_per_pacgum:
                raise ValueError("the number of pacgum must be less than (width * height - 5)")
        return self


class WindowData(BaseModel):
    width: int = Field(ge=10, default=800)
    height: int = Field(ge=10, default=600)


class GameState(str, Enum):
    menu = "menu"
    game = "game"
    win = "win"
    lose = "lose"
    clear = "clear"


class Direction(str, Enum):
    up = "up"
    down = "down"
    left = "left"
    right = "right"


class GameContext(BaseModel):
    width: int
    height: int
    level: int
    maze: list[list[int]]
    spawns: dict[str, Pos]
    pos: dict[str, Pos]
    pacman_dir: Direction = Direction.right
    edible_time_left: float = 0.0
    total_time_left: float = 0.0
    pacgum_exist: list[list[bool]]
    super_pacgum_exist: list[list[bool]]

    @model_validator(mode="after")
    def validate_details(self):
        pacgumとsuperが被りはダメとか

class GameData(BaseModel):
    """ 適宜追加 """
    config: Config              # 書き換えない。
    setting: list[GameContext]  # 書き換えない。初期値の保存
    current: list[GameContext]  # こっちを書き換える。
    level_index: int = 0        # 書き換える
    score: int = 0              # 書き換える
    dead_count: int = 0         # 書き換える
    window: WindowData = Field(default=WindowData())    # 書き換えない
    state: GameState = Field(default=GameState.menu)    # 書き換える

    def reset_level(self, index: int) -> None:
        self.level = index
        self.current = self.games[index].model_copy(deep=True)
        self.current.time_left = self.config.level_max_time


class Parser():
    def __init__(self):
        self._parse_args()
        self._parse_json()
        self._get_game_data()

    @property
    def config(self) -> Config:
        return self._config

    @property
    def game_data(self) -> GameData:
        return self._game_data

    def _parse_args(self) -> None:
        if len(sys.argv) != 2:
            raise ValueError("Program must take exactly one argument!")
        self._file = sys.argv[1]

    def _parse_json(self) -> None:
        with open(self._file) as f:
            content = f.read()
            new_content = ""
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("#"):
                    pass
                else:
                    new_content += line
            config = json.loads(new_content)
            self._config = Config(**config)

    def _get_game_data(self):
        mazegen = MazeGenerator()
        self._mazes = []
        for level in self._config.level:
            if level == 1:
                maze = mazegen.generate(seed=self._config.seed)
            else:
                maze = mazegen.generate(seed=random.randint())
            self._mazes.append(maze)
        for index in len(self._config.level):

        self._game_data = GameData(
            config=self._config,
            mazes=self._mazes
        )


if __name__ == "__main__":
    parser = Parser()
    print(parser.config)
    print(parser.game_data)
