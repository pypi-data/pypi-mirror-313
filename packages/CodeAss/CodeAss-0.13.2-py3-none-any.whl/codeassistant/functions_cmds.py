from pathlib import Path

import click
from codeassistant.functions_core import gpt
from codeassistant.functions_git import get_git_diff
from codeassistant.variables import DEFAULT_SPACING


def generate_commit_msg(directory: Path, prompt: str, silent=False) -> str:
    diff: str = get_git_diff(directory)

    if not diff:
        click.echo("No diff")
        return ""

    msg = gpt(f"{prompt}", context=f"{diff}")

    if not silent:
        click.echo()
        click.echo(f"{'#'*DEFAULT_SPACING} Commit Message {'#'*DEFAULT_SPACING}")
        click.echo(msg)
        click.echo(f"{'#'*DEFAULT_SPACING}################{'#'*DEFAULT_SPACING}")
        click.echo()
    return msg
