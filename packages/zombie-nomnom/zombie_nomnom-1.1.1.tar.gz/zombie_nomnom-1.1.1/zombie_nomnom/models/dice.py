"""
This module contains everything we care about when it comes to the die.
We define a class to contain the faces as well as be able to select one
using the random built-in library.

We can instatation an instance like this
```python
from zombie_nomnom.models.dice import Die, Face

custom_die = Die(faces=[
    Face.BRAIN,
    Face.BRAIN,
    Face.BRAIN,
    Face.SHOTGUN
    Face.SHOTGUN,
    Face.SHOTGUN,
])

# is currently set to None because it was not set.
custom_die.current_face 

# roll and calculate the current face
custom_die.roll()

# will be one of the faces in the in the faces array
custom_die.current_face
```

Most of the time you will want to use a preconfigured recipe
To build your dice which you can use our `create_die` method.

```python
from zombie_nomnom.models.dice import create_die, DieColor

green_die = create_die(DieColor.GREEN)

yellow_die = create_die(DieColor.YELLOW)

red_die = create_die(DieColor.RED)
```

Most of the die in the game are already pre-defined so you can expirement
and use different dice as you make your own custom games.

"""

from enum import Enum
from pydantic import BaseModel, Field, field_validator
import random


class Face(str, Enum):
    """
    Face of the die for the game.

    There are three core ones:
    - BRAIN: Single point scoring face
    - FOOT: Neutral dice that will be re-rolled first before any other die are given.
    - SHOTGUN: Damaging dice where you are limited to only so many before your turn is over.
    """

    BRAIN = "BRAIN"
    """Scoring `Face` worth a single point.
    """
    FOOT = "FOOT"
    """Neutral `Face` that we will reroll.
    """
    SHOTGUN = "SHOTGUN"
    """Damaging `Face` that may end the turn.
    """


class DieFace(BaseModel):
    """
    Represents a custom face on a die. Used to allow us to be able to score extra points or damage on a player when drawn.
    """

    name: str
    """Name of the face."""
    score: int
    """Amount of points a player will gain from face."""
    damage: int
    """Amount of damage a player will take from face."""


class DieColor(str, Enum):
    """
    Names of special core dice in the game.
    There are only three to begin with: RED, YELLOW, GREEN
    """

    RED = "RED"
    """The hardest die to score on in the game with only a single side.
    """
    YELLOW = "YELLOW"
    """The most medium die to score on with an equal number of brain and shot sides.
    """
    GREEN = "GREEN"
    """The most forgiving dice with only a single side that will damage you.
    """


# TODO(Milo): Update this for custom exception on invalid dice.
class Die(BaseModel):
    """
    Represents the die we are rolling in the game.
    This is currently enforced to only support 6 sided dice.
    """

    name: str | None = None
    """
        The plaintext name of the die.
    """
    faces: list[DieFace | Face] = Field(min_length=6, max_length=6)
    """
    faces of the dice. It is currently only allowed to have 6 values.
    """
    current_face: Face | DieFace | None = None
    """
    The currently displayed face of the die. Defaults to None.
    """

    def roll(self) -> Face:
        """Rolls the dice using the `builtins.random` and updates the current_face field.

        **Returns**
        - `Face`: The face that the die is now on.
        """
        self.current_face = random.choice(self.faces)
        return self.current_face


_dice_face_mapping = {
    DieColor.RED: {Face.BRAIN: 1, Face.FOOT: 2, Face.SHOTGUN: 3},
    DieColor.YELLOW: {Face.BRAIN: 2, Face.FOOT: 2, Face.SHOTGUN: 2},
    DieColor.GREEN: {Face.BRAIN: 3, Face.FOOT: 2, Face.SHOTGUN: 1},
}


# TODO(Milo): Update this with custom exception for invalid dice.
def create_die(color: DieColor) -> Die:
    """Factory method to take in a `DieColor` and then create a die based on that.
    Only supports the first three colors defined: `DieColor.RED`, `DieColor.YELLOW`, `DieColor.GREEN`.

    **Parameters**
    - color (`DieColor`): The color of the dice you want the factory to produce.

    `Raises`:
    - `ValueError`: When we are unable to resolve the color to a known recipe.

    `Returns`
    - `Die`: The dice defined by the color given.
    """
    if color not in _dice_face_mapping:
        raise ValueError(f"Unknown Die Color: {color}")

    mapped_color = _dice_face_mapping[color]
    faces = []
    for face, amount in mapped_color.items():
        faces.extend([face] * amount)
    return Die(faces=faces, name=color)
