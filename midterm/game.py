# idk why but using Ball as a class requires this.
from __future__ import annotations
import math
import os
import random
from enum import Enum
import logging

# "Cheating" ==> otherwise code gets bloated
from pyray import *  # pyright: ignore[reportWildcardImportFromLibrary]
from settings import *  # noqa: F403

# Enables VS code execute button
ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


# Maybe an over engineering, but feels good to get an autocomplete(BallSize.<autocomplete>)
# Added bonus of being type strict
class BallSize(Enum):
    BIG = "big"
    MEDIUM = "medium"
    SMALL = "small"


class MusicType(Enum):
    BACKGROUND = "background"
    TITLE = "title"


class SoundType(Enum):
    SHOOT = "shoot"
    LOSE = "lose"
    WIN = "win"
    SPLIT = "split"
    PICKUP = "pickup"


# Properties per size: (radius, points, bounce_speed)
# Cleaner in the end b/c you can do
# size,points,bounce_peed = BALL_PROPERTIES[size]
BALL_PROPERTIES: dict[BallSize, tuple[float, int, float]] = {
    BallSize.BIG: (BIG_BALL_RADIUS, BIG_BALL_POINTS, BIG_BALL_BOUNCE_SPEED),
    BallSize.MEDIUM: (MEDIUM_BALL_RADIUS, MEDIUM_BALL_POINTS, MEDIUM_BALL_BOUNCE_SPEED),
    BallSize.SMALL: (SMALL_BALL_RADIUS, SMALL_BALL_POINTS, SMALL_BALL_BOUNCE_SPEED),
}


# What a ball splits into when shot(avoding bloated if statements)
BALL_SPLIT: dict[BallSize, BallSize | None] = {
    BallSize.BIG: BallSize.MEDIUM,
    BallSize.MEDIUM: BallSize.SMALL,
    BallSize.SMALL: None,  # no split
}

# Meteor sprites (Kenney.nl Space Shooter art, CC0 - opengameart.org)
BALL_SPRITES: dict[BallSize, str] = {
    BallSize.BIG: os.path.join(ASSET_DIR, "meteor_big.png"),
    BallSize.MEDIUM: os.path.join(ASSET_DIR, "meteor_medium.png"),
    BallSize.SMALL: os.path.join(ASSET_DIR, "meteor_small.png"),
}

# Music paths
MUSICS: dict[MusicType, str] = {
    MusicType.BACKGROUND: os.path.join(ASSET_DIR, "space_bgm.wav"),
}

SOUNDS: dict[SoundType, str] = {
    SoundType.LOSE: os.path.join(ASSET_DIR, "lose.wav"),
    SoundType.SHOOT: os.path.join(ASSET_DIR, "shoot.mp3"),
    SoundType.WIN: os.path.join(ASSET_DIR, "win.mp3"),
    SoundType.SPLIT: os.path.join(ASSET_DIR, "split.mp3"),
    SoundType.PICKUP: os.path.join(ASSET_DIR, "pickup.wav"),
}


class GameScreen(Enum):
    TITLE = "title"
    PLAYING = "playing"
    GAME_OVER = "game_over"
    VICTORY = "victory"


class PlayerState(Enum):
    IDLE = 0
    MOVING_LEFT = 1
    MOVING_RIGHT = 2
    SHOOTING = 3


# Sprite sheet: 4 frames (idle, left, right, shoot) in a horizontal strip
# Source: Kenney.nl Space Shooter art, CC0 - opengameart.org
SHIP_SPRITESHEET_PATH = os.path.join(ASSET_DIR, "ship_spritesheet.png")
SHIP_FRAME_COUNT = 4

ball_textures: dict[BallSize, Texture] = {}
game_musics: dict[MusicType, Music] = {}
game_sounds: dict[SoundType, Sound] = {}


