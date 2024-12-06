import pytest
from zombie_nomnom.models.dice import Die, DieColor, Face, create_die


def create_test_die() -> Die:
    # Yellow Die
    return Die(
        faces=[
            Face.BRAIN,
            Face.BRAIN,
            Face.FOOT,
            Face.FOOT,
            Face.SHOTGUN,
            Face.SHOTGUN,
        ]
    )


# Comment


def test_dice__when_we_roll_die__then_face_is_set():
    # arrange
    sut = create_test_die()
    # precheck just in case we fucked up
    assert sut.current_face is None, "Face was not set to None before we rolled it"

    # act/assert in the same line
    assert sut.roll() is not None, "Expected to get something back"
    assert sut.current_face in {
        Face.BRAIN,
        Face.FOOT,
        Face.SHOTGUN,
    }, f"Was not expected face {sut.current_face}"


def test_create_die__when_given_a_valid_color__returns_die():
    # arrange and act
    sut = create_die(DieColor.GREEN)

    # assert
    assert isinstance(sut, Die), "Expected create_die to return a Die object."


def test_create_die__when_given_invalid_color__raises_value_error():
    with pytest.raises(ValueError):
        create_die("bogus")


@pytest.mark.parametrize(
    "color, sides",
    [
        (DieColor.GREEN, [Face.BRAIN] * 3 + [Face.FOOT] * 2 + [Face.SHOTGUN] * 1),
        (DieColor.YELLOW, [Face.BRAIN] * 2 + [Face.FOOT] * 2 + [Face.SHOTGUN] * 2),
        (DieColor.RED, [Face.BRAIN] * 1 + [Face.FOOT] * 2 + [Face.SHOTGUN] * 3),
    ],
)
def test_create_die__when_given_valid_color__returns_expected_die(color, sides):
    sut = create_die(color)
    assert sut.faces == sides


@pytest.mark.parametrize(
    "color, name",
    [
        (DieColor.GREEN, "GREEN"),
        (DieColor.YELLOW, "YELLOW"),
        (DieColor.RED, "RED"),
    ],
)
def test_create_die__when_given_red__returns_die_named_color(color, name):
    die = create_die(color)
    assert die.name == name
