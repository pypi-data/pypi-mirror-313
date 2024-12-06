import uuid

from pydantic import BaseModel, Field

from zombie_nomnom.models.bag import DieBag
from zombie_nomnom.models.dice import Die, Face, DieFace


def uuid_str() -> str:
    """Creates a stringified uuid that we can use.

    **Returns**
    - `str`: stringified uuid
    """
    return str(uuid.uuid4())


def is_scoring_face(face: Face | DieFace) -> bool:
    """Checks if a face is scoring.

    A scoring face is a face that will score points for the player.
    This is useful for determining if a player should continue rolling or not.

    **Arguments**
    - `face: Face | DieFace`: The face to check.

    **Returns**
    - `bool`: If the face is a scoring face.
    """
    return (
        isinstance(face, Face)
        and face == Face.BRAIN
        or isinstance(face, DieFace)
        and face.score
    )


def is_damaging_face(face: Face | DieFace) -> bool:
    """Checks if a face is damaging.

    A damaging face is a face that will limit the amount of dice the player can roll.
    This is useful for determining if a player should stop rolling or not.

    **Arguments**
    - `face: Face | DieFace`: The face to check.

    **Returns**
    - `bool`: If the face is a damaging face.
    """
    return (
        isinstance(face, Face)
        and face == Face.SHOTGUN
        or isinstance(face, DieFace)
        and face.damage
    )


def is_blank_face(face: Face | DieFace) -> bool:
    """Checks if a face is blank.

    A blank face is a face that doesn't score any points nor does it damage the player.
    This is useful for determining if a die should be rolled again.

    **Arguments**
    - `face: Face | DieFace`: The face to check.

    **Returns**
    - `bool`: True if the face is blank.
    """
    return (
        isinstance(face, Face)
        and face == Face.FOOT
        or isinstance(face, DieFace)
        and not face.score
        and not face.damage
    )


class Player(BaseModel):
    """Player in the game. This manages the total points
    they have and the dice they pulled from the bag. Has
    methods to manage the hand and then calculate points.
    Also has ways to be able to tell if players turn should finish.
    """

    id: str = Field(default_factory=uuid_str)
    """id field used to identify the player more unqiuely"""
    name: str
    """name of the player that we display on the screen"""
    total_brains: int = 0
    """total points they currently have in the game"""
    hand: list[Die] = []
    """the dice the player is currently holding"""

    @property
    def rerolls(self) -> list[Die]:
        """A view of the hand that shows all the dice that are re-rollable.

        **Returns**:
        - `list[zombie_nomnom.Die]`: re-rollable dice
        """
        return [die for die in self.hand if is_blank_face(die.current_face)]

    @property
    def brains(self) -> list[Die]:
        """A view of the hand that shows all the dice that scores points.

        **Returns**
        - `list[zombie_nomnom.Die]`: scoreable dice
        """
        return [die for die in self.hand if is_scoring_face(die.current_face)]

    @property
    def shots(self) -> list[Die]:
        """A view of the hand that shows the shots you have taken.

        **Returns**
        - `list[zombie_nomnom.Die]`: damaging dice
        """
        return [die for die in self.hand if is_damaging_face(die.current_face)]

    def is_player_dead(self) -> bool:
        """Calculates whether or not the player should be dead based on the shots in their hand.

        **Returns**
        - bool: True when player is considered dead.
        """
        total = 0
        for shot in self.shots:
            face = shot.current_face
            if isinstance(face, DieFace):
                total += face.damage
            else:
                total += 1
        # if you have 3 shots you are dead XP
        return total >= 3

    def add_dice(self, *dice: Die) -> "Player":
        """Creates a new player adding the dice the caller gives plus any dice in their hand currently.

        **Returns**
        - `Player`: New player instance with updated hand.
        """
        return Player(
            id=self.id,
            name=self.name,
            hand=[*self.hand, *dice],
            total_brains=self.total_brains,
        )

    def clear_hand(self) -> "Player":
        """Creates a new player with no dice in their hand.

        **Returns**
        - `Player`: New player instance with empty hand.
        """
        return Player(
            id=self.id,
            name=self.name,
            total_brains=self.total_brains,
        )

    def reset(self) -> "Player":
        """Creates a new player instance with all the game related fields set back to their default values.

        **Returns**
        - `Player`: New player instance with all values reset.
        """
        return Player(
            id=self.id,
            name=self.name,
            total_brains=0,
            hand=[],
        )

    def calculate_score(self) -> "Player":
        """Creates a new player that has added the score of the current hand and leaves an empty hand.

        **Returns**
        - `Player`: New player instance with score adjusted for scoring dice in hand and hand reset back to empty list.
        """
        additional_score = 0
        for brain_xo in self.brains:
            face = brain_xo.current_face
            if isinstance(face, DieFace):
                additional_score += face.score
            else:
                additional_score += 1
        return Player(
            id=self.id,
            name=self.name,
            total_brains=additional_score + self.total_brains,
        )


class RoundState(BaseModel):
    """
    Object representing the state of a round in the game. Keeps track of the bag, player,
    and whether or not the round has ended.
    """

    bag: DieBag
    """Bag that is currently being played in the round"""
    player: Player
    """Player that is currently playing"""
    ended: bool = False
    """Records whether or not the current round is over"""


class DieRecipe(BaseModel):
    """The recipe for a dice to be used in the bag. Will have the array of faces
    that we will use for our die and how many instances to add to our bag.
    """

    faces: list[Face]
    """The faces that will make up the dice."""
    amount: int
    """The amount of dice that will be added to the bag."""
