"""
Module containing the wordle game.
"""

import random
from itertools import count
from time import sleep
from enum import Enum
import argparse
from functools import reduce
import logging

def game_pause():
    """
    Simple convenience function for standardized calls to interface.
    """
    sleep(Settings.GAME_PAUSE.value)

class Settings(Enum):
    """
    Set global game settings
    """
    GAME_PAUSE = 0.2
    # DATABASE = "xx.db"

class Player:
    """
    Represents a player in the game. Prep for multiplayer hotseating.
    """
    _ids = count(0)

    def __init__(self, name):
        self.guesses = 6
        self.name = name
        self.id = next(self._ids)

class PlayerGroup:
    """
    Represents a group of players, so as to keep track of who is playing.
    """

    def __init__(self, players=[]):
        """
        Initialize class.
        """
        self.players = players

    def add_players(self, players):
        """
        Add a list of players to existing players in game
        """
        self.players.extend(players)

    def setup_singleplayer(self, player_name):
        player = Player(player_name)
        self.add_players([player])
        self.list_players()

    def setup_players(self, player_names):
        """
        Include given names of players into game structure
        """
        players = [ Player(player_name) for player_name in player_names ]
        self.add_players( players )
        self.reset_places()
        self.list_players()

    def list_players(self):
        """
        Prints a list of all players currently playing
        """
        i = 0
        for player in self.players:
            i += 1
            print(f'Player {i}: {player.name}')    # % (i, player.name))

def draw_screen():
    """
    Convenience function to standize calls to display current game information; main interface output
    """
    print("Screen placeholder")
    print()
    print()
    print()
    print("End of holding")


def wordle_game(n_players=1):
    """
    Function that starts and runs game
    """
    # System setup
    log = logging.getLogger(__name__)

    # Game setup
    playergroup = PlayerGroup()
    if n_players == 1:
        playergroup.setup_singleplayer("Karl Johan")
    else:
        pass


    # Main game event loop
    stop_play = False
    while not stop_play:
        try:
            log.debug("Loop initiation")
            draw_screen()
            game_pause()
            playergroup.list_players()
            input("Press return")

        except KeyboardInterrupt:
            print('\nOkay, quitting now.')
            stop_play = True
        except Exception as exc:
            print('Something went wrong.')
            print(repr(exc))
            print('Program will stop.')
            raise exc
            break
