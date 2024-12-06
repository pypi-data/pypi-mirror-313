from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING
from types import SimpleNamespace as _SimpleNamespace
import subprocess as _subprocess
from pathlib import Path as _Path

from pyshellman import exception as _exception
from pyshellman.output import ShellOutput as _ShellOutput

if _TYPE_CHECKING:
    from pyshellman.protocol import LogLevel

class Runner:

    def __init__(
        self,
        pre_command: list[str] | None = None,
        cwd: str | _Path | None = None,
        raise_execution: bool = True,
        raise_exit_code: bool = True,
        raise_stderr: bool = False,
        text_output: bool = True,
        logger = None,
        log_title: str = "Shell Process",
        log_level_execution: LogLevel = "critical",
        log_level_exit_code: LogLevel = "error",
        log_level_stderr: LogLevel = "info",
        log_level_success: LogLevel = "success",
        stack_up: int = 0,
    ):
        self.pre_command = pre_command or []
        self.cwd = _Path(cwd).resolve() if cwd else None
        self.raise_execution = raise_execution
        self.raise_exit_code = raise_exit_code
        self.raise_stderr = raise_stderr
        self.text_output = text_output
        self.logger = logger
        self.log_title = log_title
        self.log_level_execution = log_level_execution
        self.log_level_exit_code = log_level_exit_code
        self.log_level_stderr = log_level_stderr
        self.log_level_success = log_level_success
        self.stack_up = stack_up
        return

    def run(
        self,
        command: list[str],
        cwd: str | _Path | None = None,
        raise_execution: bool | None = None,
        raise_exit_code: bool | None = None,
        raise_stderr: bool | None = None,
        text_output: bool | None = None,
        log_title: str | None = None,
        log_level_execution: LogLevel | None = None,
        log_level_exit_code: LogLevel | None = None,
        log_level_stderr: LogLevel | None = None,
        log_level_success: LogLevel | None = None,
        stack_up: int | None = None,
    ) -> _ShellOutput:
        args = self._get_run_args(locals())
        command = self.pre_command + command
        cwd = _Path(args.cwd).resolve() if args.cwd else None
        try:
            process = _subprocess.run(command, text=args.text_output, cwd=args.cwd, capture_output=True)
        except FileNotFoundError:
            stdout = None
            stderr = None
            code = None
        else:
            stdout = (process.stdout.strip() if args.text_output else process.stdout) or None
            stderr = (process.stderr.strip() if args.text_output else process.stderr) or None
            code = process.returncode
        output = _ShellOutput(
            title=args.log_title,
            command=command,
            cwd=cwd or _Path.cwd(),
            code=code,
            out=stdout,
            err=stderr,
        )
        if self.logger:
            if not output.executed:
                log_level = args.log_level_execution
            elif not output.succeeded:
                log_level = args.log_level_exit_code
            elif stderr:
                log_level = args.log_level_stderr
            else:
                log_level = args.log_level_success
            self.logger.log(
                log_level,
                args.log_title,
                output.report(dropdown=False),
                stack_up=args.stack_up + 1,
            )
        if not output.executed and args.raise_execution:
            raise _exception.PyShellManExecutionError(output=output)
        if not output.succeeded and args.raise_exit_code:
            raise _exception.PyShellManNonZeroExitCodeError(output=output)
        if stderr and args.raise_stderr:
            raise _exception.PyShellManStderrError(output=output)
        return output

    def _get_run_args(self, args: dict) -> _SimpleNamespace:
        final_args = {
            key: value if value is not None else getattr(self, key)
            for key, value in args.items() if key not in ("self", "command")
        }
        return _SimpleNamespace(**final_args)


def run(
    command: list[str],
    cwd: str | _Path | None = None,
    raise_execution: bool = True,
    raise_exit_code: bool = True,
    raise_stderr: bool = False,
    text_output: bool = True,
    logger=None,
    log_title: str = "Shell SubProcess",
    log_level_execution: LogLevel = "critical",
    log_level_exit_code: LogLevel = "error",
    log_level_stderr: LogLevel = "info",
    log_level_success: LogLevel = "success",
    stack_up: int = 0,
) -> _ShellOutput:
    return Runner(
        cwd=cwd,
        raise_execution=raise_execution,
        raise_exit_code=raise_exit_code,
        raise_stderr=raise_stderr,
        text_output=text_output,
        logger=logger,
        log_title=log_title,
        log_level_execution=log_level_execution,
        log_level_exit_code=log_level_exit_code,
        log_level_stderr=log_level_stderr,
        log_level_success=log_level_success,
        stack_up=stack_up+1,
    ).run(command)
