# from datas import (
#     GameData
# )
import sys
import json


class Parser:
    def __init__(self) -> None:
        # self.config = self._get_gameconfig()
        self._config_file = self._parse_args()
        self._raw_json_data = self._parse_json()
        self._json_data_without_levels, self.json_levels_data = self._divide_json_data()

    def _parse_args(self) -> str:
        if len(sys.argv) != 2:
            raise ValueError("Program must take exactly one argument!")

        return sys.argv[1]

    def _parse_json(self) -> None:
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
        

    # def _get_gameconfig(self) -> GameData:
    #     setting = _get_jsonconfig()
    #     window = _get_windowconfig()
    #     levels = _get_levelconfigs()

    # def _get_jsonconfig(self) -> JsonConfig:
    #     a


if __name__ == "__main__":
    parser = Parser()















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
