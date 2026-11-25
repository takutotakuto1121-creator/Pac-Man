from pydantic import BaseModel, model_validator, Field
import sys
import json
from mazegenerator import MazeGenerator
import random

class Config(BaseModel):
    highscore_filename: str
    level: list[int]
    width: int = Field(ge=3)
    height: int = Field(ge=3)
    lives: int = Field(ge=1)
    pacgum: int = Field(ge=1)
    points_per_pacgum: int = Field(ge=1)
    points_per_super_pacgum: int = Field(ge=1)
    points_per_ghost: int = Field(ge=1)
    seed: int
    level_max_time: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_pacgum(self):
        if self.height * self.width - 5 < self.points_per_pacgum:
            raise ValueError("the number of pacgum must be less than (width * height - 5)")
        return self


class GameData(BaseModel):
    """ 適宜追加 """
    config: Config
    mazes: list[list[list[int]]]


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
        """ 仮で全レベルseedがレベルの迷路に """
        self._mazes = []
        for level in self._config.level:
            mazegen = MazeGenerator(seed=level)
            maze = mazegen.maze
            self._mazes.append(maze)
        self._game_data = GameData(
            config=self._config,
            mazes=self._mazes
        )


if __name__ == "__main__":
    parser = Parser()
    print(parser.config)
    print(parser.game_data)
