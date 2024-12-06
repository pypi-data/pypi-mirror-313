from pathlib import Path
import click


def arg_directory(func):
    func = click.argument(
        "directory",
        type=click.Path(
            exists=True,
            file_okay=False,
            readable=True,
            path_type=Path,
        ),
        default=".",
    )(func)
    return func
