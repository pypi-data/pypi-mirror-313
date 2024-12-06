from __future__ import annotations as _annotations

from typing import TYPE_CHECKING as _TYPE_CHECKING

from rich import text as _text
import mdit as _mdit
import ansi_sgr as _sgr

if _TYPE_CHECKING:
    from pathlib import Path


class ShellOutput:

    def __init__(
        self,
        title: str,
        command: list[str],
        cwd: Path,
        code: int | None = None,
        out: str | bytes | None = None,
        err: str | bytes | None = None,
    ):
        self.title = title
        self.cwd = cwd
        self.command = command
        self.code = code
        self.out = out
        self.err = err
        return

    @property
    def executed(self) -> bool:
        return self.code is not None

    @property
    def succeeded(self) -> bool:
        return self.code == 0

    @property
    def details(self) -> dict[str, str | bytes | int]:
        return {
            "title": self.title,
            "command": self.command,
            "executed": self.executed,
            "succeeded": self.succeeded,
            "directory": self.cwd,
            "code": self.code,
            "out": self.out,
            "err": self.err,
        }

    def report(self, dropdown: bool = True):

        def process_output(output: str | bytes, title: str, icon: str):
            output = _mdit.element.rich(_text.Text.from_ansi(self.out)) if (
                isinstance(output, str) and _sgr.has_sequence(output)
            ) else _mdit.element.code_block(str(output))
            return _mdit.element.dropdown(
                title=title,
                body=output,
                opened=True,
                icon=icon,
            )

        emoji_fail = "🔴"
        emoji_success = "🟢"
        content = _mdit.block_container()
        info_bar = _mdit.inline_container(
            f"Execution: {emoji_success if self.executed else emoji_fail}",
            separator="   ",
        )
        if self.executed:
            exit_info = emoji_success if self.succeeded else f"{emoji_fail} (Code: {self.code})"
            info_bar.append(f"Exit: {exit_info}")
        content.append(info_bar)
        content.append(_mdit.element.code_block(" ".join(self.command), caption="Command"))
        content.append(_mdit.element.code_block(str(self.cwd), caption="Directory"))
        if self.out:
            content.append(process_output(self.out, "Output", "📤"))
        if self.err:
            content.append(process_output(self.err, "Logs", "📝"))
        return _mdit.element.dropdown(
            title=self.title,
            body=content,
            opened=True,
            icon="🐚",
        ) if dropdown else content

    def __rich__(self):
        return self.report().source("console")
