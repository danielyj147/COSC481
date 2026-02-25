"""

"""
import pyray
from os.path import join
from settings import * 
import math 
class Brick():
    def __init__(self, pos:pyray.Vector2, size: pyray.Vector2, color) -> None:
        self.active = True
        self.pos = pos
        self.size = size
        self.color = color

    def update(self):
        pass 

    def draw(self):
        pyray.draw_rectangle_v(self.pos, self.size, self.color)
        
class Player:
    def __init__(self):
        self.pos =pyray.Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT * 7 / 8)
        self.size = pyray.Vector2(WINDOW_WIDTH / 10, 20)
        self.life = MAX_LIFE
        
    def update(self):
        if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT):
            self.pos.x -= SPEED * pyray.get_frame_time()
        if pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT):
            self.pos.x += SPEED * pyray.get_frame_time()
        
    def draw(self):
        pyray.draw_rectangle_v(self.pos, self.size, pyray.GRAY)

class Ball():
    def __init__(self, radius, position:pyray.Vector2, velocity:pyray.Vector2):
        self.radius = radius
        self.pos = position
        self.velocity = velocity
        self.active = True

    def update(self, player: Player, bricks: list[Brick]):
        dt = pyray.get_frame_time()
        if self.active:
            for brick in bricks:
                if brick.active:
                    //

            self.pos.x += self.velocity.x * dt
            self.pos.y += self.velocity.y * dt

            if (self.pos.y + self.radius <= 0):
                self.velocity.y =  self.velocity.y * - 1.0

            if (self.pos.x - self.radius <= 0 or self.pos.x + self.radius >= WINDOW_WIDTH):
                self.velocity.x =  self.velocity.x * - 1.0

            if pyray.check_collision_circle_rec(self.pos, self.radius, pyray.Rectangle(player.pos.x,player.pos.y, player.size.x, player.size.y)):
                self.velocity.y *= -1

    def draw(self):
        pyray.draw_circle_v(self.pos, self.radius+5, pyray.BLACK)
        pyray.draw_circle_v(self.pos, self.radius, pyray.WHITE)



class Game:

    def __init__(self):
        self.moving = True
        self.paddle_speed = 200
        self.bricks = []
        
        self.level_map = [
            '0000000000000000',
            '1111111111111111',
            '1111111111111111',
            '1111111111111111']

        self.brick_size = WINDOW_WIDTH // len(self.level_map[0])
        self.player = Player()
        
    # where game assets/resources will be initialized
    def startup(self):

        self.ball = Ball(10, pyray.Vector2(self.player.pos.x, self.player.pos.y - self.player.size.y/2 - 10), pyray.Vector2(200, 200))
        for row_index, row in enumerate(self.level_map):
            for col_index, col in enumerate(row):
                if col == '1':
                    x = col_index * self.brick_size
                    y = row_index * self.brick_size
                    color = pyray.GRAY if (col_index+row_index) % 2 else pyray.BLACK
                    brick = Brick(pyray.Vector2(x,y), pyray.Vector2(self.brick_size, self.brick_size), color)
                    self.bricks.append(brick)
        


    def update(self):
       if pyray.is_key_pressed(pyray.KeyboardKey.KEY_S):
           self.moving = not self.moving
           
       if self.moving: 
            self.player.update()
            # if (self.ball.pos.x - self.self.radius) <= 0:
            #     self.ball.pos = pyray.Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            # elif (self.ball.pos.x + self.self.radius) > pyray.get_screen_width(): 
            #     self.ball.pos = pyray.Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            self.ball.update(self.player, self.bricks)

            

                    
        
    def draw(self):
        pyray.draw_fps(20, 20)

        self.player.draw()
        self.ball.draw()
        for brick in self.bricks:
            if brick.active:
                brick.draw()
        

        # pyray.draw_text(str(self.player_score), 100, 10, 30, pyray.BLUE)
        # pyray.draw_text(str(self.enemy_score), pyray.get_screen_width() - 200, 10, 30, pyray.DARKGREEN)

    def shutdown(self):
        pass

