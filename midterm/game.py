from pyray import *  # pyright: ignore[reportWildcardImportFromLibrary]
import settings as config
class Player(): # player width, height, texture
    def __init__(self, pos: Vector2, speed: int, size: Vector2):
        self.pos = pos
        self.vel = speed
        self.size = size

    def startup(self):
        pass

    def update(self):
        pass 

    def draw(self):
        pass 

class Shoot():
    def __init__(self, pos: Vector2, speed: int, timeout: int):
        self.pos = pos
        self.speed = speed
        self.timeout = timeout
        self.active = False

    def startup(self):
        pass

    def update(self):
        pass 

    def draw(self):
        pass 

class Meteor(): 
    def __init__(self, pos: Vector2, velocity: Vector2, radius: int, active:bool):
        self.pos = pos

    def startup(self):
        pass

    def update(self):
        pass 

    def draw(self):
        pass 

class Points():
    def __init__(self, pos: Vector2, val: int, alpha: float):
        self.pos = pos
        self.val = val
        self.alpha = alpha

    def startup(self):
        pass

    def update(self):
        pass 

    def draw(self):
        pass 

class Game():
    def __init__(self):
        self.score = 0
        self.player= Player(Vector2(config.WINDOW_WIDTH //2, 
                                    config.WINDOW_HEIGHT), 
                            200, 
                            Vector2(200, 200))
        self.meteors = [Meteor()] * (config.METEOR_COUNT*3)
        self.shoot = Shoot()

    def startup(self):
        pass

    def update(self):
        pass 

    def draw(self):
        pass 

    def shutdown(self):
        pass