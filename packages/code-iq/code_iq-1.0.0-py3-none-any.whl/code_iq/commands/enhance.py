""" CodeIQ enhance command """

from typing import Annotated, Optional
import typer
from huggingface_hub import InferenceClient
from rich import print
from code_iq import CHAT_LLM, SYSTEM_MESSAGE, create_panel


def enhance(
    code: Annotated[
        typer.FileText,
        typer.Argument(
            help="File containing code to enhance for quality improvements."
        ),
    ],
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
    ] = 2048,
) -> None:
    """
    Applies improvements or optimizations to existing code, such as refactoring,
    performance tuning, or adding new features.

    Examples:
    ```shell
    code-iq enhance code.py
    code-iq enhance code.py -o code-enhancements.md
    ```
    """

    client = InferenceClient(CHAT_LLM)

    try:
        response = client.chat_completion(
            messages=[
                SYSTEM_MESSAGE,
                {
                    "role": "user",
                    "content": "As a an expert software engineer and site reliability engineer "
                    "that puts code into production in large scale systems. Your job is to ensure "
                    "that code runs effectively, quickly, at scale, and securely. Please profile it, "
                    "and find any issues that need to be fixed or updated. Also apply best practices, "
                    "enhancements, and industry standards to the provided code to make it more efficient, "
                    f"secure, and maintainable:\n{code.read()}",
                },
            ],
            max_tokens=max_tokens,
        )

        if output:
            with output as file:
                file.write(str(response.choices[0].message.content))

            print(f"Output [bold green]saved[/bold green] to {output.name}.")

        else:
            print(create_panel("CodeIQ", str(response.choices[0].message.content)))

    except Exception as error:
        print(f"[bold red]Error[/bold red]: {error}")
