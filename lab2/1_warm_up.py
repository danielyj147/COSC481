from pyray import *

# Initialization
screenWidth = 800
screenHeight = 450
xmid = screenWidth // 2
ymid = screenHeight // 2
y_thrid_q = screenHeight * 3 // 4
x_thrid_q = screenWidth * 3 // 4
init_window(screenWidth, screenHeight, "warm-up")

XP = 60 # x padding
YP = 30 # y padding

# RED Tri
THICKNESS = 5
RED_VECTORS = [
    Vector2(XP, YP),
    Vector2(xmid - XP, YP),
    Vector2(XP, ymid - YP),
    Vector2(xmid - XP, ymid - YP),
]

def summon_triangles(tops: list[Vector2], height: float, width: float):
    for top in tops:
        xl = top.x - (width/2) # left
        xr = top.x + (width/2) # right
        y = top.y + height
    
        draw_triangle(top,
                      Vector2(xl, y),
                      Vector2(xr, y),
                      YELLOW)

set_target_fps(60)

# Main game loop
while not window_should_close():
    # Update

    begin_drawing()

    clear_background(RAYWHITE)

    # RED Lines
    for idx in range(0, 3): # 3 is vector count
        draw_line_ex(RED_VECTORS[idx], RED_VECTORS[idx + 1], THICKNESS, RED)


    # Circle
    draw_circle(screenWidth // 4, y_thrid_q, 100, BLACK)
    draw_circle(screenWidth // 4, y_thrid_q, 90, BLUE)


    # Blue Lines
    for i in range(1, 6):
        start = Vector2(xmid + XP, YP * i)
        end = Vector2(screenWidth - XP, YP * i)
        draw_line_ex(start, end, THICKNESS, BLUE)


    # Pink Polygon
    draw_poly(Vector2(x_thrid_q, y_thrid_q), 12, 100, 0, PINK)


    # Yellow Triangles
    summon_triangles([Vector2(x_thrid_q - XP, YP * 5 + 2),
                      Vector2(x_thrid_q + XP, YP * 5 + 2),
                      ], 60, 40)

    end_drawing()

# De-Initialization
close_window()
