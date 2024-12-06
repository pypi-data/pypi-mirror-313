"""
Module that contains the code related to the dice bag and how we draw and manage it.
This allows us to create custom sets per game of zombiedice by creating a method that creates `DieBag` objects.

For example of making your own diebag.
```python
from zombie_nomnom import DieBag, Die, Face

bag = DieBag(
    dice=[
        Die(faces=[Face.Brain] * 6), # Dice with only brains
        Die(faces=[Face.Brain] * 6),
        Die(faces=[Face.Brain] * 6),
        Die(faces=[Face.Brain] * 6),
    ]
)

# every bag action creates a new bag so you can store both 
new_bag = bag.draw_dice(1)

# drawing dice adds the die to your drawn_dice field
new_bag.drawn_dice

# You can check the amount of the dice in your bag using len()
len(new_bag) # 3 dice since this is the bag after you drew one.

# Clears the dice in the drawn_dice field and sets it to empty array
newer_bag = new_bag.clear_drawn_dice()

newer_bag.drawn_dice # is not empty array

# Bag also supports bool check which returns true if there are dice in the bag
bool(new_bag) # True since there are 3 dice

# We can also check if the bag is empty
new_bag.is_empty # False since there are 3 dice in the bag

# we can even add dice on the fly
bag.add_dice([Die(faces=[Face.Brain] * 6)])

len(bag) # will now be 5 since there are 5 dice.
```

If you don't want to bother making dice manually you can create our standard 13 dice bag:
```python
from zombie_nomnom import DieBag

# New bag containing: 6 Green Dice, 4 Yellow Dice, 3 Red Dice.
standard = DieBag.standard_bag()

len(standard) # will be 13 
```
"""

from copy import deepcopy
import random
from typing import Iterable

from pydantic import BaseModel

from .dice import Die, create_die, DieColor


class DieBag(BaseModel):
    """DieBag that contains and manages the dice in the game."""

    dice: list[Die]
    """The collection of dice in the bag"""
    drawn_dice: list[Die] = []
    """The dice the bag last drew"""

    @property
    def is_empty(self) -> bool:
        """The property that represents when the bag is considered empty.

        **Returns**
        - bool: True when bag is empty
        """
        return len(self) == 0

    def clear_drawn_dice(self) -> "DieBag":
        """Creates a new `DieBag` where its `drawn_dice` field is empty.

        **Returns**
        - `DieBag`: The new instance of DieBag without any drawn_dice.
        """
        return DieBag(
            dice=self.dice,
        )

    def add_dice(self, dice: Iterable[Die]) -> "DieBag":
        """Creates a new Diebag where you added the dice in this bag with
        the dice from the caller.

        **Parameters**
        - dice (`Iterable[zombie_nomnom.Die]`): Dice we are adding to the new bag.

        **Returns**
        - `DieBag`: The new bag of dice with both dice.
        """
        new_dice = [
            *(deepcopy(die) for die in self.dice),
            *(deepcopy(die) for die in dice),
        ]
        return DieBag(dice=new_dice, drawn_dice=[])

    def draw_dice(self, amount: int = 1) -> "DieBag":
        """Creates a new bag where we select dice from this one randomly
        and then set both the dice_drawn, and dice to a subset of the dice
        minus the dice we drew.

        **Parameters**
        - amount (`int`, optional): the total amount of dice we are getting from the bag. Defaults to 1.

        **Raises**
        - `ValueError`: Raised when there are not enough dice to be able to draw from the bag.

        **Returns**
            `DieBag`: The new bag with the dice_drawn set to the dice we drew from the bag.
        """
        if amount < 0 or amount > len(self):
            raise ValueError("The die bag does not have enough dice.")

        total = len(self)
        selected_dice = set()
        while len(selected_dice) < amount:
            selected_dice.add(random.randint(0, total - 1))
        return DieBag(
            dice=[
                die for index, die in enumerate(self.dice) if index not in selected_dice
            ],
            drawn_dice=[self.dice[index] for index in selected_dice],
        )

    def __len__(self):
        return len(self.dice)

    def __bool__(self):
        return len(self) > 0

    @classmethod
    def standard_bag(cls) -> "DieBag":
        """Creates a bag using the standard rules format.

        The bag will contain 6 GREEN dice, 4 YELLOW dice, and 3 RED dice.

        **Returns**
        - `DieBag`: the standard diebag that was created.
        """
        return cls(
            dice=[
                *(create_die(DieColor.GREEN) for _ in range(6)),
                *(create_die(DieColor.YELLOW) for _ in range(4)),
                *(create_die(DieColor.RED) for _ in range(3)),
            ],
        )
