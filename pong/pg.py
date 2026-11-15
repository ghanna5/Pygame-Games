#!/usr/bin/env python3

from videogame.game import PongGame


def main():
    """Start the Pong game."""
    game = PongGame()
    game.run()


if __name__ == '__main__':
    main()