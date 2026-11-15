"""Game objects to create PyGame based games."""

import warnings

import pygame
from videogame import assets

def display_info():
    """Print out information about the display driver and video information."""
    print(f'The display is using the "{pygame.display.get_driver()}" driver.')
    print("Video Info:")
    print(pygame.display.Info())


# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html


# pylint: disable=too-few-public-methods
class VideoGame:
    """Base class for creating PyGame games."""

    def __init__(
        self,
        window_width=800,
        window_height=800,
        window_title="My Awesome Game",
    ):
        """Initialize a new game with the given window size and window title."""
        pygame.init()
        self._window_size = (window_width, window_height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size)
        self._title = window_title
        pygame.display.set_caption(self._title)
        self._game_is_over = False
        if not pygame.font:
            warnings.warn("Fonts disabled.", RuntimeWarning)
        if not pygame.mixer:
            warnings.warn("Sound disabled.", RuntimeWarning)
        else:
            pygame.mixer.init()
        self._scene_manager = None

    def run(self):
        """Run the game; the main game loop."""
        raise NotImplementedError

class PongGame(VideoGame):
    """Simple Pong game shell."""

    def __init__(self):
        """Initialize the Pong game window."""
        super().__init__(
            window_width=800,
            window_height=600,
            window_title="Pong",
        )

        paddle_width = 20
        paddle_height = 100
        left_x = 30
        right_x = self._window_size[0] - 30 - paddle_width
        center_y = (self._window_size[1] - paddle_height) // 2

        self._left_paddle = pygame.Rect(
            left_x, center_y, paddle_width, paddle_height
        )
        self._right_paddle = pygame.Rect(
            right_x, center_y, paddle_width, paddle_height
        )

        self._paddle_sound = pygame.mixer.Sound(assets.get("paddle"))

        self._paddle_speed = 7
        self._ai_speed = 5

        ball_size = 20
        ball_x = (self._window_size[0] - ball_size) // 2
        ball_y = (self._window_size[1] - ball_size) // 2
        self._ball = pygame.Rect(ball_x, ball_y, ball_size, ball_size)
        self._ball_dx = 5
        self._ball_dy = 5

        self._left_score = 0
        self._right_score = 0
        self._font = pygame.font.Font(None, 50)

        self._ball_start_x = ball_x
        self._ball_start_y = ball_y

    def _show_title_screen(self):
        waiting = True

        title_font = pygame.font.Font(None, 80)
        text_font = pygame.font.Font(None, 40)

        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._game_is_over = True
                    return
                if event.type == pygame.KEYDOWN:
                    waiting = False

            self._screen.fill((0, 0, 0))

            title_text = title_font.render("PONG", True, (255, 255, 255))
            controls_text = text_font.render("Use ↑ ↓ arrows to move", True, (255, 255, 255))
            start_text = text_font.render("Press any key to start", True, (255, 255, 255))

            self._screen.blit(title_text, (self._window_size[0] // 2 - 100, 150))
            self._screen.blit(controls_text, (self._window_size[0] // 2 - 150, 300))
            self._screen.blit(start_text, (self._window_size[0] // 2 - 150, 350))

            pygame.display.flip()
            self._clock.tick(60)

    def run(self):
        self._show_title_screen()
        while not self._game_is_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._game_is_over = True

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self._left_paddle.top > 0:
                self._left_paddle.y -= self._paddle_speed
            if keys[pygame.K_DOWN] and self._left_paddle.bottom < self._window_size[1]:
                self._left_paddle.y += self._paddle_speed

            if self._ball.centery < self._right_paddle.centery and self._right_paddle.top > 0:
                self._right_paddle.y -= self._ai_speed
            if (
                self._ball.centery > self._right_paddle.centery
                and self._right_paddle.bottom < self._window_size[1]
            ):
                self._right_paddle.y += self._ai_speed

            self._ball.x += self._ball_dx
            self._ball.y += self._ball_dy

            if self._ball.top <= 0 or self._ball.bottom >= self._window_size[1]:
                self._ball_dy *= -1

            if self._ball.colliderect(self._left_paddle):
                self._ball_dx = abs(self._ball_dx)
                self._paddle_sound.play()

            if self._ball.colliderect(self._right_paddle):
                self._ball_dx = -abs(self._ball_dx)
                self._paddle_sound.play()

            if self._ball.right < 0:
                self._right_score += 1
                self._ball.x = self._ball_start_x
                self._ball.y = self._ball_start_y
                self._ball_dx *= -1

            if self._ball.left > self._window_size[0]:
                self._left_score += 1
                self._ball.x = self._ball_start_x
                self._ball.y = self._ball_start_y
                self._ball_dx *= -1

            if self._left_score == 3 or self._right_score == 3:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    self._left_score = 0
                    self._right_score = 0
                    self._ball.x = self._ball_start_x
                    self._ball.y = self._ball_start_y
                    self._ball_dx = 5
                    self._ball_dy = 5

            self._screen.fill((0, 0, 0))
            pygame.draw.rect(self._screen, (255, 255, 255), self._left_paddle)
            pygame.draw.rect(self._screen, (255, 255, 255), self._right_paddle)
            pygame.draw.rect(self._screen, (255, 255, 255), self._ball)

            left_text = self._font.render(str(self._left_score), True, (255, 255, 255))
            right_text = self._font.render(str(self._right_score), True, (255, 255, 255))

            self._screen.blit(left_text, (self._window_size[0] // 4, 20))
            self._screen.blit(right_text, (self._window_size[0] * 3 // 4, 20))

            if self._left_score == 3 or self._right_score == 3:
                text = self._font.render("Press R to restart", True, (255, 255, 255))
                self._screen.blit(text, (self._window_size[0] // 2 - 150, 100))
            
            pygame.display.flip()
            self._clock.tick(60)

        pygame.quit()

# pylint: enable=too-few-public-methods