class Player:
    def __init__(self) -> None:
        self.position: Vector2 = Vector2(0, 0)
        self.speed: float = PLAYER_SPEED
        self.width: float = 0.0
        self.height: float = 0.0
        self.state: PlayerState = PlayerState.IDLE
        self.shoot_timer: int = 0
        self.spritesheet: Texture | None = None
        self.frame_width: float = 0.0
        self.frame_height: float = 0.0

    def load_texture(self) -> None:
        self.spritesheet = load_texture(SHIP_SPRITESHEET_PATH)
        self.frame_width = self.spritesheet.width / SHIP_FRAME_COUNT
        self.frame_height = self.spritesheet.height
        scale = PLAYER_DRAW_HEIGHT / self.frame_height
        self.width = self.frame_width * scale
        self.height = self.frame_height * scale

    def unload_texture(self) -> None:
        if self.spritesheet is not None:
            unload_texture(self.spritesheet)

    def setup(self) -> None:
        self.position = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT)
        self.state = PlayerState.IDLE
        self.shoot_timer = 0

    # Enables player.collider_center
    @property
    def collider_center(self) -> Vector2:
        return Vector2(self.position.x, self.position.y - self.height / 2)

    @property
    def collider_radius(self) -> float:
        return min(self.width, self.height) / 2

    def update(self) -> None:
        moving_left = is_key_down(KeyboardKey.KEY_LEFT)
        moving_right = is_key_down(KeyboardKey.KEY_RIGHT)

        if moving_left:
            self.position.x -= self.speed
        if moving_right:
            self.position.x += self.speed

        half_w = self.width / 2
        self.position.x = max(half_w, min(self.position.x, WINDOW_WIDTH - half_w))

        if self.shoot_timer > 0:
            self.shoot_timer -= 1
            self.state = PlayerState.SHOOTING
        elif moving_left and not moving_right:
            self.state = PlayerState.MOVING_LEFT
        elif moving_right and not moving_left:
            self.state = PlayerState.MOVING_RIGHT
        else:
            self.state = PlayerState.IDLE

    def draw(self) -> None:
        if self.spritesheet is None:
            return
        frame_idx = self.state.value
        source = Rectangle(
            frame_idx * self.frame_width, 0, self.frame_width, self.frame_height
        )
        dest = Rectangle(
            self.position.x,
            self.position.y - self.height,
            self.width,
            self.height,
        )
        draw_texture_pro(
            self.spritesheet, source, dest, Vector2(self.width / 2, 0), 0.0, WHITE
        )


class Shoot:
    """A beam that travels from the player upward (or at an angle for side shoots)."""

    def __init__(self, angle_deg: float = 0.0) -> None:
        self.tip: Vector2 = Vector2(0, 0)       # moving end of the beam
        self.origin: Vector2 = Vector2(0, 0)     # stays at the player's position
        self.speed: float = 0.0
        self.life_frames: int = 0
        self.active: bool = False
        self.width: float = SHOOT_BASE_WIDTH     # wider = charged shot
        self.angle_deg: float = angle_deg        # 0 = straight up, +/- for side shoots
        self.dx: float = 0.0                     # per-frame x movement (from angle)
        self.dy: float = 0.0                     # per-frame y movement (from angle)

    def setup(self) -> None:
        self.active = False
        self.life_frames = 0
        self.width = SHOOT_BASE_WIDTH

    def fire(self, player: Player, width: float = SHOOT_BASE_WIDTH) -> None:
        self.origin = Vector2(player.position.x, player.position.y)
        self.tip = Vector2(player.position.x, player.position.y - player.height)
        self.speed = PLAYER_SPEED
        self.active = True
        self.life_frames = 0
        self.width = width
        # Convert angle to per-frame velocity components
        # sin for horizontal spread, -cos so 0 degrees = straight up
        angle_rad = math.radians(self.angle_deg)
        self.dx = math.sin(angle_rad) * self.speed
        self.dy = -math.cos(angle_rad) * self.speed
        play_sound(game_sounds[SoundType.SHOOT])

    def update(self) -> None:
        if not self.active:
            return

        self.tip.x += self.dx
        self.tip.y += self.dy
        self.life_frames += 1

        # Deactivate when off-screen or expired
        if (
            self.tip.y < 0
            or self.tip.x < 0
            or self.tip.x > WINDOW_WIDTH
            or self.life_frames >= SHOOT_LIFETIME
        ):
            self.active = False

    def draw(self) -> None:
        if self.active:
            draw_line_ex(
                self.origin,
                self.tip,
                self.width,
                RED,
            )


