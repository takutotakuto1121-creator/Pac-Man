from pydantic import BaseModel, model_validator, Field


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
    def __init__():


    def parse() -> Config:
