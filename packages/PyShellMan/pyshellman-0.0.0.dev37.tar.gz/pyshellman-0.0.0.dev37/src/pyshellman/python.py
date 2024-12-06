from pathlib import Path as _Path

from pyshellman.output import ShellOutput as _ShellOutput
from pyshellman.shell import run as _run


def run(
    command: list[str],
    cwd: str | _Path | None = None,
    raise_execution: bool = True,
    raise_exit_code: bool = True,
    raise_stderr: bool = False,
    text_output: bool = True,
) -> _ShellOutput | None:
    kwargs = locals()
    kwargs["command"] = ["python", *command]
    return _run(**kwargs)


def module(
    command: list[str],
    cwd: str | _Path | None = None,
    raise_execution: bool = True,
    raise_exit_code: bool = True,
    raise_stderr: bool = False,
    text_output: bool = True,
) -> _ShellOutput | None:
    kwargs = locals()
    kwargs["command"] = ["-m", *command]
    return run(**kwargs)
