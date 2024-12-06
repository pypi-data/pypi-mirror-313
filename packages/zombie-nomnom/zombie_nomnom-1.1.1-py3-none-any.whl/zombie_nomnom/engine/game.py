from copy import deepcopy
import operator
from typing import Callable


from zombie_nomnom.models import DieBag
from zombie_nomnom.models.dice import Die

from .models import DieRecipe, Player, RoundState
from .commands import Command


def bag_from_recipes(dice_recipes: list[DieRecipe]):
    """Function that can be used to create a bag_function from a list of dice recipes.

    **Parameters**
    - dice_recipes (`list[DieRecipe]`): the list of recipes to create the dice in the bag.

    **Returns**
    - `Callable[[], DieBag]`: The new closure that creates bags by referencing the dice_recipes array.

    **Raises**
    - `ValueError`: When give no recipes. Must have recipes to be able to create a bag that is non-empty.
    """
    if not dice_recipes:
        raise ValueError("Need recipes to build bag from.")

    def _bag_function():
        dice = []
        for recipe in dice_recipes:
            dice.extend(
                Die(
                    faces=deepcopy(recipe.faces),
                )
                for _ in range(recipe.amount)
            )
        return DieBag(
            dice=dice,
        )

    return _bag_function


class ZombieDieGame:
    """Instance of the zombie dice that that manages a bag of dice that will be used to coordinate how the game is played.

    **Parameters**
    - players (`list[PlayerScore]`): players in the game
    - commands (`list[tuple[Command, RoundState]]`, optional): previous commands that have been run before in the game. Defaults to `[]`
    - bag_function (`Callable[[], DieBag]`, optional): function that will generate a `zombie_nomnom.DieBag` that will be used in the round transitions. Defaults to `zombie_nomnom.DieBag.standard_bag`
    - score_threshold (`int`, optional): the score threshold that will trigger the end game. Defaults to `13`
    - current_player (`int | None` optional): the index in the player array to represent the current player. Defaults to `None`
    - first_winning_player (`int | None` optional): the index in the player array that represents the first player to meet or exceed the score threshold. Defaults to `None`
    - game_over (`bool`, optional): marks whether or not game is over. Defaults to `False`
    - round (`RoundState | None`, optional): the current round of the game being played. Defaults to a new instance that is created for the first player in the player array.
    - bag_recipes (`list[DieRecipe]`):

    **Raises**
    - `ValueError`: When there is not enough players to play a game.
    """

    players: list[Player]
    """Players that are in the game."""
    commands: list[tuple[Command, RoundState]]
    """Commands that have been processed in the game and the round state they were in before it started."""
    bag_function: Callable[[], DieBag]
    """Function that we use when we need to create a new bag for a round."""
    round: RoundState | None
    """Current round that we are on."""
    current_player: int | None
    """Index of player in the players array who's turn it currently is."""
    first_winning_player: int | None
    """Index of player who first exceeded or matched the `score_threshold`."""
    game_over: bool
    """Marker for when the game is over."""
    score_threshold: int
    """Threshold required for a player to start the end game."""
    bag_recipes: list[DieRecipe]

    def __init__(
        self,
        players: list[str | Player],
        commands: list[tuple[Command, RoundState]] | None = None,
        bag_function: Callable[[], DieBag] | None = None,
        score_threshold: int = 13,
        current_player: int | None = None,
        first_winning_player: int | None = None,
        game_over: bool = False,
        round: RoundState | None = None,
        bag_recipes: list[DieRecipe] | None = None,
    ) -> None:
        if len(players) == 0:
            raise ValueError("Not enough players for the game we need at least one.")

        self.commands = list(commands) if commands else []
        self.players = [
            (
                Player(name=name_or_score)
                if isinstance(name_or_score, str)
                else name_or_score
            )
            for name_or_score in players
        ]
        if not bag_recipes:
            self.bag_function = bag_function or DieBag.standard_bag
            self.bag_recipes = []
        else:
            self.bag_function = bag_from_recipes(bag_recipes)
            self.bag_recipes = bag_recipes
        self.score_threshold = score_threshold

        self.round = round
        self.current_player = current_player
        self.first_winning_player = first_winning_player
        self.game_over = game_over

        if self.round is None and self.current_player is None:
            self.next_round()

    @property
    def winner(self) -> Player:
        """The player with the highest score in the players array. On Ties uses the player with the lowest index.

        **Returns**
        - `Player`: The winning player
        """
        return max(self.players, key=operator.attrgetter("total_brains"))

    def reset_players(self):
        """Resets the game state so that players scores are set to zero and the current_player is reset to `None` as well as the first_winning_player"""
        self.players = [player.reset() for player in self.players]
        self.current_player = None
        self.first_winning_player = None

    def reset_game(self):
        """Resets the game state by resetting the players, clearing commands, and transitioning to the next round which will be the first players round."""
        self.reset_players()
        self.commands = []
        self.next_round()

    def next_round(self):
        """Transitions the current player index point to the next players turn and then sets the round field with that player and a new bag to play the round."""
        if self.current_player is not None and self.round:
            self.players[self.current_player] = self.round.player

        if self.current_player is None:
            self.current_player = 0
        elif self.current_player + 1 < len(self.players):
            self.current_player = self.current_player + 1
        else:
            self.current_player = 0
        self.round = RoundState(
            bag=self.bag_function(),
            player=self.players[self.current_player],
            ended=False,
        )

    def check_for_game_over(self) -> bool:
        """Checks if game is over and sets the game_over field."""
        if not self.round.ended:
            return  # Still not done with their turns.
        game_over = False
        # GAME IS OVER WHEN THE LAST PLAYER IN A ROUND TAKES THERE TURN
        # I.E. IF SOMEONE MEETS THRESHOLD AND LAST PLAYER HAS HAD A TURN
        if len(self.players) == 1 and self.winner.total_brains >= self.score_threshold:
            game_over = True

        if self.first_winning_player is None:
            if self.players[self.current_player].total_brains >= self.score_threshold:
                self.first_winning_player = self.current_player
        else:
            if (
                self.first_winning_player == 0
                and self.current_player == len(self.players) - 1
            ):
                game_over = True
            elif (
                self.first_winning_player > self.current_player
                and self.first_winning_player - self.current_player == 1
            ):
                game_over = True

        self.game_over = game_over

    def update_player(self):
        """Updates the player in the players array with the instance that is currently on the round field for the current player index."""
        self.players[self.current_player] = self.round.player

    def process_command(self, command: Command) -> RoundState:
        """Applies the given command to the active round and transitions to the next round if the current round is over.

        **Parameters**
        - command (`Command`): command that will modify the round state.

        **Raises**
        - `ValueError`: When trying to process a command when the game is already over.

        **Returns**
        - `RoundState`: The round information that happened due to the command.
        """
        if self.game_over:
            raise ValueError("Cannot command an ended game please reset game.")

        self.commands.append((command, self.round))

        resulting_round = command.execute(self.round)
        self.round = resulting_round
        if self.round.ended:
            self.update_player()
            self.check_for_game_over()
            self.next_round()
        return resulting_round
