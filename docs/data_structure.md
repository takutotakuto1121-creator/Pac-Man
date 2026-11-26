



# memo
## GameData
- GameDataが一番上
- その下に不変(GameConfig)、levelが変わると変わる(SessionState)、level内でも変わる3段階のクラス分け(LevelState)

## GameConfig
- frozen=True
- JsonConfig: config.jsonのデータ
- WindowConfig: pygameで作成するwindowのデータ
- list[LevelConfig]: 

## SessionState
- GameScene: menuとか
- 

## LevelState
- 