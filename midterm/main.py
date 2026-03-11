"""PANG - Classic arcade game reimplemented in Python with Pyray.

Author: Daniel Jeong
"""

from game import Game
from pyray import *  # pyright: ignore[reportWildcardImportFromLibrary]
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, FPS

game = Game()

if __name__ == "__main__":
    init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "PANG")
    set_target_fps(FPS)
    init_audio_device()

    game.load_textures()
    game.load_music()
    game.startup()



    while not window_should_close():
        game.update()

        begin_drawing()
        clear_background(RAYWHITE)
        game.draw()
        end_drawing()

    game.shutdown()
    close_window()
