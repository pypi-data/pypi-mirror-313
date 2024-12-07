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

from abc import ABC, abstractmethod
from montty.app.status import Status
from montty.app.check.check import Check
from montty.app.check.check_level import CheckLevel
from montty.app.check.check_header import CheckHeader
from montty.app.check.check_body import CheckBody


class CollectBaseCheck(Check, ABC):
    def __init__(self, header_title: str, level_index: int = None):
        self._header_title = header_title

        # Check level
        if level_index:
            self._check_level = CheckLevel(level_index)
        else:
            self._check_level = CheckLevel(0)

        # Status
        self._status: Status = Status.create_na()

        # Body
        self._body: CheckBody = CheckBody()

        # Checks
        self._checks = []

    # @implement
    def run(self) -> None:
        self._run_checks()

    @abstractmethod
    def _add_checks(self, checks: list[Check]) -> None:
        raise Exception("You must override this method")  # pragma: no cover

    @abstractmethod
    def _run_checks(self) -> None:
        raise Exception("You must override this method")  # pragma: no cover

    # @implement
    def get_header(self) -> CheckHeader:
        # E1120: No value for argument in constructor call (check_level)
        # pylint: disable=E1120
        return CheckHeader(self._header_title, self._status, self._check_level)

    # @implement
    def get_status(self) -> Status:
        return self._status

    # @implement
    def get_body(self) -> CheckBody:
        return self._body

    def get_level(self) -> CheckLevel:
        return self._check_level
