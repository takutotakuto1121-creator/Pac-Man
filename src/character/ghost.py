from src.character.character import Character
from src.data.enums import GhostMode, Speed
from src.data.datas import LevelConfig

class Ghost(Character):
    mode: GhostMode

    def __init__(self, config: LevelConfig) -> None:
        self.super().__init__()
        self.mode = GhostMode.SCATTER

    def _get_default_speed(self):
        return Speed.GHOST_NORMAL

    def 