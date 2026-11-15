"""Scene objects for making games with PyGame."""

import pygame
from videogame import assets
from videogame import rgbcolors

# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html


class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(self, screen, background_color, screen_flags=None, soundtrack=None):
        """Scene initializer"""
        self._screen = screen
        self._screen_flags = screen_flags
        if not self._screen_flags:
            self._screen_flags = pygame.SCALED
        self._background = pygame.Surface(
            self._screen.get_size(), flags=self._screen_flags
        )
        self._background.fill(background_color)
        self._frame_rate = 60
        self._is_valid = True
        self._soundtrack = soundtrack
        self._render_updates = None

    def draw(self):
        """Draw the scene."""
        self._screen.blit(self._background, (0, 0))

    def process_event(self, event):
        """Process a game event by the scene."""
        # This should be commented out or removed since it generates a lot of noise.
        # print(str(event))
        if event.type == pygame.QUIT:
            print("Good Bye!")
            self._is_valid = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            print("Bye bye!")
            self._is_valid = False

    def is_valid(self):
        """Is the scene valid? A valid scene can be used to play a scene."""
        return self._is_valid

    def render_updates(self):
        """Render all sprite updates."""

    def update_scene(self):
        """Update the scene state."""

    def start_scene(self):
        """Start the scene."""
        if self._soundtrack:
            try:
                pygame.mixer.music.load(self._soundtrack)
                pygame.mixer.music.set_volume(0.05)
            except pygame.error as pygame_error:
                print("\n".join(pygame_error.args))
                raise SystemExit("broken!!") from pygame_error
            pygame.mixer.music.play(loops=-1, fade_ms=500)

    def end_scene(self):
        """End the scene."""
        if self._soundtrack and pygame.mixer.music.get_busy():
            pygame.mixer.music.fadeout(500)
            pygame.mixer.music.stop()

    def frame_rate(self):
        """Return the frame rate the scene desires."""
        return self._frame_rate


class PressEscToExitScene(Scene):
    """Empty scene where it will invalidate when a key is pressed."""

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._is_valid = False

class TicTacToeScene(PressEscToExitScene):
    """Tic Tac Toe Game Scene"""

    def __init__(self, screen, num_circles=1000):
        super().__init__(screen, rgbcolors.black)

        self._board = [None] * 9
        self._human_turn = True
        self._game_over = False
        self._winner = False
        self._width, self._height = screen.get_size()

    def draw(self):
        super().draw()
        cell = self._width // 3

        for i in range(1, 3):
            pygame.draw.line(self._screen, rgbcolors.white,
                            (cell * i, 0), (cell * i, self._height), 3)
            pygame.draw.line(self._screen, rgbcolors.white,
                            (0, cell * i), (self._width, cell * i), 3)

        for i, choice in enumerate(self._board):
            column = i % 3
            row = i // 3
            center_x = column * cell + cell // 2
            center_y = row * cell + cell // 2
            if choice == 'X':
                pygame.draw.line(self._screen, rgbcolors.red,
                    (center_x - 80, center_y - 80), (center_x + 80, center_y + 80), 8)
                pygame.draw.line(self._screen, rgbcolors.red,
                    (center_x + 80, center_y - 80), (center_x - 80, center_y + 80), 8)
            elif choice == 'O':
                pygame.draw.circle(self._screen, rgbcolors.blue, (center_x, center_y), 80, 8)

            if self._game_over:
                font = pygame.font.SysFont(None, 80)
                msg = font.render(f"{self._winner}! Click to restart", True, rgbcolors.yellow)
                self._screen.blit(msg, (
                    self._width // 2 - msg.get_width() // 2,
                    self._height // 2 - msg.get_height() // 2))

    def process_event(self, event):
        super().process_event(event)
        if self._human_turn and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = x // (self._width // 3)
            row = y // (self._height // 3)
            self._board[row * 3 + col] = 'X'
            self._human_turn = False

        if self._game_over and event.type == pygame.MOUSEBUTTONDOWN:
            self._board = [None] * 9
            self._human_turn = True
            self._game_over = False
            self._winner = None

    def check_winner(self):
        wins = [
            [0,1,2], [3,4,5], [6,7,8],
            [0,3,6], [1,4,7], [2,5,8],
            [0,4,8], [2,4,6]
        ]

        for a, b, c in wins:
            if self._board[a] == self._board[b] == self._board[c] == 'X':
                return 'X'
            if self._board[a] == self._board[b] == self._board[c] == 'O':
                return 'O'
        if all(cell is not None for cell in self._board):
            return 'Draw'
        return None

    def update_scene(self):
        self._winner = self.check_winner()
        if self._winner:
            self._game_over = True
            return
        if not self._human_turn:
            self.computer_move()
            self._human_turn = True

    def computer_move(self):
        preferred = [4, 0, 2, 6, 8, 1, 3, 5, 7]
        for i in preferred:
            if self._board[i] is None:
                self._board[i] = 'O'
                break
