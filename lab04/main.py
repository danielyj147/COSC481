import pyray
from ball_game import *
from settings import * 
current_game = Game()

if __name__ == '__main__':  

  pyray.init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Python Game")
  pyray.set_target_fps(120)

  current_game.startup()

  while not pyray.window_should_close():

    current_game.update()
      
    pyray.begin_drawing()
    pyray.clear_background(pyray.PINK)

    current_game.draw()

    pyray.end_drawing()

pyray.close_window()
  
current_game.shutdown()
