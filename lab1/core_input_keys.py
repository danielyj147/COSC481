"""

raylib [core] example - Keyboard input

"""
import pyray


# Initialization
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
RADIUS = 50
INCREMENT = 2

pyray.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, 'raylib [core] example - keyboard input')
ball_position = pyray.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
pyray.set_target_fps(60)  # Set our game to run at 60 frames-per-second


# Main game loop
while not pyray.window_should_close():  # Detect window close button or ESC key
    # Update
    if (pyray.is_key_down(pyray.KeyboardKey.KEY_RIGHT)):
        if ball_position.x < SCREEN_WIDTH - RADIUS - INCREMENT:
            ball_position.x += INCREMENT
    if (pyray.is_key_down(pyray.KeyboardKey.KEY_LEFT)):
        if ball_position.x > 0 + RADIUS + INCREMENT:
            ball_position.x -= INCREMENT
    if pyray.is_key_down(pyray.KeyboardKey.KEY_UP):
        if ball_position.y > 0 + RADIUS + INCREMENT:
            ball_position.y -= INCREMENT
    if pyray.is_key_down(pyray.KeyboardKey.KEY_DOWN):
        if ball_position.y < SCREEN_HEIGHT - RADIUS - INCREMENT:
            ball_position.y += INCREMENT

    # Draw
    pyray.begin_drawing()

    pyray.clear_background(pyray.RAYWHITE)
    pyray.draw_text('move the ball with arrow keys', 10, 10, 20, pyray.DARKGRAY)
    pyray.draw_circle_v(ball_position, RADIUS, pyray.MAROON)
    pyray.end_drawing()


# De-Initialization
pyray.close_window()  # Close window and OpenGL context
