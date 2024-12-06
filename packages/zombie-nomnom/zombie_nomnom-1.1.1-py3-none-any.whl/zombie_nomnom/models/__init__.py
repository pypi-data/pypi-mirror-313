"""
Models
===

We contain the following models for the core of the game.

[`DieBag` information found here](models/bag#DieBag)
```python
from zombie_nomnom.models import DieBag, Die, DieColor, Face


# The core of the models is the bag which is our custom 
# collection that contains the code to select dice from the bag.
# It allows us to manage 
bag = DieBag(
    dice=[
        Die(
            faces=[
                Face.BRAIN,
                Face.BRAIN,
                Face.BRAIN,
                Face.SHOTGUN,
                Face.SHOTGUN,
                Face.SHOTGUN
            ]
        )
    ]
)
```

[`Die` information found here](models/dice#Die)
```python
from zombie_nomnom.models import Die


# Model to keep track of and roll the die we have 
# defined in the game.

custom_die = Die(
    faces=[
        Face.BRAIN,
        Face.BRAIN,
        Face.BRAIN,
        Face.SHOTGUN,
        Face.SHOTGUN,
        Face.SHOTGUN
    ]
)

```
"""

from .bag import DieBag
from .dice import Die, DieColor, Face

__all__ = [
    "DieBag",
    "Die",
    "DieColor",
    "Face",
    "bag",
    "dice",
]
