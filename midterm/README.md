# PANG

A Python reimplementation of the classic PANG (Buster Bros) arcade game using
[Pyray](https://github.com/electronstudio/raylib-python-cffi) (Python bindings
for [Raylib](https://www.raylib.com/)).

Based on the C/Raylib reference implementation by Ramon Santamaria:
<https://github.com/raysan5/raylib-games/blob/master/classics/src/pang.c>

## Gameplay

Bouncing balls fall from the top of the screen. The player moves left and right
at the bottom and fires a vertical line upward to pop them. When a ball is hit
it splits into two smaller balls. Destroy all balls to win. If a ball touches
the player, the game is over.

### Controls

| Key          | Action            |
|--------------|-------------------|
| Left / Right | Move player       |
| Space        | Fire              |
| P            | Pause / unpause   |
| Enter        | Restart (on game over or victory) |
| Esc          | Quit              |

### Scoring

| Ball Size | Points |
|-----------|--------|
| Big       | 200    |
| Medium    | 100    |
| Small     | 50     |

## Project Structure

```
midterm/
├── main.py          Entry point: creates window and runs the game loop
├── game.py          All game logic: Player, Shoot, Ball, FloatingPoints, Game
├── settings.py      Tunable constants (speeds, radii, scoring, etc.)
├── Makefile         Run and clean targets
└── assets/
    ├── player.png       Player sprite
    ├── ball_big.png     Big ball sprite (red, 80x80)
    ├── ball_medium.png  Medium ball sprite (blue, 40x40)
    └── ball_small.png   Small ball sprite (green, 20x20)
```

### Class Overview

- **`BallSize`** : Enum with three tiers: `BIG`, `MEDIUM`, `SMALL`.
- **`Player`** : Loads a sprite texture, moves left/right, exposes a circular
  hitbox derived from sprite dimensions.
- **`Shoot`** : A vertical line with an `origin` (fixed at player) and a `tip`
  (moves upward). Deactivates when off-screen or after 120 frames.
- **`Ball`** : Bouncing circle with gravity. Properties (radius, points, extra
  gravity) are looked up from `BALL_PROPERTIES` by size. Splits into two
  smaller balls on hit via `BALL_SPLIT` mapping.
- **`FloatingPoints`** : Score text that rises and fades out when a ball is
  popped.
- **`Game`** : Top-level controller. Owns all entities, runs update/draw each
  frame, handles collisions and state transitions (pause, game over, victory).

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (for virtual environment management)

The parent directory (`..`) should have a uv-managed virtual environment at
`../.venv`.

## Setup

From the parent directory:

```bash
uv init          # if not already done
uv add raylib    # install raylib/pyray
```

## Running

```bash
make run
```

Or directly:

```bash
../.venv/bin/python main.py
```

## Configuration

All game constants live in `settings.py`. Key values:

| Constant           | Default | Description                           |
|--------------------|---------|---------------------------------------|
| `WINDOW_WIDTH`     | 800     | Window width in pixels                |
| `WINDOW_HEIGHT`    | 450     | Window height in pixels               |
| `FPS`              | 60      | Target frame rate                     |
| `PLAYER_SPEED`     | 5.0     | Player horizontal speed (px/frame)    |
| `MAX_BIG_BALLS`    | 2       | Number of big balls at game start     |
| `BALLS_SPEED`      | 2.0     | Base ball speed (px/frame)            |
| `GRAVITY`          | 0.25    | Downward acceleration per frame       |
| `BIG_BALL_RADIUS`  | 40.0    | Big ball collision/draw radius        |
| `SHOOT_LIFETIME`   | 120     | Max frames a shot stays active        |

