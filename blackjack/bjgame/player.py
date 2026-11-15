"""Generic Player class and Black Jack Player, including Dealer"""

from locale import currency, setlocale, LC_ALL


class Player:
    """A generic player class."""

    def __init__(self, name, player_id):
        """Initialize a generic game player"""
        self._name = name
        self._player_id = player_id

    @property
    def name(self):
        """Return the player's name"""
        return self._name

    @property
    def player_id(self):
        """Return the player's ID"""
        return self._player_id

    def __str__(self):
        """Return the player's name"""
        return self._name

    def __repr__(self):
        """Return a pythonic representation of the Player"""
        return (
            f"{self.__class__.__name__}("
            f"name='{self._name}', "
            f"player_id='{self._player_id}')"
        )


class BlackJackPlayer(Player):
    """A black jack player class"""

    def __init__(self, name, player_id, bankroll=100):
        """Initialize a player with a name and a bankroll"""
        # Note to students: uuids are not a good idea here. It's just
        # a place holder.
        super().__init__(name, player_id)
        self._bank_balance = bankroll
        self.hand = []
        setlocale(LC_ALL, "")

    @property
    def bank_balance(self):
        """The player's bank balance"""
        return self._bank_balance

    @bank_balance.setter
    def bank_balance(self, money):
        """Set the player's bank balance to the value money"""
        self._bank_balance = money

    @property
    def bank_balance_string(self):
        """Return the player's bank balance as a formatted currency string"""
        return currency(self._bank_balance, grouping=True)

    def is_dealer(self):
        """Return True if the player is the dealer."""
        return False

    def is_AI(self):  # pylint: disable=invalid-name
        """Return True if the player is a non-human player"""
        return False

    def reset_hand(self):
        """Resets the players hand"""
        self.hand = []

    def hand_value(self):
        """Returns the total value of a players hand"""
        total = 0
        aces = 0

        for card in self.hand:
            rank = card.rank

            if rank in ["Jack", "Queen", "King"]:
                total += 10

            elif rank == "Ace":
                aces += 1
                total += 11

            else:
                total += int(rank)

        while total > 21 and aces > 0:
            total -= 10
            aces -= 1

        return total

    def is_busted(self):
        """Determines whether a player has busted"""
        return self.hand_value() > 21

    def is_blackjack(self):
        """Determines whether a player has blackjack"""
        return len(self.hand) == 2 and self.hand_value() == 21

    def hand_string(self):
        """Returns the players card in a nice string format"""
        return " and ".join(str(card) for card in self.hand)


class Dealer(BlackJackPlayer):
    """The Blackjack dealer as a player with special behaviors"""

    hit_on_value = 17

    def __init__(self):
        """Initialize a new dealer named Dealer"""
        super().__init__("RoboDealer", 0)

    def is_dealer(self):
        """Return True if the player is the dealer."""
        return True

    def is_AI(self):
        """Return True if the player is a non-human player"""
        return True

    # The dealer never should be asked about the bank balance.
    @property
    def bank_balance(self):
        """Not implemented"""
        raise NotImplementedError

    @bank_balance.setter
    def bank_balance(self, money):
        """Not implemented"""
        raise NotImplementedError

    @property
    def bank_balance_string(self):
        """Not implemented"""
        raise NotImplementedError
