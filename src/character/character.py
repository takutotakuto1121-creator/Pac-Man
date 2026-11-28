from abc import ABC, abstractmethod
from src.data.datas import LevelConfig, LevelState
from src.data.enums import Direction
from math import floor, sqrt
from pygame import clock

class Character(ABC):
    config: LevelConfig
    spawn: tuple[int, int]
    x: float
    y: float
    current_dir: Direction
    next_dir: Direction
    speed_multiplier: float
    speed: float

    def __init__(self, config: LevelConfig) -> None:
        self.config = config
        self.spawn = self._get_spawn_point()
        self.x, self.y = self.spawn
        self.current_dir = Direction.RIGHT
        self.next_dir = Direction.RIGHT
        self.speed_multiplier = 1
        self.speed = self._get_default_speed() * self.speed_multiplier

    @abstractmethod
    def update(self, dt: float, level: LevelState) -> None:
        ...

    @abstractmethod
    def _get_spawn_point(self) -> tuple[int, int]:
        ...

    @abstractmethod
    def _get_default_speed(self) -> int:
        ...

    @abstractmethod
    def _get_next_dir(self, level: LevelState) -> Direction:
        ...

    def _move(self, dt: float) -> None:
        """
        座標を更新する。手順は以下の通り。

        1. Characterの次に向く方角(next_dir)を求める。
        2. もしnext_dirがcurrent_dirの逆(180度回転)なら、current_dirをnext_dirにする。
           これによって、180度反転の時のみ即時反転ができる。
        2. Characterがこのフレームで移動するそう距離(total)を求める。
        3. Characterが今向いている方角(current_dir)の向きに存在する最も近い
           セルの中心座標(nearest)を求める。
        4. Characterの現在座標からnearestへの距離を求める
        5. Characterがcurrent_dirに向かって進む距離(distance_direction)を求める
        6. その後にCharacterがnext_dirに向かって進む距離(distance_next_direction)を求める。
        7. 座標を更新する

        なお、迷路の壁の判定は_get_next_dir()内で行うため、この関数内では壁の条件は考慮していない。

        Args:
            dt: 1フレームで経過する秒数。単位は秒。
        """
        self.next_dir = self.get_next_dir()

        if self.next_dir == self._oppssite_to_current():
            self.current_dir == self.next_dir

        total = self.speed * dt
        nearest = self._get_next_center()
        distance_to_center = self._get_distance_to(nearest)
        distance_direction, distance_next_direction = self._get_direction_distance(total, distance_to_center, nearest)
        self._update_position(self, distance_direction, distance_next_direction)
        if self._change_current_dir:
            self.current_dir = self.next_dir

    def _opposite_to_current(self) -> bool:
        """
        Characterの現在の方向(current_dir)と次の方角(next_dir)が真逆(180度回転)
        の関係にあるかを判定する。

        Returns:
            真逆ならTrue
            そうでなければFalse
        """
        if self.current_dir == Direction.UP:
            if self.next_dir == Direction.DOWN:
                return True
        elif self.current_dir == Direction.DOWN:
            if self.next_dir == Direction.UP:
                return True
        elif self.current_dir == Direction.LEFT:
            if self.next_dir == Direction.RIGHT:
                return True
        elif self.current_dir == Direction.RIGHT:
            if self.next_dir == Direction.LEFT:
                return True
        else:
            raise ValueError("direction must be one of up, down, left or right.") 

        return False

    def _get_next_center(self) -> tuple[int, int]:
        """
        現在の座標からdirectionの向きに存在する最も近いセルの中心座標を求める。

        floor()は引数の値の小数点以下を切り捨てる関数。
        これを利用して最も近いセルの中心座標を求める。

        Returns:
            Characterのcurrent_dirの向きの最も近いセルの中心座標
        """
        if self.current_dir == Direction.UP:
            x = self.x
            y = floor(self.y)
        elif self.current_dir == Direction.DOWN:
            x = self.x
            y = floor(self.y) + 1
        elif self.current_dir == Direction.LEFT:
            x = floor(self.x)
            y = self.y
        elif self.current_dir == Direction.RIGHT:
            x = floor(self, x) + 1
            y = self.y
        else:
            raise ValueError("direction must be one of up, down, left or right.")

        return (x, y)

    def _get_distance_to(self, nearest: tuple[int, int]) -> float:
        """
        現在の座標から現在の方角の向きで最も近いセルの中心座標との距離を求める

        sqrt()は引数の２乗根を求める関数である。
        これを用いて、3平方の定理により距離を求めている。

        Args:
            nearest: Characterの現在の座標からCharacterのcurrent_dirの方角に
                     に存在する最も近いセルの中心の座標
        
        Returns:
            Characterの現在の座標からCharacterのcurrent_dirの方角に
            に存在する最も近いセルの中心の座標への距離
        """
        nearest_x, nearest_y = nearest
        distance = sqrt((self.x - nearest_x) ** 2 + (self.y - nearest_y) ** 2)

        return distance

    def _get_direction_distance(self, total: float, distance: float, nearest: tuple[int, int]) -> tuple[float, float]:
        """
        Characterがcurrent_dirに向かってどの程度の距離進むかを求める。

        Characterがこのフレームで動く全ての距離(total)がCharacterのcurrent_dirの方角に存在する最も
        近いセルの中心座標への距離(distance)以下の場)合は、totalだけcurrent_dirに動く。
        そうでない場合は、next_dirに迷路の構造上移動できるなら移動する
        ついでに次にフレーム用にcurrent_dirを今のフレームのnext_dirに変更できるようにフラグを立てておく
        移動できないなら直進できるなら直進。できないならストップ。

        Args:
            total: Characterがこのフレームで動く全ての距離
            distance: Characterのcurrent_dirの方角に存在する最も
                      近いセルの中心座標への距離
        Returns:
            Characterがcurrent_dirに向かって進む距離
            その後にnext_dirに向かって進む距離のタプル
        """
        if total <= distance:
            return (total, 0)
        else:
            if self._is_open(self.next_dir, nearest):
                self._change_current_dir = True
                return (distance, total - distance)
            elif self._is_open(self.current_dir, nearest):
                return (total, 0)
            else:
                return (distance, 0)

    def _is_open(self, direction: Direction, pos: tuple[int, int]) -> bool:
        maze = self.config.maze
        x, y = pos
        if direction == Direction.UP:
            if maze[y][x] & 8 == 0:
                return True
        elif direction == Direction.DOWN:
            if maze[y][x] & 2 == 0:
                return True
        elif direction == Direction.RIGHT:
            if maze[y][x] & 4 == 0:
                return True
        elif direction == Direction.LEFT:
            if maze[y][x] & 1 == 0:
                return True
        else:
            raise ValueError("direction must be one of up, down, left or right.")

        return False

    def _update_position(self, cur_dir_len: float, next_dir_len: float) -> None:
        """
        座標を更新する。

        Args:
            cur_dir_len: Characterの今向いている方角へ進む距離
            next_dir_len: Characterが今向いている方角へcur_dir_lenだけ進んだ
                          後に次に向く方角へ進む距離
        """
        if self.current_dir == Direction.UP:
            self.y -= cur_dir_len
        elif self.current_dir == Direction.DOWN:
            self.y += cur_dir_len
        elif self.current_dir == Direction.LEFT:
            self.x -= cur_dir_len
        elif self.current_dir == Direction.RIGHT:
            self.x += cur_dir_len
        else:
            raise ValueError("direction must be one of up, down, left or right.")  

        if self.next_dir == Direction.UP:
            self.y -= next_dir_len
        elif self.next_dir == Direction.DOWN:
            self.y += next_dir_len
        elif self.next_dir == Direction.LEFT:
            self.x -= next_dir_len
        elif self.next_dir == Direction.RIGHT:
            self.x += next_dir_len
        else:
            raise ValueError("direction must be one of up, down, left or right.")    
    


