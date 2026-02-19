import random
from itertools import count
from time import sleep
from enum import Enum
import argparse
from functools import reduce

def game_pause():
    sleep(Settings.GAME_PAUSE.value)

class Settings(Enum):
    GAME_PAUSE = 0.2
    # DATABASE = "xx.db"

class Player:
    """
    Represents a player in the game. Prep for multiplayer hotseating
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
    _ids = count(0)

    def __init__(self, players=[]):
        self.players = players
        self.id = next(self._ids)

    def add_players(self, players):
        self.players.extend(players)

    def setup_singleplayer(self, player_name):
        player = Player(player_name)
        self.add_players([player])
        self.list_players()

    def setup_players(self, player_names):
        players = [ Player(player_name) for player_name in player_names ]
        self.add_players( players )
        self.reset_places()
        self.list_players()

    def list_players(self):
        i = 0
        for player in self.players:
            i += 1
            print('Player %i: %s' % (i, player.name))

def draw_screen():
    print("Screen placeholder")
    print()
    print()
    print()
    print("End of holding")


# Argument parsing
parser = argparse.ArgumentParser(description='A program for playing wordle.')
parser.add_argument('--players', type=int, default=1)
args = parser.parse_args()


# Game setup
playergroup = PlayerGroup()
playergroup.setup_singleplayer("Karl Johan")


# Main game event loop
stop_play = False
while not stop_play:
    try:
        draw_screen()
        game_pause()
        playergroup.list_players()
        #raise Exception('State out of bounds')
        input("Press return")

    except KeyboardInterrupt as kint:
        print('\nOkay, quitting now.')
        stop_play = True
    except Exception as exc:
        print('Something went wrong.')
        print(repr(exc))
        print('Program will stop.')
        raise exc
        break
