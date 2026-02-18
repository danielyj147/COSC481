import pyray
from os.path import join
from settings import * 

class Character():
    def __init__(self):
        self.pos = pyray.Vector2(640, 320)
        self.speed = 200 # 200 pixels/sec
        self.grounded = True # would jump

    def startup(self):
        # be careful path: how you run?>
        self.texture = pyray.load_texture('lab04/resources/cat.png')

    def update(self):
        motion = pyray.Vector2(0, 0)

        if pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT):
            motion.x += 1
        if pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT):
            motion.x += -1 

        if pyray.is_key_down(pyray.KeyboardKey.KEY_UP):
            motion.y += -1
        if pyray.is_key_down(pyray.KeyboardKey.KEY_DOWN):
            motion.y += 1 

        motion_this_frame = pyray.vector2_scale(motion, pyray.get_frame_time() * self.speed)
    
        self.pos = pyray.vector2_add(self.pos, motion_this_frame)
 
   
    def draw(self):
        #draw_texture_v(self.texture, self.pos, WHITE)
        pyray.draw_texture_ex(self.texture, self.pos, 0, 4, pyray.WHITE)


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
       self.visible = not pyray.is_key_down(pyray.KeyboardKey.KEY_SPACE) # change it to a toogle
       
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
        else:      
            pyray.draw_text("Invisible!", 200, 200, 40, pyray.WHITE)

    def shutdown(self):
        pass

