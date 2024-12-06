"""
Module containing the code to run the cli for zombie dice and expose the first implemenation of the game.

If you want to just play a game using click's interface for getting users inputs from the cli 
you may use the `run_game` function.

```python
from zombie_nomnom import ZombieDieGame
from zombie_nomnom.cli import run_game


# Starts a full game from setup to full play by play.
run_game() 

existing_game = ZombieDieGame(players=["Me", "You", "Mr. McGee"])

# Run the cli for an already running/existing game.
run_game(existing_game)

```

If you would like to just use some of the functions we have to render different objects
you can use our print functions such as: `render_players`, `render_turn`, `render_winner`

```python
from zombie_nomnom import ZombieDieGame
from zombie_nomnom.cli import render_players, render_turn, render_winner

existing_game = ZombieDieGame(players=["Billy", "Zabka"])

# Prints out the details of the players of the game and their scores.
render_players(existing_game)

# Prints out the given round information object.
render_turn(existing_game.round)

# Prints out the highest scoring player 
# defaults to the player that went first in the case of a tie.
render_winner(existing_game)

```

This module is primarly used by app and should not be used by other parts of our library.

"""

from typing import Any, Callable, TypeVar
import click

from .engine import DrawDice, Player, RoundState, Score, ZombieDieGame

draw_command = DrawDice()
"""Command used to draw the dice required for a turn."""

score_command = Score()
"""Command used to score a players hand during the game."""


def draw_dice(game: ZombieDieGame):
    """Applys the DrawDice command to the game instance and
    renders the result to the console.

    **Parameters**
    - game (`zombie_nomnom.ZombieDieGame`): instance of the game to apply the draw command too.
    """
    click.echo("Drawing dice...")
    turn = game.process_command(draw_command)
    if not turn.ended:
        click.echo(_format_turn_info(turn))
    else:
        click.echo(f"Ohh no!! {turn.player.name} Has Died(T_T) R.I.P")


def score_hand(game: ZombieDieGame):
    """Applys the score command to a game instance and
    prints out result to the console.

    **Parameters**
    - game (`zombie_nomnom.ZombieDieGame`): game instance you want to score with.
    """
    click.echo("Scoring hand...")
    turn = game.process_command(score_command)
    click.echo(_format_turn_info(turn))


def exit(game: ZombieDieGame):
    """
    Exits the game by marking the game as over for players
    who wish to finish the current game they are playing
    and prints out to the console.

    **Parameters**
    - game (`zombie_nomnom.ZombieDieGame`): game instance you want to end.
    """
    click.echo("Ending game...")
    game.game_over = True


_actions: dict[str, Callable[[ZombieDieGame], None]] = {
    "Exit": exit,
    "Draw dice": draw_dice,
    "Score hand": score_hand,
}


def run_game(game: ZombieDieGame | None = None):
    """
    Main entrypoint for prompting and running the game,
    either an existing instance or creates a new one if not given.
    Will allow users to get prompted and play the game as well as run setup if no game
    is given.

    **Parameters**
    - game (`zombie_nomnom.ZombieDieGame` | `None`, optional): game instance that we want to run. Defaults to None.

    **Returns**
    - `zombie_nomnom.ZombieDieGame`: The instance of the game that has been played.
    """
    game = game or setup_game()
    while not game.game_over:
        # prime game with initial turn.
        render_players(game)
        play_turn(game)
    render_winner(game)
    return game


def render_winner(game: ZombieDieGame):
    """Prints out the current winner of the game instance to the console.

    **Parmeters**
    - game (`zombie_nomnom.ZombieDieGame`): instance that we are looking for the winner on.
    """
    formatted_player = _format_player(game.winner)
    click.echo(f"{formatted_player} Has Won!!")


def play_turn(game: ZombieDieGame):
    """Prompts the user on the console to select action for the turn and prints out the current turn information.

    **Parameters**
    - game (`zombie_nomnom.ZombieDieGame`): game we want to do a turn action on.
    """
    render_turn(game.round)
    select_dict_item(_actions)(game)


