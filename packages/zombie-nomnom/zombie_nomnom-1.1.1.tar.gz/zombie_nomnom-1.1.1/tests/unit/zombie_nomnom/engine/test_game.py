import pytest
from zombie_nomnom.engine.game import ZombieDieGame, bag_from_recipes
from zombie_nomnom.engine.models import DieRecipe
from zombie_nomnom.models.bag import DieBag
from zombie_nomnom.models.dice import Face


def test_bag_from_recipes__when_given_no_recipes__raises_value_error():
    with pytest.raises(ValueError):
        bag_from_recipes([])


def test_bag_from_recipes__when_given_single_recipe__returns_bag_that_only_creates_single_type_of_dice():
    recipes = [DieRecipe(amount=2, faces=[Face.BRAIN] * 6)]
    only_score_recipe = recipes[0]

    func = bag_from_recipes(recipes)
    new_bag = func()

    assert len(new_bag) == 2
    assert new_bag.dice[0].faces == only_score_recipe.faces


def test_zombie_die_game__when_creating_a_game_with_no_bag_function_but_recipes__creates_a_new_bag_func():
    sut = ZombieDieGame(
        players=["Skibbidy"],
        # the bag only contains rerolls mwuah-hahaha
        bag_recipes=[DieRecipe(faces=[Face.FOOT] * 6, amount=3)],
    )
    assert sut.bag_function is not None
    assert sut.bag_function is not DieBag.standard_bag
    assert sut.bag_recipes != []
