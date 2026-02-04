from pyray import *
from os.path import join
from settings import * 

class Peddle():
    def __init__(self, pos:Vector2, side:str):
        self.pos = pos
        self.speed = 200 # 200 pixels/sec
        self.side = side
        self.score = 0
    def startup(self):
        pass

    def update(self):
        y = 0
        if self.side == "left": 
            if is_key_down(KeyboardKey.KEY_UP):
                y -= 1
            if is_key_down(KeyboardKey.KEY_DOWN):
                y += 1
        if self.side == "right":
            if is_key_down(KeyboardKey.KEY_W):
                y -= 1
            if is_key_down(KeyboardKey.KEY_S):
                y += 1

    
        self.pos.y += y * get_frame_time() * self.speed
    def getPos(self) -> Vector2:
        return self.pos
   
    def draw(self):
        draw_rectangle(int(self.pos.x), int(self.pos.y), PEDDLE_WIDTH, PEDDLE_HEIGHT, BLACK)

class Ball():
    def __init__(self, radius, position:Vector2, velocity):
        self.radius = radius
        self.pos = position
        self.velocity = velocity

    def update(self, x1:int, y1:int, x2:int, y2:int):
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y

        if(self.pos.y <= y1 + PEDDLE_HEIGHT and self.pos.y >= y1):
            if(self.pos.x <= x1 + PEDDLE_WIDTH and self.pos.x >= x1):
                self.velocity.x = self.velocity.x * -1.0           

        if(self.pos.y <= y2 + PEDDLE_HEIGHT and self.pos.y >= y2):
            if(self.pos.x <= x2 + PEDDLE_WIDTH and self.pos.x >= x2):
                self.velocity.x = self.velocity.x * -1.0            

        # Check walls collision for bouncing
        if(self.pos.x > WINDOW_WIDTH):
            # increment right score by 1
            self.pos = Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            
        if(self.pos.x <= 0):
            # set score
            self.pos = Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            


        if (self.pos.y >=  WINDOW_HEIGHT  or self.pos.y <= self.radius):
            self.velocity.y =  self.velocity.y * - 1.0

    def draw(self):
        #draw_circle_lines_v(self.pos, self.radius, BLACK)
        draw_circle_v(self.pos, self.radius+5, BLACK)
        draw_circle_v(self.pos, self.radius, DARKPURPLE)


class Game:

    def __init__(self):
        self.moving = False
        self.ball = Ball(10, Vector2(100, 100),
                Vector2(2.0, 2.5))
        self.peddle1 = Peddle(Vector2(50, 100), "left")
        self.peddle2 = Peddle(Vector2(WINDOW_WIDTH-PEDDLE_WIDTH-50, 100), "right")

    # where game assets/resources will be initialized
    def startup(self):
        pass
        


    def update(self):
       
       if is_key_pressed(KeyboardKey.KEY_P): # change it to a toogle
           self.moving = not self.moving
           
    
       
       if self.moving: 
           self.peddle1.update()
           self.peddle2.update()
           pos1 = self.peddle1.getPos()
           pos2 = self.peddle2.getPos()
           self.ball.update(pos1.x, pos1.y, pos2.x, pos2.y) # need pos2
           if (is_key_down(KeyboardKey.KEY_RIGHT_BRACKET)):
               self.peddle1.speed += 20
               self.peddle2.speed += 20
           if (is_key_down(KeyboardKey.KEY_LEFT_BRACKET)):
               self.peddle1.speed -= 20
               self.peddle2.speed -= 20


        
    def draw(self):
        draw_fps(20, 20)

        self.ball.draw()
        self.peddle1.draw()
        self.peddle2.draw()

    def shutdown(self):
        pass

