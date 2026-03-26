from pyray import *
from settings import *

# from Player import * # uncomment once you have your own

class Game:

    def __init__(self):
        self.visible = True
        self.moving = False
        #self.player = Player() #uncomment once you have yours
        self.ground = Rectangle(0, WINDOW_HEIGHT - 50, WINDOW_WIDTH, 50)

    # functions below need to be completed
    def startup(self):
        pass

    def update(self):
        dt =  get_frame_time()
      

    def draw(self):
        draw_fps(20, 20)
        draw_rectangle_rec(self.ground, YELLOW)


    def shutdown(self):
        pass

