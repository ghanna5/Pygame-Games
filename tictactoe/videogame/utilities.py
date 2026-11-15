"""Useful tools to get the job done."""

from pygame.math import Vector2
from random import randint, uniform

def random_position(max_width: int, max_height: int) -> Vector2:
    """Given a width and height extent, return a random 2D position as a pygame.math.Vector2"""
    return Vector2(
        randint(0, max_width - 1), randint(0, max_height - 1)
    )

def singleton(cls):
    """Make a class a singleton class."""
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance
