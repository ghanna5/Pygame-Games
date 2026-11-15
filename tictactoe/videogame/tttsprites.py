"""Tic Tac Toe Sprites and Surfaces"""

import pygame

class TTTSurface(pygame.Surface):
    """Class representing an abstract Tic Tac Toe Surface with a bounding rect."""

    def __init__(
        self,
        width: int,
        stroke_color: tuple,
        background_color: tuple,
        name: str = "None",
    ) -> None:
        super().__init__((width, width))
        # TODO: Define the surfaces that you need for your game (or not)
        raise NotImplementedError

class TTTSprite(pygame.sprite.Sprite):
    """Abstract Tic Tac Toe Sprite"""

    def __init__(self) -> None:
        super().__init__()
        # TODO: implment your sprites
        raise NotImplementedError

