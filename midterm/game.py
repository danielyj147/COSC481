"""PANG game implementation using Pyray.

Reimplements the classic PANG/Buster Bros arcade game where the player
shoots upward to pop bouncing balls that split into smaller ones.
"""

from __future__ import annotations

import os
import random
from enum import Enum

from pyray import *  # pyright: ignore[reportWildcardImportFromLibrary]

from settings import *  # noqa: F403

# Resolve asset paths relative to this file, not the working directory
_ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")


class BallSize(Enum):
    """Represents the three tiers of ball sizes."""

    BIG = "big"
    MEDIUM = "medium"
    SMALL = "small"


# Properties per size: (radius, points, bounce_speed)
BALL_PROPERTIES: dict[BallSize, tuple[float, int, float]] = {
    BallSize.BIG: (BIG_BALL_RADIUS, BIG_BALL_POINTS, BIG_BALL_BOUNCE_SPEED),
    BallSize.MEDIUM: (MEDIUM_BALL_RADIUS, MEDIUM_BALL_POINTS, MEDIUM_BALL_BOUNCE_SPEED),
    BallSize.SMALL: (SMALL_BALL_RADIUS, SMALL_BALL_POINTS, SMALL_BALL_BOUNCE_SPEED),
}


# What a ball splits into when shot (None = doesn't split)
BALL_SPLIT: dict[BallSize, BallSize | None] = {
    BallSize.BIG: BallSize.MEDIUM,
    BallSize.MEDIUM: BallSize.SMALL,
    BallSize.SMALL: None,
}

# Sprite paths per ball tier
BALL_SPRITES: dict[BallSize, str] = {
    BallSize.BIG: os.path.join(_ASSET_DIR, "ball_big.png"),
    BallSize.MEDIUM: os.path.join(_ASSET_DIR, "ball_medium.png"),
    BallSize.SMALL: os.path.join(_ASSET_DIR, "ball_small.png"),
}

# Loaded textures (populated by Game.load_textures)
ball_textures: dict[BallSize, Texture] = {}


class Player:
    """The player character that moves left/right and fires upward."""

    def __init__(self) -> None:
        self.position: Vector2 = Vector2(0, 0)
        self.speed: float = PLAYER_SPEED
        self.texture: Texture | None = None
        self.width: float = 0.0
        self.height: float = 0.0

    def load_texture(self) -> None:
        """Load the player sprite from assets/player.png."""
        self.texture = load_texture(os.path.join(_ASSET_DIR, "player.png"))
        # Scale sprite to a reasonable game size (roughly 40px tall)
        scale = 40.0 / self.texture.height
        self.width = self.texture.width * scale
        self.height = self.texture.height * scale

    def unload_texture(self) -> None:
        """Unload the player sprite texture."""
        if self.texture is not None:
            unload_texture(self.texture)

    def init(self) -> None:
        """Reset player to starting position (bottom-center)."""
        self.position = Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT)

    @property
    def collider_center(self) -> Vector2:
        """Center of the player's hitbox (middle of the sprite)."""
        return Vector2(self.position.x, self.position.y - self.height / 2)

    @property
    def collider_radius(self) -> float:
        """Collision radius based on sprite size."""
        return min(self.width, self.height) / 2

    def update(self) -> None:
        """Handle left/right movement, clamped to screen."""
        if is_key_down(KeyboardKey.KEY_LEFT):
            self.position.x -= self.speed
        if is_key_down(KeyboardKey.KEY_RIGHT):
            self.position.x += self.speed

        half_w = self.width / 2
        self.position.x = max(half_w, min(self.position.x, WINDOW_WIDTH - half_w))

    def draw(self) -> None:
        """Draw the player sprite centered at position."""
        if self.texture is None:
            return
        dest = Rectangle(
            self.position.x, self.position.y - self.height,
            self.width, self.height,
        )
        source = Rectangle(0, 0, self.texture.width, self.texture.height)
        draw_texture_pro(self.texture, source, dest, Vector2(self.width / 2, 0), 0.0, WHITE)


