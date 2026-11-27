from src.datas import (
    JsonConfig, LevelConfig, WindowConfig, GameConfig, GameData
)
from mazegenerator import MazeGenerator
import sys
import json


class Parser:
    def __init__(self) -> None:
        self._config_file = self._parse_args()
        self._raw_json_data = self._parse_json()
        self._json_data_without_levels, self._json_data_levels = self._divide_json_data()
        self._jsonconfig = self._add_to_jsonconfig()
        self._levelconfigs = self._add_to_levelconfigs()
        self._windowconfig = self._get_windowconfig()
        self._gameconfig = self._get_gameconfig()
        self._gamedata = self._get_gamedata()

    @property
    def gamedata(self) -> GameData:
        return self._gamedata

    def _parse_args(self) -> str:
        if len(sys.argv) != 2:
            raise ValueError("Program must take exactly one argument!")

        return sys.argv[1]

    def _parse_json(self) -> dict:
        with open(self._config_file) as f:
            content = f.read()
            new_content = ""

            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("#"):
                    pass
                else:
                    new_content += line

        return json.loads(new_content)

    def _divide_json_data(self) -> tuple[dict, dict]:
        data_without_levels = {k: v for k, v in self._raw_json_data.items() if k != "levels"}
        data_raw_levels = {k: v for k, v in self._raw_json_data.items() if k == "levels"}
        data_levels = data_raw_levels["levels"]

        return (data_without_levels, data_levels)

    def _add_to_jsonconfig(self) -> JsonConfig:
        return JsonConfig(**self._json_data_without_levels)

    def _add_to_levelconfigs(self) -> list[LevelConfig]:
        levelconfigs = []
        for level in self._json_data_levels:
            level, width, height = level.values()
            mazegen = MazeGenerator(
                size = (width, height),
                seed=0 if level == 0 else self._jsonconfig.seed
            )
            maze=mazegen.maze
            levelconfig = LevelConfig(
                level=level,
                width=width,
                height=height,
                maze=maze
            )
            levelconfigs.append(levelconfig)
        return levelconfigs

    def _get_windowconfig(self) -> WindowConfig:
        return WindowConfig()

    def _get_gameconfig(self) -> GameConfig:
        return GameConfig(
            self._jsonconfig,
            self._windowconfig,
            self._levelconfigs
        )

    def _get_gamedata(self) -> GameData:
        return GameData(self._gameconfig)




    # def _get_gameconfig(self) -> GameData:
    #     setting = _get_jsonconfig()
    #     window = _get_windowconfig()
    #     levels = _get_levelconfigs()

    # def _get_jsonconfig(self) -> JsonConfig:
    #     a


# if __name__ == "__main__":
#     parser = Parser()















# class Parser():
#     def __init__(self):
#         self._parse_args()
#         self._parse_json()
#         self._get_game_data()

#     @property
#     def config(self) -> Config:
#         return self._config

#     @property
#     def game_data(self) -> GameData:
#         return self._game_data

#     def _parse_args(self) -> None:
#         if len(sys.argv) != 2:
#             raise ValueError("Program must take exactly one argument!")
#         self._file = sys.argv[1]

#     def _parse_json(self) -> None:
#         with open(self._file) as f:
#             content = f.read()
#             new_content = ""
#             for line in content.split("\n"):
#                 line = line.strip()
#                 if line.startswith("#"):
#                     pass
#                 else:
#                     new_content += line
#             config = json.loads(new_content)
#             self._config = Config(**config)

#     def _get_game_data(self):
#         mazegen = MazeGenerator()
#         self._mazes = []
#         for level in self._config.level:
#             if level == 1:
#                 maze = mazegen.generate(seed=self._config.seed)
#             else:
#                 maze = mazegen.generate(seed=random.randint())
#             self._mazes.append(maze)
#         for index in len(self._config.level):

#         self._game_data = GameData(
#             config=self._config,
#             mazes=self._mazes
#         )


# if __name__ == "__main__":
#     parser = Parser()
#     print(parser.config)
#     print(parser.game_data)
