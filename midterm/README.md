# Space PANG

A space-themed reimplementation of the classic PANG (Buster Bros) arcade game, built with Python and [Pyray](https://github.com/electronstudio/raylib-python-cffi).

## Game Description

The player controls a spaceship at the bottom of the screen, firing beams upward to destroy bouncing meteors. When a meteor is hit, it splits into two smaller, faster fragments. The goal is to destroy all fragments without getting hit.

Charging a beam makes it wider but diverts energy from the ship, leaving it visually damaged and vulnerable. Powerups dropped from destroyed meteors grant additional angled beams that fire simultaneously.

Based on the [C/Raylib PANG](https://github.com/raysan5/raylib-games/blob/master/classics/src/pang.c) by Ramon Santamaria.

## Key Features

### Charged Shoot

Holding Space charges a wider beam. The ship switches to its damaged sprite during charge to communicate the energy drain. Releasing fires all available beams at once. Quick taps fire a thin beam with no penalty.

![Gameplay](screenshots/final_play.png)

### Meteor Split

Big meteors split into two medium, medium into two small, and small ones pop. Each size has different bounce height and speed. Splitting creates progressively harder situations as the screen fills with faster fragments.

### Powerups

Splitting a meteor has a 40% chance to drop a powerup. Picking one up adds an extra beam at a 30-degree angle (left first, then right). All beams fire simultaneously on release.

### Sprite Animation

The ship uses a 4-frame sprite sheet with states for idle, banking left, banking right, and damaged (charging). The current state selects the appropriate frame each tick.

### Title, Pause & Debug

Title screen on launch. Press P to pause and view controls. Press D to toggle debug mode, which overlays hitboxes, velocity vectors, and live stats (FPS, entity counts, player state, charge level).

![Title screen](screenshots/final_title.png)
![Pause/instructions](screenshots/final_puase_instruction.png)

## Screenshots

### Before (Original PANG)

| Gameplay | Win | Game Over |
|----------|-----|-----------|
| ![](screenshots/original_play.png) | ![](screenshots/original_win.png) | ![](screenshots/original_lose.png) |

### After (Space PANG)

| Title | Gameplay | Pause/Instructions | Game Over |
|-------|----------|--------------------|-----------|
| ![](screenshots/final_title.png) | ![](screenshots/final_play.png) | ![](screenshots/final_puase_instruction.png) | ![](screenshots/final_lose.png) |

## List of Resources Used

**Art:** [Kenney.nl Space Shooter Art](https://opengameart.org/content/space-shooter-art) (CC0). Ship sprites, meteor sprites, star background. Medium meteor scaled from big with Excalidraw. Sprite sheet assembled from individual frames with Excalidraw.

**Sounds from [Pixabay](https://pixabay.com/)** (Pixabay Content License):
- Shoot sound (`shoot.mp3`) by ahmed_abdulaal
- Win sound (`win.mp3`) by freesound_community
- Lose sound (`lose.wav`)
- Meteor split sound (`split.mp3`)

**Generated sounds** (Python `wave` + `math` modules):
- Pickup sound (`pickup.wav`), ascending sine tone
- Background music (`space_bgm.wav`), chiptune in C minor at 140 BPM

**Tools:** VLC (audio editing/conversion), [ExcaliDraw](https://excalidraw.com/) (sprite sheet assembly), [uv](https://github.com/astral-sh/uv) (package management)

**Frameworks:** [Raylib](https://www.raylib.com/) + [Pyray](https://github.com/electronstudio/raylib-python-cffi)

**Reference:** [Original PANG in C/Raylib](https://github.com/raysan5/raylib-games/blob/master/classics/src/pang.c) by Ramon Santamaria

## Bonus: If I Had More Time

- **Slow-motion charging:** Scale all entity velocities and gravity by a time factor while charging. Meteors drift in slow motion, stretching the moment of vulnerability and reinforcing the energy drain narrative.
- **Multiple levels:** Progressive difficulty with more and faster meteors per stage, different meteor types with unique split patterns.
- **Ship upgrades:** Persistent upgrades between rounds (shield recharge, charge speed, beam customization).
- **Particle effects:** Explosions on meteor kills, thruster flames, spark trails on beams.
- **Leaderboard:** Local high score table with initials, arcade-style.
