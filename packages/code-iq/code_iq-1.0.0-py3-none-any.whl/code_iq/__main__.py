""" Allows to run the CLI using python -m """

from code_iq.main import code_iq


def main() -> None:
    """Entry point function for running the CLI."""

    # Run the cli
    code_iq(prog_name="code-iq")


if __name__ == "__main__":
    main()
