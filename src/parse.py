from pydantic import BaseModel, model_validator, Field
import sys
import json

class Config(BaseModel):
    highscore_filename: str
    level: list[int]
    width: int
    height: int
    lives: int
    pacgum: int
    points_per_pacgum: int
    points_per_super_pacgum: int
    points_per_ghost: int
    seed: int
    level_max_time: int


class Parser():
    def __init__(self):
        self._parse_args()
        self._parse()

    @property
    def config(self) -> Config:
        return self._config

    def _parse_args(self) -> None:
        if len(sys.argv) != 2:
            raise ValueError("Program must take exactly one argument!")
        self._file = sys.argv[1]

    def _parse(self) -> None:
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


if __name__ == "__main__":
    parser = Parser()
    print(parser.config)
