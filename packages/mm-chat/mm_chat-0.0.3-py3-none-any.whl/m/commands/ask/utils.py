from contextlib import redirect_stderr
from functools import cache
from io import StringIO

from m.utils.path import global_store
from typer import Exit


@cache
def _get_session():
    from prompt_toolkit import PromptSession
    from prompt_toolkit.history import FileHistory
    from prompt_toolkit.input import create_input
    from prompt_toolkit.styles import Style

    history = FileHistory(global_store / ".history")
    style = Style([("", "ansiyellow")])

    with redirect_stderr(io := StringIO()):
        session = PromptSession(history=history, style=style)

    if "Input is not a terminal (fd=0)" in io.getvalue():  # Warning: Input is not a terminal (fd=0).
        return PromptSession(input=create_input(open("/dev/tty")), history=history, style=style)  # noqa: PTH123

    return session


def prompt(*args, **kwargs):
    return _get_session().prompt(*args, **kwargs)


def get_user_message():
    print()

    message = prompt(" > ")
    if not message:
        print()
        raise Exit

    print()

    return message
