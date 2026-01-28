"""

raylib version: 5.5.0.3

raylib [core] example - random sequence

"""
# Warm-up
# load_random_sequence: Rcore / Raylib Cheat Sheet - Load random values sequence. No values repeated.
# remap: Raymath / It's Math cheatsheet - Input value within input range to output range

from pyray import *


class ColorRect:
    color: Color
    rect: Rectangle


def generate_random_color_rect_sequence(
    rect_count: int, rect_width: float, screen_width: int, screen_height: float
) -> list:
    rectangles = []

    seq = load_random_sequence(rect_count, 0, rect_count - 1)
    rect_seq_width = rect_count * rect_width
    start_x = (screen_width - rect_seq_width) * 0.5

    for i in range(rect_count):
        rect_height = remap(seq[i], 0, rect_count - 1, 0, screen_height)

        rectangles += [ColorRect()]
        rectangles[i].color = Color(
            get_random_value(0, 255),
            get_random_value(0, 255),
            get_random_value(0, 255),
            255,
        )
        rectangles[i].rect = Rectangle(
            start_x + i * rect_width,
            screen_height - rect_height,
            rect_width,
            rect_height,
        )
    return rectangles


def shuffle_color_rect_sequence(rectangles: list, rect_count: int):
    seq = load_random_sequence(rect_count, 0, rect_count - 1)

    for i in range(rect_count):
        r1 = rectangles[i]
        r2 = rectangles[seq[i]]

        tmp_color = r1.color
        tmp_h = r1.rect.height
        tmp_y = r1.rect.y

        r1.color = r2.color
        r1.rect.height = r2.rect.height
        r1.rect.y = r2.rect.y
        r2.color = tmp_color
        r2.rect.height = tmp_h
        r2.rect.y = tmp_y


def shift_rect_sequence(rectangles: list, rect_count: int):
    end_color = rectangles[rect_count-1].color
    end_h = rectangles[rect_count-1].rect.height
    end_y = rectangles[rect_count-1].rect.y

    for i in range(rect_count-1, 0, -1):
        rectangles[i].color = rectangles[i-1].color
        rectangles[i].rect.height = rectangles[i - 1].rect.height
        rectangles[i].rect.y = rectangles[i-1].rect.y

    rectangles[0].color = end_color
    rectangles[0].rect.height = end_h
    rectangles[0].rect.y = end_y

def sort_rect_sequence(rectangles: list, rect_count: int):
    sorted_rects = sorted(rectangles, key=lambda rectangle: rectangle.rect.height)
    values = [(r.color, r.rect.height, r.rect.y) for r in sorted_rects]

    print(values)
    
    for i in range(rect_count):
        rectangles[i].color = values[i][0]
        rectangles[i].rect.height = values[i][1]
        rectangles[i].rect.y = values[i][2]


screen_width = 800
screen_height = 450

init_window(screen_width, screen_height, "raylib [core] example - random sequence")
set_target_fps(60)
rect_count = 4
rect_size = screen_width / rect_count
rectangles = generate_random_color_rect_sequence(
    rect_count, rect_size, screen_width, 0.7 * screen_height
)

while not window_should_close():

    if is_key_pressed(KeyboardKey.KEY_SPACE):
        shuffle_color_rect_sequence(rectangles, rect_count)

    if is_key_pressed(KeyboardKey.KEY_UP):
        rect_count += 1
        rect_size = screen_width / rect_count
        rectangles = generate_random_color_rect_sequence(
            rect_count, rect_size, screen_width, 0.70 * screen_height
        )

    if is_key_pressed(KeyboardKey.KEY_RIGHT):
        shift_rect_sequence(rectangles, rect_count)

    if is_key_pressed(KeyboardKey.KEY_LEFT):
        sort_rect_sequence(rectangles, rect_count)

    if is_key_pressed(KeyboardKey.KEY_DOWN):
        if rect_count >= 4:
            rect_count -= 1
            rect_size = screen_width / rect_count
            rectangles = generate_random_color_rect_sequence(
                rect_count, rect_size, screen_width, 0.70 * screen_height
            )

    begin_drawing()

    clear_background(RAYWHITE)

    for i in range(rect_count):
        draw_rectangle_rec(rectangles[i].rect, rectangles[i].color)
        draw_text(
            "Press SPACE to shuffle the current sequence",
            10,
            screen_height - 128,
            20,
            BLACK,
        )
        draw_text(
            "Press UP to add a rectangle and generate a new sequence",
            10,
            screen_height - 96,
            20,
            BLACK,
        )
        draw_text(
            "Press DOWN to remove a rectangle and generate a new sequence",
            10,
            screen_height - 64,
            20,
            BLACK,
        )
        draw_text(
            "Press RIGHT to shift rectangles by one and generate a new rectangle",
            10,
            screen_height -32,
            20,
            BLACK,
        )

    draw_text(f"Count: {rect_count} rectangles", 10, 10, 20, MAROON)
    draw_fps(screen_width - 80, 10)
    end_drawing()
close_window()
