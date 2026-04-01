from enum import Enum

from pyray import *  # type: ignore
from settings import *

from Player import *

TEXTURES_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "hero-sheet.png"
)
BACKGROUND_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")

MAX_BUILDINGS = 100




class Game:

    def __init__(self):
        self.visible = True
        self.moving = False
        self.player = Player()
        self.ground = Rectangle(0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50)
        self.camera = Camera2D()

        # BACKGROUND
        self.spacing = 0
        self.buildings = []
        self.build_colors = []

        self.background_textures = []
        self.background = None

    def startup(self):
        self.player.load_texture(TEXTURES_PATH)
        self.camera.target = Vector2(self.player.pos.x, self.player.pos.y)
        self.camera.offset = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT)
        self.camera.rotation = 0.0
        self.camera.zoom = 1.0

        for i in range(MAX_BUILDINGS):
            width = get_random_value(50, 200)
            height = get_random_value(100, 800)
            y = WINDOW_HEIGHT - height
            x = -6000 + self.spacing

            self.buildings.append(Rectangle(x, y, width, height))

            self.spacing += width

            self.build_colors.append(
                Color(
                    get_random_value(200, 240),
                    get_random_value(200, 240),
                    get_random_value(200, 250),
                    255,
                )
            )
        for dirpath, dirnames, filenames in os.walk(BACKGROUND_PATH):
            self.background_textures.extend(filenames)
        
    def update(self):
        dt = get_frame_time()
        self.player.update(dt)

        # move
        if is_key_down(KeyboardKey.KEY_RIGHT):
            self.player.pos.x += 2
        elif is_key_down(KeyboardKey.KEY_LEFT):
            self.player.pos.x -= 2
        # Rotation
        if is_key_down(KeyboardKey.KEY_A):
            self.camera.rotation -= 1
        if is_key_down(KeyboardKey.KEY_S):
            self.camera.rotation += 1

        if self.camera.rotation > 40:
            self.camera.rotation = 40
        if self.camera.rotation < -40:
            self.camera.rotation = -40

        self.camera.target = self.player.pos

        # Zoom
        self.camera.zoom += get_mouse_wheel_move() * 0.5

        if self.camera.zoom > 3.0:
            self.camera.zoom = 3.0
        if self.camera.zoom < 0.1:
            self.camera.zoom = 0.1

        # reset camera
        if is_key_down(KeyboardKey.KEY_R):
            self.camera.zoom = 1.0
            self.camera.rotation = 0.0

    def draw(self):
        draw_fps(20, 20)
        # draw_texture_pro() # missing background textures
        for i in range(MAX_BUILDINGS):
            draw_rectangle_rec(self.buildings[i], self.build_colors[i])
        draw_rectangle_rec(self.ground, YELLOW)
        self.player.draw()

    def shutdown(self):
        pass
