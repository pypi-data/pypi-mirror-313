from __future__ import annotations as _annotations
from typing import TYPE_CHECKING as _TYPE_CHECKING
from functools import partial as _partial

from exceptionman import ReporterException as _ReporterException
import mdit as _mdit

if _TYPE_CHECKING:
    from pyshellman.output import ShellOutput


class PyShellManError(_ReporterException):
    """Base class for exceptions in this module."""
    def __init__(
        self,
        title: str,
        intro: str,
        output: ShellOutput
    ):
        sphinx_config = {"html_title": "PyShellMan Error Report"}
        sphinx_target_config = _mdit.target.sphinx(
            renderer=_partial(
                _mdit.render.sphinx,
                config=_mdit.render.get_sphinx_config(sphinx_config)
            )
        )
        report = _mdit.document(
            heading=title,
            body={"intro": intro},
            section={"details": _mdit.document(heading="Execution Details", body=output.report())},
            target_configs_md={"sphinx": sphinx_target_config},
        )
        super().__init__(report=report)
        self.output = output
        return


class PyShellManExecutionError(PyShellManError):
    """Exception raised for errors in the execution of a command."""
    def __init__(self, output: ShellOutput):
        super().__init__(
            title="Execution Error",
            intro=f"Shell command was invalid and could not be executed.",
            output=output
        )
        return


class PyShellManNonZeroExitCodeError(PyShellManError):
    """Exception raised for non-zero exit code in the execution of a command."""
    def __init__(self, output: ShellOutput):
        super().__init__(
            title="Non-Zero Exit Code Error",
            intro=f"Shell command exited with a non-zero code.",
            output=output
        )
        return


class PyShellManStderrError(PyShellManError):
    """Exception raised for non-empty stderr in the execution of a command."""

    def __init__(self, output: ShellOutput):
        super().__init__(
            title="Non-Empty Stderr Error",
            intro=f"Shell command produced output on stderr.",
            output=output
        )
        return
