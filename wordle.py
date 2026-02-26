"""
Module containing the wordle game.
"""

import random
from itertools import count
from time import sleep
from enum import Enum
import logging

# System setup
log = logging.getLogger(__name__)


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

class GameError(Exception):
    """
    Exception raised for unexpected occurences during play,
    such as player input not meeting requirements.
    Most of these can be handled in game - those that cannot
    are re-raised.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

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
        init_dict = {}
        init_dict['letter']  = ''
        init_dict['taken'] = False
        for i in range(5):
            self.answer.append( init_dict )

    def set_answer(self, answer):
        self.answer = []
        for i in range(5):
            self.answer.append({ 'letter': answer[i], 'taken': False })

    def evaluate_guess(self, guess):
        result = []
        for i in range(5):
            if guess[i] == self.answer[i]['letter']:
                self.answer[i]['taken'] = True
                result.append({ 'in_pos': True, 'present': True })
            else:
                result.append({ 'in_pos': False, 'present': False })
        for i in range(5):
            for j in range(5):
                if not self.answer[j]['taken']:
                    if guess[i] == self.answer[j]['letter']:
                        self.answer[j]['taken'] = True
                        result[i]['present'] = True
        return result

class ResultBoard:
    """
    Board for storing and displaying guesses and the results of their evaluation
    """
    def __init__(self):
        self.guesses = []

    def middle(self, string):
        return string[ len(string)//2 ]

    def colour_default(self, letter):
        return f"{ self.middle(letter) }".lower()

    def colour_present(self, letter):
        return f".{ self.middle(letter) }."

    def colour_in_position(self, letter):
        return f"{ self.middle(letter) }".upper()

    def add_evaluation(self, guess, evaluation):
        entry = evaluation
        for i in range(5):
            entry[i]['guessed'] = guess[i]
        self.guesses.append(entry)

    def nb_guesses(self):
        return len(self.guesses)

    def print_results(self):
        for guess in self.guesses:
            line = ""
            for i in range(5):
                guessed_letter = guess[i]['guessed']
                log.debug(f'{guessed_letter} \
                Present: {guess[i]['present']} Positioned: {guess[i]['in_pos']}')
                if guess[i]['in_pos']:
                    guessed_letter = self.colour_in_position(guessed_letter)
                elif guess[i]['present']:
                    guessed_letter = self.colour_present(guessed_letter)
                line = line + guessed_letter
            print(line)

def draw_screen(playergroup, resultboard):
    """
    Convenience function to standize calls to display current game information
    """
    cur_player = playergroup.players[0]
    print(f"Players:")
    playergroup.list_players()
    print(f"Current player: {cur_player.get_name()}")
    resultboard.print_results()
    print()

def wordle_game(n_players=1):
    """
    Function that starts and runs game
    """

    random.seed(9) # Working with fixed randomness while developing

    # Game setup
    playergroup = PlayerGroup()
    valid_guesses = []
    answer = None
    evaluator = Evaluator()
    resultboard = ResultBoard()

    if n_players == 1:
        playergroup.setup_singleplayer("Karl Johan")
    else:
        pass

    with open('wordle-words.txt') as f:
        lines = f.readlines()
        for line in lines:
            log.debug( f'Read line: {repr(line)}' )
            log.debug( f'Appending: {repr(line[0:5])}' )
            valid_guesses.append( line[0:5] )

    # Main game event loop
    stop_play = False
    answer = random.choice(valid_guesses)
    while not stop_play:
        try:
            log.debug("Loop initiation")
            draw_screen(playergroup, resultboard)
            game_pause()
            guess = input("Your guess? ")
            game_pause()

            if not len(guess) == 5:
                raise GameError("Incorrect number of letters")
            if not guess.isalpha():
                raise GameError("Non-letters used while guessing")
            guess = guess.lower()
            if not guess in valid_guesses:
                log.info('invalid guess')
                log.info(f'guess made: { repr(guess) }')
                raise GameError("Invalid word")

            evaluator.set_answer(answer)
            result = evaluator.evaluate_guess(guess)
            resultboard.add_evaluation(guess, result)

        except GameError as ge:
            print(ge)
            print()
            game_pause()
        except KeyboardInterrupt:
            print('\nOkay, quitting now.')
            game_pause()
            stop_play = True
        except Exception as exc:
            print('Something went wrong.')
            print(repr(exc))
            print('Program will stop.')
            game_pause()
            raise exc