class Shoot:
    """A vertical line shot fired upward from the player."""

    def __init__(self) -> None:
        self.tip: Vector2 = Vector2(0, 0)       # top end (moves up)
        self.origin: Vector2 = Vector2(0, 0)     # bottom end (stays fixed)
        self.speed: float = 0.0
        self.life_frames: int = 0
        self.active: bool = False

    def init(self) -> None:
        """Reset to inactive."""
        self.active = False
        self.life_frames = 0

    def fire(self, player: Player) -> None:
        """Fire from the player's top."""
        self.origin = Vector2(player.position.x, player.position.y)
        self.tip = Vector2(player.position.x, player.position.y - player.height)
        self.speed = PLAYER_SPEED
        self.active = True
        self.life_frames = 0

    def update(self) -> None:
        """Move tip upward; deactivate if off-screen or expired."""
        if not self.active:
            return

        self.tip.y -= self.speed
        self.life_frames += 1

        if self.tip.y < 0 or self.life_frames >= SHOOT_LIFETIME:
            self.active = False

    def draw(self) -> None:
        """Draw a red vertical line from origin to tip."""
        if self.active:
            draw_line(
                int(self.origin.x), int(self.origin.y),
                int(self.tip.x), int(self.tip.y),
                RED,
            )


class Ball:
    """A bouncing ball that splits into smaller balls when shot.

    Balls obey gravity and bounce off walls and the floor.
    """

    def __init__(self, size: BallSize, position: Vector2, speed: Vector2,
                 active: bool = True) -> None:
        radius, points, bounce_speed = BALL_PROPERTIES[size]
        self.size: BallSize = size
        self.position: Vector2 = position
        self.speed: Vector2 = speed
        self.radius: float = radius
        self.points: int = points
        self.bounce_speed: float = bounce_speed
        self.active: bool = active

    def update(self) -> None:
        """Apply movement, gravity, and wall bouncing."""
        if not self.active:
            return

        self.position.x += self.speed.x
        self.position.y += self.speed.y

        # Horizontal wall bounce
        if (self.position.x + self.radius >= WINDOW_WIDTH or
                self.position.x - self.radius <= 0):
            self.speed.x *= -1

        # Ceiling bounce
        if self.position.y - self.radius <= 0:
            self.speed.y = abs(self.speed.y)

        # Floor bounce — use fixed velocity for consistent bounce height
        if self.position.y + self.radius >= WINDOW_HEIGHT:
            self.speed.y = self.bounce_speed
            self.position.y = WINDOW_HEIGHT - self.radius

        # Gravity
        self.speed.y += GRAVITY

    def draw(self) -> None:
        """Draw the ball sprite centered at position."""
        texture = ball_textures.get(self.size)
        if texture is None:
            # Fallback to circle if texture not loaded
            color = DARKGRAY if self.active else fade(LIGHTGRAY, 0.3)
            draw_circle_v(self.position, self.radius, color)
            return

        tint = WHITE if self.active else fade(WHITE, 0.3)
        diameter = self.radius * 2
        source = Rectangle(0, 0, texture.width, texture.height)
        dest = Rectangle(self.position.x, self.position.y, diameter, diameter)
        # Draw centered on position
        draw_texture_pro(texture, source, dest, Vector2(self.radius, self.radius), 0.0, tint)

    def split(self) -> list[Ball]:
        """Split this ball into two smaller balls, or return empty if smallest.

        Returns:
            List of 0 or 2 child balls.
        """
        child_size = BALL_SPLIT[self.size]
        if child_size is None:
            return []

        return [
            Ball(
                child_size,
                Vector2(self.position.x, self.position.y),
                Vector2(-BALLS_SPEED, BALLS_SPEED if child_size == BallSize.MEDIUM else -BALLS_SPEED),
            ),
            Ball(
                child_size,
                Vector2(self.position.x, self.position.y),
                Vector2(BALLS_SPEED, BALLS_SPEED if child_size == BallSize.MEDIUM else -BALLS_SPEED),
            ),
        ]


class FloatingPoints:
    """Animated score text that rises and fades out."""

    def __init__(self) -> None:
        self.position: Vector2 = Vector2(0, 0)
        self.value: int = 0
        self.alpha: float = 0.0

    def activate(self, position: Vector2, value: int) -> None:
        """Start displaying at the given position."""
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
            draw_text(text, int(self.position.x), int(self.position.y), 20,
                      fade(BLUE, self.alpha))


