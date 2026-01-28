from pyray import *

screen_width = 900
screen_height = 400

init_window(screen_width, screen_height, "FedEx Logo")
set_target_fps(60)

# Colors
FEDEX_BLUE = Color(75, 0, 130, 255)
FEDEX_ORANGE = Color(255, 102, 0, 255)

# Paddings
OFFSET_X = 60
OFFSET_Y = 80

# Base Unit
UNIT = 18


# Letter Size
MAX_HEIGHT = UNIT * 11
MIN_HEIGHT = UNIT * 7
STROKE = UNIT * 2

BASELINE = OFFSET_Y + MAX_HEIGHT
CENTER_Y = BASELINE - MIN_HEIGHT // 2

# Init x
x = 0

def draw_F(x):
    # Column
    draw_rectangle(x, OFFSET_Y, STROKE, MAX_HEIGHT, FEDEX_BLUE)

    # Rows
    draw_rectangle(x, OFFSET_Y, UNIT * 6, STROKE, FEDEX_BLUE)
    draw_rectangle(x, OFFSET_Y + UNIT * 4, UNIT * 5, STROKE, FEDEX_BLUE)

    return UNIT * 4

def draw_e(x):
    radius_outer = MIN_HEIGHT // 2
    radius_inner = radius_outer - STROKE
    center_x = x + radius_outer

    # circles
    draw_circle(center_x, 
                 CENTER_Y, 
                 radius_outer,  
                 FEDEX_BLUE)
    draw_ellipse(center_x, 
                 CENTER_Y, 
                 radius_inner, 
                 radius_inner + 10, 
                 RAYWHITE)
    
    # rects
    draw_rectangle(x+10, CENTER_Y - STROKE // 2 , radius_outer * 2 - 14, STROKE-10, FEDEX_BLUE)
    draw_rectangle(x+70, CENTER_Y - STROKE // 2 + (STROKE-10), 350, STROKE-15, RAYWHITE)

    return UNIT * 6

def draw_d(x):
    radius_outer = MIN_HEIGHT // 2
    radius_inner = radius_outer - STROKE

    # circles
    draw_circle(x + radius_outer, CENTER_Y, radius_outer, FEDEX_BLUE)
    draw_circle(x + radius_outer, CENTER_Y, radius_inner, RAYWHITE)

    # rect
    draw_rectangle(x + MIN_HEIGHT - STROKE, 
                   OFFSET_Y, STROKE, 
                   MAX_HEIGHT, 
                   FEDEX_BLUE)

    return UNIT * 7

def draw_E(x):
    # column
    draw_rectangle(x, OFFSET_Y, STROKE, MAX_HEIGHT, FEDEX_ORANGE)
    
    # rows
    draw_rectangle(x, OFFSET_Y, UNIT * 6, STROKE, FEDEX_ORANGE)
    draw_rectangle(x, 
                   OFFSET_Y + MAX_HEIGHT // 2 - STROKE // 2, 
                   UNIT * 6, 
                   STROKE, 
                   FEDEX_ORANGE)
    draw_rectangle(x, OFFSET_Y + MAX_HEIGHT - STROKE, UNIT * 6, STROKE, FEDEX_ORANGE)

    return UNIT * 6

def draw_x(x):
    top = BASELINE - MIN_HEIGHT + 9
    width = UNIT * 9
    sw = STROKE * 1.5
    
    # \ + / is more efficient than square - 4 triangles
    # \
    draw_triangle(
        Vector2(x + sw, top),
        Vector2(x, top),
        Vector2(x + width - sw, BASELINE),
        FEDEX_ORANGE
    )
    draw_triangle(
        Vector2(x + sw, top),
        Vector2(x + width - sw, BASELINE),
        Vector2(x + width, BASELINE),
        FEDEX_ORANGE
    )
    
    # /
    draw_triangle(
        Vector2(x + width, top),
        Vector2(x + width - sw, top),
        Vector2(x, BASELINE),
        FEDEX_ORANGE
    )
    draw_triangle(
        Vector2(x + width, top),
        Vector2(x, BASELINE),
        Vector2(x + sw, BASELINE),
        FEDEX_ORANGE
    )
    
    return OFFSET_X

while not window_should_close():
    begin_drawing()
    clear_background(RAYWHITE)
    
    x += draw_F(x)
    x += draw_e(x)
    x += draw_d(x)
    x += draw_E(x)
    x = draw_x(x) # reset x
    
    end_drawing()

close_window()