"""
.. include:: ../README.md
   :start-line: 2
   :end-before: Contribution
"""

from .models.bag import DieBag
from .models.dice import Die, DieColor, Face, create_die
from .engine import Command, ZombieDieGame, Player, RoundState

__version__ = "1.0.0"


__all__ = [
    "app",
    "models",
    "engine",
    "cli",
    "DieBag",
    "Die",
    "DieColor",
    "Face",
    "create_die",
    "ZombieDieGame",
    "Player",
    "RoundState",
    "Command",
]
