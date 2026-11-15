"""Blackjack Game"""

import pickle
import random
import os

from .card import Card
from .player import BlackJackPlayer, Dealer
from .playerqueue import PlayerQueue


class BlackJackGame:
    """A Blackjack game"""

    def __init__(self):
        """Initialize a Black Jack game object"""
        super().__init__()
        self._is_game_over = False
        num_players = self._get_number_of_players()

        self._players = []
        self._dealer = Dealer()
        self._hands = {}
        self._wagers = {}
        self._balances_file = "balances.pkl"
        self._balances = self._load_balances()
        self._setup_players(num_players)
        self._build_shoe()
        self._cut_reached = False

    def _get_number_of_players(self):
        """Prompt and return the number of players.
           Only return on valid input."""
        not_valid_input = True
        nplayers = 0
        while not_valid_input:
            nplayers = int(input
                           ("\nHow many players would like to play? [1-4] "))
            if 0 < nplayers < 5:
                not_valid_input = False
            else:
                print("Please enter a valid input of a number "
                      "between 1 and 4.")
        return nplayers

    def _rules(self):
        """Black Jack rules in a human readable format"""
        print("\nBlackjack rules:")
        print("You will be asked \"Do you want to hit?\" You must answer y/n")
        print("Dealer hits when total is less than 17 "
              "and stands when it is greater")

    def _load_balances(self):
        """Load the balances"""
        if os.path.exists("balances.pkl"):
            with open("balances.pkl", "rb") as file:
                return pickle.load(file)

        return {}

    def _save_balances(self):
        """Save the balances"""
        with open("balances.pkl", "wb") as file:
            pickle.dump(self._balances, file)

    def _setup_players(self, num_players):
        """Create players with an identifier for each"""
        for i in range(1, num_players + 1):
            name = input(f"Enter Player {i} name: ")
            identifier = input(f"Enter identifier for {name}: ")
            bankroll = self._balances.get(identifier, 100)
            player = BlackJackPlayer(name, identifier, bankroll)
            self._players.append(player)
            self._wagers[player] = 0

        self._hands[self._dealer] = []
        self._wagers[self._dealer] = 0

    def _build_shoe(self):
        """Create and shuffle the decks and place the cut card"""
        self._shoe = []

        for _ in range(8):
            for suit in Card.suits:
                for rank in Card.ranks:
                    self._shoe.append(Card(rank, suit))

        random.shuffle(self._shoe)

        self._cut_index = random.randint(60, 80)
        self._cut_reached = False

    def _initial_deal(self):
        """Deal the first 2 cards to the players
           and the second card to the dealer face down"""
        for contestant in self._players:
            self._deal_card(contestant, face_down=False)

        self._deal_card(self._dealer, face_down=False)

        for contestant in self._players:
            self._deal_card(contestant, face_down=False)

        self._deal_card(self._dealer, face_down=True)

    def _deal_card(self, player, face_down=False):
        """Deal a card from the shoe and check cut card status"""
        card = self._shoe.pop(0)

        if len(self._shoe) <= self._cut_index:
            self._cut_reached = True

        player.hand.append(card)

        if player.is_dealer() and face_down:
            print("\nDealer received a card face down.\n")

        else:
            print(f"\n{player.name} receives: {card}")

    def _prompt_wager(self, player):
        """Prompt the wager"""
        if player.bank_balance <= 0:
            donation = None

            while donation not in ("y", "n"):
                donation = input("You are broke. "
                                 "Accept anonymous donor offer"
                                 " of $100? (y/n): ")

            if donation == "y":
                player.bank_balance = 100

        while True:
            print(f"{player.name}'s balance: {player.bank_balance_string}")
            wager = int(input("Enter wager: "))

            if wager < 1:
                print("Minimum wager is $1.")
            elif wager > player.bank_balance:
                print("Cannot wager more than your balance.")
            else:
                return wager

    def _player_turn(self, player):
        """Loop for player on whether to stand or hit"""
        print(f"Dealer has: {self._dealer.hand[0]}")
        print(f"{player.name} has: {player.hand_string()} "
              f"(value {player.hand_value()})")

        if player.is_blackjack():
            print(f"{player.name} has BLACKJACK!")
            return

        while not player.is_busted() and player.hand_value() != 21:
            question = None
            while question not in ("y", "n"):
                question = input("Do you want to hit? (y/n): ")

            if question == "n":
                break

            self._deal_card(player, face_down=False)
            print(f"{player.name} has value {player.hand_value()}")

        if player.is_busted():
            print(f"{player.name} has busted.")

    def _dealer_turn(self):
        """Dealer reveals the face down card and hits when less than 17"""
        if len(self._dealer.hand) >= 2:
            print(f"Dealer has: {self._dealer.hand[1]}")

        if all(contestants.is_busted() for contestants in self._players):
            print("All players have busted. Dealer stands.")
            return

        while self._dealer.hand_value() < 17:
            self._deal_card(self._dealer, face_down=False)
            print(f"Dealer has value {self._dealer.hand_value()}")

    def _payout(self, wagers):
        """Prints the winner/loser and adds money to balance"""
        dealer_value = self._dealer.hand_value()
        dealer_busted = self._dealer.is_busted()

        print("\n--- Final Results ---")

        for player in self._players:
            bet = wagers[player]
            player_value = player.hand_value()

            if player.is_busted():
                print(f"{player.name} has busted and loses ${bet}.")
                print(f"{player.name}'s "
                      f"total balance is ${player.bank_balance}.")
                continue

            if dealer_busted:
                player.bank_balance += 2 * bet
                print(f"{player.name} wins ${bet * 2} - dealer busted.")
                print(f"{player.name}'s "
                      f"total balance is ${player.bank_balance}.")
                continue

            if player_value == dealer_value:
                player.bank_balance += bet
                print(f"{player.name} pushes. ${bet} returned.")
                print(f"{player.name}'s "
                      f"total balance is ${player.bank_balance}.")
                continue

            if player_value > dealer_value:
                player.bank_balance += 2 * bet
                print(f"{player.name} wins ${bet * 2}.")

            else:
                print(f"{player.name} loses.")

            print(f"{player.name}'s total balance is ${player.bank_balance}.")

    def _play_round(self):
        """Blackjack round is run here."""
        if self._cut_reached:
            print("\nCut card has been reached. Reshuffling shoe.\n")
            self._build_shoe()

        for contestants in self._players:
            contestants.reset_hand()
        self._dealer.reset_hand()

        for contestants in self._players:
            bet = self._prompt_wager(contestants)
            self._wagers[contestants] = bet
            contestants.bank_balance -= bet

        self._initial_deal()

        next_player = PlayerQueue(self._players)

        for contestants in next_player:
            self._player_turn(contestants)

            if contestants == self._players[-1]:
                next_player.stop()

        self._dealer_turn()
        self._payout(self._wagers)

        for contestants in self._players:
            self._balances[contestants.player_id] = contestants.bank_balance

        self._save_balances()

    def run(self):
        """Main function for the Black Jack game"""
        self._rules()
        while not self._is_game_over:
            # Main game loop
            self._play_round()

            answer = None
            while answer not in ("y", "n"):
                answer = input("Do you want to play again? (y/n) ")
                print("")
            self._is_game_over = "n" == answer
        return 0
