# Space PANG

A space-themed reimplementation of the classic PANG arcade game using
[Pyray](https://github.com/electronstudio/raylib-python-cffi) (Python bindings
for [Raylib](https://www.raylib.com/)).

Based on the C/Raylib reference implementation by Ramon Santamaria:
<https://github.com/raysan5/raylib-games/blob/master/classics/src/pang.c>

## Game Description

**Elevator pitch:** Pilot a spaceship to blast bouncing meteors out of the sky before they crush you.

Meteors bounce around the screen under gravity. The player controls a spaceship at the bottom, firing vertical beams("shoots") upward to destroy them. When a meteor is hit, it splits into two smaller, faster meteors. Destroy every last fragment to win. Getting touched by any meteor means game over.

On top of the classic PANG, this version adds:

- **Charged shots**: hold the fire key(space) to charge a wider beam.
- **Powerups**: splitting meteors sometimes drop powerups that let you fire multiple shots at the same time.
- **Animation**: the ship visually tilts when moving and flashes when shooting.

## Controls

| Key          | Action                                     |
|--------------|--------------------------------------------|
| Left / Right | Move spaceship                             |
| Space (tap)  | Fire a thin beam                           |
| Space (hold) | Charge shot -- release for a wider beam    |
| P            | Pause / unpause                            |
| Enter        | Restart (on game over or victory)          |
| Esc          | Quit                                       |

## Key Features

### 1. Charged Shoot Mechanic

The player can hold the Space key to accumulate charge. A charge bar appears above the ship showing current charge level. On release, a beam is fired whose width scales linearly with charge time:

```
width = SHOOT_BASE_WIDTH + charge_frames * CHARGE_RATE
width = min(width, SHOOT_MAX_WIDTH)
```

- `SHOOT_BASE_WIDTH` = 2 px (a quick tap fires a thin line)
- `CHARGE_RATE` = 0.3 px per frame
- `CHARGE_MAX` = 60 frames (1 second at 60 FPS)
- `SHOOT_MAX_WIDTH` = 20 px (maximum beam width)

**How it works:**

1. Each frame Space is held, `charge_frames` increments (capped at `CHARGE_MAX`).
2. A charge bar is drawn above the ship: a dark gray background (50 px wide) filled proportionally with red.
3. On Space release, the accumulated `charge_frames` is converted to beam `width` using the formula above.
4. The beam is drawn as a filled rectangle from the ship to the tip, and collision detection uses the full rectangle width -- `shoot_left` to `shoot_right` -- instead of a single line.
5. Wider beams are easier to hit with but cost time standing still while charging.

### 2. Meteor Split and Collision

Meteors come in three sizes, each with distinct physics:

| Size   | Radius | Points | Bounce Speed |
|--------|--------|--------|--------------|
| Big    | 40 px  | 200    | -8.0         |
| Medium | 20 px  | 100    | -6.5         |
| Small  | 10 px  | 50     | -5.0         |

**Split algorithm:**

1. When a beam overlaps a meteor (AABB-style check: beam's left/right edges vs. meteor's horizontal extent, and beam tip vs. meteor's bottom), the meteor is deactivated.
2. The `BALL_SPLIT` dictionary maps each size to its child: Big -> Medium, Medium -> Small, Small -> None.
3. Two child meteors spawn at the parent's position with mirrored horizontal velocities (`-BALLS_SPEED` and `+BALLS_SPEED`).
4. The score increases by the meteor's point value and a floating `+NNN` text animates upward and fades out.

**Gravity and bouncing:**

Each frame, `speed.y += GRAVITY` (0.25). On floor contact, the vertical speed is set to a fixed upward value (`bounce_speed`) rather than being reflected -- this prevents the "stuck to floor" bug that occurs with naive reflection when gravity continuously pushes the ball down.

### 3. Powerup System

When a meteor splits into children, there is a 40% chance (`POWERUP_DROP_CHANCE`) a powerup drops at the split location.

**Powerup behavior:**

1. Falls at `POWERUP_FALL_SPEED` (2 px/frame). Drawn as an orange circle with an "S" label.
2. Collision is checked via circle-circle overlap between the powerup and the player's hitbox.
3. On pickup, `max_shoots` increments by 1 and a new `Shoot` object is appended to the shoots list.
4. This means the player can fire additional beams simultaneously -- each beam is independent.
5. Powerups that fall off the bottom of the screen are deactivated.

### 4. Sprite Animation

The player ship uses a **sprite sheet** (`ship_spritesheet.png`) -- a horizontal strip of 4 frames, each 99x77 pixels:

| Frame | Index | State         |
|-------|-------|---------------|
| 0     | 0     | IDLE          |
| 1     | 1     | MOVING_LEFT   |
| 2     | 2     | MOVING_RIGHT  |
| 3     | 3     | SHOOTING      |

The `PlayerState` enum maps directly to frame indices. Each frame, the state is determined by priority:

1. If `shoot_timer > 0` (set to 15 frames when firing), state = `SHOOTING`.
2. Else if Left key held, state = `MOVING_LEFT`.
3. Else if Right key held, state = `MOVING_RIGHT`.
4. Otherwise, state = `IDLE`.

The source rectangle for `draw_texture_pro` is calculated as:

```python
source = Rectangle(frame_idx * frame_width, 0, frame_width, frame_height)
```

This selects the correct frame from the horizontal strip without needing separate texture loads.

### 5. Sound Effects and Music

| Event          | Sound File     | Source                            |
|----------------|----------------|-----------------------------------|
| Shoot fired    | `shoot.mp3`    | Pixabay (ahmed_abdulaal)          |
| Meteor split   | `split.mp3`    | Pixabay                           |
| Player hit     | `lose.wav`     | Pixabay                           |
| Victory        | `win.mp3`      | Pixabay (freesound_community)     |
| Powerup pickup | `pickup.wav`   | Generated with Python `wave` module (ascending sine tone, 600-1200 Hz, 0.25s) |
| Background     | `space_bgm.wav`| Generated with Python `wave` module (chiptune: square bass, sawtooth melody, triangle arpeggio in C minor at 140 BPM) |

Background music loops continuously via `play_music_stream` / `update_music_stream`.

## Scoring

| Meteor Size | Points |
|-------------|--------|
| Big         | 200    |
| Medium      | 100    |
| Small       | 50     |

Floating score text (`+200`, `+100`, `+50`) rises and fades at the point of impact.

## Project Structure

```
midterm/
├── main.py              Entry point: window init, game loop
├── game.py              All game logic: Player, Shoot, Ball, Powerup, FloatingPoints, Game
├── settings.py          Tunable constants (speeds, radii, scoring, charge, powerups)
├── CLAUDE.md            Project instructions for development
├── spec.md              Original assignment specification
├── Makefile             Run and clean targets
└── assets/
    ├── ship_spritesheet.png   Player ship sprite sheet (4 frames: idle, left, right, shoot)
    ├── ship_idle.png          Ship idle frame (source)
    ├── ship_left.png          Ship banking left (source)
    ├── ship_right.png         Ship banking right (source)
    ├── ship_shoot.png         Ship firing (source)
    ├── meteor_big.png         Big meteor sprite
    ├── meteor_medium.png      Medium meteor sprite (scaled from big)
    ├── meteor_small.png       Small meteor sprite
    ├── star_bg.png            Star background texture
    ├── space_bgm.wav          Background music (generated chiptune)
    ├── shoot.mp3              Shoot sound effect
    ├── split.mp3              Meteor split sound effect
    ├── lose.wav               Game over sound effect
    ├── win.mp3                Victory sound effect
    ├── pickup.wav             Powerup pickup sound (generated)
    ├── background.mp3         Original background music (Pixabay)
    ├── player.png             Original player sprite
    ├── ball_big.png           Original big ball sprite
    ├── ball_medium.png        Original medium ball sprite
    └── ball_small.png         Original small ball sprite
```

### Class Overview

- **`BallSize`** (Enum): Three tiers -- `BIG`, `MEDIUM`, `SMALL`. Properties looked up from `BALL_PROPERTIES` dict.
- **`PlayerState`** (Enum): `IDLE`, `MOVING_LEFT`, `MOVING_RIGHT`, `SHOOTING`. Integer values map to sprite sheet frame indices.
- **`Player`**: Loads a horizontal sprite sheet, selects the frame matching current `PlayerState`. Circular hitbox derived from draw dimensions.
- **`Shoot`**: A vertical rectangle with configurable `width` (from charged shoot). Moves upward from the ship. Deactivates off-screen or after 120 frames.
- **`Ball`**: Bouncing meteor with gravity. Fixed upward bounce speed on floor contact. Splits via `BALL_SPLIT` mapping. Rendered with meteor textures.
- **`Powerup`**: Orange circle that falls after a meteor split. On player collision, increases `max_shoots` by 1.
- **`FloatingPoints`**: Score text that rises and fades when a meteor is popped.
- **`Game`**: Top-level controller. Manages entities, input (including charge accumulation), collisions, state transitions, and draw ordering (beams behind ship).

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (for virtual environment management)

The parent directory (`..`) should have a uv-managed virtual environment at `../.venv`.

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

| Constant             | Default | Description                           |
|----------------------|---------|---------------------------------------|
| `WINDOW_WIDTH`       | 800     | Window width in pixels                |
| `WINDOW_HEIGHT`      | 450     | Window height in pixels               |
| `FPS`                | 60      | Target frame rate                     |
| `PLAYER_SPEED`       | 5.0     | Horizontal speed (px/frame)           |
| `PLAYER_DRAW_HEIGHT` | 50.0    | Ship draw height in pixels            |
| `MAX_BIG_BALLS`      | 2       | Number of big meteors at start        |
| `BALLS_SPEED`        | 2.0     | Base meteor speed (px/frame)          |
| `GRAVITY`            | 0.25    | Downward acceleration per frame       |
| `SHOOT_BASE_WIDTH`   | 2.0     | Minimum beam width                    |
| `SHOOT_MAX_WIDTH`    | 20.0    | Maximum charged beam width            |
| `CHARGE_RATE`        | 0.3     | Width gain per charge frame           |
| `CHARGE_MAX`         | 60      | Maximum charge frames (1 sec)         |
| `POWERUP_DROP_CHANCE`| 0.4     | Chance of powerup on meteor split     |

## Resources Used

### Art Assets

- **Ship sprites (idle, left, right, damaged):** [Kenney.nl Space Shooter Art](https://opengameart.org/content/space-shooter-art) -- CC0 (Public Domain). Credit: Kenney (kenney.nl).
- **Meteor sprites (big, small):** Same Kenney.nl Space Shooter Art pack. Medium meteor scaled from big using Python Pillow.
- **Star background:** Same Kenney.nl Space Shooter Art pack.
- **Sprite sheet assembly:** Individual ship frames combined into a horizontal strip using Python Pillow (`PIL.Image`).

### Sound Effects

- **Laser/shoot sound (`shoot.mp3`):** [Pixabay](https://pixabay.com/) -- by ahmed_abdulaal. Pixabay Content License.
- **Win sound (`win.mp3`):** [Pixabay](https://pixabay.com/) -- by freesound_community. Pixabay Content License.
- **Lose sound (`lose.wav`):** [Pixabay](https://pixabay.com/). Pixabay Content License.
- **Meteor split sound (`split.mp3`):** [Pixabay](https://pixabay.com/). Pixabay Content License.
- **Powerup pickup sound (`pickup.wav`):** Programmatically generated using Python `wave` and `math` modules. Ascending sine wave from 600 Hz to 1200 Hz over 0.25 seconds with linear amplitude fade-out.
- **Background music (`space_bgm.wav`):** Programmatically generated using Python `wave` and `math` modules. Chiptune composition: square-wave bass line, sawtooth melody, and triangle-wave arpeggio in C minor at 140 BPM. Loops at ~14 seconds.

### Audio Tools

- **VLC:** Used to edit and convert audio files sourced from Pixabay.

### Frameworks and Libraries

- **[Raylib](https://www.raylib.com/):** Game library for graphics, input, and audio.
- **[Pyray](https://github.com/electronstudio/raylib-python-cffi):** Python bindings for Raylib.
- **[Pillow (PIL)](https://pillow.readthedocs.io/):** Used to assemble the ship sprite sheet and resize meteor sprites.
- **[uv](https://github.com/astral-sh/uv):** Python virtual environment and package manager.

### Reference Implementation

- **Original PANG in C/Raylib:** [raylib-games by Ramon Santamaria](https://github.com/raysan5/raylib-games/blob/master/classics/src/pang.c)
