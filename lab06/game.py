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
    SPAWN_POS = pyray.Vector2(100, 100)

    def __init__(self, radius):
        self.radius = radius
        self.position = pyray.Vector2(self.SPAWN_POS.x, self.SPAWN_POS.y)
        self.y_vel = 0
        self.gravity = 800
        self.elasticity = 0.8
        self.elasticity_toggle = True
        self.ground = WINDOW_HEIGHT - self.radius

    def respawn(self):
        self.position.x = self.SPAWN_POS.x
        self.position.y = self.SPAWN_POS.y
        self.y_vel = 0

    def update(self):
        if pyray.is_key_pressed(pyray.KeyboardKey.KEY_E):
            self.elasticity_toggle = not self.elasticity_toggle
            self.respawn()

        if self.elasticity_toggle:
            if pyray.is_key_pressed(pyray.KeyboardKey.KEY_UP):
                self.elasticity = min(1.0, self.elasticity + 0.05)
            if pyray.is_key_pressed(pyray.KeyboardKey.KEY_DOWN):
                self.elasticity = max(0.0, self.elasticity - 0.05)

        dt = pyray.get_frame_time()
        self.y_vel += self.gravity * dt
        self.position.y += self.y_vel * dt

        if self.position.y >= self.ground:
            self.position.y = self.ground
            self.y_vel = -self.y_vel * self.elasticity

        if self.position.y <= self.radius:
            self.position.y = self.radius
            self.y_vel = -self.y_vel * self.elasticity

    def draw(self):
        pyray.draw_circle_v(self.position, self.radius + 5, pyray.BLACK)
        pyray.draw_circle_v(self.position, self.radius, pyray.DARKPURPLE)


class Game:

    def __init__(self):
        self.visible = True
        self.moving = True
        self.ball = Ball(10)
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
            if self.ball.elasticity_toggle:
                self.character.time_toggle = False
            if self.character.time_toggle:
                self.ball.elasticity_toggle = False
            if (pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT_BRACKET)):
                self.character.speed += 20
            if (pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT_BRACKET)):
                self.character.speed -= 20


        
    def draw(self):
        pyray.draw_fps(20, 20)
        if (self.visible):
            if self.ball.elasticity_toggle:
                self.ball.draw()
            self.character.draw()

            if self.character.time_toggle:
                pyray.draw_text("TIME MODE ACTIVATED", 100,100,50,pyray.GREEN)
                pyray.draw_text(f"Jump Time: {self.character.jump_time}", 100,150,50,pyray.GREEN)

            if self.character.mouse_clicked:
                pyray.draw_circle(int(self.character.mouse_pos.x), int(self.character.mouse_pos.y), 5, pyray.BLACK)
            
            if self.ball.elasticity_toggle:
                pyray.draw_text("Press E: Respawn", 100, 100, 50, pyray.ORANGE)
                pyray.draw_text("UP/DOWN: adjust e", 100, 150, 50, pyray.ORANGE)
                pyray.draw_text(f"Elasticity: {self.ball.elasticity:.2f}", 100, 200, 50, pyray.ORANGE)


        else:      
            pyray.draw_text("Invisible!", 200, 200, 40, pyray.WHITE)

    def shutdown(self):
        pass

