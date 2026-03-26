from enum import Enum

from pyray import *  # type: ignore
from settings import *

from Player import *

TEXTURES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "hero-sheet.png"
)


class Game:

    def __init__(self):
        self.visible = True
        self.moving = False
        self.player = Player()
        self.ground = Rectangle(0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50)

    def startup(self):
        self.player.load_texture(TEXTURES_PATH)

    def update(self):
        dt = get_frame_time()
        self.player.update(dt)

    def draw(self):
        draw_fps(20, 20)
        draw_rectangle_rec(self.ground, YELLOW)
        self.player.draw()

    def shutdown(self):
        pass
