#!/usr/bin/env python3

"""Imports the black jack game and executes the main function."""

import sys
from bjgame import game

if __name__ == "__main__":
    sys.exit(game.BlackJackGame().run())