class Ball:
    def __init__(
        self, size: BallSize, position: Vector2, speed: Vector2, active: bool = True
    ) -> None:
        radius, points, bounce_speed = BALL_PROPERTIES[size]
        self.size: BallSize = size
        self.position: Vector2 = position
        self.speed: Vector2 = speed
        self.radius: float = radius
        self.points: int = points
        self.bounce_speed: float = bounce_speed
        self.active: bool = active

    def update(self) -> None:
        if not self.active:
            return

        self.position.x += self.speed.x
        self.position.y += self.speed.y

        # Horizontal wall bounce
        if (
            self.position.x + self.radius >= WINDOW_WIDTH
            or self.position.x - self.radius <= 0
        ):
            self.speed.x *= -1

        # Ceiling bounce
        if self.position.y - self.radius <= 0:
            self.speed.y = abs(self.speed.y)

        # Floor bounce: !!! use fixed velocity for consistent bounce height
        # otherwise gets stuck to the floor
        if self.position.y + self.radius >= WINDOW_HEIGHT:
            self.speed.y = self.bounce_speed
            self.position.y = WINDOW_HEIGHT - self.radius

        # Gravity
        self.speed.y += GRAVITY

    def draw(self) -> None:
        texture = ball_textures.get(self.size)
        if (
            texture is None
        ):  # Since we are loading texture after window init, it can be null.
            # To make type happy, fallback to circle if texture not loaded
            color = DARKGRAY if self.active else fade(LIGHTGRAY, 0.3)
            draw_circle_v(self.position, self.radius, color)
            return

        tint = WHITE if self.active else fade(WHITE, 0.3)
        diameter = self.radius * 2
        source = Rectangle(0, 0, texture.width, texture.height)
        dest = Rectangle(self.position.x, self.position.y, diameter, diameter)
        # Draw centered on position
        draw_texture_pro(
            texture,
            source,
            dest,
            Vector2(self.radius, self.radius),
            0.0,
            tint,
        )

    def split(self) -> list[Ball]:
        # Using split map
        child_size = BALL_SPLIT[self.size]
        if child_size is None:
            return []
        play_sound(game_sounds[SoundType.SPLIT])
        return [
            Ball(
                child_size,
                Vector2(self.position.x, self.position.y),
                Vector2(
                    -BALLS_SPEED,
                    BALLS_SPEED if child_size == BallSize.MEDIUM else -BALLS_SPEED,
                ),
            ),
            Ball(
                child_size,
                Vector2(self.position.x, self.position.y),
                Vector2(
                    BALLS_SPEED,
                    BALLS_SPEED if child_size == BallSize.MEDIUM else -BALLS_SPEED,
                ),
            ),
        ]


class Powerup:
    def __init__(self, position: Vector2) -> None:
        self.position: Vector2 = Vector2(position.x, position.y)
        self.active: bool = True

    def update(self) -> None:
        if not self.active:
            return
        self.position.y += POWERUP_FALL_SPEED
        if self.position.y > WINDOW_HEIGHT + POWERUP_RADIUS:
            self.active = False

    def draw(self) -> None:
        if not self.active:
            return
        draw_circle_v(self.position, POWERUP_RADIUS, ORANGE)
        draw_text("S", int(self.position.x - 4), int(self.position.y - 5), 12, WHITE)


class FloatingPoints:
    """Animated score text that rises and fades out(NOT decimals)"""

    def __init__(self) -> None:
        self.position: Vector2 = Vector2(0, 0)
        self.value: int = 0
        self.alpha: float = 0.0

    def activate(self, position: Vector2, value: int) -> None:
        self.position = Vector2(position.x, position.y)
        self.value = value
        self.alpha = 1.0

    def update(self) -> None:
        """Rise upward and fade out."""
        if self.alpha > 0.0:
            self.position.y -= POINTS_RISE_SPEED
            self.alpha -= POINTS_FADE_SPEED
            if self.alpha < 0.0:
                self.alpha = 0.0

    def draw(self) -> None:
        """Draw the score text if still visible."""
        if self.alpha > 0.0:
            text = f"+{self.value:02d}"
            draw_text(
                text,
                int(self.position.x),
                int(self.position.y),
                20,
                fade(BLUE, self.alpha),
            )


