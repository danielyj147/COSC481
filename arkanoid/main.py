"""
Authors: Daniel Jeong, Sebastian Cole
"""
from ball_game import *
from settings import * 
current_game = Game()

if __name__ == '__main__':  

  pyray.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Game")
  pyray.set_target_fps(60)

  current_game.startup()
  
  while not pyray.window_should_close():

    current_game.update()
    
    pyray.begin_drawing()
    pyray.clear_background(pyray.WHITE)

    current_game.draw()

    pyray.end_drawing()

pyray.close_window()
  
current_game.shutdown()
