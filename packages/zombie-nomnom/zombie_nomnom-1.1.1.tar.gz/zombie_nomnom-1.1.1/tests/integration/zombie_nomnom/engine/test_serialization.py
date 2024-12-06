import pytest
from zombie_nomnom.engine.commands import Score, DrawDice
from zombie_nomnom.engine.serialization import format_command, parse_command_dict


@pytest.mark.parametrize(
    "_cls,instance",
    [
        (Score, Score()),
        (DrawDice, DrawDice(3)),
    ],
)
def test__when_given_a_valid_command__can_format_then_parse_dict(
    _cls,
    instance,
):
    value_dict = format_command(instance)
    new_command = parse_command_dict(value_dict)

    assert isinstance(new_command, _cls)
