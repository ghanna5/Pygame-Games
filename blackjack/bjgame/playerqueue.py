"""A circular queue for players in a card game."""


class PlayerQueue:
    """A circular queue class for game players"""

    def __init__(self, players):
        """Initialize the circular queue given a list of players"""
        self._players = players
        self._counter = 0
        self._should_stop = False

    def __str__(self):
        """Return a comma delimited string of all the players"""
        return ", ".join(map(str, self._players))

    def stop(self):
        """Signal to stop iterating"""
        self._should_stop = True

    def __iter__(self):
        """Return an iterator"""
        return self

    def __next__(self):
        """Next player in the circular queue"""
        if self._should_stop:
            raise StopIteration
        player = self._players[self._counter]
        self._counter = (self._counter + 1) % len(self._players)
        return player
