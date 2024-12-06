"""Module that contains the code to run the core game engine.
You can create an instance directly by using the `ZombieDieGame`.

```python
from zombie_nomnom import ZombieDieGame, DrawDice, Score

score = Score()
draw_dice = DrawDice(3)

game = ZombieDieGame(players=["Mellow"])

game.process_command(draw_dice)
game.process_command(score)

```

For the core of the engine it doesn't actually know how to play but only 
how to manage a turn based on tracking the changes in a round with a `RoundState` object.

This allows you to extend the game by creating your own custom actions with the `Command` class.
This class defines the `execute` method and then allows you to specify what that action does to the game state.
You will need to return an new instance of `RoundState` objects that represents the effect of game state after the round is over.

```python
from zombie_nomnom import Command, ZombieDieGame

class CustomCommand(Command):
    def execute(self, round: RoundState) -> RoundState:
        # do meaningful work to define what you want this command to do to the round.
        return round  # return either a new command or the exact same command unchanged.

custom_command = CustomCommand()
game = ZombieDieGame(players=["Meelow"])

game.process_command(custom_command) # now it just works in the game!!

```

This only allows you to modify the state of the current player or the current turn that is active in the engine.
That being said it should provide a nice way to extend the app with custom actions for a players.

The core objects that we use in our engine are three:
- `Player`
- `RoundState`

```python
from zombie_nomnom.models import DieBag, Die, Face
from zombie_nomnom.engine import Player, RoundState

player = Player(
    name="Mega Man"
)

# you can add dice to their hand.
player_with_die_added = player.add_dice(
    Die(
        faces=[Face.BRAIN] * 6
    )
)
player_with_die_added.hand # dice is now updated with new die.

player.rerolls # pulls the dice that are re-rollable in hand
player.brains # pulls all the scoring dice in hand.
player.shots # pulls all the damaging dice in hand.

# counts the shots in the hand and see if you have been shot 3 or more times.
player.is_player_dead() # player is not dead

# new player with nothing in their hand.
new_player = player.clear_hand()
new_player.hand # is empty list

# resets the players game stats
new_player = player.reset() 
new_player.total_brains # now 0
new_player.hand # empty list

# counts the dice in the hand and adds to score.
new_player = player.calculate_score()
new_player.total_brains # player had 1 brain so it will now be 1
new_player.hand # is not empty list

# no methods just holds value to package it in a single object.
round = RoundState(
    bag=DieBag.standard_bag(),
    player=player,
)
```
"""

from .models import Player, RoundState, uuid_str
from .commands import Command, Score, DrawDice
from .game import ZombieDieGame


__all__ = [
    "Player",
    "RoundState",
    "uuid_str",
    "Command",
    "Score",
    "DrawDice",
    "ZombieDieGame",
    "commands",
    "game",
    "models",
    "serialization",
]
