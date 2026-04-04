# Space PANG

A space-themed twist on the classic PANG (Buster Bros) arcade game, built with Python and [Pyray](https://github.com/electronstudio/raylib-python-cffi).

## Game Description

Pilot a spaceship. Blast bouncing meteors. Don't get hit.

Meteors bounce around the screen under gravity. You fire beams upward to destroy them -- but every hit splits a meteor into two smaller, faster ones. Your job is to destroy every last fragment without getting crushed.

The twist? You can hold Space to charge a wider beam, but charging drains your ship's energy -- it visibly weakens, leaving you exposed. Pick up powerups from destroyed meteors to unlock angled side-shots that fire simultaneously with your main beam.

Based on the [C/Raylib PANG](https://github.com/raysan5/raylib-games/blob/master/classics/src/pang.c) by Ramon Santamaria.

## Key Features

### 1. Charged Shoot -- Energy Drain

Hold Space to charge a wider beam. The longer you hold, the wider it gets:

```
width = BASE_WIDTH + charge_frames * 0.3
```

Capped at 20px after 1 second of charging. Here's the catch: while charging, your ship diverts power from shields to weapons. The sprite switches to its damaged frame to show you're vulnerable. Wider beams are easier to aim, but you're a sitting duck while you charge.

![Gameplay with charged beam and meteors](screenshots/final_play.png)

### 2. Meteor Split

Three sizes of meteor, each with their own bounce physics:

| Size   | Radius | Points | Bounce Speed |
|--------|--------|--------|--------------|
| Big    | 40 px  | 200    | -8.0         |
| Medium | 20 px  | 100    | -6.5         |
| Small  | 10 px  | 50     | -7.0         |

When hit, a meteor deactivates and two children spawn at the impact point, flying in opposite directions. Small meteors just pop. Each floor bounce uses a fixed upward velocity instead of reflection -- this prevents the "stuck to floor" bug where gravity pins the ball down on naive reflection.

### 3. Powerup System

When a meteor splits, there's a 40% chance it drops an orange powerup. Pick it up and you gain an extra beam that fires at a 30-degree angle. First pickup gives you a left beam, second gives you a right beam, and so on -- all fire simultaneously on release. The powerup falls slowly enough to actually grab it, but you still have to dodge meteors to reach it.

### 4. Sprite Sheet Animation

The ship uses a 4-frame horizontal sprite sheet (Kenney.nl Space Shooter art):

| Frame | State        | When                          |
|-------|--------------|-------------------------------|
| 0     | Idle         | Standing still                |
| 1     | Banking left | Moving left                   |
| 2     | Banking right| Moving right                  |
| 3     | Damaged      | Charging (energy drain!)      |

`PlayerState` enum values map directly to frame indices -- the source rectangle just slides across the strip. No separate texture loads needed.

### 5. Screens and Debug

- **Title screen** with starfield background
- **Pause overlay** doubles as an instruction reference (press P)
- **Debug mode** (press D) shows hitbox circles, velocity vectors, collision boxes, and live stats (FPS, active entities, player state, charge level)

![Title screen](screenshots/final_title.png)
![Pause/instructions overlay](screenshots/final_puase_instruction.png)

## Screenshots

### Before (Original PANG)

| Gameplay | Win | Game Over |
|----------|-----|-----------|
| ![](screenshots/original_play.png) | ![](screenshots/original_win.png) | ![](screenshots/original_lose.png) |

White background, rubber balls, basic player sprite. Functional but plain.

### After (Space PANG)

| Title | Gameplay | Pause/Instructions | Game Over |
|-------|----------|--------------------|-----------|
| ![](screenshots/final_title.png) | ![](screenshots/final_play.png) | ![](screenshots/final_puase_instruction.png) | ![](screenshots/final_lose.png) |

Starfield background, meteor sprites, spaceship with tilt animation, charged beams, powerups, and a proper title/pause flow.

## List of Resources Used

**Art:** [Kenney.nl Space Shooter Art](https://opengameart.org/content/space-shooter-art) (CC0) -- ship sprites, meteor sprites, star background. Medium meteor scaled from big with Python Pillow. Sprite sheet assembled from individual frames with Pillow.

**Sounds from [Pixabay](https://pixabay.com/)** (Pixabay Content License):
- Shoot sound (`shoot.mp3`) -- by ahmed_abdulaal
- Win sound (`win.mp3`) -- by freesound_community
- Lose sound (`lose.wav`)
- Meteor split sound (`split.mp3`)

**Generated sounds** (Python `wave` + `math` modules):
- Pickup sound (`pickup.wav`) -- ascending sine tone, 600-1200 Hz, 0.25s
- Background music (`space_bgm.wav`) -- chiptune in C minor at 140 BPM (square bass, sawtooth melody, triangle arpeggio)

**Tools:** VLC (audio editing/conversion), [Pillow](https://pillow.readthedocs.io/) (sprite sheet assembly), [uv](https://github.com/astral-sh/uv) (package management)

**Frameworks:** [Raylib](https://www.raylib.com/) + [Pyray](https://github.com/electronstudio/raylib-python-cffi)

**Reference:** [Original PANG in C/Raylib](https://github.com/raysan5/raylib-games/blob/master/classics/src/pang.c) by Ramon Santamaria

## Bonus: If I Had More Time

- **Slow-motion charging:** Scale all entity velocities and gravity by a `time_scale` factor (e.g., 0.3) while charging. Meteors drift in slow motion, giving you time to aim but stretching out the moment of vulnerability. Reinforces the energy drain narrative -- the ship is bending spacetime around itself at great cost.
- **Multiple levels:** Progressive difficulty with more/faster meteors per stage, maybe different meteor types with unique split patterns.
- **Ship upgrades:** Persistent upgrades between rounds -- shield recharge speed, charge rate, beam color customization.
- **Particle effects:** Explosion particles on meteor destruction, thruster flames on the ship, spark trails on beams.
- **Leaderboard:** Local high score table with initials, arcade-style.
