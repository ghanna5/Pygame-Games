"""Game objects to create PyGame based games."""

import warnings

import pygame

from videogame.scene import GameScene, TitleScene

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


# pylint: enable=too-few-public-methods

class GalagaGame(VideoGame):

    def __init__(self):
        super().__init__(
            window_width=600,
            window_height=900,
            window_title='Galaga'
        )

    def run(self):
        from videogame.scene import TitleScene, GameScene, GameOverScene, LeaderboardScene
        from videogame import leaderboard
        clock = pygame.time.Clock()

        title = TitleScene(self._screen)
        title.start_scene()
        while title.is_valid():
            for event in pygame.event.get():
                title.process_event(event)
            title.draw()
            clock.tick(60)
        title.end_scene()

        level = 1
        quit_game = False
        while not quit_game:
            game = GameScene(self._screen, level)
            game.start_scene()
            while game.is_valid():
                for event in pygame.event.get():
                    game.process_event(event)
                game.update_scene()
                game.draw()
                clock.tick(60)
            game.end_scene()

            if event.type == pygame.QUIT:
                quit_game = True
                break

            if game.is_game_over():
                game_over = GameOverScene(self._screen, game._score)
                game_over.start_scene()
                while game_over.is_valid():
                    for event in pygame.event.get():
                        game_over.process_event(event)
                    game_over.draw()
                    clock.tick(60)
                game_over.end_scene()
                leaderboard.save('AAA', game._score)
                lb = LeaderboardScene(self._screen)
                lb.start_scene()
                while lb.is_valid():
                    for event in pygame.event.get():
                        lb.process_event(event)
                    lb.draw()
                    clock.tick(60)
                lb.end_scene()
                break
            level += 1

        pygame.quit()