class Game:
    """Main game controller managing all entities and game state.

    Handles initialization, input, physics, collisions, scoring,
    and rendering each frame.
    """

    def __init__(self) -> None:
        self.score: int = 0
        self.game_over: bool = False
        self.victory: bool = False
        self.paused: bool = False
        self.player: Player = Player()
        self.shoots: list[Shoot] = [Shoot() for _ in range(PLAYER_MAX_SHOOTS)]
        self.balls: list[Ball] = []
        self.floating_points: list[FloatingPoints] = [
            FloatingPoints() for _ in range(MAX_FLOATING_POINTS)
        ]

    def startup(self) -> None:
        """Initialize / reset all game state."""
        self.score = 0
        self.game_over = False
        self.victory = False
        self.paused = False

        self.player.init()

        for s in self.shoots:
            s.init()

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
        """Update one frame of game logic."""
        # Always update floating points (even during game over)
        for fp in self.floating_points:
            fp.update()

        if self.game_over or self.victory:
            if is_key_pressed(KeyboardKey.KEY_ENTER):
                self.startup()
            return

        if is_key_pressed(KeyboardKey.KEY_P):
            self.paused = not self.paused

        if self.paused:
            return

        # Player
        self.player.update()

        # Shooting
        if is_key_pressed(KeyboardKey.KEY_SPACE):
            for s in self.shoots:
                if not s.active:
                    s.fire(self.player)
                    break

        # Update shoots
        for s in self.shoots:
            s.update()

        # Update balls
        for ball in self.balls:
            ball.update()

        # Check player-ball collisions
        for ball in self.balls:
            if ball.active and check_collision_circles(
                self.player.collider_center, self.player.collider_radius,
                ball.position, ball.radius,
            ):
                self.game_over = True
                return

        # Check shoot-ball collisions
        self._check_shoot_ball_collisions()

        # Check victory: all balls inactive
        if all(not ball.active for ball in self.balls) and len(self.balls) > 0:
            self.victory = True

    def _check_shoot_ball_collisions(self) -> None:
        """Detect collisions between active shoots and active balls.

        When a ball is hit, it deactivates, scores points, spawns child
        balls (if not the smallest size), and shows floating score text.
        """
        for shoot in self.shoots:
            if not shoot.active:
                continue

            for ball in self.balls:
                if not ball.active:
                    continue

                # Check if the ball overlaps the shoot's vertical line
                line_x = shoot.origin.x
                if (ball.position.x - ball.radius <= line_x <= ball.position.x + ball.radius
                        and ball.position.y + ball.radius >= shoot.tip.y):
                    shoot.active = False
                    ball.active = False
                    self.score += ball.points
                    self._spawn_floating_points(ball.position, ball.points)

                    # Split the ball
                    children = ball.split()
                    self.balls.extend(children)
                    break  # One shoot can only hit one ball

    def _spawn_floating_points(self, position: Vector2, value: int) -> None:
        """Activate the first available floating points slot."""
        for fp in self.floating_points:
            if fp.alpha <= 0.0:
                fp.activate(position, value)
                return

    def draw(self) -> None:
        """Render the current frame."""
        if not self.game_over:
            self.player.draw()

            for ball in self.balls:
                ball.draw()

            for s in self.shoots:
                s.draw()

            for fp in self.floating_points:
                fp.draw()

            # Score UI
            draw_text(f"SCORE: {self.score}", 10, 10, 20, LIGHTGRAY)

            if self.victory:
                title = "YOU WIN!"
                draw_text(title,
                          WINDOW_WIDTH // 2 - measure_text(title, 60) // 2,
                          100, 60, LIGHTGRAY)
                msg = "PRESS [ENTER] TO PLAY AGAIN"
                draw_text(msg,
                          WINDOW_WIDTH // 2 - measure_text(msg, 20) // 2,
                          WINDOW_HEIGHT // 2 - 50, 20, LIGHTGRAY)

            if self.paused:
                msg = "GAME PAUSED"
                draw_text(msg,
                          WINDOW_WIDTH // 2 - measure_text(msg, 40) // 2,
                          WINDOW_HEIGHT // 2 - 40, 40, LIGHTGRAY)
        else:
            msg = "PRESS [ENTER] TO PLAY AGAIN"
            draw_text(msg,
                      WINDOW_WIDTH // 2 - measure_text(msg, 20) // 2,
                      WINDOW_HEIGHT // 2 - 50, 20, LIGHTGRAY)

    def load_textures(self) -> None:
        """Load all game textures (call after init_window)."""
        self.player.load_texture()
        for size, path in BALL_SPRITES.items():
            ball_textures[size] = load_texture(path)

    def shutdown(self) -> None:
        """Clean up game resources."""
        self.player.unload_texture()
        for texture in ball_textures.values():
            unload_texture(texture)
        ball_textures.clear()
