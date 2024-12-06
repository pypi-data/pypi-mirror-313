from unittest.mock import patch

import pytest


@pytest.fixture
def patch_random_randint():
    with patch("random.randint") as mock_random:
        yield mock_random


@pytest.fixture
def patch_random_choice():
    with patch("random.choice") as mock_choice:
        yield mock_choice
