"""
Module containing base game settings
"""

import logging
from enum import Enum

# System setup
log = logging.getLogger(__name__)

class Settings(Enum):
    """
    Set global game settings
    """
    GAME_PAUSE = 0.2
    # DATABASE = "xx.db"
