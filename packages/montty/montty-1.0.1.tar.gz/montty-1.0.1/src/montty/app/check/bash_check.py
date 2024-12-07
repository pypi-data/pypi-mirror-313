# MIT License
#
# Copyright (c) 2024 Gwyn Davies
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR,
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from montty.app.status import Status
from montty.app.check.check import Check
from montty.app.check.check_level import CheckLevel
from montty.app.check.check_header import CheckHeader
from montty.app.check.check_body import CheckBody
from montty.platform.config_values import ConfigValues
from montty.platform.platform_command import PlatformCommand


class BashCheck(Check):
    def __init__(self, header_title: str, bash_script: str, *arguments: str, level_index: int = None):
        self._header_title = header_title

        if level_index:
            self._check_level = CheckLevel(level_index)
        else:
            self._check_level = CheckLevel(0)

        self._command = PlatformCommand(bash_script, *arguments)
        self._status: Status = Status.create_na()
        self._body: CheckBody = CheckBody()

    # @implement

    def run(self):
        self._run_command()

    def _run_command(self):
        self._command.run()

        # Get status
        self._status = self._check_result(
            self._command.get_status(), self._command.get_output())

        # Get command output for check's body text
        body_text = self._get_command_output(
            self._status, self._command.get_output())
        self._body.append_text(body_text)

    # @implement
    def get_status(self) -> Status:
        return self._status

    # @implement
    def get_header(self) -> CheckHeader:
        # E1120: No value for argument in constructor call (check_level)
        # pylint: disable=E1120
        return CheckHeader(self._header_title, self._status, self._check_level)

    # @implement
    def get_body(self) -> CheckBody:
        return self._body

    def get_level(self) -> CheckLevel:
        return self._check_level

    # Subclass hooks

    # subclasses can override this method, to manually set the status
    def _check_result(self, command_status: int, _: str) -> Status:
        # Code == 0
        if command_status == ConfigValues.LINUX_COMMAND_EXIT_STATUS_CODE_OKAY:
            status = Status.create_okay()
        # Code == 255
        elif command_status == ConfigValues.LINUX_COMMAND_EXIT_STATUS_CODE_WARN:
            status = Status.create_warn()
        # Code == 254
        elif command_status == ConfigValues.LINUX_COMMAND_EXIT_STATUS_CODE_NA:
            status = Status.create_na()
        # Code 1 <= and <= 253
        elif ConfigValues.LINUX_COMMAND_EXIT_STATUS_CODE_ALERT_MIN \
                <= command_status <= \
        ConfigValues.LINUX_COMMAND_EXIT_STATUS_CODE_ALERT_MAX:
            status = Status.create_alert()
        else:
            raise Exception(
                f"Unknown status value, expect {ConfigValues.LINUX_COMMAND_EXIT_STATUS_CODE_OKAY}..{ConfigValues.LINUX_COMMAND_EXIT_STATUS_CODE_WARN} - given {self._command.get_status()}")
        return status

    # subclasses can override this method, to manually set the output
    def _get_command_output(self, _: Status, command_output: str) -> str:
        return command_output
