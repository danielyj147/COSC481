# idk why but using Ball as a class requires this.
from __future__ import annotations
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
    SHOOT = "shoot"
    LOSE = "lose"
    WIN = "win"
    BACKGROUND = "background"


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

#  Image paths for balls
BALL_SPRITES: dict[BallSize, str] = {
    BallSize.BIG: os.path.join(ASSET_DIR, "ball_big.png"),
    BallSize.MEDIUM: os.path.join(ASSET_DIR, "ball_medium.png"),
    BallSize.SMALL: os.path.join(ASSET_DIR, "ball_small.png"),
}

# Music paths
MUSICS: dict[MusicType, str] = {
    # MusicType.SHOOT: os.path.join(ASSET_DIR, "shoot.mp3"),
    # MusicType.WIN: os.path.join(ASSET_DIR, "win.mp3"),
    # MusicType.LOSE: os.path.join(ASSET_DIR, "lose.wave"),
    MusicType.BACKGROUND: os.path.join(ASSET_DIR, "background.mp3"),
}

ball_textures: dict[BallSize, Texture] = {}
game_musics: dict[MusicType, Music] = {}


class Player:
    def __init__(self) -> None:
        self.position: Vector2 = Vector2(0, 0)
        self.speed: float = PLAYER_SPEED
        self.texture: Texture | None = None
        self.width: float = 0.0
        self.height: float = 0.0

    def load_texture(self) -> None:
        self.texture = load_texture(os.path.join(ASSET_DIR, "player.png"))
        scale = 40.0 / self.texture.height
        self.width = self.texture.width * scale
        self.height = self.texture.height * scale

    def unload_texture(self) -> None:
        if self.texture is not None:
            unload_texture(self.texture)

    def setup(self) -> None:
        self.position = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT)

    # Enables player.collider_center
    @property
    def collider_center(self) -> Vector2:
        return Vector2(self.position.x, self.position.y - self.height / 2)

    @property
    def collider_radius(self) -> float:
        return min(self.width, self.height) / 2

    def update(self) -> None:
        if is_key_down(KeyboardKey.KEY_LEFT):
            self.position.x -= self.speed
        if is_key_down(KeyboardKey.KEY_RIGHT):
            self.position.x += self.speed

        half_w = self.width / 2
        self.position.x = max(half_w, min(self.position.x, WINDOW_WIDTH - half_w))

    def draw(self) -> None:
        if self.texture is None:
            return
        dest = Rectangle(
            self.position.x,
            self.position.y - self.height,
            self.width,
            self.height,
        )
        source = Rectangle(0, 0, self.texture.width, self.texture.height)
        draw_texture_pro(
            self.texture, source, dest, Vector2(self.width / 2, 0), 0.0, WHITE
        )


