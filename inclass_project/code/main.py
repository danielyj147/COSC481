from pyray import *  # type: ignore
from game import *
from settings import *

current_game = Game()

if __name__ == "__main__":

    init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Sprite sheet demo")
    set_target_fps(FPS)

    current_game.startup()

    while not window_should_close():
        current_game.update()

        begin_drawing()
        clear_background(RAYWHITE)
        begin_mode_2d(current_game.camera)

        current_game.draw()

        end_mode_2d()
        end_drawing()

    close_window()
    current_game.shutdown()
