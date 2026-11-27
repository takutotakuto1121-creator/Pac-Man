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