class Game:
    def __init__(self) -> None:
        self.score: int = 0

        # Game States
        self.screen: GameScreen = GameScreen.TITLE
        self.paused: bool = False

        self.player: Player = Player()

        self.max_shoots: int = PLAYER_MAX_SHOOTS
        self.shoots: list[Shoot] = [Shoot() for _ in range(PLAYER_MAX_SHOOTS)]

        self.balls: list[Ball] = []
        self.powerups: list[Powerup] = []

        self.floating_points: list[FloatingPoints] = [
            FloatingPoints() for _ in range(MAX_FLOATING_POINTS)
        ]

        self.charge_frames: int = 0
        self.charging: bool = False

        self.background_music: Music
        self.sound: dict[SoundType, Sound]
        self.bg_texture: Texture | None = None
        self.debug: bool = False

    def startup(self) -> None:
        self.score = 0
        self.screen = GameScreen.PLAYING
        self.paused = False
        self.charge_frames = 0
        self.charging = False
        self.max_shoots = PLAYER_MAX_SHOOTS

        self.player.setup()

        # Background music
        self.background_music = game_musics[MusicType.BACKGROUND]
        play_music_stream(self.background_music)

        self.shoots = [Shoot() for _ in range(self.max_shoots)]
        for s in self.shoots:
            s.setup()

        self.powerups = []

        # Create initial big balls with random positions and non-zero velocities
        self.balls = []
        for _ in range(MAX_BIG_BALLS):
            pos = Vector2(
                random.uniform(BIG_BALL_RADIUS, WINDOW_WIDTH - BIG_BALL_RADIUS),
                random.uniform(BIG_BALL_RADIUS, WINDOW_HEIGHT / 2),
            )
            # Ensure non-zero velocity
            vx = 0.0
            vy = 0.0
            while vx == 0 or vy == 0:
                vx = random.uniform(-BALLS_SPEED, BALLS_SPEED)
                vy = random.uniform(-BALLS_SPEED, BALLS_SPEED)
            speed = Vector2(vx, vy)
            self.balls.append(Ball(BallSize.BIG, pos, speed))

        for fp in self.floating_points:
            fp.alpha = 0.0

    def update(self) -> None:
        if self.screen == GameScreen.TITLE:
            if is_key_pressed(KeyboardKey.KEY_ENTER):
                self.startup()
            return

        # Updating fp before anything b/c there was a bug where fp gets "stuck" on gameover screen.
        for fp in self.floating_points:
            fp.update()

        if self.screen in (GameScreen.GAME_OVER, GameScreen.VICTORY):
            if is_key_pressed(KeyboardKey.KEY_ENTER):
                self.screen = GameScreen.TITLE
            return

        if is_key_pressed(KeyboardKey.KEY_P):
            self.paused = not self.paused

        if is_key_pressed(KeyboardKey.KEY_D):
            self.debug = not self.debug

        # No need to update anything if paused!
        if self.paused:
            return

        if self.background_music:
            update_music_stream(self.background_music)

        self.player.update()

        if is_key_down(KeyboardKey.KEY_SPACE):
            self.charging = True
            self.charge_frames = min(self.charge_frames + 1, CHARGE_MAX)

        if is_key_released(KeyboardKey.KEY_SPACE) and self.charging:
            width = SHOOT_BASE_WIDTH + self.charge_frames * CHARGE_RATE
            width = min(width, SHOOT_MAX_WIDTH)
            for s in self.shoots:
                if not s.active:
                    s.fire(self.player, width)
            self.player.shoot_timer = PLAYER_SHOOT_ANIM_FRAMES
            self.charge_frames = 0
            self.charging = False

        for s in self.shoots:
            s.update()

        for ball in self.balls:
            ball.update()

        for pu in self.powerups:
            pu.update()

        # Check player-powerup collisions
        for pu in self.powerups:
            if pu.active and check_collision_circles(
                self.player.collider_center,
                self.player.collider_radius,
                pu.position,
                POWERUP_RADIUS,
            ):
                pu.active = False
                self.max_shoots += 1
                side_count = self.max_shoots - 1
                if side_count % 2 == 1:
                    angle = -SHOOT_ANGLE_DEG * ((side_count + 1) // 2)
                else:
                    angle = SHOOT_ANGLE_DEG * (side_count // 2)
                self.shoots.append(Shoot(angle_deg=angle))
                play_sound(game_sounds[SoundType.PICKUP])

        # Check player-ball collisions
        for ball in self.balls:
            if ball.active and check_collision_circles(
                self.player.collider_center,
                self.player.collider_radius,
                ball.position,
                ball.radius,
            ):
                self.screen = GameScreen.GAME_OVER
                play_sound(game_sounds[SoundType.LOSE])

                return

        # Check shoot-ball collisions
        self._check_shoot_ball_collisions()

        # Check victory: all balls inactive
        if all(not ball.active for ball in self.balls) and len(self.balls) > 0:
            self.screen = GameScreen.VICTORY
            play_sound(game_sounds[SoundType.WIN])

    # "Private" helper func
    def _check_shoot_ball_collisions(self) -> None:
        for shoot in self.shoots:
            if not shoot.active:
                continue

            for ball in self.balls:
                if not ball.active:
                    continue

                hit_radius = ball.radius + shoot.width / 2
                if check_collision_circle_rec(
                    ball.position,
                    hit_radius,
                    Rectangle(
                        min(shoot.origin.x, shoot.tip.x) - shoot.width / 2,
                        min(shoot.origin.y, shoot.tip.y),
                        abs(shoot.tip.x - shoot.origin.x) + shoot.width,
                        abs(shoot.origin.y - shoot.tip.y),
                    ),
                ):
                    shoot.active = False
                    ball.active = False
                    self.score += ball.points
                    self._spawn_floating_points(ball.position, ball.points)

                    # Split the ball
                    children = ball.split()
                    self.balls.extend(children)

                    if children and random.random() < POWERUP_DROP_CHANCE:
                        self.powerups.append(
                            Powerup(Vector2(ball.position.x, ball.position.y))
                        )

                    break  # One shoot can only hit one ball

    def _spawn_floating_points(self, position: Vector2, value: int) -> None:
        for fp in self.floating_points:
            if fp.alpha <= 0.0:
                fp.activate(position, value)
                return

    def _draw_background(self) -> None:
        if self.bg_texture is None:
            return
        tw = self.bg_texture.width
        th = self.bg_texture.height
        for x in range(0, WINDOW_WIDTH, tw):
            for y in range(0, WINDOW_HEIGHT, th):
                draw_texture(self.bg_texture, x, y, WHITE)

    def _draw_centered(self, text: str, y: int, size: int, color: Color) -> None:
        draw_text(
            text, WINDOW_WIDTH // 2 - measure_text(text, size) // 2, y, size, color
        )

    def draw(self) -> None:
        self._draw_background()

        if self.screen == GameScreen.TITLE:
            self._draw_centered("SPACE PANG", 80, 60, WHITE)
            self._draw_centered("Destroy all meteors to survive!", 160, 20, LIGHTGRAY)
            self._draw_centered(
                "PRESS [ENTER] TO START", WINDOW_HEIGHT // 2 + 20, 20, LIGHTGRAY
            )
            self._draw_centered(
                "PRESS [P] IN-GAME FOR INSTRUCTIONS", WINDOW_HEIGHT // 2 + 50, 16, GRAY
            )
            return

        if self.screen == GameScreen.PLAYING:
            for s in self.shoots:
                s.draw()

            self.player.draw()

            for ball in self.balls:
                ball.draw()

            for pu in self.powerups:
                pu.draw()

            for fp in self.floating_points:
                fp.draw()

            draw_text(f"SCORE: {self.score}", 10, 10, 20, LIGHTGRAY)

            if self.charging:
                charge_pct = self.charge_frames / CHARGE_MAX
                bar_width = int(50 * charge_pct)
                bar_x = int(self.player.position.x - 25)
                bar_y = int(self.player.position.y - self.player.height - 15)
                draw_rectangle(bar_x, bar_y, 50, 6, DARKGRAY)
                draw_rectangle(bar_x, bar_y, bar_width, 6, RED)

            if self.paused:
                draw_rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, fade(BLACK, 0.7))
                self._draw_centered("PAUSED", 30, 40, WHITE)
                instructions = [
                    ("[LEFT / RIGHT]  Move", LIGHTGRAY),
                    ("[SPACE]  Fire", LIGHTGRAY),
                    ("[SPACE hold]  Charge", LIGHTGRAY),
                    ("[P]  Unpause    [D]  Debug", LIGHTGRAY),
                    ("", LIGHTGRAY),
                    ("Pick up [S] powerups for extra side shots!", ORANGE),
                ]
                y = 90
                for line, color in instructions:
                    if line:
                        draw_text(line, 60, y, 18, color)
                    y += 28
                self._draw_centered(
                    "PRESS [P] TO RESUME", WINDOW_HEIGHT - 50, 20, LIGHTGRAY
                )

            if self.debug:
                self._draw_debug()
            return

        if self.screen == GameScreen.VICTORY:
            self._draw_centered("YOU WIN!", 100, 60, GREEN)
            self._draw_centered(f"FINAL SCORE: {self.score}", 180, 30, WHITE)
            self._draw_centered(
                "PRESS [ENTER] FOR TITLE", WINDOW_HEIGHT // 2 + 40, 20, LIGHTGRAY
            )
            return

        if self.screen == GameScreen.GAME_OVER:
            self._draw_centered("GAME OVER", 100, 60, MAROON)
            self._draw_centered(f"SCORE: {self.score}", 180, 30, WHITE)
            self._draw_centered(
                "PRESS [ENTER] FOR TITLE", WINDOW_HEIGHT // 2 + 40, 20, LIGHTGRAY
            )

    def _draw_debug(self) -> None:
        # Player hitbox
        draw_circle_lines_v(
            self.player.collider_center, self.player.collider_radius, GREEN
        )

        # Ball hitboxes and velocity vectors
        for ball in self.balls:
            if not ball.active:
                continue
            draw_circle_lines_v(ball.position, ball.radius, YELLOW)

        # Shoot collision boxes
        for s in self.shoots:
            if not s.active:
                continue
            x1 = min(s.origin.x, s.tip.x) - s.width / 2
            y1 = min(s.origin.y, s.tip.y)
            w = abs(s.tip.x - s.origin.x) + s.width
            h = abs(s.origin.y - s.tip.y)
            draw_rectangle_lines(int(x1), int(y1), int(w), int(h), GREEN)

        # Powerup hitboxes
        for pu in self.powerups:
            if pu.active:
                draw_circle_lines_v(pu.position, POWERUP_RADIUS, ORANGE)

        # Stats overlay
        active_balls = sum(1 for b in self.balls if b.active)
        active_shoots = sum(1 for s in self.shoots if s.active)
        active_powerups = sum(1 for p in self.powerups if p.active)
        stats = [
            f"FPS: {get_fps()}",
            f"Balls: {active_balls}/{len(self.balls)}",
            f"Shoots: {active_shoots}/{len(self.shoots)} (max {self.max_shoots})",
            f"Powerups: {active_powerups}",
            f"Player: ({self.player.position.x:.0f}, {self.player.position.y:.0f})",
            f"State: {self.player.state.name}",
            f"Charge: {self.charge_frames}/{CHARGE_MAX}",
        ]
        for i, line in enumerate(stats):
            draw_text(line, WINDOW_WIDTH - 220, 10 + i * 18, 14, GREEN)

    def load_textures(self) -> None:
        self.player.load_texture()
        for size, path in BALL_SPRITES.items():
            ball_textures[size] = load_texture(path)
        self.bg_texture = load_texture(os.path.join(ASSET_DIR, "star_bg.png"))

    def load_music(self) -> None:
        for music, path in MUSICS.items():
            game_musics[music] = load_music_stream(path)
        for sound, path in SOUNDS.items():
            game_sounds[sound] = load_sound(path)

    def shutdown(self) -> None:
        self.player.unload_texture()

        if self.bg_texture is not None:
            unload_texture(self.bg_texture)

        for texture in ball_textures.values():
            unload_texture(texture)

        for music in game_musics.values():
            unload_music_stream(music)

        for sound in game_sounds.values():
            unload_sound(sound)

        ball_textures.clear()
