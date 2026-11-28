from abc import ABC, abstractmethod
from src.data.datas import LevelConfig
from src.data.enums import Direction
from math import floor, sqrt

class Character(ABC):
    config: LevelConfig
    x: float
    y: float
    current_dir: Direction
    next_dir: Direction
    speed_multiplier: float
    speed: int

    def __init__(self, config: LevelConfig) -> None:
        self.config = config
        self.x, self.y = self._get_spwan_point()
        self.current_dir = Direction.RIGHT
        self.next_dir = Direction.RIGHT
        self.speed_multiplier = 1
        self.speed = self._get_default_speed() * self.speed_multiplier

    @abstractmethod
    def _get_spwan_point(self) -> tuple[int, int]:
        ...

    @abstractmethod
    def _get_default_speed(self) -> int:
        ...

    @abstractmethod
    def _get_next_dir(self) -> Direction:
        ...

    def update(self, dt: float) -> None:
        """
        座標を更新する。手順は以下の通り。

        1. Characterの次に向く方角(next_dir)を求める。
        2. Characterがこのフレームで移動するそう距離(total)を求める。
        3. Characterが今向いている方角(current_dir)の向きに存在する最も近い
           セルの中心座標(nearest)を求める。
        4. Characterの現在座標からnearestへの距離を求める
        5. Characterがcurrent_dirに向かって進む距離(distance_direction)を求める
        6. その後にCharacterがnext_dirに向かって進む距離(distance_next_direction)を求める。
        7. 座標を更新する

        Args:
            dt: 1フレームで経過する秒数。単位は秒。
        """
        self.next_dir = self.get_next_dir()
        total = self.speed * dt
        nearest = self._get_nearest_center()
        distance_to_center = self._get_distance_to(nearest)
        distance_direction = self._get_direction_distance(total, distance_to_center)
        distance_next_direction = total - distance_direction
        self._update_position(self, distance_direction, distance_next_direction)

    def _get_nearest_center(self) -> tuple[int, int]:
        """
        現在の座標からdirectionの向きに存在する最も近いセルの中心座標を求める。

        floor()は引数の値の小数点以下を切り捨てる関数。
        これを利用して最も近いセルの中心座標を求める。

        Returns:
            Characterのcurrent_dirの向きの最も近いセルの中心座標
        """
        if self.current_dir == Direction.UP:
            x = self.x
            y = floor(self.y) - 1
        elif self.current_dir == Direction.DOWN:
            x = self.x
            y = floor(self.y)
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

    def _get_direction_distance(self, total: float, distance: float) -> float:
        """
        Characterがcurrent_dirに向かってどの程度の距離進むかを求める。

        Characterがこのフレームで動く全ての距離(total)がCharacterのcurrent_dirの方角に存在する最も
        近いセルの中心座標への距離(distance)以下の場)合は、totalだけcurrent_dirに動く。
        そうでない場合は、distanceだけcurrent_dirに動く

        Args:
            total: Characterがこのフレームで動く全ての距離
            distance: Characterのcurrent_dirの方角に存在する最も
                      近いセルの中心座標への距離
        Returns:
            Characterがcurrent_dirに向かって進む距離
        """
        if total <= distance:
            return total
        else:
            return distance

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
    