def _format_turn_info(turn: RoundState):
    player = turn.player
    bag = turn.bag

    return f"{player.name}, Hand: Brains({len(player.brains)}), Feet({len(player.rerolls)}), Shots({len(player.shots)}), Dice Remaining: {len(bag)}"


def render_turn(turn: RoundState):
    """Prints turn info to the console for a given RoundState.

    **Parameters**
    - turn (`zombie_nomnom.RoundState`): RoundState we are printing.
    """
    click.echo(f"Currently Playing {_format_turn_info(turn)}")


def _format_player(player: Player):
    """
    Formats a player object into a string for our rendering fuctions.

    **Parameters**
    - player (`zombie_nomnom.Player`): player we want to format as string

    **Returns**
    - `str`: Stringified version of player
    """
    return f"{player.name} ({player.total_brains})"


def render_players(game: ZombieDieGame):
    """Prints out the players currently playing in
    game instance. Will put them all on a single line.

    **Parameters**
    - game (`zombie_nomnom.ZombieDieGame`): game instance that we are getting players from.
    """
    players_listed = ", ".join(_format_player(player) for player in game.players)
    click.echo(f"Players: {players_listed}")


class StrippedStr(click.ParamType):
    """Custom `str` parameters that will take in the input from the cli
    and trim any trailing or leading spaces so that I can focus on just the value itself.
    """

    def convert(
        self, value: Any, param: click.Parameter | None, ctx: click.Context | None
    ) -> str:
        """Converts a value from clicks input function into a stripped `str`.
        If given an object will turn the object to a `str` using the `__str__` and then trim the output.

        **Parameters**
        - value (`Any`): Value that was taken by clicks input functions.
        - param (`click.Parameter` | `None`): Optional Parameter form click.
        - ctx (`click.Context` | `None`): Optional context form click.

        **Returns**
        - `str`: str value that has been trimmed.
        """
        if isinstance(value, str):
            return value.strip()
        else:
            return str(value).strip()


def setup_game() -> ZombieDieGame:
    """Runs the setup game cli prompts for users to enter the players in the game.
    This will prompt you for each player in the game then create and return the
    game instance you have with those players.

    **Returns**
    - `zombie_nomnom.ZombieDieGame`: The instance of the game you setup.
    """
    names = prompt_list(
        "Enter Player Name",
        _type=StrippedStr(),
        confirmation_prompt="Add Another Player?",
    )
    # TODO(Milo): Figure out a bunch of game types to play that we can use as templates for the die.
    return ZombieDieGame(
        players=[Player(name=name) for name in names],
    )


TVar = TypeVar("TVar")


def select_dict_item(value: dict[str, TVar]) -> TVar:
    """Prompts the user to select an item from a dictionary and
    then return the value stored at that key. The selection is
    based on an array of options that is orded the same as the
    way they are stored in the keys.

    **Parameters**
    - value (`dict[str, TVar]`): dictionary with values the user will select from.

    **Returns**
    - `TVar`: The value that was selected by the user.
    """
    menu_items = list(value)
    menu = "\n".join(f"{index}) {item}" for index, item in enumerate(menu_items))
    click.echo(menu)
    selected_index = click.prompt(
        f"Select Item (0-{len(menu_items) - 1})",
        type=click.IntRange(0, len(menu_items) - 1),
    )
    return value[menu_items[selected_index]]


def prompt_list(
    prompt: str,
    _type: type,
    confirmation_prompt: str = "Add Another?",
) -> list:
    """Prompts the user to input a list of items using the click library.
    Allows you to define the type of information you want in your list and then return that to you.

    **Parameters**
    - prompt (`str`): Prompt to display to the user.
    - _type (`type`): The type that you wish to get back, can also be a `click.ParamType`
    - confirmation_prompt (`str`, optional): Optional prompt for when the user is asked to add another item. Defaults to "Add Another?".

    **Returns**
    - `list`: Collection of items that the user has given.
    """
    inputs = []
    inputs.append(click.prompt(prompt, type=_type))

    while click.confirm(confirmation_prompt):
        inputs.append(click.prompt(prompt, type=_type))
    return inputs
