"""
Module providing interface functionality
"""

from time import sleep
from wdl_settings import Settings
import logging

# System setup
log = logging.getLogger(__name__)

def game_pause():
    """
    Simple convenience function for standardized calls to interface.
    """
    sleep(Settings.GAME_PAUSE.value)

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
