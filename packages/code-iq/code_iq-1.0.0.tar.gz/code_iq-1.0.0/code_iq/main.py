""" CodeIQ """

import typer
from code_iq.commands import command_list


# CodeIQ
code_iq = typer.Typer(
    name="code-iq",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="CodeIQ is an AI-powered command-line interface (CLI) tool designed to enhance coding efficiency and productivity.",
)


# Add the commands
for command in command_list:
    code_iq.command(no_args_is_help=True)(command)


if __name__ == "__main__":
    code_iq()
