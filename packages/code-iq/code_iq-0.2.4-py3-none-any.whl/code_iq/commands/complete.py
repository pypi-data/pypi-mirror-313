""" CodeIQ complete command """

from typing import Annotated, Optional
import typer
from huggingface_hub import InferenceClient
from rich import print
from code_iq import COMPLETION_LLM, create_panel


def complete(
    code: Annotated[str, typer.Argument(help="Code snippet to complete.")],
    language: Annotated[
        Optional[str],
        typer.Option(
            "--lang",
            "-l",
            help="Programming language of the code snippet.",
        ),
    ] = None,
    output: Annotated[
        Optional[typer.FileTextWrite],
        typer.Option(
            "--output",
            "-o",
            help="Output file to write the response to.",
            encoding="utf-8",
        ),
    ] = None,
    max_tokens: Annotated[
        Optional[int],
        typer.Option(
            "--max-tokens",
            "-t",
            help="Maximum number of tokens allowed in the response.",
        ),
    ] = 128,
) -> None:
    """
    Provides code completion features, offering suggestions to complete partially
    written code based on context and best practices.

    Examples:
    ```shell
    code-iq completions 'def hello_world():'
    code-iq completions -l python 'def hello_world():'
    code-iq completions -o code-completions.md 'def hello_world():'
    ```
    """

    client = InferenceClient(COMPLETION_LLM)

    try:
        response = client.text_generation(
            f"```{language if language else ''}\n{code}",
            max_new_tokens=max_tokens,
        )

        if output:
            with output as file:
                file.write(f"```{language if language else ''}\n{code + response}")

            print(f"Output [bold green]saved[/bold green] to {output.name}.")

        else:
            print(
                create_panel(
                    "CodeIQ", f"```{language if language else ''}\n{code + response}"
                )
            )

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
