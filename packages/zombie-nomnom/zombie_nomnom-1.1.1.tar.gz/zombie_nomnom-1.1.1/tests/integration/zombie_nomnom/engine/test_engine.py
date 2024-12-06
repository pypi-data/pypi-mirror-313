from zombie_nomnom.engine import DrawDice, Score, ZombieDieGame
from zombie_nomnom.models.dice import Face


def test_zombie_dice_game__plays_a_valid_single_player_game_of_zombie_dice__finishes_in_my_victory(
    patch_random_randint,
    patch_random_choice,
):
    # basically always pick the first three die in the array and then default to always the first face on each die.
    patch_random_randint.side_effect = [
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
    ]
    patch_random_choice.side_effect = lambda collection: collection[0]

    draw_three = DrawDice()
    score = Score()

    game = ZombieDieGame(
        players=["Game Ova"],
    )

    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(score)

    assert game.winner.total_brains == 15
    assert game.game_over, "Game should be finished"
    assert game.winner.name == "Game Ova"


def test_zombie_dice_game__plays_a_valid_two_player_game_of_zombie_dice__finishes_in_player_one_victory(
    patch_random_randint,
    patch_random_choice,
):
    # basically always pick the first three die in the array and then default to always the first face on each die.
    patch_random_randint.side_effect = [
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
        *[0, 1, 2],
    ]
    patch_random_choice.side_effect = [
        *([Face.BRAIN] * 15),
        *([Face.BRAIN] * 14),
        Face.SHOTGUN,
    ]

    draw_three = DrawDice()
    score = Score()

    game = ZombieDieGame(
        players=[
            "Game Ova",
            "Looser",
        ],
    )

    # First Players Turn
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(score)

    # Second Players Turn
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(draw_three)
    game.process_command(score)

    assert game.winner.total_brains == 15
    assert game.game_over, "Game should be finished"
    assert game.winner.name == "Game Ova"
