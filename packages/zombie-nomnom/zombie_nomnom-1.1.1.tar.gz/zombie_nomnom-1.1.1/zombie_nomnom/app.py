"""
Module that contains the click entrypoint for our cli interface.

Currently this only contains code to run the game form the cli but this will be extended 
to also run this as a web app including a built in server with react spa app.
"""

import click
from .cli import run_game


@click.group()
def main():
    """
    main group that represents the top-level: ***zombie-nomnom***

    This will be used to decorate sub-commands for zombie-nomnom.

    ***Example Usage:***
    ```python
    @main.command("sub-command")
    def sub_command():
        # do actual meaningful work.
        pass
    ```
    """
    pass


@main.command("cli")
def cli():
    """
    Command to start the zombie_dice game from the command line.
    """
    run_game()

    # ask after we finish a single game assume they will quit when they want to.
    while click.confirm(text="Play another game of zombie dice?"):
        run_game()

    click.echo("Thank you for playing!!")