class Shoot:
    def __init__(self) -> None:
        self.tip: Vector2 = Vector2(0, 0)
        self.origin: Vector2 = Vector2(0, 0)
        self.speed: float = 0.0
        self.life_frames: int = 0
        self.active: bool = False

    def setup(self) -> None:
        self.active = False
        self.life_frames = 0

    def fire(self, player: Player) -> None:
        self.origin = Vector2(player.position.x, player.position.y)
        self.tip = Vector2(player.position.x, player.position.y - player.height)
        self.speed = PLAYER_SPEED
        self.active = True
        self.life_frames = 0

    def update(self) -> None:
        if not self.active:
            return

        self.tip.y -= self.speed
        self.life_frames += 1

        if self.tip.y < 0 or self.life_frames >= SHOOT_LIFETIME:
            self.active = False

    def draw(self) -> None:
        if self.active:
            draw_line(
                int(self.origin.x),
                int(self.origin.y),
                int(self.tip.x),
                int(self.tip.y),
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
        self.game_over: bool = False
        self.victory: bool = False
        self.paused: bool = False
        self.title: Rectangle = Rectangle(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.player: Player = Player()

        self.shoots: list[Shoot] = [Shoot() for _ in range(PLAYER_MAX_SHOOTS)]

        self.balls: list[Ball] = []

        self.floating_points: list[FloatingPoints] = [
            FloatingPoints() for _ in range(MAX_FLOATING_POINTS)
        ]

    def startup(self) -> None:
        self.score = 0
        self.game_over = False
        self.victory = False
        self.paused = False

        self.player.setup()

        # Background music
        self.music = game_musics[MusicType.BACKGROUND]
        play_music_stream(self.music)

        for s in self.shoots:
            s.setup()

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
        # Updating fp before antyhing b/c there was a bug where fp gets "stuck" on gameover screen.
        for fp in self.floating_points:
            fp.update()

        if self.game_over or self.victory:
            if is_key_pressed(KeyboardKey.KEY_ENTER):
                self.startup()
            return

        if is_key_pressed(KeyboardKey.KEY_P):
            self.paused = not self.paused

        # No need to update anything if paused!
        if self.paused:
            return

        if self.music:
            update_music_stream(self.music)

        self.player.update()

        if is_key_pressed(KeyboardKey.KEY_SPACE):
            for s in self.shoots:
                if not s.active:
                    s.fire(self.player)
                    break

        for s in self.shoots:
            s.update()

        for ball in self.balls:
            ball.update()

        # Check player-ball collisions
        for ball in self.balls:
            if ball.active and check_collision_circles(
                self.player.collider_center,
                self.player.collider_radius,
                ball.position,
                ball.radius,
            ):
                self.game_over = True
                return

        # Check shoot-ball collisions
        self._check_shoot_ball_collisions()

        # Check victory: all balls inactive
        if all(not ball.active for ball in self.balls) and len(self.balls) > 0:
            self.victory = True

    # "Private" helper func
    def _check_shoot_ball_collisions(self) -> None:
        for shoot in self.shoots:
            if not shoot.active:
                continue

            for ball in self.balls:
                if not ball.active:
                    continue

                # Check if the ball overlaps the shoot's vertical line
                line_x = shoot.origin.x
                if (
                    ball.position.x - ball.radius
                    <= line_x
                    <= ball.position.x + ball.radius
                    and ball.position.y + ball.radius >= shoot.tip.y
                ):
                    shoot.active = False
                    ball.active = False
                    self.score += ball.points
                    self._spawn_floating_points(ball.position, ball.points)

                    # Split the ball
                    children = ball.split()
                    self.balls.extend(children)
                    break  # One shoot can only hit one ball

    def _spawn_floating_points(self, position: Vector2, value: int) -> None:
        for fp in self.floating_points:
            if fp.alpha <= 0.0:
                fp.activate(position, value)
                return

    def draw(self) -> None:
        if not self.game_over:
            self.player.draw()

            for ball in self.balls:
                ball.draw()

            for s in self.shoots:
                s.draw()

            for fp in self.floating_points:
                fp.draw()

            draw_text(f"SCORE: {self.score}", 10, 10, 20, LIGHTGRAY)

            if self.victory:
                title = "YOU WIN!"
                draw_text(
                    title,
                    WINDOW_WIDTH // 2 - measure_text(title, 60) // 2,
                    100,
                    60,
                    LIGHTGRAY,
                )
                msg = "PRESS [ENTER] TO PLAY AGAIN"
                draw_text(
                    msg,
                    WINDOW_WIDTH // 2 - measure_text(msg, 20) // 2,
                    WINDOW_HEIGHT // 2 - 50,
                    20,
                    LIGHTGRAY,
                )

            if self.paused:
                msg = "GAME PAUSED"
                draw_text(
                    msg,
                    WINDOW_WIDTH // 2 - measure_text(msg, 40) // 2,
                    WINDOW_HEIGHT // 2 - 40,
                    40,
                    LIGHTGRAY,
                )

        else: # Gameover / Title
            draw_rectangle_gradient_ex(
                self.title,
                DARKBLUE,
                RAYWHITE,
                MAROON,
                RAYWHITE,
            )

            msg = "PRESS [ENTER] TO PLAY"
            draw_text(
                msg,
                WINDOW_WIDTH // 2 - measure_text(msg, 20) // 2,
                WINDOW_HEIGHT // 2 - 50,
                20,
                LIGHTGRAY,
            )

    def load_textures(self) -> None:
        self.player.load_texture()
        for size, path in BALL_SPRITES.items():
            ball_textures[size] = load_texture(path)

    def load_music(self) -> None:
        for music, path in MUSICS.items():
            game_musics[music] = load_music_stream(path)

    def shutdown(self) -> None:
        self.player.unload_texture()

        for texture in ball_textures.values():
            unload_texture(texture)

        for music in game_musics.values():
            unload_music_stream(music)

        ball_textures.clear()
