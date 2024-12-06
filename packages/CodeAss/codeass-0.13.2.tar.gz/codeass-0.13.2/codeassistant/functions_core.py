from enum import Enum
import shlex
from subprocess import run
from time import time
import click
import functools


def timer(func):
    """Decorator to measure and display the execution time of a function."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        elapsed_time = round(time() - start_time, 3)
        click.echo(f"{elapsed_time}s\n")
        return result

    return wrapper


def proper_escape(text: str) -> str:
    return shlex.quote(str(text))


@timer
def shell(
    cmd: str,
    standard_input: str = "",
    silent=True,
    raise_error=True,
    check_returncode=False,
) -> str:
    """Run shell command.

    silent
        silent, but still print error
    """
    try:
        p = run(cmd, shell=True, capture_output=True, input=standard_input)

        if check_returncode:
            p.check_returncode()

        if not silent:
            click.echo(p.stdout)
            click.echo(p.stderr)

    except Exception as e:
        if raise_error:
            raise e
        else:
            click.echo("\n\nERROR (EXCEPTION):")
            click.echo(p.stderr)

    return p.stdout if p.stdout else ""


# class syntax


class OpenAIModels(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


@timer
def gpt(
    prompt: str, context: str = "", strip: bool = True, model: str = "gpt-4o-mini"
) -> str:
    """Run Shell-GPT and get answer from ChatGPT.

    prompt
        The prompt to send to Shell-GPT.
    context
        The code or text input to pass as stdin to the Shell-GPT command.
    strip
        Strip the response to remove leading/trailing whitespace.

    model
        gpt-4o-mini (default)
        gpt-4-1106-preview
    """
    # prompt = shlex.quote(str(prompt))
    # context = shlex.quote(str(context))

    p = run(
        f"sgpt --model {model} '{prompt}'",
        shell=True,
        input=context,
        capture_output=True,
        encoding="utf-8",
    )

    # click.echo(p.stdout)
    if p.stderr:
        click.echo("\n\nERROR\n")
        click.echo(p.stderr)
        raise ValueError(p.stderr)

    # Parse
    text: str = p.stdout

    if strip:
        text = text.strip()

    # return proper_escape(text)
    return text
