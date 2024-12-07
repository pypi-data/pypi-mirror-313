from pathlib import Path as _Path

from pyshellman.output import ShellOutput as _ShellOutput
from pyshellman.python import module as _python_module


_list = list


def run(
    command: list[str],
    cwd: str | _Path | None = None,
    raise_execution: bool = True,
    raise_exit_code: bool = True,
    raise_stderr: bool = False,
    text_output: bool = True,
) -> _ShellOutput | None:
    kwargs = locals()
    kwargs["command"] = ["pip", *command]
    return _python_module(**kwargs)


def list(
    cwd: str | _Path | None = None,
    raise_execution: bool = True,
    raise_exit_code: bool = True,
    raise_stderr: bool = False,
    text_output: bool = True,
) -> _ShellOutput | None:
    kwargs = locals()
    kwargs["command"] = ["list"]
    return run(**kwargs)


def install(
    command: _list[str],
    cwd: str | _Path | None = None,
    raise_execution: bool = True,
    raise_exit_code: bool = True,
    raise_stderr: bool = False,
    text_output: bool = True,
) -> _ShellOutput | None:
    kwargs = locals()
    kwargs["command"] = ["install", *command]
    return run(**kwargs)


def install_requirements(
    path: str | _Path,
    cwd: str | _Path | None = None,
    raise_execution: bool = True,
    raise_exit_code: bool = True,
    raise_stderr: bool = False,
    text_output: bool = True,
) -> _ShellOutput | None:
    kwargs = locals()
    kwargs["command"] = ["-r", str(kwargs.pop("path"))]
    return install(**kwargs)


def install_package(
    name: str,
    requirement_specifier: str | None = None,
    upgrade: bool = False,
    install_dependencies: bool = True,
    index: str | None = None,
    cwd: str | _Path | None = None,
    raise_execution: bool = True,
    raise_exit_code: bool = True,
    raise_stderr: bool = False,
    text_output: bool = True,
) -> _ShellOutput | None:
    index_name_url = {
        "testpypi": "https://test.pypi.org/simple/",
    }
    command = []
    if upgrade:
        command.append("--upgrade")
    command.append(f"{name}{requirement_specifier or ''}")
    if not install_dependencies:
        command.append("--no-deps")
    if index:
        index_url = index_name_url.get(index) or index
        command.extend(["--index-url", index_url])
    return install(
        command=command,
        cwd=cwd,
        raise_execution=raise_execution,
        raise_exit_code=raise_exit_code,
        raise_stderr=raise_stderr,
        text_output=text_output,
    )
