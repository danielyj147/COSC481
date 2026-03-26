from enum import Enum
from settings import *
import os

from pyray import *  # type: ignore


class Action(Enum):
    STAND = "stand"  # row 5, 4 cols
    DASH = "dash"  # row 2,, 6 cols
    DUCK = "duck"  # row 10, 2 cols
    WALK = "walk"  # row 6, 3 cols


ACTION_PROPERTIES: dict[
    Action, tuple[int, int, int, int, float, float, bool, int, int, bool]
] = {
    Action.STAND: (
        0,  # first
        3,  # last
        0,  # cur
        1,  # step
        1.0,  # duration
        1.0,  # duration_left
        True,  # repeat
        5,  # row
        4,  # sprites_in_row
        False,  # done
    ),
    Action.WALK: (
        0,  # first
        3,  # last
        0,  # cur
        1,  # step
        1.0,  # duration
        1.0,  # duration_left
        True,  # repeat
        6,  # row
        3,  # sprites_in_row
        False,  # done
    ),
    Action.DASH: (
        0,  # first
        5,  # last
        0,  # cur
        1,  # step
        1.0,  # duration
        1.0,  # duration_left
        False,  # repeat
        2,  # row
        6,  # sprites_in_row
        False,  # done
    ),
    Action.DUCK: (
        0,  # first
        1,  # last
        0,  # cur
        1,  # step
        0.1,  # duration
        0.1,  # duration_left
        False,  # repeat
        10,  # row
        2,  # sprites_in_row
        False,  # done
    ),
}

player_textures: dict[Action, str] = {}


class Player:

    def __init__(self):
        # defaults to standing
        (
            self.frist,
            self.last,
            self.cur,
            self.step,
            self.duration,
            self.duration_left,
            self.repeat,
            self.row,
            self.sprites_in_row,
            self.done,
        ) = ACTION_PROPERTIES[Action.STAND]

        self.direction = 1
        self.pos = Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT)
        self.width = PLAYER_SIZE
        self.height = PLAYER_SIZE
        self.texture: Texture | None = None

    def load_texture(self, path: str):
        self.texture = load_texture(path)

    def update(self, dt: float):
        self.duration_left -= dt

        if self.duration_left <= 0:
            self.duration_left = self.duration
            self.cur += self.step
            if self.cur > self.last:
                if self.repeat:
                    self.cur = self.frist
                else:
                    self.cur = self.last
                    self.doen = True

    def draw(self):
        if self.texture is None:
            return
        dest = Rectangle(
            self.pos.x,
            self.pos.y - self.height,
            self.width,
            self.height,
        )
        frame = self.frame()
        draw_texture_pro(
            self.texture, frame, dest, Vector2(self.width / 2, 0), 0.0, WHITE
        )

    def frame(self):
        x = (self.cur % self.sprites_in_row) * SPRITE_SHEET_TILE_SIZE
        y = SPRITE_SHEET_TILE_SIZE * self.row

        return Rectangle(x, y, SPRITE_SHEET_TILE_SIZE, SPRITE_SHEET_TILE_SIZE)

    def dash(self):
        (
            self.frist,
            self.last,
            self.cur,
            self.step,
            self.duration,
            self.duration_left,
            self.repeat,
            self.row,
            self.sprites_in_row,
            self.done,
        ) = ACTION_PROPERTIES[Action.DASH]

    def walk(self):
        (
            self.frist,
            self.last,
            self.cur,
            self.step,
            self.duration,
            self.duration_left,
            self.repeat,
            self.row,
            self.sprites_in_row,
            self.done,
        ) = ACTION_PROPERTIES[Action.DASH]

    def stand(self):
        (
            self.frist,
            self.last,
            self.cur,
            self.step,
            self.duration,
            self.duration_left,
            self.repeat,
            self.row,
            self.sprites_in_row,
            self.done,
        ) = ACTION_PROPERTIES[Action.STAND]

    def duck(self):
        (
            self.frist,
            self.last,
            self.cur,
            self.step,
            self.duration,
            self.duration_left,
            self.repeat,
            self.row,
            self.sprites_in_row,
            self.done,
        ) = ACTION_PROPERTIES[Action.DUCK]

    def unload_texture(self) -> None:
        if self.texture:
            unload_texture(self.texture)
