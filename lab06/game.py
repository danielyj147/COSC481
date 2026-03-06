import pyray
from os.path import join
from settings import * 
from pathlib import Path

class Character():
    def __init__(self):
        self.pos = pyray.Vector2(WINDOW_WIDTH//2, WINDOW_HEIGHT)
        self.speed = 200 # 200 pixels/sec
        self.x_vel = 0

        self.y_max = MAX_HEIGHT
        self.jump_time = JUMP_TIME

        self.gravity = 2 * MAX_HEIGHT / (JUMP_TIME**2)
        self.jump_force = -(2*MAX_HEIGHT/JUMP_TIME)

        self.mouse_pos = pyray.Vector2(0,0)

        self.y_vel = 0
        self.grounded = True
        self.ground = 0

        # modes
        self.time_toggle = False # `c` to activate
        self.lateral_toggle = False # `x` to activate

        self.mouse_clicked = False
       

    def startup(self):
        # be careful path: how you run?>
        THIS_DIR = Path(__file__).resolve().parent 
        TEXTURE_PATH = f"{THIS_DIR}/resources/z.png"
        self.texture = pyray.load_texture(TEXTURE_PATH)
        self.texture.height = 100
        self.texture.width = 100
        self.ground = WINDOW_HEIGHT - self.texture.height
        self.pos.y = self.ground

    def update(self):
        self.gravity = 2 * self.y_max/ (self.jump_time**2)
        self.jump_force = -(2*self.y_max/self.jump_time)

        motion = pyray.Vector2(0, 0)

        if pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT):
            motion.x += 1
            
        if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT):
            motion.x += -1 
        
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_C):
            self.time_toggle = not self.time_toggle

        if self.time_toggle and pyray.is_key_pressed(pyray.KeyboardKey.KEY_UP):
            self.jump_time += 0.1

        if self.time_toggle and pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
            self.jump_time -= 0.1
        
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_SPACE) and self.grounded:
            if self.lateral_toggle:
                distance  = -(self.pos.x - self.mouse_pos.x)
                self.x_vel = distance / self.jump_time
        
            self.y_vel = self.jump_force
            self.grounded = False

        
        if pyray.is_mouse_button_pressed(0):
            self.mouse_pos = pyray.get_mouse_position()
            self.y_max = WINDOW_HEIGHT - self.mouse_pos.y
            self.mouse_clicked = True

        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_X):
            self.lateral_toggle = not self.lateral_toggle
            

        
        self.y_vel += self.gravity * pyray.get_frame_time()
        self.pos.y += self.y_vel * pyray.get_frame_time()
        self.pos.x += self.x_vel * pyray.get_frame_time()
        
        self.pos.x += motion.x * pyray.get_frame_time() * self.speed

        if self.pos.x < 0:
            self.pos.x =0
        if self.pos.x+self.texture.width > WINDOW_WIDTH:
            self.pos.x = WINDOW_WIDTH - self.texture.width
        if self.pos.y >= self.ground:
            self.pos.y = self.ground

            self.y_vel = 0
            self.x_vel = 0
            self.grounded= True
        else:
            self.grounded = False

    def draw(self):
        #draw_texture_v(self.texture, self.pos, WHITE)
        pyray.draw_texture_ex(self.texture, self.pos, 0, 1, pyray.WHITE)


class Ball():
    def __init__(self, radius, position, velocity):
        self.radius = radius
        self.position = position
        self.velocity = velocity

    def update(self):
        self.position.x += self.velocity.x
        self.position.y += self.velocity.y

        # Check walls collision for bouncing
        if (self.position.x > WINDOW_WIDTH or self.position.x <= 0):
            self.velocity.x = self.velocity.x * -1.0


        if (self.position.y >=  WINDOW_HEIGHT  or self.position.y <= self.radius):
            self.velocity.y =  self.velocity.y * - 1.0

    def draw(self):
        #draw_circle_lines_v(self.position, self.radius, BLACK)
        pyray.draw_circle_v(self.position, self.radius+5, pyray.BLACK)
        pyray.draw_circle_v(self.position, self.radius, pyray.DARKPURPLE)




class Game:

    def __init__(self):
        self.visible = True
        self.moving = True
        self.ball = Ball(10,pyray.Vector2(100, 100),
                pyray.Vector2(2.0, 2.5))
        self.character = Character()

    # where game assets/resources will be initialized
    def startup(self):
        self.character.startup()
        


    def update(self):
       self.visible = not pyray.is_key_down(pyray.KeyboardKey.KEY_I) # change it to a toogle
       
       if pyray.is_key_pressed(pyray.KeyboardKey.KEY_S): # change it to a toogle
           self.moving = not self.moving
           
    
       
       if self.visible and self.moving: 
           
           self.ball.update()#, self.screenWidth, 0, self.screenHeight)
           self.character.update()
           if (pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT_BRACKET)):
               self.character.speed += 20
           if (pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT_BRACKET)):
               self.character.speed -= 20


        
    def draw(self):
        pyray.draw_fps(20, 20)
        if (self.visible):
            self.ball.draw()
            self.character.draw()

            if self.character.time_toggle:
                pyray.draw_text("TIME MODE ACTIVATED", 100,100,50,pyray.GREEN)
                pyray.draw_text(f"Jump Time: {self.character.jump_time}", 100,150,50,pyray.GREEN)

            if self.character.mouse_clicked:
                pyray.draw_circle(int(self.character.mouse_pos.x), int(self.character.mouse_pos.y), 5, pyray.BLACK)

        else:      
            pyray.draw_text("Invisible!", 200, 200, 40, pyray.WHITE)

    def shutdown(self):
        pass

