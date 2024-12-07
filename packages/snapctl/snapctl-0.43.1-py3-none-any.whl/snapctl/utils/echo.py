"""
This module contains functions to print messages to the console.
"""
import json
import typer
from rich import print
from snapctl.config.constants import SNAPCTL_ERROR
from snapctl.types.definitions import ErrorResponse
# Run `python -m rich.emoji` to get a list of all emojis that are supported


def error(msg: str, code: int = SNAPCTL_ERROR, data: object = None) -> None:
    """
    Prints an error message to the console.
    """
    error_response = ErrorResponse(
        error=True, code=code, msg=msg, data=data if data else ''
    )
    print(f"[bold red]Error[/bold red] {msg}")
    typer.echo(json.dumps(error_response.to_dict()), err=True)


def warning(msg: str) -> None:
    """
    Prints a warning message to the console.
    """
    print(f"[bold yellow]Warning[/bold yellow] {msg}")


def info(msg: str) -> None:
    """
    Prints an info message to the console.
    """
    print(f"[bold blue]Info[/bold blue] {msg}")


def success(msg: str) -> None:
    """
    Prints a success message to the console.
    """
    print(f"[bold green]Success[/bold green] {msg}")
