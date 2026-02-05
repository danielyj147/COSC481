from pyray import *
from os.path import join
from settings import * 

class Ball():
    def __init__(self, radius, position:Vector2, velocity):
        self.radius = radius
        self.pos = position
        self.velocity:Vector2 = velocity

    def update(self, player:Rectangle, enemy: Rectangle):
        self.pos.x += self.velocity.x
        self.pos.y += self.velocity.y

        if CheckCollisionCircleRec(self.pos, self.radius, player):
            self.velocity.x *= -1

        if CheckCollisionCircleRec(self.pos, self.radius, enemy):
            self.velocity.x *= -1

        if (self.pos.y + self.radius >=  WINDOW_HEIGHT  or self.pos.y <= self.radius):
            self.velocity.y =  self.velocity.y * - 1.0

    def draw(self):
        draw_circle_v(self.pos, self.radius+5, BLACK)
        draw_circle_v(self.pos, self.radius, WHITE)


class Game:

    def __init__(self):
        self.moving = True
        self.player_score = 0
        self.enemy_score = 0
        self.paddle_speed = 200
    # where game assets/resources will be initialized
    def startup(self):
        self.enemy_vision = get_screen_width()//2
        self.ball = Ball(10, Vector2(get_screen_width()//2, get_screen_height()//2), Vector2(2.0, 2.5))
        self.enemy = Rectangle(50, get_screen_height()//2, PEDDLE_WIDTH, PEDDLE_HEIGHT)
        self.player = Rectangle(get_screen_width()-50, get_screen_height()//2, PEDDLE_WIDTH, PEDDLE_HEIGHT)
        


    def update(self):
       if is_key_pressed(KeyboardKey.KEY_P):
           self.moving = not self.moving
           
       if self.moving: 
            y = 0
            if is_key_down(KeyboardKey.KEY_UP):
                y -= 1
            if is_key_down(KeyboardKey.KEY_DOWN):
                y += 1

            self.player.y += y * get_frame_time() * self.paddle_speed
            if (self.ball.pos.x - self.ball.radius) <= 0:
                self.enemy_score += 1000
                self.ball.pos = Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            elif (self.ball.pos.x + self.ball.radius) > get_screen_width(): 
                self.player_score += 1000
                self.ball.pos = Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)
            self.ball.update(self.player, self.enemy)


            if self.ball.pos.x < self.enemy_vision:
                if self.ball.pos.y > (self.enemy.y + self.enemy.height/2):
                    self.enemy.y += get_frame_time() * self.paddle_speed
                elif self.ball.pos.y < (self.enemy.y + self.enemy.height/2):
                    self.enemy.y -= get_frame_time() * self.paddle_speed
            

                    
        
    def draw(self):
        draw_fps(20, 20)

        draw_rectangle_rec(self.player, BLACK)
        draw_rectangle_rec(self.enemy, BLACK)
        self.ball.draw()

        draw_text(str(self.player_score), 100, 10, 30, BLUE)
        draw_text(str(self.enemy_score), get_screen_width() - 200, 10, 30, DARKGREEN)

    def shutdown(self):
        pass

