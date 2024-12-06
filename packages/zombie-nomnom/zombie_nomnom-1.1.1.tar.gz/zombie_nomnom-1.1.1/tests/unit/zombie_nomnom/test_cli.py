from unittest.mock import Mock

import pytest
from zombie_nomnom.cli import StrippedStr


@pytest.fixture
def mock_param():
    return Mock(name="param")


@pytest.fixture
def mock_ctx():
    return Mock(name="context")


class StaticStrObject:
    def __str__(self) -> str:
        return "Static"


class ObjectWithSpacesInStr:
    def __str__(self) -> str:
        return " spaces "


@pytest.mark.parametrize(
    "value,expected_value",
    [
        (" string with leading spaces", "string with leading spaces"),
        ("string with trailing spaces ", "string with trailing spaces"),
        (" string with both ", "string with both"),
        (StaticStrObject(), "Static"),
        (ObjectWithSpacesInStr(), "spaces"),
    ],
)
def test_stripped_str__when_given_value__formats_string_as_expected(
    value, expected_value, mock_ctx, mock_param
):
    sut = StrippedStr()

    actual_value = sut.convert(value, mock_param, mock_ctx)

    assert actual_value == expected_value
