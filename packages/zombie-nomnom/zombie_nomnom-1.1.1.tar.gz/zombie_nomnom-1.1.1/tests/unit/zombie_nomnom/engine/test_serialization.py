import pytest

from zombie_nomnom.engine.models import Face
from zombie_nomnom.engine.commands import DrawDice, Score
from zombie_nomnom.engine.serialization import (
    format_command,
    parse_command_dict,
    format_to_json_dict,
    parse_game_json_dict,
    ZombieDieGame,
    DieRecipe,
)


@pytest.fixture
def game():
    zombie_game = ZombieDieGame(players=["Player Uno"])
    zombie_game.bag_recipes = [DieRecipe(faces=[Face.FOOT] * 6, amount=3)]
    zombie_game.bag_function = DrawDice(amount_drawn=3)
    yield zombie_game


def test_format_command__when_formatting_known_command__uses_fully_qualified_name_for_class():
    command = Score()
    expected = {
        "cls": "zombie_nomnom.engine.commands.Score",
        "args": [],
        "kwargs": {},
    }
    actual = format_command(command)

    assert actual == expected


def test_format_command__when_formatting_command_with_args__puts_args_as_kwargs():
    command = DrawDice(amount_drawn=3)
    expected = {
        "cls": "zombie_nomnom.engine.commands.DrawDice",
        "args": [],
        "kwargs": {
            "amount_drawn": 3,
        },
    }
    actual = format_command(command)

    assert actual == expected


def test_parse_command_dict__when_parsing_will_load_class_and_initialize_correctly__loads_command_class():
    cmd_dict = {
        "cls": "zombie_nomnom.engine.commands.Score",
        "args": [],
        "kwargs": {},
    }

    actual = parse_command_dict(cmd_dict)

    assert isinstance(actual, Score)


def test_parse_command_dict__when_parsing_command_with_parameters_kwargs__loads_command_class():
    cmd_dict = {
        "cls": "zombie_nomnom.engine.commands.DrawDice",
        "args": [],
        "kwargs": {"amount_drawn": 3},
    }

    actual = parse_command_dict(cmd_dict)

    assert isinstance(actual, DrawDice)
    assert actual.amount_drawn == 3


def test_parse_command_dict__when_parsing_command_with_parameters_args__loads_command_class():
    cmd_dict = {
        "cls": "zombie_nomnom.engine.commands.DrawDice",
        "args": [3],
        "kwargs": {},
    }

    actual = parse_command_dict(cmd_dict)

    assert isinstance(actual, DrawDice)
    assert actual.amount_drawn == 3


def test_format_to_json_dict__when_bag_function_is_none_and_bag_recipes_is_empty__assumes_standard_bag():
    game = ZombieDieGame(players=["Player Uno"])
    json = format_to_json_dict(game)
    assert json["bag_function"] == "standard"


def test_format_to_json_dict__when_bag_function_is_not_none_and_bag_recipes_exists__returns_valid_dict(
    game,
):
    sut = format_to_json_dict(game)
    assert sut
    assert isinstance(sut, dict)
    assert sut["bag_function"]
    assert sut["players"]


def test_parse_game_json_dict__when_given_valid_dict__returns_game_instance(
    game,
):
    game_dict = format_to_json_dict(game)
    sut = parse_game_json_dict(game_dict)

    assert sut
    assert sut.bag_recipes == game.bag_recipes
    assert sut.players == game.players
    assert sut.score_threshold == game.score_threshold
    assert sut.round == game.round


def test_parse_game_json_dict__when_bag_function_is_str_and_bag_function_is_not_standard_bag__raises_value_error(
    game,
):
    with pytest.raises(ValueError):
        game_dict = format_to_json_dict(game)
        game_dict["bag_function"] = "DrawDice"

        parse_game_json_dict(game_dict)
