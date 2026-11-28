# tsugimot
- config.jsonのwidth, heightを各レベルごとに指定できるように変更
- GameDataで各レベルごとのmaze、書くエンテティの座標などを一つのクラスに集約
- GameDataを扱いやすいように改変する
- level_max_timeもarrayに対応させる

# メモ
config.jsonのlevelsについて
levelが順番に0, 1, 2, 3, ....
""0スタートに固定するめんどいし""
という連続した値のみしか許さないようにする。

levelのindex == levelになる

# pacgum自動生成のアルゴリズム
pacgumの数だけ四隅以外でランダムに生成するのもいいけど、
なんかダサいからいい感じにガウス分布のようなまとまりが何個かあるような生成にしたい。

# ゲームループ
2通り
- GameDataに全て突っ込んでCharacterなどはGameDataを書き換える。
この場合、
```python
def step(gamedata):

```
- Characterの座標などの情報はCharacterに持たせる。Unityのゲームループを参考にして。updateとか決まった名前のメソッドをメインループがわで呼び出す。衝突判定などもメインループで行う。unityみたいな感じにする
どっちにしようかな

aaaa

まあ普通にCharacterに持たせて
list[Character]
をLevelStateに持たせて、
メインループで
```python
def step():
    updata_character() # forのループで全部呼び出す
    detect_collision() # 本来forの二重ループやけどパックマンだけでいいか
    ...
    draw() # これは担当じゃない
```
みたいな感じでやる

fps依存の回避
前回の呼び出しからの秒数dtをかけた分だけ移動させることにより回避
dt = clock.tick(fps) / 1000

スピードの調整はSpeedを倍率を最後にいい感じに調整

- Pinkyの４マス先の設定とInky
今だとセグフォ起きるから後で対応あと1スタートやからズレてる後でやる

飽きたからBlinky以外のゴーストの追跡は明日やって下さい
