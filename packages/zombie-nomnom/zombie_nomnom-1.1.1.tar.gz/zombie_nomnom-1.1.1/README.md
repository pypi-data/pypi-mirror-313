Zombie Nom Nom
===

This is a game engine that is modeled after the popular board game zombie dice. This is meant for practice to be able to be messed with and explored.

[![Test and Deploy Docs](https://github.com/Carrera-Dev-Consulting/zombie_nomnom/actions/workflows/deploy-docs.yaml/badge.svg)](https://github.com/Carrera-Dev-Consulting/zombie_nomnom/actions/workflows/deploy-docs.yaml)

Useful Links
---

Links to result of code coverage and pytest of latest builds.

* [Coverage Report](https://consulting.gxldcptrick.dev/zombie_nomnom/coverage/)
* [Latest Test Run](https://consulting.gxldcptrick.dev/zombie_nomnom/coverage/report.html)
* [Documentation](https://consulting.gxldcptrick.dev/zombie_nomnom/)

Installation
---

`pip install zombie_nomnom`


We require at least python 3.10 to be able to run properly.


Usage
---

You can use the zombie_nomnom engine directly in code like this:

```python
...
from zombie_nomnom import ZombieDieGame, DrawDice, Score

draw_three = DrawDice(3)
score_hand = Score()
game = ZombieDieGame(players=["Player One", "Player Two])

logger.info(game.round)

result = game.process_command(draw_three)
logger.info(result)

result = game.process_command(score_hand)
logger.info(result)

loger.info(game.round)
# ... keep playing game below
```

Or you can play it using the CLI that is already baked into the package:

```bash
> zombie-nomnom cli
Enter Player Name: Jeffery
Add Another Player? [y/N]: 
Players: Jeffery (0)
Currently Playing Jeffery, Hand: Brains(0), Feet(0), Shots(0), Dice Remaining: 13
0) Exit
1) Draw dice
2) Score hand
Select Item (0-2): 1
```

Contribution
---

For details of conduct and expactations please refer to [CONTRIBUTION.md](https://github.com/Carrera-Dev-Consulting/zombie_nomnom/blob/main/CONTRIBUTING.md)

Pull requests will be pending review of at least one maintainer.

Pull requests are required to have finished the template checklist before they will be reviewed by a maintainer. 

All code is formatted with the black formatter and we expect types and may run mypy to check that your code is properly typed as expected.

Names should make sense and be self descriptive of the proposed changes.
