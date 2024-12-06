from abc import ABC, abstractmethod
import sys

from pydantic import validate_call
from .models import RoundState


class Command(ABC):
    """
    Used to modify round state. Cannot be used to reset game.
    """

    @abstractmethod
    def execute(self, round: RoundState) -> RoundState:  # pragma: no cover
        """
        Method to generate a new RoundState that represents modifications on the command.

        **Parameters**
        - round(`RoundState`): the round we are on.

        **Returns** `RoundState`

        New instance of round with modified state.
        """


class DrawDice(Command):
    """
    The core command that represents handling a draw action in the game.
    This will attempt to draw dice in your hand to fill in any dice that
    are not re-rollable then roll the dice for the turn. Then it will
    check to make sure you are still alive and if so keep dice in your hand
    and return a new round object.

    **Parameters**
    - amount_drawn (`int`): Dice this action will attempt to draw.
    """

    amount_drawn: int
    """Amount of dice that this action will attempt to draw."""

    def __init__(self, amount_drawn: int = 3) -> None:
        if amount_drawn <= 0:
            raise ValueError("Cannot draw a no or a negative amount of dice.")
        self.amount_drawn = amount_drawn

    @validate_call
    def execute(self, round: RoundState) -> RoundState:
        """
        Executes a dice draw on a round that is active.

        If round is already over will return given round context.

        **Parameters**
        - round(`RoundState`): the round we are on.

        **Returns** `RoundState`

        New instance of a round with player adding dice to hand.
        """
        if round.ended:
            return round
        player = round.player
        dice_to_roll = player.rerolls
        total_dice = len(dice_to_roll)
        try:
            bag = (
                round.bag.clear_drawn_dice()
                if total_dice == self.amount_drawn
                else round.bag.draw_dice(amount=self.amount_drawn - total_dice)
            )
        except ValueError as exc:
            return self.execute(
                round=RoundState(
                    bag=round.bag.add_dice(player.brains),
                    player=player,
                    ended=round.ended,
                )
            )
        dice_to_roll.extend(bag.drawn_dice)
        player = player.add_dice(*bag.drawn_dice)

        for die in dice_to_roll:
            die.roll()

        ended = player.is_player_dead()
        if ended:
            player = player.clear_hand()

        return RoundState(
            bag=bag,
            player=player,
            ended=ended,
        )


class Score(Command):
    """
    Command to score the hand of a player and add the brains they have as points to their total.
    """

    def execute(self, round: RoundState) -> RoundState:
        """
        Scores the hand of the current player by rolling up all the scoring faces and adding it to their hand.

        **Parameters**
        - round (`RoundState`): The round we are currently in.

        **Returns** `RoundState`

        Roundstate that is now ended with the player with hand cleared and new score added to them.
        """
        if round.ended:
            return round
        player = round.player.calculate_score()
        return RoundState(
            bag=round.bag,
            player=player,
            ended=True,
        )
