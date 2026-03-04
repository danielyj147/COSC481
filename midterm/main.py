"""
PANG
Author: Daniel Jeong
"""
from game import Game
from pyray import * # pyright: ignore[reportWildcardImportFromLibrary]
from settings import * 

game = Game()

if __name__ == '__main__':  

  init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Game")
  set_target_fps(60)

  game.startup()
  
  while not window_should_close():

    game.update()
    
    begin_drawing()
    clear_background(WHITE)

    game.draw()

    end_drawing()

close_window()
  
game.shutdown()
