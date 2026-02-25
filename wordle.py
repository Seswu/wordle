"""
Module containing the wordle game.
"""

import random
from itertools import count
from time import sleep
from enum import Enum
import logging
from functools import filter, map, reduce
from termcolor import colored

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
        """
        Initializes player data
        """
        self.guesses = []
        self.name = name
        self.id = next(self._ids)

    def get_name(self):
        """
        Returns player name
        """
        return self.name

    def get_id(self):
        """
        Returns id number of player
        """
        return self.id

    def add_guess(self, guess=None):
        if guess == None:
            raise Exception("No guess supplied")
        self.guesses.append(guess)

    def print_guesses(self):
        for guess in self.guesses:
            print(guess)

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
        """
        Setup function for the single-player case
        """
        player = Player(player_name)
        self.add_players([player])
        self.list_players()

    def setup_players(self, player_names):
        """
        Include given names of players into game structure
        """
        players = [ Player(player_name) for player_name in player_names ]
        self.add_players( players )
        self.list_players()

    def list_players(self):
        """
        Prints a list of all players currently playing
        """
        i = 0
        for player in self.players:
            i += 1
            print(f'Player {i}: {player.name}')    # % (i, player.name))

class Evaluator:
    """
    Hold the answer and validate guesses against it
    """

    def __init__(self):
        self.answer = []
        for i in range(5):
            self.answer.append({ letter:'', taken: False })

    def set_answer(self, answer):
        self.answer = []
        for i in range(5):
            self.answer.append({ letter: answer[i], taken: False })

    def evaluate_guess(self, guess):
        result = []
        for i in range(5):
            if guess[i] == self.answer[i].letter:
                self.answer[i].taken = True
                self.result.append({ in_pos: True, present = True })
            else:
                self.result.append({ inpos: False, present = False })
        for i in range(5):
            for j in range(5):
                if not self.answer[j].taken:
                    if guess[i] == self.answer[j].letter:
                        self.answer[j].taken = True
                        self.result[i].present = True

class ResultBoard:
    """
    Board for storing and displaying guesses and the results of their evaluation
    """
    def __init__(self):
        self.guesses = []

    def add_evaluation(self, guess, evaluation):
        entry = evaluation
        for i in range(5):
            entry[i].guessed = guess[i]
        guesses.append(entry)

    def nb_guesses(self):
        return len(self.guesses)

    def print_results(self):
        for guess in self.guesses:
            line = ""
            for i in range(5):
                letter = guess[i].letter
                if guess[i].

def draw_screen(playergroup):
    """
    Convenience function to standize calls to display current game information
    """
    cur_player = playergroup.players[0]
    print(f"Players:")
    playergroup.list_players()
    print(f"Current player: {cur_player.get_name()}")
    for guess in cur_player.guesses:
        print(guess)

def wordle_game(n_players=1):
    """
    Function that starts and runs game
    """

    # System setup
    log = logging.getLogger(__name__)
    random.seed(9) # Working with fixed randomness while developing

    # Game setup
    playergroup = PlayerGroup()
    valid_guesses = None
    answer = None
    evaluator = Evaluator()

    if n_players == 1:
        playergroup.setup_singleplayer("Karl Johan")
    else:
        pass

    with open('wordle-words.txt') as f:
        lines = f.readlines()
        valid_guesses = lines

    # Main game event loop
    stop_play = False
    answer = random.choice(valid_guesses)
    while not stop_play:
        try:
            log.debug("Loop initiation")
            draw_screen(playergroup)
            game_pause()
            guess = input("Your guess?")

            if not len(guess == 5):
                raise Exception("Incorrect number of letters")
            if not guess.isalpha():
                raise Exception("Non-letters used while guessing")
            guess = guess.lower()
            if not guess in valid_guesses:
                raise Exception("Invalid word")

            evaluator.set_answer(answer)
            result = evaluator.evaluate_guess(guess)
                pass

        except KeyboardInterrupt:
            print('\nOkay, quitting now.')
            stop_play = True
        except Exception as exc:
            print('Something went wrong.')
            print(repr(exc))
            print('Program will stop.')
            raise exc
            #break
