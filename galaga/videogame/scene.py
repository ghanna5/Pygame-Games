"""Scene objects for making games with PyGame."""

import pygame

from videogame import assets

# If you're interested in using abstract base classes, feel free to rewrite
# these classes.
# For more information about Python Abstract Base classes, see
# https://docs.python.org/3.8/library/abc.html


class Scene:
    """Base class for making PyGame Scenes."""

    def __init__(
        self, screen, background_color, screen_flags=None, soundtrack=None
    ):
        """Scene initializer"""
        self._screen = screen
        if not screen_flags:
            screen_flags = pygame.SCALED
        self._background = pygame.Surface(
            self._screen.get_size(), flags=screen_flags
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


class PressAnyKeyToExitScene(Scene):
    """Empty scene where it will invalidate when a key is pressed."""

    def process_event(self, event):
        """Process game events."""
        super().process_event(event)
        if event.type == pygame.KEYDOWN:
            self._is_valid = False

class TitleScene(PressAnyKeyToExitScene):
    """Title screen scene."""

    def __init__(self, screen):
        super().__init__(screen, (0, 0, 0))
        self._font = pygame.font.SysFont('Arial', 60)
        self._sub_font = pygame.font.SysFont('Arial', 24)

    def draw(self):
        super().draw()
        title = self._font.render('Galaga', True, (255, 255, 0))
        sub = self._sub_font.render('Press any key to start', True, (255, 255, 255))
        self._screen.blit(title, (300 - title.get_width() // 2, 350))
        self._screen.blit(sub, (300 - sub.get_width() // 2, 440))
        pygame.display.flip()

class Player(pygame.sprite.Sprite):

    def __init__(self, screen_width, screen_height):
        super().__init__()
        from videogame import assets
        self.image = pygame.image.load(assets.get('player')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 40))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self._speed = 5
        self._screen_width = screen_width

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self._speed
        if keys[pygame.K_RIGHT] and self.rect.right < self._screen_width:
            self.rect.x += self._speed

class GameScene(Scene):

    def __init__(self, screen, level=1):
        from videogame import assets
        self._shoot_sound = pygame.mixer.Sound(assets.get('player_shoot'))
        self._enemy_die_sound = pygame.mixer.Sound(assets.get('enemy_die'))
        self._player_die_sound = pygame.mixer.Sound(assets.get('player_die'))
        super().__init__(screen, (0, 0, 0), soundtrack=assets.get('soundtrack'))
        self_level = level
        self._player = Player(screen.get_width(), screen.get_height())
        self._all_sprites = pygame.sprite.Group()
        self._enemies = pygame.sprite.Group()
        self._bullets = pygame.sprite.Group()
        self._enemy_bullets = pygame.sprite.Group()
        self._all_sprites.add(self._player)
        self._spawn_enemies()
        self._score = 0
        self._font = pygame.font.SysFont('Arial', 24)
        self._lives = 3
        self._enemy_shoot_timer = 0
        self._dive_timer = 0

    def _spawn_enemies(self):
        rows = 4
        cols = 8
        x_start = 60
        y_start = 80
        x_gap = 65
        y_gap = 55
        for row in range(rows):
            for col in range(cols):
                x = x_start + col * x_gap
                y = y_start + row * y_gap
                enemy = Enemy(x, y)
                self._all_sprites.add(enemy)
                self._enemies.add(enemy)

    def draw(self):
        super().draw()
        self._all_sprites.draw(self._screen)
        score_text = self._font.render(f'Score: {self._score}', True, (255, 255, 255))
        lives_text = self._font.render(f'Lives: {self._lives}', True, (255, 255, 255))
        self._screen.blit(score_text, (10, 10))
        self._screen.blit(lives_text, (480, 10))
        pygame.display.flip()

    def update_scene(self):
        self._all_sprites.update()
        hits = pygame.sprite.groupcollide(self._enemies, self._bullets, True, True)
        for _ in hits:
            self._score += 50
            self._enemy_die_sound.play()
        self._enemy_shoot_timer += 1
        if self._enemy_shoot_timer >= 90 and len(self._enemies) > 0:
            self._enemy_shoot_timer = 0
            import random
            shooter = random.choice(self._enemies.sprites())
            bullet = Bullet(shooter.rect.centerx, shooter.rect.bottom, 1)
            self._all_sprites.add(bullet)
            self._enemy_bullets.add(bullet)

        self._dive_timer += 1
        if self._dive_timer >= 180 and len(self._enemies) > 0:
            self._dive_timer = 0
            import random
            diver = random.choice(self._enemies.sprites())
            diver.start_dive()
        
        if pygame.sprite.spritecollide(self._player, self._enemy_bullets, True):
            self._lives -= 1
            self._player_die_sound.play()
            if self._lives <= 0:
                self._is_valid = False
        
        if pygame.sprite.spritecollide(self._player, self._enemies, True):
            self._lives -= 1
            if self._lives <= 0:
                self._is_valid = False
        
        if len(self._enemies) == 0:
            self._is_valid = False

    def process_event(self, event):
        super().process_event(event)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(self._player.rect.centerx, self._player.rect.top, -1)
            self._bullets.add(bullet)
            self._all_sprites.add(bullet)
            self._shoot_sound.play()
        if event.type == pygame.QUIT:
            self._lives = 0
            self._is_valid = False
    
    def is_game_over(self):
        return self._lives <= 0

class Enemy(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()
        from videogame import assets
        self.image = pygame.image.load(assets.get('enemy')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self._original_y = y
        self._is_diving = False
        self._dive_speed = 3

    def update(self):
        if self._is_diving:
            self.rect.y += self._dive_speed
            if self.rect.top > 900:
                self._is_diving = False
                self.rect.y = self._original_y

    def start_dive(self):
        self._original_y = self.rect.y
        self._is_diving = True

    def is_diving(self):
        return self._is_diving
    
class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 15))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self._speed = 8
        self._direction = direction

    def update(self):
        self.rect.y += self._speed * self._direction
        if self.rect.bottom < 0 or self.rect.top > 900:
            self.kill()

class GameOverScene(PressAnyKeyToExitScene):

    def __init__(self, screen, score):
        super().__init__(screen, (0, 0, 0))
        self._score = score
        self._font = pygame.font.SysFont('Arial', 60)
        self._sub_font = pygame.font.SysFont('Arial', 24)

    def draw(self):
        super().draw()
        game_over = self._font.render('Game Over', True, (255, 0, 0))
        score = self._sub_font.render(f'Final Score: {self._score}', True, (255, 255, 255))
        press = self._sub_font.render('Press any key to continue', True, (255, 255, 255))
        self._screen.blit(game_over, (300 - game_over.get_width() // 2, 350))
        self._screen.blit(score, (300 - score.get_width() // 2, 440))
        self._screen.blit(press, (300 - press.get_width() // 2, 480))
        pygame.display.flip()

class LeaderboardScene(PressAnyKeyToExitScene):

    def __init__(self, screen):
        super().__init__(screen, (0, 0, 0))
        self._font = pygame.font.SysFont('Arial', 48)
        self._sub_font = pygame.font.SysFont('Arial', 24)
        from videogame import leaderboard
        self._scores = leaderboard.load()

    def draw(self):
        super().draw()
        title = self._font.render('Leaderboard', True, (255, 255, 0))
        self._screen.blit(title, (300 - title.get_width() // 2, 200))
        for i, entry in enumerate(self._scores):
            text = self._sub_font.render(f"{i + 1}. {entry['name']} - {entry['score']}", True, (255, 255, 255))
            self._screen.blit(text, (300 - text.get_width() // 2, 300 + i * 40))
        press = self._sub_font.render('Press any key to return to title', True, (255, 255, 255))
        self._screen.blit(press, (300 - press.get_width() // 2, 500))
        pygame.display.flip()