"""raylib [textures] example - Sprite animation
Example complexity rating: [★★☆☆] 2/4
Example originally created with raylib 1.3, last time updated with raylib 1.3
Example licensed under an unmodified zlib/libpng license, which is an OSI-certified,
BSD-like license that allows static linking with closed source software
Copyright (c) 2014-2025 Ramon Santamaria (@raysan5)

This source has been converted from C raylib examples to Python.
"""

from pyray import *  # type: ignore
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent

TEXTURE_PATH = f"{THIS_DIR}/resources/man_walking.png"
SCENE_NUM = 8

# TEXTURE_PATH = f"{THIS_DIR}/resources/girl_running.png"
# SCENE_NUM = 8

# TEXTURE_PATH = f"{THIS_DIR}/resources/scarfy.png"
# SCENE_NUM = 6

MAX_FRAME_SPEED = 15
MIN_FRAME_SPEED = 1

# Initialization
screenWidth = 800
screenHeight = 450

init_window(screenWidth, screenHeight, "raylib [texture] example - sprite anim")

# Important NOTE: Textures MUST be loaded after Window initialization 
# (OpenGL context is required)
# Texture loading: one step vs. two steps (see other example)
texture = load_texture(TEXTURE_PATH)
scale = (screenWidth-30)/texture.width
texture.width = int(texture.width * scale)
texture.height = int(texture.height * scale)

position = Vector2(350.0, 280.0)
frameRec = Rectangle(0.0, 0.0, float(texture.width)/SCENE_NUM, float(texture.height))
currentFrame = 0

framesCounter = 0
framesSpeed = 8  # Number of spritesheet frames shown by second

set_target_fps(60)  # Set our game to run at 60 frames-per-second

# Main game loop
while not window_should_close():  # Detect window close button or ESC key
    # Update
    framesCounter += 1

    if framesCounter >= (60/framesSpeed):
        framesCounter = 0
        currentFrame += 1

        if currentFrame > SCENE_NUM-1:
            currentFrame = 0

        frameRec.x = float(currentFrame) * float(texture.width)/SCENE_NUM

    # Control frames speed
    if is_key_pressed(KeyboardKey.KEY_RIGHT):
        framesSpeed += 1
    elif is_key_pressed(KeyboardKey.KEY_LEFT):
        framesSpeed -= 1

    if framesSpeed > MAX_FRAME_SPEED:
        framesSpeed = MAX_FRAME_SPEED
    elif framesSpeed < MIN_FRAME_SPEED:
        framesSpeed = MIN_FRAME_SPEED

    # Draw
    begin_drawing()
    
    clear_background(RAYWHITE)
    
    draw_texture(texture, 15, 40, WHITE)
    draw_rectangle_lines(15, 40, texture.width, texture.height, LIME)
    draw_rectangle_lines(15 + int(frameRec.x), 40 + int(frameRec.y), 
                           int(frameRec.width), int(frameRec.height), RED)
    
    draw_text("FRAME SPEED: ", 165, 210, 10, DARKGRAY)
    draw_text(f"{framesSpeed:02d} FPS", 575, 210, 10, DARKGRAY)
    draw_text("PRESS RIGHT/LEFT KEYS to CHANGE SPEED!", 290, 240, 10, 
    DARKGRAY)
    
    for i in range(MAX_FRAME_SPEED):
        if i < framesSpeed:
            draw_rectangle(250 + 21*i, 205, 20, 20, RED)
        #draw_rectangle_lines(250 + 21*i, 205, 20, 20, MAROON)

    # Draw part of the texture
    draw_texture_rec(texture, frameRec, position, WHITE)  
    
    draw_text("(c) texture sprite by Eiden Marsal", screenWidth - 200,
               screenHeight - 20, 10, GRAY)
    end_drawing()

# De-Initialization
unload_texture(texture)  # Texture unloading
close_window()  # Close window and OpenGL context