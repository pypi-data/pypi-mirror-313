"""This module contains the code that relates to how we can turn our game instances into a dictionary as well as
how we can store commands and load them back dynamically 
i.e. if you make custom commands how to load those commands back.

```python
from zombie_nomnom import ZombieDieGame
from zombie_nomnom.engine.serialization import format_to_json_dict

game = ZombieDieGame(players=["Player Uno"])

game_dict = format_to_json_dict(game)

# now you can write it as a yaml or json using whatever you like.
import json
with open('save_file.dat', 'w') as fp:
    json.dump(game_dict, fp) # write it out to the file!!

# at a later date...
from zombie_nomnom.engine.serialization import parse_game_json_dict
with open('save_file.dat', 'r') as fp:
    game_dict = json.load(fp)

# now we can keep playing like nothing happened!!
game = parse_game_json_dict(game_dict)
```

This allows you to control how you want to seralize the data and we store the format
in the TypedDict definitions within the module if you need to have some more information on how it looks.
This means that whatever way you wanna store these models you can and we can load it as long as the dict 
matches our defined structure.
"""

from enum import Enum
import importlib
from typing import Any, TypedDict

from zombie_nomnom.engine.commands import Command
from zombie_nomnom.engine.game import ZombieDieGame
from zombie_nomnom.engine.models import DieRecipe, Player, RoundState
from zombie_nomnom.models.bag import DieBag


class DieDict(TypedDict):
    sides: list[str]
    current_face: str | None


class PlayerDict(TypedDict):
    id: str
    name: str
    total_brains: int
    hand: list[DieDict]


class DieBagDict(TypedDict):
    dice: list[DieDict]
    drawn_dice: list[DieDict] | None


class RoundStateDict(TypedDict):
    diebag: DieBagDict


class CommandDict(TypedDict):
    cls: str
    args: list[Any]
    kwargs: dict[str, Any]


class DieRecipeDict(TypedDict):
    faces: list[str]
    amount: int


class ZombieDieGameDict(TypedDict):
    players: list[PlayerDict]
    commands: list[tuple[CommandDict, RoundStateDict]]
    current_player: int | None
    first_winning_player: int | None
    round: RoundStateDict
    game_over: bool
    score_threshold: int
    bag_function: str | list[DieRecipeDict]


# We may want this to be removed later idk yet?
class KnownFunctions(str, Enum):
    STANDARD = "standard"


def format_command(command: Command) -> CommandDict:
    cmd_type = type(command)
    module = cmd_type.__module__
    qual_name = cmd_type.__qualname__
    return {
        "cls": f"{module}.{qual_name}",
        "args": [],
        # only works if the field on the class matches the param in __init__.py
        "kwargs": command.__dict__,
    }


def parse_command_dict(command: CommandDict) -> Command:
    [*module_path, cls_name] = command.get("cls").split(".")
    module_name = ".".join(module_path)
    module = importlib.import_module(module_name)
    cls = getattr(module, cls_name)
    return cls(*command.get("args"), **command.get("kwargs"))


def format_to_json_dict(game: ZombieDieGame) -> ZombieDieGameDict:
    """Will default any game to be using the standard bag unless given a recipe to create dice.

    **Parameters**
    - game (`ZombieDieGame`): The game to serialize

    **Returns**
    - `ZombieDieGameDict`: The serialized game as a dict that is json serializable
    """
    return {
        "players": [player.model_dump(mode="json") for player in game.players],
        "bag_function": (
            KnownFunctions.STANDARD
            if not game.bag_recipes
            else [recipe.model_dump(mode="json") for recipe in game.bag_recipes]
        ),
        "commands": [
            (format_command(command), state.model_dump(mode="json"))
            for command, state in game.commands
        ],
        "current_player": game.current_player,
        "first_winning_player": game.first_winning_player,
        "game_over": game.game_over,
        "round": game.round.model_dump(mode="json"),
        "score_threshold": game.score_threshold,
    }


UNTRANSFORMED_KEYS = {
    "score_threshold",
    "current_player",
    "first_winning_player",
    "game_over",
}


def parse_game_json_dict(game_data: ZombieDieGameDict) -> ZombieDieGame:
    parameters = {
        key: value for key, value in game_data.items() if key in UNTRANSFORMED_KEYS
    }
    # ones we just need a simple model_validate_on
    parameters["commands"] = [
        (parse_command_dict(command), RoundState.model_validate(state))
        for command, state in game_data["commands"]
    ]
    parameters["players"] = [
        Player.model_validate(player) for player in game_data["players"]
    ]
    parameters["round"] = RoundState.model_validate(game_data.get("round"))

    # special fields to set.
    bag_func = game_data["bag_function"]
    if isinstance(bag_func, str) and bag_func != KnownFunctions.STANDARD:
        # We only allow us to use standard_bag when we load a dict.
        raise ValueError(
            f"Unable to understand the bag_function referenced: {bag_func}"
        )
    # default function for a game is standard anyway so this will just work lol.
    parameters["bag_function"] = None
    if not isinstance(bag_func, str):
        # basically we know these are recipes so load them.
        parameters["bag_recipes"] = [
            DieRecipe.model_validate(raw_recipe) for raw_recipe in bag_func
        ]

    return ZombieDieGame(**parameters)
