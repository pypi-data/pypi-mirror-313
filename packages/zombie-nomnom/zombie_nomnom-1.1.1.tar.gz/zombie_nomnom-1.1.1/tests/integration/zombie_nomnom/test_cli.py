from typing import Callable
from click.testing import CliRunner, Result
import pytest

from zombie_nomnom.app import main


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def run_game_with_input(runner: CliRunner):
    def _run_with_input(cli_input: str = "") -> Result:
        return runner.invoke(main, args=["cli"], input=cli_input)

    return _run_with_input


def test_app__when_user_types_name__prints_name_to_screen(
    run_game_with_input: Callable[[str], Result]
):
    # this works by putting in the name of the player then new line to tell it to no more players then zero
    # to select exit option and then final new line to not continue
    cli_input = """milo

    0
    """
    result = run_game_with_input(cli_input)
    assert "Players: milo" in result.output


def test_app__when_replaying_game__setups_game_again(
    run_game_with_input: Callable[[str], Result]
):
    # this works by putting in the name of the player then new line to tell it to no more players then zero
    # to select exit option and then final new line to not continue
    cli_input = """milo

    0
    y
    milo
    
    0
    n
    """
    result = run_game_with_input(cli_input)
    assert "Players: milo" in result.output


def test_app__when_setting_up__allows_multiple_players(
    run_game_with_input: Callable[[str], Result]
):
    # this works by putting in the name of the player then new line to tell it to no more players then zero
    # to select exit option and then final new line to not continue
    cli_input = """milo
y
Dean

    0
    """
    result = run_game_with_input(cli_input)
    assert "Players: milo" in result.output
    assert "Dean (0)" in result.output


def test_app__when_playing_and_drawing_dice__dice_goes_down_by_3_for_first_draw(
    run_game_with_input: Callable[[str], Result]
):
    # this works by putting in the name of the player then new line to tell it to no more players then zero
    # to select exit option and then final new line to not continue
    cli_input = """milo
    
    1
    0
    """
    result = run_game_with_input(cli_input)
    assert "Drawing dice..." in result.output, "Did not display drawing dice"
    assert (
        "Dice Remaining: 10" in result.output
    ), "Did not take three dice correctly from the game."


def test_app__when_playing_and_drawing_dice__dice_goes_down_by_3_for_first_draw(
    run_game_with_input: Callable[[str], Result]
):
    # this works by putting in the name of the player then new line to tell it to no more players then zero
    # to select exit option and then final new line to not continue
    cli_input = """milo
    
    1
    0
    """
    result = run_game_with_input(cli_input)
    assert "Drawing dice..." in result.output, "Did not display drawing dice"
    assert (
        "Dice Remaining: 10" in result.output
    ), "Did not take three dice correctly from the game."


def test_app__when_playing_and_scoring_hand__scores_dice_and_transitions_turn(
    run_game_with_input: Callable[[str], Result]
):
    # this works by putting in the name of the player then new line to tell it to no more players then zero
    # to select exit option and then final new line to not continue
    cli_input = """milo
    y
    dean
    n
    2
    0
    """
    result = run_game_with_input(cli_input)
    assert "Scoring hand..." in result.output, "Did not display scoring hand..."
    assert "Currently Playing dean" in result.output, "Did not display deans turn..."


def test_app__when_playing_and_scoring_hand__scores_dice_and_transitions_turn(
    run_game_with_input: Callable[[str], Result],
):
    # this works by putting in the name of the player then new line to tell it to no more players then zero
    # to select exit option and then final new line to not continue
    cli_input = """milo
    y
    dean
    n
    2
    0
    """
    result = run_game_with_input(cli_input)
    assert "Scoring hand..." in result.output, "Did not display scoring hand..."
    assert "Currently Playing dean" in result.output, "Did not display deans turn..."


def test_app__when_playing_and_rolling_until_death__transitions_turn_to_other_player(
    run_game_with_input: Callable[[str], Result]
):
    # this works by putting in the name of the player then new line to tell it to no more players then zero
    # to select exit option and then final new line to not continue
    cli_input = """milo
    y
    dean

    1
    1
    1
    1
    1
    1
    1
    1
    1
    0
    """
    result = run_game_with_input(cli_input)
    assert "milo Has Died" in result.output, "He is a god gamer and survived."
