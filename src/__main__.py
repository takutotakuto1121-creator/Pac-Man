from src.data.parse import Parser
from src.character.character import Character

parser = Parser()
print(parser.gamedata.config)
print(parser.gamedata.scene)
print(parser.gamedata.session)
print(parser.gamedata.level)

character = Character(parser.gamedata.config.levels[0])
